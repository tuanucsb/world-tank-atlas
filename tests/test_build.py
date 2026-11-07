"""Build and data checks for the World Tank Atlas generator.

Run from world-tank-atlas/:  python3 -m pytest tests/
"""
import contextlib
import io
import os
import re
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tank_atlas_src")
PAGE = os.path.join(ROOT, "world_tanks_atlas.html")
sys.path.insert(0, SRC)

N_TANKS = 86
N_BATTLES = 27


@pytest.fixture(scope="session")
def data():
    from enrich_v3_80tanks import get_v3_data
    from battle_timelines_and_destruction import enrich_all_battles_with_forensics

    with contextlib.redirect_stdout(io.StringIO()):  # the enrichers print progress
        eras, nations, tanks, edges, battles = get_v3_data()
        battles = enrich_all_battles_with_forensics(battles)
    return {"eras": eras, "nations": nations, "tanks": tanks, "edges": edges, "battles": battles}


def build(out_path):
    subprocess.run([sys.executable, os.path.join(SRC, "assemble_v2.py"), out_path],
                   check=True, capture_output=True, text=True)
    with open(out_path, encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="session")
def built(tmp_path_factory):
    return build(str(tmp_path_factory.mktemp("build") / "page.html"))


# Build

def test_committed_page_matches_a_fresh_build(built):
    with open(PAGE, encoding="utf-8") as f:
        committed = f.read()
    assert committed == built, "world_tanks_atlas.html is stale: run python3 tank_atlas_src/assemble_v2.py"


def test_build_is_deterministic(built, tmp_path):
    assert build(str(tmp_path / "again.html")) == built


def test_count_placeholders_are_replaced(built):
    assert "__N_TANKS__" not in built and "__N_BATTLES__" not in built


def test_counts_in_copy_come_from_data(built):
    assert f"{N_TANKS} tanks" in built
    assert f"{N_BATTLES} battles" in built


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_inline_scripts_parse(built, tmp_path):
    scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", built, flags=re.S)
    assert len(scripts) >= 2
    for i, js in enumerate(scripts):
        path = tmp_path / f"script{i}.js"
        path.write_text(js, encoding="utf-8")
        res = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
        assert res.returncode == 0, f"inline script {i} does not parse:\n{res.stderr[:2000]}"


def test_external_scripts_pin_versions(built):
    for src in re.findall(r'<script[^>]*\bsrc="([^"]+)"', built):
        if "cdn.tailwindcss.com" in src:
            continue  # Play CDN has a single URL
        assert re.search(r"@\d+\.\d+\.\d+|/\d+\.\d+\.\d+/", src), f"unpinned script: {src}"


def test_redirect_and_pages_files_exist():
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        assert "world_tanks_atlas.html" in f.read()


# Data

def test_counts(data):
    assert len(data["tanks"]) == N_TANKS
    assert len(data["battles"]) == N_BATTLES


def test_ids_are_unique_and_route_safe(data):
    for kind in ("tanks", "battles"):
        ids = [x["id"] for x in data[kind]]
        assert len(ids) == len(set(ids)), f"duplicate {kind} ids"
        bad = [i for i in ids if not re.fullmatch(r"[a-z0-9_]+", i)]
        assert not bad, f"{kind} ids not usable in #/{kind}/<id>: {bad}"


def test_tank_fields(data):
    era_ids = {e["id"] for e in data["eras"]}
    nation_ids = {n["id"] for n in data["nations"]}
    for t in data["tanks"]:
        assert t["name"], t["id"]
        assert t["era"] in era_ids, t["id"]
        assert t["nation"] in nation_ids, t["id"]
        assert isinstance(t["year"], int) and 1900 <= t["year"] <= 2030, t["id"]
        assert t.get("photo_url", t.get("image_url", "")).startswith("https://"), t["id"]


def test_edges_point_at_real_tanks(data):
    ids = {t["id"] for t in data["tanks"]}
    for e in data["edges"]:
        assert e["source"] in ids and e["target"] in ids, e


@pytest.mark.parametrize("idx", range(N_BATTLES))
def test_battle_fields(data, idx):
    tank_ids = {t["id"] for t in data["tanks"]}
    b = data["battles"][idx]
    bid = b["id"]
    assert b["name"] and b["date"] and b["location"] and b["summary"], bid
    assert -90 <= b["lat"] <= 90 and -180 <= b["lon"] <= 180, bid
    assert b["winner_side"] in ("A", "B", "DRAW"), bid
    assert b["side_a_num"] > 0 and b["side_b_num"] > 0, bid
    for side in ("side_a", "side_b"):
        s = b[side]
        assert s["name"], (bid, side)
        assert s["tanks"], (bid, side)
        missing = [t for t in s["tanks"] if t not in tank_ids]
        assert not missing, f"{bid} {side} names unknown tanks {missing}"
    phases = b["phases"]
    assert phases, bid
    for ph in phases:
        assert ph["title"], bid
        for k in ("lost_a_pct", "lost_b_pct"):
            assert 0 <= ph[k] <= 100, (bid, ph["title"], k)
    assert b["killcam_scenarios"], bid
    for sc in b["killcam_scenarios"]:
        assert sc["title"] and sc["desc"], bid

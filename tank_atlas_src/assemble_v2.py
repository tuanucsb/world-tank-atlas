import json
import os
import sys

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC_DIR)

from enrich_v3_80tanks import get_v3_data
from battle_timelines_and_destruction import enrich_all_battles_with_forensics
from build_v2_part1 import HTML_HEAD_AND_BODY
from build_v2_part2a import JS_PART_2A
from build_v2_part2b import JS_PART_2B

# World map coastline polygons (extracted from the legacy render_html.py)
with open(os.path.join(SRC_DIR, "world_polygons.json"), "r", encoding="utf-8") as f:
    world_poly_line = f"const WORLD_POLYGONS = {json.dumps(json.load(f))};"

ERAS, NATIONS, TANKS, EDGES, BATTLES = get_v3_data()
for t in TANKS:
    t["photo_url"] = t.get("image_url", "")
BATTLES = enrich_all_battles_with_forensics(BATTLES)

SHORT_MAP = {
    "UK": "UK",
    "FR": "FRANCE",
    "DE": "GERMANY",
    "SU_RU": "USSR / RU / UA",
    "US": "USA",
    "IL": "ISRAEL",
    "ASIA_OTHER": "ASIA / OTHER"
}
for n in NATIONS:
    n["short"] = SHORT_MAP.get(n["id"], n["name"].upper())

data_js = (
    "  <script>\n"
    f"    const ERAS = {json.dumps(ERAS, ensure_ascii=False)};\n"
    f"    const NATIONS = {json.dumps(NATIONS, ensure_ascii=False)};\n"
    f"    const TANKS = {json.dumps(TANKS, ensure_ascii=False)};\n"
    f"    const EDGES = {json.dumps(EDGES, ensure_ascii=False)};\n"
    f"    const BATTLES = {json.dumps(BATTLES, ensure_ascii=False)};\n"
    f"    {world_poly_line}\n"
)

full_html = HTML_HEAD_AND_BODY + "\n" + data_js + "\n" + JS_PART_2A + "\n" + JS_PART_2B
# Counts shown in the UI come from the data, never hand-typed
full_html = full_html.replace("__N_TANKS__", str(len(TANKS))).replace("__N_BATTLES__", str(len(BATTLES)))

# Output path: first CLI argument, else world_tanks_atlas.html next to this folder
out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SRC_DIR, "..", "world_tanks_atlas.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(full_html)
print(f"Successfully wrote {len(full_html):,} bytes to {os.path.abspath(out_path)}")

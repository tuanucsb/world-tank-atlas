import json
import sys
sys.path.insert(0, '/Users/tuandinh/.gemini/antigravity/brain/0bba3639-6aa1-4358-af48-fa98be8e3cf6/scratch')

from enrich_v3_80tanks import get_v3_data
from battle_timelines_and_destruction import enrich_all_battles_with_forensics
from build_v2_part1 import HTML_HEAD_AND_BODY
from build_v2_part2a import JS_PART_2A
from build_v2_part2b import JS_PART_2B

# Read WORLD_POLYGONS line from existing world_tanks_atlas.html
world_poly_line = None
with open("/Users/tuandinh/Scifi/world-tank-atlas/world_tanks_atlas.html", "r", encoding="utf-8") as f:
    for line in f:
        if "const WORLD_POLYGONS =" in line:
            world_poly_line = line.strip()
            break

assert world_poly_line is not None, "Could not find WORLD_POLYGONS line"

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

out_paths = [
    "/Users/tuandinh/Scifi/world-tank-atlas/world_tanks_atlas.html",
    "/Users/tuandinh/.gemini/antigravity/brain/0bba3639-6aa1-4358-af48-fa98be8e3cf6/world_tanks_atlas.html"
]
for p in out_paths:
    with open(p, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Successfully wrote {len(full_html):,} bytes to {p}")

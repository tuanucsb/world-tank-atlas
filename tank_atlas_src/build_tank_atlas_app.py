#!/usr/bin/env python3
"""
Generates the complete World Tank Lineage, Similarity, Combat Graph & Battle Map Atlas (1916-2026).
"""
import json
import os
import sys

import generate_data as gd
import expand_tanks as et

# Merge and refine tanks so all 47 nodes are distinct and well-spaced
base_tanks = []
for t in gd.TANKS:
    # Rename a few grouped nodes so they pair cleanly with the newly split nodes
    t_copy = dict(t)
    if t_copy["id"] == "amx13_30":
        t_copy["name"] = "AMX-13 (75mm / 90mm / SS.11)"
        t_copy["role"] = "Light Oscillating-Turret Tank"
        t_copy["weight_t"] = 15.0
        t_copy["gun"] = "75mm SA 50 / 90mm F3 (12-rd Autoloader)"
        t_copy["armor_mm"] = 40
        t_copy["speed_kmh"] = 60
        t_copy["power_hp"] = 250
        t_copy["crew"] = 3
        t_copy["produced"] = 7700
        t_copy["summary"] = "French light air-portable tank featuring the revolutionary FL-10 two-part oscillating turret with dual 6-round revolver magazines (12 rounds ready to fire). Fought with Israel in 1956/1967, India in 1965, and France in Suez & Algeria."
    elif t_copy["id"] == "type59_74_strv103":
        # Replace with Type 61 / early post-war Asian or skip since we have dedicated Type 59, Type 74, Strv 103
        continue
    elif t_copy["id"] == "t64_t80":
        t_copy["name"] = "T-64A / T-64BV (Morozov)"
        t_copy["role"] = "Composite Autoloaded Soviet/Ukrainian MBT"
        t_copy["weight_t"] = 42.4
        t_copy["gun"] = "125mm 2A46 smoothbore + Kobra ATGM"
        t_copy["armor_mm"] = 550
        t_copy["speed_kmh"] = 60
        t_copy["power_hp"] = 700
        t_copy["crew"] = 3
        t_copy["produced"] = 13000
        t_copy["summary"] = "Alexander Morozov's Kharkiv masterpiece: the first tank in history with composite armor ('Combination K'), a 125mm smoothbore cannon, and a 3-man crew with a vertical-carousel autoloader. Retained exclusively by elite Soviet units and later became the backbone of the Ukrainian Army."
    elif t_copy["id"] == "k2_type10_ztz99a":
        t_copy["name"] = "K2 Black Panther (ROK / Poland)"
        t_copy["role"] = "3.5+ Gen Digital Autoloaded MBT"
        t_copy["weight_t"] = 55.0
        t_copy["gun"] = "120mm CN08 L/55 smoothbore (Autoloaded)"
        t_copy["armor_mm"] = 860
        t_copy["speed_kmh"] = 70
        t_copy["power_hp"] = 1500
        t_copy["crew"] = 3
        t_copy["produced"] = 440
        t_copy["summary"] = "South Korea's cutting-edge Main Battle Tank (also adopted in huge numbers by Poland). Combines a 120mm L/55 gun, bustle autoloader, In-arm Hydropneumatic Suspension ('sit/stand/lean' posture control), millimeter-wave radar, and KSTAM top-attack smart munitions."
    base_tanks.append(t_copy)

ALL_TANKS = base_tanks + et.EXTRA_TANKS

# Add 2 more historic battles (Flers-Courcelette 1916 & Raseiniai 1941) to make 22 battles
EXTRA_BATTLES = [
    {
        "id": "flers_1916",
        "name": "Battle of Flers-Courcelette (Somme)",
        "date": "September 15, 1916",
        "year": 1916,
        "era": 1,
        "theatre": "EUROPE_WEST",
        "location": "Flers & Courcelette, Somme, France",
        "lat": 50.048, "lon": 2.822,
        "total_tanks": "49 British Mark I Tanks (32 reached start line)",
        "side_a": {"name": "British Fourth Army (Heavy Branch Machine Gun Corps)", "flag": "🇬🇧", "tanks": ["mark_i_iv"], "count": "49 Mark I Tanks (Male 6-pdr & Female Vickers MG)"},
        "side_b": {"name": "German 1st Army (Bavarian Divisions)", "flag": "🇩🇪", "tanks": ["a7v"], "count": "Fortified trenches, machine-gun nests & 77mm field guns"},
        "outcome": "World's first combat use of tanks; Mark I 'D1' led the capture of Flers ('A tank is walking up the High Street of Flers with the British Army cheering behind').",
        "tactical_zoom": {
            "terrain": "Shell-cratered Somme mud, shattered High Wood & Flers village street",
            "range_m": "20–150m point-blank wire crushing & trench enfilade fire",
            "formations": [
                {"side": "A", "label": "Mark I 'D1' (Capt. H.W. Mortimore) & C/D Companies", "x": 24, "y": 52, "tx": 60, "ty": 48},
                {"side": "B", "label": "German Switch Line Trenches & Flers Strongpoints", "x": 70, "y": 48, "tx": 55, "ty": 48}
            ],
            "key_lesson": "Even though mechanical breakdowns limited numbers, the psychological shock and ability to crush wire and straddle trenches proved the armored fighting vehicle had arrived."
        },
        "summary": "At dawn on September 15, 1916, Capt. H.W. Mortimore steered Mark I 'D1' into action near Delville Wood—the first tank in human history to enter combat. Later that morning, Mark I 'D17' ('Dinnaken') lumbered straight up the main street of Flers crushing machine-gun nests as British Reconnaissance airplanes wirelessed the famous report back to headquarters."
    },
    {
        "id": "raseiniai_1941",
        "name": "Battle of Raseiniai (The Lone KV-1 Stand)",
        "date": "June 23–27, 1941",
        "year": 1941,
        "era": 3,
        "theatre": "EUROPE_EAST",
        "location": "Raseiniai & Dubysa River, Lithuania",
        "lat": 55.383, "lon": 23.116,
        "total_tanks": "~990 Tanks (749 SU vs 245 DE)",
        "side_a": {"name": "Soviet 3rd & 12th Mechanized Corps (2nd Tank Division)", "flag": "☭", "tanks": ["kv1", "t26", "bt7"], "count": "749 Tanks (incl. ~50 KV-1 and KV-2 Heavy Tanks)"},
        "side_b": {"name": "German XXXXI Panzer Corps (6th & 1st Panzer Divisions)", "flag": "🇩🇪", "tanks": ["pz_38t", "panzer_iii", "panzer_iv", "panzer_ii"], "count": "245 Tanks (mostly Panzer 35(t)/38(t), Panzer III & IV)"},
        "outcome": "A single Soviet KV-1 / KV-2 tank sat on a crossroads behind the 6th Panzer Division for an entire day and night, destroying 12 supply trucks and an 88mm battery while shrugging off dozens of 50mm hits.",
        "tactical_zoom": {
            "terrain": "Dubysa River bridgeheads & wooded crossroads north of Raseiniai",
            "range_m": "100–600m crossroads blockade against 50mm Pak 38 & 88mm Flak",
            "formations": [
                {"side": "A", "label": "Lone Soviet KV-1/KV-2 Blocking Kampfgruppe Raus Crossroads", "x": 52, "y": 48, "tx": 48, "ty": 48},
                {"side": "B", "label": "German 6th Panzer Div (Pz 35(t)/38(t), 50mm AT & 88mm Flak)", "x": 25, "y": 48, "tx": 46, "ty": 48}
            ],
            "key_lesson": "Proved 37mm and 50mm guns were obsolete overnight against 75–90mm Soviet heavy armor; only distracting the KV crew with Panzer IIIs while another 88mm Flak gun fired six rounds into its rear finally stopped the lone giant."
        },
        "summary": "During Gen. Solyankin's 2nd Tank Division counterattack in Lithuania, a single Soviet KV heavy tank drove onto the only supply road behind Kampfgruppe Raus (6th Panzer Division) and halted. It survived a 50mm anti-tank battery, blew up a 105mm howitzer, destroyed an 88mm Flak gun as it set up, and withstood nighttime pioneer demolition charges before finally being knocked out by multiple 88mm hits the next day while distracted by swarming Panzer 35(t)s."
    }
]

ALL_BATTLES = sorted(gd.BATTLES + EXTRA_BATTLES, key=lambda b: (b["year"], b["id"]))

# Remap any edges that pointed to type59_74_strv103 and add edges for the 12 new distinct tanks
CLEAN_EDGES = []
for e in gd.EDGES:
    ec = dict(e)
    if ec["source"] == "type59_74_strv103":
        ec["source"] = "type59_69"
    if ec["target"] == "type59_74_strv103":
        if ec["source"] == "type95_97":
            ec["target"] = "type74_90"
        elif ec["source"] == "shot_magach":
            ec["target"] = "strv103"
        else:
            ec["target"] = "type59_69"
    CLEAN_EDGES.append(ec)

EXTRA_EDGES = [
    # Lineage for new distinct nodes
    {"source": "matilda_ii", "target": "churchill", "type": "lineage", "label": "Heavy Infantry Trench/Hill Tank Successor"},
    {"source": "churchill", "target": "centurion_mk1", "type": "lineage", "label": "Infantry Heavy Armor Merges with Cruiser Mobility"},
    {"source": "char_b1", "target": "arl44_foch", "type": "lineage", "label": "Secret Wartime Heavy Tank Successor"},
    {"source": "arl44_foch", "target": "amx13_30", "type": "lineage", "label": "Post-War French Tank Industry Rebirth"},
    {"source": "amx13_30", "target": "amx30", "type": "lineage", "label": "French 2nd-Gen MBT Evolution"},
    {"source": "amx30", "target": "leclerc", "type": "lineage", "label": "AMX-30B2 → High-Speed Autoloaded Leclerc"},
    {"source": "panzer_iii", "target": "stug_iii", "type": "lineage", "label": "Panzer III Chassis → Casemate StuG III Assault Gun"},
    {"source": "m4_sherman", "target": "m18_hellcat", "type": "lineage", "label": "US Tank Destroyer Doctrine (Torsion-Bar 76mm)"},
    {"source": "is2", "target": "is3", "type": "lineage", "label": "Pike-Nose Glacis & Hemispherical Turret"},
    {"source": "is3", "target": "t54_55", "type": "lineage", "label": "Hemispherical Cast Turret Geometry Adopted on T-54"},
    {"source": "t64_t80", "target": "t80bvm", "type": "lineage", "label": "T-64A Chassis + Gas Turbine = T-80 / T-80BVM"},
    {"source": "type95_97", "target": "type74_90", "type": "lineage", "label": "Mitsubishi Air-Cooled Diesel & Hydropneumatic Lineage"},
    {"source": "type74_90", "target": "type10", "type": "lineage", "label": "Type 90 → 44-Ton Networked Type 10 Hitomaru"},
    {"source": "type59_69", "target": "ztz99a", "type": "lineage", "label": "Type 59 → Type 80/88 → Type 96 → ZTZ-99A"},
    {"source": "centurion_mk1", "target": "strv103", "type": "lineage", "label": "Swedish Centurion (Strv 81/101) → Indigenous S-Tank"},

    # Similarity for new distinct nodes
    {"source": "strv103", "target": "type74_90", "type": "similarity", "label": "Pioneered Active Hydropneumatic Hull-Tilting Suspension"},
    {"source": "type74_90", "target": "k2_type10_ztz99a", "type": "similarity", "label": "Hydropneumatic Mountain Suspension & 120mm Bustle Autoloader"},
    {"source": "leopard2_a4", "target": "type74_90", "type": "similarity", "label": "Type 90 Adopted Rheinmetall 120mm L/44 & Western Turret Layout"},
    {"source": "t72", "target": "ztz99a", "type": "similarity", "label": "Shared 125mm Carousel Autoloader & Driver Center-Hull Architecture"},
    {"source": "is3", "target": "chieftain", "type": "similarity", "label": "IS-3 Shock Triggered British 120mm Gun Development"},
    {"source": "t80bvm", "target": "m1_abrams", "type": "similarity", "label": "World's Only Two All-Gas-Turbine Main Battle Tank Families"},
    {"source": "leopard1", "target": "amx30", "type": "similarity", "label": "Sister Tanks Born from 1957 Franco-German Europanzer Program"},

    # Combat for new distinct nodes
    {"source": "churchill", "target": "tiger_i", "type": "combat", "label": "Tunisia (1943, Tiger 131 Capture) & Normandy (1944)", "battles": ["normandy_1944"]},
    {"source": "churchill", "target": "panther", "type": "combat", "label": "Normandy Hill 112 & Operation Goodwood (1944)", "battles": ["normandy_1944"]},
    {"source": "stug_iii", "target": "t34_76", "type": "combat", "label": "Barbarossa, Stalingrad & Kursk (1941–43): Ambush Tank Hunter", "battles": ["brody_1941", "kursk_1943"]},
    {"source": "stug_iii", "target": "m4_sherman", "type": "combat", "label": "Italy, Normandy & Arracourt (1943–44)", "battles": ["normandy_1944", "arracourt_1944"]},
    {"source": "m18_hellcat", "target": "panther", "type": "combat", "label": "Arracourt & Noville / Ardennes (1944): 89 km/h Flank Ambushes", "battles": ["arracourt_1944", "bulge_1944"]},
    {"source": "m18_hellcat", "target": "tiger_ii", "type": "combat", "label": "Battle of the Bulge (Dec 1944): Hellcat Shoot-and-Scoot Defense", "battles": ["bulge_1944"]},
    {"source": "is3", "target": "shot_magach", "type": "combat", "label": "Six-Day War (Rafah & Sinai, 1967): Israeli 105mm vs Egyptian IS-3M", "battles": ["sinai_1967"]},
    {"source": "is3", "target": "m48_m60_patton", "type": "combat", "label": "Rafah Junction (Jun 1967): Israeli M48A2C Patton vs Egyptian IS-3M", "battles": ["sinai_1967"]},
    {"source": "amx30", "target": "t54_55", "type": "combat", "label": "Battle of Khafji & Operation Daguet (1991 Gulf War): Qatari/French AMX-30 vs Iraqi T-55", "battles": ["easting_1991"]},
    {"source": "t80bvm", "target": "t84_oplot", "type": "combat", "label": "Kharkiv, Izium & Donbas (2022–24): Russian T-80BVM vs Ukrainian T-64BV/T-84", "battles": ["ukraine_2022_2024"]},
    {"source": "t80bvm", "target": "m1a2_sepv3", "type": "combat", "label": "Donbas / Avdiivka Sector (2024): Russian T-80BVM vs Ukrainian M1A1 SA Abrams", "battles": ["ukraine_2022_2024"]}
]

ALL_EDGES = CLEAN_EDGES + EXTRA_EDGES

# Update battle tank lists to include the new distinct tanks where historically accurate
battle_extra_map = {
    "normandy_1944": {"a": ["churchill"], "b": ["stug_iii"]},
    "arracourt_1944": {"a": ["m18_hellcat"], "b": ["stug_iii"]},
    "bulge_1944": {"a": ["m18_hellcat"], "b": []},
    "kursk_1943": {"a": [], "b": ["stug_iii"]},
    "sinai_1967": {"a": [], "b": ["is3"]},
    "easting_1991": {"a": ["amx30"], "b": ["type59_69"]},
    "ukraine_2022_2024": {"a": [], "b": ["t80bvm"]}
}

for b in ALL_BATTLES:
    # replace any old type59_74_strv103 with type59_69
    b["side_a"]["tanks"] = ["type59_69" if x == "type59_74_strv103" else x for x in b["side_a"]["tanks"]]
    b["side_b"]["tanks"] = ["type59_69" if x == "type59_74_strv103" else x for x in b["side_b"]["tanks"]]
    if b["id"] in battle_extra_map:
        for ta in battle_extra_map[b["id"]]["a"]:
            if ta not in b["side_a"]["tanks"]:
                b["side_a"]["tanks"].append(ta)
        for tb in battle_extra_map[b["id"]]["b"]:
            if tb not in b["side_b"]["tanks"]:
                b["side_b"]["tanks"].append(tb)

# Assign neat, non-overlapping vertical lane_offset within each (era, nation) bucket!
from collections import defaultdict
bucket = defaultdict(list)
for t in ALL_TANKS:
    bucket[(t["era"], t["nation"])].append(t)

for (era, nat), group in bucket.items():
    group.sort(key=lambda x: x["year"])
    n = len(group)
    for idx, t in enumerate(group):
        if n == 1:
            t["x_offset"] = 0.0
            t["lane_offset"] = 0.0
        elif n == 2:
            t["x_offset"] = -0.22 if idx == 0 else 0.22
            t["lane_offset"] = -0.20 if idx == 0 else 0.20
        elif n == 3:
            t["x_offset"] = [-0.26, 0.0, 0.26][idx]
            t["lane_offset"] = [-0.24, 0.0, 0.24][idx]
        else:
            t["x_offset"] = -0.3 + (0.6 * idx / (n - 1))
            t["lane_offset"] = -0.26 + (0.52 * idx / (n - 1))

# Final validation check
tank_ids = {t["id"] for t in ALL_TANKS}
battle_ids = {b["id"] for b in ALL_BATTLES}

for e in ALL_EDGES:
    assert e["source"] in tank_ids, f"Missing source: {e['source']}"
    assert e["target"] in tank_ids, f"Missing target: {e['target']}"
    for bid in e.get("battles", []):
        assert bid in battle_ids, f"Missing battle: {bid}"

for b in ALL_BATTLES:
    for tid in b["side_a"]["tanks"] + b["side_b"]["tanks"]:
        assert tid in tank_ids, f"Missing tank in battle {b['id']}: {tid}"

print(f"MERGED DATASET READY: {len(ALL_TANKS)} Distinct Tanks | {len(ALL_EDGES)} Edges | {len(ALL_BATTLES)} Historic Tank Battles")

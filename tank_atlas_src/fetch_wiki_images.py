import os
import urllib.request
import urllib.parse
import json
import sys

# Map each tank ID (all 67 existing + 13 newly split/added = 80 tanks) to its exact English Wikipedia article title
WIKI_TITLES = {
    "mark_i_iv": "Mark_IV_tank",
    "mark_v": "Mark_V_tank",
    "whippet": "Medium_Mark_A_Whippet",
    "saint_chamond_schneider": "Saint-Chamond_(tank)",
    "schneider_ca1": "Schneider_CA1",
    "renault_ft": "Renault_FT",
    "a7v": "A7V",
    "m1917_light": "M1917_light_tank",
    "vickers_6ton": "Vickers_6-Ton",
    "matilda_ii": "Matilda_II",
    "somua_s35": "SOMUA_S35",
    "char_b1": "Char_B1",
    "panzer_ii": "Panzer_II",
    "pz_38t": "Panzer_38(t)",
    "t26": "T-26",
    "bt7": "BT-7",
    "christie_m2": "M2_medium_tank",
    "type95_hago": "Type_95_Ha-Go",
    "type95_97": "Type_97_Chi-Ha",
    "crusader_valentine": "Crusader_tank",
    "valentine": "Valentine_tank",
    "m13_40": "Carro_Armato_M13/40",
    "panzer_iii": "Panzer_III",
    "panzer_iv": "Panzer_IV",
    "stug_iii": "Sturmgeschütz_III",
    "t34_76": "T-34",
    "kv1": "KV_tank",
    "m3_stuart": "M3_Stuart",
    "m3_lee_grant": "M3_Lee",
    "m4_sherman": "M4_Sherman",
    "cromwell_firefly": "Sherman_Firefly",
    "cromwell": "Cromwell_tank",
    "churchill": "Churchill_tank",
    "centurion_mk1": "Centurion_(tank)",
    "arl44_foch": "ARL_44",
    "tiger_i": "Tiger_I",
    "panther": "Panther_tank",
    "tiger_ii": "Tiger_II",
    "elefant": "Elefant",
    "jagdpanther_hetzer": "Jagdpanther",
    "t34_85": "T-34",
    "su76m": "SU-76",
    "isu152": "ISU-152",
    "is2": "IS-2",
    "is3": "IS-3",
    "m4a3e8": "M4_Sherman",
    "m18_hellcat": "M18_Hellcat",
    "m24_chaffee": "M24_Chaffee",
    "m26_pershing": "M26_Pershing",
    "chieftain": "Chieftain_(tank)",
    "amx13_30": "AMX-13",
    "amx30": "AMX-30",
    "leopard1": "Leopard_1",
    "t54_55": "T-54/T-55",
    "pt76": "PT-76",
    "t62": "T-62",
    "bmp1": "BMP-1",
    "m41_bulldog": "M41_Walker_Bulldog",
    "m48_m60_patton": "M48_Patton",
    "m60_patton": "M60_tank",
    "m551_sheridan": "M551_Sheridan",
    "super_sherman": "Super_Sherman",
    "shot_magach": "Sho't",
    "magach": "Magach",
    "type59_69": "Type_59_tank",
    "type74_90": "Type_74_tank",
    "strv103": "Stridsvagn_103",
    "challenger1": "Challenger_1",
    "leopard2_a4": "Leopard_2",
    "t64_t80": "T-64",
    "t72": "T-72",
    "m1_abrams": "M1_Abrams",
    "m2_bradley": "M2_Bradley",
    "merkava_i_ii": "Merkava",
    "challenger2_3": "Challenger_2",
    "leclerc": "Leclerc_tank",
    "leopard2_a7_kf51": "Leopard_2",
    "t80bvm": "T-80",
    "t90m": "T-90",
    "t84_oplot": "BM_Oplot",
    "m1a2_sepv3": "M1_Abrams",
    "merkava_iv": "Merkava",
    "ztz99a": "Type_99_tank",
    "type10": "Type_10",
    "k2_type10_ztz99a": "K2_Black_Panther"
}

def fetch_wiki_images():
    results = {}
    items = list(WIKI_TITLES.items())
    # Query in batches of 20
    for i in range(0, len(items), 20):
        batch = items[i:i+20]
        titles_param = "|".join(t for _, t in batch)
        url = (
            "https://en.wikipedia.org/w/api.php?"
            + urllib.parse.urlencode({
                "action": "query",
                "prop": "pageimages",
                "format": "json",
                "piprop": "original|thumbnail",
                "pithumbsize": "800",
                "redirects": "1",
                "titles": titles_param
            })
        )
        req = urllib.request.Request(url, headers={"User-Agent": "WorldTanksAtlas/2.0 (Educational Project)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        
        pages = data.get("query", {}).get("pages", {})
        redirects = {r["from"]: r["to"] for r in data.get("query", {}).get("redirects", [])}
        normalized = {n["from"]: n["to"] for n in data.get("query", {}).get("normalized", [])}
        
        title_to_img = {}
        for pid, pdata in pages.items():
            title = pdata.get("title", "")
            thumb = pdata.get("thumbnail", {}).get("source")
            orig = pdata.get("original", {}).get("source")
            if thumb or orig:
                title_to_img[title] = thumb or orig

        for tid, raw_title in batch:
            norm_t = normalized.get(raw_title, raw_title.replace("_", " "))
            final_t = redirects.get(norm_t, norm_t)
            img = title_to_img.get(final_t) or title_to_img.get(norm_t)
            results[tid] = img
            print(f"{tid:22s} -> {final_t:28s} -> {'OK' if img else 'MISSING'}")

    missing = [k for k, v in results.items() if not v]
    print(f"\nTotal resolved: {len(results) - len(missing)}/{len(results)}. Missing: {missing}")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verified_wiki_images.json"), "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    fetch_wiki_images()

#!/usr/bin/env python3
"""
Builds the interactive World Tank Lineage, Similarity, Combat Graph & Battle Map Atlas (1916-2026).
Validates all nodes, edges (lineage, similarity, combat), and battle coordinates before generating HTML.
"""
import json
import os

# 1. Define the 7 Eras (Horizontal Axis of Lineage Graph)
ERAS = [
    {"id": 1, "code": "WWI", "name": "Era I: WWI Dawn of Armor", "years": "1916–1918", "desc": "Trench-crossing rhomboids & the revolutionary Renault FT turret layout."},
    {"id": 2, "code": "INTERWAR", "name": "Era II: Interwar & Cruiser Experiments", "years": "1919–1938", "desc": "Christie suspension, Vickers exports, multi-turret experiments & early Blitzkrieg."},
    {"id": 3, "code": "WWII_EARLY", "name": "Era III: Early–Mid WWII Blitzkrieg", "years": "1939–1942", "desc": "Combined-arms breakthroughs, sloped armor shock (T-34), and desert warfare."},
    {"id": 4, "code": "WWII_LATE", "name": "Era IV: Late WWII Heavy & Gun Escalation", "years": "1943–1945", "desc": "Big Cats (Tiger, Panther), up-gunned Shermans & T-34-85, and birth of the universal tank."},
    {"id": 5, "code": "COLDWAR_EARLY", "name": "Era V: 1st & 2nd Gen Main Battle Tanks", "years": "1946–1973", "desc": "Centurion, T-54/55, T-62, M48/M60 Patton, Leopard 1 & the 105mm L7 / 115mm smoothbore revolution."},
    {"id": 6, "code": "COLDWAR_LATE", "name": "Era VI: 3rd Gen Composite & Thermal MBTs", "years": "1974–1991", "desc": "Chobham composite armor, laser rangefinders, thermal sights, autoloaders (T-64/72/80, Abrams, Leopard 2)."},
    {"id": 7, "code": "MODERN", "name": "Era VII: Digital Networked & APS MBTs", "years": "1992–2026", "desc": "Active Protection Systems (Trophy/ Afganit), hunter-killer thermals, drone-era armor & 4th-gen concepts."}
]

# 2. Nations / Lanes (Vertical Axis Option A)
NATIONS = [
    {"id": "UK", "name": "United Kingdom", "flag": "🇬🇧", "color": "#38bdf8", "lane": 0},
    {"id": "FR", "name": "France", "flag": "🇫🇷", "color": "#818cf8", "lane": 1},
    {"id": "DE", "name": "Germany", "flag": "🇩🇪", "color": "#f59e0b", "lane": 2},
    {"id": "SU_RU", "name": "USSR / Russia / Ukraine", "flag": "☭/🇷🇺/🇺🇦", "color": "#f43f5e", "lane": 3},
    {"id": "US", "name": "United States", "flag": "🇺🇸", "color": "#10b981", "lane": 4},
    {"id": "IL", "name": "Israel", "flag": "🇮🇱", "color": "#06b6d4", "lane": 5},
    {"id": "ASIA_OTHER", "name": "Japan / China / S. Korea / Sweden", "flag": "🌏", "color": "#a855f7", "lane": 6}
]

print("Setup constants complete.")

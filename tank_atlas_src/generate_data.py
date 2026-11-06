#!/usr/bin/env python3
import json

ERAS = [
    {"id": 1, "code": "WWI", "name": "Era I: WWI Dawn of Armor", "short": "I. WWI (1916–18)", "years": "1916–1918", "desc": "Trench-crossing rhomboids, first tank-vs-tank duel at Villers-Bretonneux, and Renault FT's rotating turret blueprint."},
    {"id": 2, "code": "INTERWAR", "name": "Era II: Interwar & Cruiser Experiments", "short": "II. Interwar (1919–38)", "years": "1919–1938", "desc": "Vickers 6-Ton global proliferation, Christie high-speed suspension, and doctrinal split between infantry & cruiser tanks."},
    {"id": 3, "code": "WWII_EARLY", "name": "Era III: Early–Mid WWII Blitzkrieg", "short": "III. Early WWII (1939–42)", "years": "1939–1942", "desc": "Radio-coordinated Panzer divisions, thick French/British infantry armor, and the T-34/KV-1 sloped-armor shock of 1941."},
    {"id": 4, "code": "WWII_LATE", "name": "Era IV: Late WWII Heavy & Gun Escalation", "short": "IV. Late WWII (1943–45)", "years": "1943–1945", "desc": "German Big Cats (Tiger I/II, Panther) answered by Allied 76mm/17-pdr/85mm/122mm guns and the birth of the Universal Tank."},
    {"id": 5, "code": "COLDWAR_EARLY", "name": "Era V: 1st & 2nd Gen Main Battle Tanks", "short": "V. Cold War I (1946–73)", "years": "1946–1973", "desc": "Centurion, T-54/55, T-62, M48/M60 Patton, Leopard 1 & the 105mm L7 / 115mm smoothbore clashes in the Middle East & Asia."},
    {"id": 6, "code": "COLDWAR_LATE", "name": "Era VI: 3rd Gen Composite & Thermal MBTs", "short": "VI. Cold War II (1974–91)", "years": "1974–1991", "desc": "Chobham composite armor, APFSDS darts, laser rangefinders, thermal imaging, and Soviet autoloaders (T-64/72/80 vs Abrams/Leopard 2)."},
    {"id": 7, "code": "MODERN", "name": "Era VII: Digital Networked & APS MBTs", "short": "VII. Modern (1992–2026)", "years": "1992–2026", "desc": "Active Protection Systems (Trophy), ERA evolutions, hunter-killer digital fire control, and anti-drone/loitering munition warfare."}
]

NATIONS = [
    {"id": "UK", "name": "United Kingdom", "flag": "🇬🇧", "color": "#38bdf8", "lane": 0},
    {"id": "FR", "name": "France", "flag": "🇫🇷", "color": "#818cf8", "lane": 1},
    {"id": "DE", "name": "Germany", "flag": "🇩🇪", "color": "#f59e0b", "lane": 2},
    {"id": "SU_RU", "name": "USSR / Russia / Ukraine", "flag": "☭/🇷🇺/🇺🇦", "color": "#f43f5e", "lane": 3},
    {"id": "US", "name": "United States", "flag": "🇺🇸", "color": "#10b981", "lane": 4},
    {"id": "IL", "name": "Israel", "flag": "🇮🇱", "color": "#06b6d4", "lane": 5},
    {"id": "ASIA_OTHER", "name": "Japan / China / S. Korea / Sweden", "flag": "🌏", "color": "#c084fc", "lane": 6}
]

TANKS = [
    # ERA 1: WWI (1916-1918)
    {
        "id": "mark_i_iv", "name": "Mark I / Mark IV", "nation": "UK", "era": 1, "year": 1916,
        "role": "Heavy Trench-Crossing Tank", "weight_t": 28.0, "gun": "2x 57mm 6-pdr (Male) / Lewis MGs",
        "armor_mm": 12, "speed_kmh": 6, "power_hp": 105, "crew": 8, "produced": 1220,
        "x_offset": -0.15, "lane_offset": -0.15,
        "stats": {"firepower": 25, "armor": 20, "mobility": 10, "optics": 10, "impact": 98},
        "summary": "The world's first combat tank (Flers-Courcelette, Sep 1916) and mass-breakthrough weapon (Cambrai, 1917). Its rhomboid tracked frame crushed barbed wire and crossed wide trenches, and at Villers-Bretonneux (1918) a Male Mark IV fought the first tank-vs-tank duel in history against Germany's A7V.",
        "innovations": ["First tracked armored fighting vehicle in combat", "Rhomboid all-around track profile for trench crossing", "Side sponsons with 6-pounder naval guns"]
    },
    {
        "id": "whippet", "name": "Medium Mark A Whippet", "nation": "UK", "era": 1, "year": 1918,
        "role": "Cavalry / Exploitation Tank", "weight_t": 14.0, "gun": "4x 7.7mm Hotchkiss MGs",
        "armor_mm": 14, "speed_kmh": 13, "power_hp": 90, "crew": 3, "produced": 200,
        "x_offset": 0.22, "lane_offset": 0.22,
        "stats": {"firepower": 15, "armor": 18, "mobility": 28, "optics": 12, "impact": 75},
        "summary": "Designed to exploit gaps punched by heavy Mark IVs, the Whippet pioneered the British 'Cruiser/Cavalry' tank concept. Faster than infantry, Whippets wreaked havoc behind German lines in 1918 and clashed with an A7V at Villers-Bretonneux.",
        "innovations": ["Twin-engine steering layout", "Pioneered mobile exploitation / cavalry tank doctrine"]
    },
    {
        "id": "renault_ft", "name": "Renault FT", "nation": "FR", "era": 1, "year": 1917,
        "role": "Light Infantry Support Tank", "weight_t": 6.5, "gun": "37mm Puteaux SA 18 / 8mm MG",
        "armor_mm": 22, "speed_kmh": 7, "power_hp": 39, "crew": 2, "produced": 3694,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 20, "armor": 22, "mobility": 22, "optics": 18, "impact": 100},
        "summary": "The single most influential tank layout in history: front driver, fully rotating 360° top turret, and rear engine compartment. Almost every modern Main Battle Tank descends structurally from the Renault FT. Licensed/copied by the US (M1917), USSR (T-18), and Italy (Fiat 3000).",
        "innovations": ["First production tank with a 360° rotating turret", "Front crew, middle fighting compartment, rear engine architecture", "Cast/riveted compact hull for assembly-line mass production"]
    },
    {
        "id": "a7v", "name": "Sturmpanzerwagen A7V", "nation": "DE", "era": 1, "year": 1918,
        "role": "Heavy Box Tank", "weight_t": 33.0, "gun": "57mm Maxim-Nordenfelt + 6x MGs",
        "armor_mm": 30, "speed_kmh": 15, "power_hp": 200, "crew": 18, "produced": 20,
        "x_offset": 0.1, "lane_offset": 0.0,
        "stats": {"firepower": 28, "armor": 26, "mobility": 15, "optics": 14, "impact": 68},
        "summary": "Germany's only operational indigenous tank of WWI. Packing an 18-man crew and a bow-mounted 57mm cannon, A7V 'Nixe' fought three British Mark IV tanks at Villers-Bretonneux on April 24, 1918—history's very first tank-versus-tank engagement.",
        "innovations": ["30mm frontal armor plate", "High road speed (15 km/h) on coil-spring Holt bogies", "Participant in first tank-vs-tank duel in history"]
    },
    {
        "id": "m1917_light", "name": "M1917 Six-Ton", "nation": "US", "era": 1, "year": 1918,
        "role": "Light Tank", "weight_t": 6.6, "gun": "37mm M1916 / .30 cal MG",
        "armor_mm": 16, "speed_kmh": 9, "power_hp": 42, "crew": 2, "produced": 950,
        "x_offset": 0.2, "lane_offset": 0.0,
        "stats": {"firepower": 20, "armor": 20, "mobility": 22, "optics": 16, "impact": 60},
        "summary": "America's license-built version of the French Renault FT, adapted to imperial measurements and a Buda engine. It formed the foundation of the US Army Tank Corps under George S. Patton and Dwight D. Eisenhower.",
        "innovations": ["First mass-produced US armored vehicle", "Converted French metric blueprints to US industrial standards"]
    },

    # ERA 2: INTERWAR (1919-1938)
    {
        "id": "vickers_6ton", "name": "Vickers Mark E (6-Ton)", "nation": "UK", "era": 2, "year": 1928,
        "role": "Light Export Tank", "weight_t": 7.3, "gun": "47mm OQF 3-pdr",
        "armor_mm": 13, "speed_kmh": 35, "power_hp": 85, "crew": 3, "produced": 153,
        "x_offset": -0.2, "lane_offset": -0.18,
        "stats": {"firepower": 30, "armor": 22, "mobility": 45, "optics": 25, "impact": 94},
        "summary": "Though rejected by the British Army, the Vickers 6-Ton was licensed around the globe—becoming the Soviet T-26 (over 11,000 built), Polish 7TP, and influencing Italian and Japanese interwar armor.",
        "innovations": ["Patented double-bogie leaf-spring suspension", "3-man turret option (Type B) with 47mm gun", "Most licensed interwar tank design in the world"]
    },
    {
        "id": "matilda_ii", "name": "Infantry Tank Mk II Matilda", "nation": "UK", "era": 2, "year": 1938,
        "role": "Heavy Infantry Tank", "weight_t": 26.9, "gun": "40mm QF 2-pounder",
        "armor_mm": 78, "speed_kmh": 24, "power_hp": 190, "crew": 4, "produced": 2987,
        "x_offset": 0.22, "lane_offset": 0.18,
        "stats": {"firepower": 38, "armor": 68, "mobility": 26, "optics": 35, "impact": 84},
        "summary": "Nicknamed 'Queen of the Desert,' the Matilda II's 78mm cast frontal armor was immune to standard German 37mm/50mm tank guns at Arras (1940) and Italian anti-tank guns during Operation Compass (1940–41), forcing Rommel to deploy 88mm Flak anti-aircraft guns in a ground role.",
        "innovations": ["78mm heavy cast armor immune to early WWII AT guns", "3-man turret with high-velocity 2-pounder AP gun"]
    },
    {
        "id": "somua_s35", "name": "SOMUA S35", "nation": "FR", "era": 2, "year": 1936,
        "role": "Cavalry Medium Tank", "weight_t": 19.5, "gun": "47mm SA 35",
        "armor_mm": 47, "speed_kmh": 40, "power_hp": 190, "crew": 3, "produced": 440,
        "x_offset": -0.1, "lane_offset": -0.16,
        "stats": {"firepower": 42, "armor": 52, "mobility": 48, "optics": 28, "impact": 78},
        "summary": "Widely regarded as one of the finest medium/cavalry tanks of the late 1930s, featuring bolted cast armor sections, a potent 47mm gun, and good speed. At the Battle of Hannut (May 1940), S35s outduelled German Panzer IIIs and IVs before being outmaneuvered due to single-man turret overload and lack of radios.",
        "innovations": ["All-cast bolted hull and turret sections", "Superior balance of 47mm armor and 40 km/h speed in 1940"]
    },
    {
        "id": "char_b1", "name": "Char B1 bis", "nation": "FR", "era": 2, "year": 1937,
        "role": "Heavy Breakthrough Tank", "weight_t": 31.5, "gun": "75mm ABS hull howitzer + 47mm SA 35 turret",
        "armor_mm": 60, "speed_kmh": 28, "power_hp": 307, "crew": 4, "produced": 403,
        "x_offset": 0.2, "lane_offset": 0.18,
        "stats": {"firepower": 46, "armor": 62, "mobility": 30, "optics": 26, "impact": 80},
        "summary": "A heavily armored French breakthrough colossus with 60mm armor and dual guns (hull 75mm + turret 47mm). At Stonne (May 1940), a single Char B1 bis ('Eure' commanded by Pierre Billotte) destroyed 13 German Panzer III and IV tanks while shrugging off 140 hits.",
        "innovations": ["Naeder hydrostatic steering system for precision hull-gun aiming", "60mm armor nearly impenetrable to 1940 German tank guns"]
    },
    {
        "id": "panzer_ii", "name": "Panzerkampfwagen II", "nation": "DE", "era": 2, "year": 1936,
        "role": "Light Reconnaissance / Blitzkrieg Tank", "weight_t": 8.9, "gun": "20mm KwK 30 autocannon",
        "armor_mm": 15, "speed_kmh": 40, "power_hp": 140, "crew": 3, "produced": 1856,
        "x_offset": -0.1, "lane_offset": -0.15,
        "stats": {"firepower": 28, "armor": 24, "mobility": 50, "optics": 44, "impact": 82},
        "summary": "Built as a stopgap while Panzer III and IV production ramped up, the Panzer II formed the numerical backbone of the German Panzer divisions in Poland (1939) and France (1940), winning battles via universal onboard radios and combined-arms coordination rather than armor thickness.",
        "innovations": ["Standardized FuG radio in every tank for Blitzkrieg command", "20mm dual-purpose autocannon"]
    },
    {
        "id": "pz_38t", "name": "LT vz. 38 / Panzer 38(t)", "nation": "DE", "era": 2, "year": 1938,
        "role": "Light / Medium Tank", "weight_t": 9.8, "gun": "37mm KwK 38(t) L/47.8",
        "armor_mm": 25, "speed_kmh": 42, "power_hp": 125, "crew": 4, "produced": 1414,
        "x_offset": 0.2, "lane_offset": 0.18,
        "stats": {"firepower": 36, "armor": 30, "mobility": 52, "optics": 45, "impact": 85},
        "summary": "Designed in Czechoslovakia by ČKD and adopted by Germany after 1939, the mechanically reliable Panzer 38(t) equipped Rommel's 7th Panzer Division in France and fought deep into Barbarossa. Its chassis later spawned the legendary Hetzer and Marder III tank destroyers.",
        "innovations": ["Exceptional mechanical reliability & leaf-spring bogie chassis", "Chassis later adapted for Jagdpanzer 38(t) Hetzer"]
    },
    {
        "id": "t26", "name": "T-26 (Vickers Derivative)", "nation": "SU_RU", "era": 2, "year": 1931,
        "role": "Infantry Support Light Tank", "weight_t": 9.6, "gun": "45mm 20-K L/46",
        "armor_mm": 15, "speed_kmh": 31, "power_hp": 90, "crew": 3, "produced": 11218,
        "x_offset": -0.22, "lane_offset": -0.18,
        "stats": {"firepower": 40, "armor": 22, "mobility": 38, "optics": 30, "impact": 86},
        "summary": "The most widely produced tank of the 1930s. Derived from the British Vickers 6-Ton and up-gunned with a high-velocity Soviet 45mm cannon, the T-26 dominated the Spanish Civil War, clashed with Japanese armor at Khalkhin Gol (1939), and bore the brunt of Operation Barbarossa (1941).",
        "innovations": ["Potent 45mm 20-K gun outranging 1930s rivals", "Over 11,000 produced—backbone of 1930s Red Army"]
    },
    {
        "id": "bt7", "name": "BT-5 / BT-7 (Christie Fast Tank)", "nation": "SU_RU", "era": 2, "year": 1935,
        "role": "Cavalry / Fast Exploitation Tank", "weight_t": 13.9, "gun": "45mm 20-K L/46",
        "armor_mm": 22, "speed_kmh": 72, "power_hp": 450, "crew": 3, "produced": 5753,
        "x_offset": 0.2, "lane_offset": 0.18,
        "stats": {"firepower": 40, "armor": 26, "mobility": 78, "optics": 32, "impact": 92},
        "summary": "Born from American inventor J. Walter Christie's M1928 convertible wheel/track suspension, the BT-7 could reach 72 km/h and featured a sloped nose cone. Zhukov used massed BT-5/BT-7 formations to encircle the Japanese 6th Army at Khalkhin Gol (1939), and the BT-7 directly evolved into the T-34.",
        "innovations": ["Christie coil-spring independent suspension", "Sloped frontal hull armor & V-2 diesel testbeds leading directly to T-34"]
    },
    {
        "id": "christie_m2", "name": "Christie M1928 / M2 Medium", "nation": "US", "era": 2, "year": 1935,
        "role": "Experimental Fast / Medium Tank", "weight_t": 17.2, "gun": "37mm M3 + 7x .30 MGs",
        "armor_mm": 32, "speed_kmh": 42, "power_hp": 350, "crew": 6, "produced": 112,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 34, "armor": 32, "mobility": 60, "optics": 35, "impact": 88},
        "summary": "J. Walter Christie's revolutionary high-speed suspension spawned the Soviet BT/T-34 and British Cruiser lineages, while the US Ordnance Department developed the vertical volute spring suspension (VVSS) on the M2 Light and M2 Medium—the direct mechanical ancestor of the M3 Lee and M4 Sherman.",
        "innovations": ["Christie suspension exported to USSR & UK", "Vertical Volute Spring Suspension (VVSS) & radial aircraft engine layout"]
    },
    {
        "id": "type95_97", "name": "Type 95 Ha-Go / Type 97 Chi-Ha", "nation": "ASIA_OTHER", "era": 2, "year": 1936,
        "role": "Imperial Japanese Light / Medium Tank", "weight_t": 15.0, "gun": "57mm Type 97 / 47mm Type 1 (Kai)",
        "armor_mm": 25, "speed_kmh": 38, "power_hp": 170, "crew": 4, "produced": 4400,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 35, "armor": 28, "mobility": 48, "optics": 30, "impact": 78},
        "summary": "Pioneers of air-cooled diesel tank engines, the Type 95 Ha-Go and Type 97 Chi-Ha fought Soviet BT-7s at Khalkhin Gol (1939), spearheaded the rapid bicycle-and-tank blitz through Malaya and the Philippines (1941–42), and later clashed with US M3 Stuarts, M4 Shermans, and Soviet T-34-85s.",
        "innovations": ["World pioneer in air-cooled diesel tank engines", "Bell-crank coil suspension suited for jungle & island terrain"]
    },

    # ERA 3: EARLY-MID WWII (1939-1942)
    {
        "id": "crusader_valentine", "name": "Crusader III / Valentine", "nation": "UK", "era": 3, "year": 1940,
        "role": "Cruiser / Infantry Tank Pair", "weight_t": 19.7, "gun": "57mm QF 6-pounder (Crusader III)",
        "armor_mm": 51, "speed_kmh": 42, "power_hp": 340, "crew": 3, "produced": 13500,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 50, "armor": 48, "mobility": 58, "optics": 45, "impact": 83},
        "summary": "The workhorses of the British Eighth Army in North Africa. Using Christie suspension, the low-slung Crusader raced across the desert and in Mk III form packed a potent 57mm 6-pounder at El Alamein, while the ultra-reliable Valentine served both in North Africa and via Lend-Lease in the USSR.",
        "innovations": ["Christie suspension cruiser mobility", "Up-gunned with 57mm 6-pounder capable of penetrating Panzer III/IV"]
    },
    {
        "id": "panzer_iii", "name": "Panzerkampfwagen III (Ausf. F–L)", "nation": "DE", "era": 3, "year": 1939,
        "role": "Medium Anti-Armor Tank", "weight_t": 22.3, "gun": "50mm KwK 39 L/60",
        "armor_mm": 50, "speed_kmh": 40, "power_hp": 300, "crew": 5, "produced": 5774,
        "x_offset": -0.2, "lane_offset": -0.18,
        "stats": {"firepower": 48, "armor": 48, "mobility": 52, "optics": 62, "impact": 90},
        "summary": "Heinz Guderian's intended tank-killer for the Panzer Divisions. It pioneered the modern 3-man turret (commander in cupola exclusively directing the crew, gunner, loader) and torsion-bar suspension. Fought in France, North Africa, and Barbarossa before its turret ring reached its limit against the T-34.",
        "innovations": ["Three-man turret ergonomic standard (Commander, Gunner, Loader)", "Torsion-bar suspension & Intercom + Radio in every vehicle"]
    },
    {
        "id": "panzer_iv", "name": "Panzerkampfwagen IV (Ausf. D–H)", "nation": "DE", "era": 3, "year": 1939,
        "role": "Medium Mainstay Tank", "weight_t": 25.0, "gun": "75mm KwK 40 L/48",
        "armor_mm": 80, "speed_kmh": 38, "power_hp": 300, "crew": 5, "produced": 8553,
        "x_offset": 0.2, "lane_offset": 0.18,
        "stats": {"firepower": 64, "armor": 56, "mobility": 48, "optics": 66, "impact": 95},
        "summary": "The only German tank to remain in continuous production throughout all of WWII. Originally armed with a short 75mm infantry-support gun, its wide turret ring allowed up-gunning to the long, high-velocity 75mm KwK 40 (Ausf. F2/G/H), turning it into a lethal adversary from El Alamein and Kursk to Normandy.",
        "innovations": ["Wide turret ring permitting upgrade from short 75mm L/24 to long 75mm L/48", "Schürzen spaced side skirts against anti-tank rifles and shaped charges"]
    },
    {
        "id": "t34_76", "name": "T-34/76", "nation": "SU_RU", "era": 3, "year": 1940,
        "role": "Medium Tank", "weight_t": 26.5, "gun": "76.2mm F-34 L/42",
        "armor_mm": 45, "speed_kmh": 53, "power_hp": 500, "crew": 4, "produced": 35120,
        "x_offset": -0.2, "lane_offset": -0.18,
        "stats": {"firepower": 58, "armor": 64, "mobility": 70, "optics": 36, "impact": 100},
        "summary": "Mikhail Koshkin's masterpiece that shocked the Wehrmacht in 1941. Combining 45mm armor sloped at 60° (doubling effective thickness), a 76.2mm dual-purpose gun, wide tracks for Russian mud/snow, and the V-2 aluminum diesel engine, the T-34 forced Germany to design the Panther and Tiger.",
        "innovations": ["60° sloped all-around armor revolutionary geometry", "500 hp V-2 V12 diesel engine & wide low-ground-pressure tracks", "Unmatched wartime mass-production simplicity"]
    },
    {
        "id": "kv1", "name": "KV-1 / KV-2 Heavy Tank", "nation": "SU_RU", "era": 3, "year": 1939,
        "role": "Heavy Breakthrough Tank", "weight_t": 45.0, "gun": "76.2mm ZiS-5 (KV-1) / 152mm M-10 (KV-2)",
        "armor_mm": 90, "speed_kmh": 35, "power_hp": 600, "crew": 5, "produced": 5219,
        "x_offset": 0.2, "lane_offset": 0.18,
        "stats": {"firepower": 58, "armor": 74, "mobility": 38, "optics": 34, "impact": 87},
        "summary": "In June 1941 at Raseiniai and Brody, KV-1 and KV-2 heavy tanks proved virtually invulnerable to every tank gun in the German arsenal. Featuring torsion-bar suspension and up to 90–110mm of armor, a single KV-1 under Zinoviy Kolobanov ambushed and destroyed 22 German tanks in 30 minutes.",
        "innovations": ["Heavy torsion-bar suspension", "90mm+ armor immune to 37mm and 50mm anti-tank guns in 1941"]
    },
    {
        "id": "m3_lee_grant", "name": "M3 Lee / Grant", "nation": "US", "era": 3, "year": 1941,
        "role": "Medium Tank", "weight_t": 27.9, "gun": "75mm M2/M3 (hull) + 37mm M5 (turret)",
        "armor_mm": 51, "speed_kmh": 42, "power_hp": 400, "crew": 6, "produced": 6258,
        "x_offset": -0.22, "lane_offset": -0.18,
        "stats": {"firepower": 54, "armor": 48, "mobility": 50, "optics": 48, "impact": 79},
        "summary": "Rushed into production to get a 75mm gun onto the battlefield before a large turret could be cast, the M3 Grant stunned Rommel's Afrika Korps at Gazala (May 1942) by outranging German Panzer IIIs with both high-explosive and armor-piercing rounds while the M4 Sherman was finalized.",
        "innovations": ["First vertical-stabilized 75mm and 37mm guns", "Shared M3 chassis, engine, and drivetrain directly with the M4 Sherman"]
    },
    {
        "id": "m4_sherman", "name": "M4 Sherman (75mm)", "nation": "US", "era": 3, "year": 1942,
        "role": "Medium Tank", "weight_t": 30.3, "gun": "75mm M3 L/40",
        "armor_mm": 51, "speed_kmh": 48, "power_hp": 400, "crew": 5, "produced": 49234,
        "x_offset": 0.22, "lane_offset": 0.18,
        "stats": {"firepower": 56, "armor": 56, "mobility": 62, "optics": 65, "impact": 99},
        "summary": "The Arsenal of Democracy's iconic workhorse. Debuting at Second El Alamein (Oct 1942), the M4 Sherman combined sloped 51mm frontal armor ( ~90mm effective), a gyrostabilized 75mm gun, dual commander/gunner periscopes, and unmatched mechanical reliability across Europe, Africa, the Pacific, and USSR.",
        "innovations": ["Westinghouse vertical gun gyrostabilizer", "Commander override traverse & dual sighting system", "Standardized shipping dimensions & global logistics reliability"]
    },

    # ERA 4: LATE WWII (1943-1945)
    {
        "id": "cromwell_firefly", "name": "Sherman Firefly / Cromwell", "nation": "UK", "era": 4, "year": 1944,
        "role": "Cruiser / Heavy Tank Hunter", "weight_t": 32.7, "gun": "76.2mm QF 17-pounder (Firefly)",
        "armor_mm": 76, "speed_kmh": 64, "power_hp": 600, "crew": 4, "produced": 6140,
        "x_offset": -0.2, "lane_offset": -0.18,
        "stats": {"firepower": 78, "armor": 58, "mobility": 68, "optics": 62, "impact": 90},
        "summary": "By mounting the Rolls-Royce Meteor (Spitfire Merlin) engine in the Cromwell and fitting the devastating 17-pounder anti-tank gun sideways into the M4 Sherman ('Firefly'), Britain fielded an armor killer in Normandy (1944) that penetrated Tiger I and Panther frontal armor at over 1,000 meters.",
        "innovations": ["QF 17-pounder firing APDS (Armor-Piercing Discarding Sabot) rounds", "600 hp Rolls-Royce Meteor V12 engine in Cromwell"]
    },
    {
        "id": "centurion_mk1", "name": "Centurion Mk 1 / Mk 3", "nation": "UK", "era": 4, "year": 1945,
        "role": "First Universal Tank (MBT)", "weight_t": 50.8, "gun": "76.2mm 17-pdr (Mk 1) / 84mm 20-pdr (Mk 3)",
        "armor_mm": 118, "speed_kmh": 35, "power_hp": 650, "crew": 4, "produced": 4423,
        "x_offset": 0.22, "lane_offset": 0.18,
        "stats": {"firepower": 82, "armor": 78, "mobility": 58, "optics": 76, "impact": 99},
        "summary": "Conceived in 1943–45 to end the split between lightly armored Cruiser tanks and slow Infantry tanks, the Centurion became the world's first true 'Universal Tank' (Main Battle Tank). Featuring sloped armor, Horstmann suspension, and full two-plane gun stabilization, it dominated from Korea to the Golan Heights.",
        "innovations": ["First Universal Tank / Main Battle Tank concept", "Full two-axis gyroscopic gun stabilization (fire on the move)", "Horstmann coil-spring external bogie suspension for easy mine repair"]
    },
    {
        "id": "tiger_i", "name": "Panzer VI Tiger I", "nation": "DE", "era": 4, "year": 1942,
        "role": "Heavy Breakthrough Tank", "weight_t": 54.0, "gun": "88mm KwK 36 L/56",
        "armor_mm": 100, "speed_kmh": 38, "power_hp": 700, "crew": 5, "produced": 1347,
        "x_offset": -0.25, "lane_offset": -0.22,
        "stats": {"firepower": 80, "armor": 74, "mobility": 42, "optics": 74, "impact": 96},
        "summary": "Armed with the legendary 88mm KwK 36 L/56 gun and protected by 100mm of frontal armor, the Tiger I created 'Tiger-phobia' from Kursk and Tunisia to Villers-Bocage. While formidable in long-range gunnery, its complex interleaved roadwheels and high maintenance limited production to 1,347 units.",
        "innovations": ["88mm KwK 36 high-velocity gun with Carl Zeiss TZF 9b optics", "Double-differential Maybach Olvar regenerative steering"]
    },
    {
        "id": "panther", "name": "Panzer V Panther", "nation": "DE", "era": 4, "year": 1943,
        "role": "Heavy-Medium Tank", "weight_t": 44.8, "gun": "75mm KwK 42 L/70",
        "armor_mm": 80, "speed_kmh": 55, "power_hp": 700, "crew": 5, "produced": 6000,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 82, "armor": 76, "mobility": 62, "optics": 75, "impact": 96},
        "summary": "Germany's direct response to the Soviet T-34. Combining 80mm of 55°-sloped frontal glacis armor with the hyper-velocity 75mm L/70 cannon, the Panther debuted at Kursk (1943) and proved a lethal long-range duelist on both fronts, foreshadowing post-war Main Battle Tank weight and firepower.",
        "innovations": ["80mm sloped glacis plate inspired by T-34 encounter", "Hyper-velocity 75mm KwK 42 L/70 (935 m/s muzzle velocity)", "Late-war FG 1250 active infrared night-vision sights"]
    },
    {
        "id": "tiger_ii", "name": "Panzer VI Ausf. B Tiger II (King Tiger)", "nation": "DE", "era": 4, "year": 1944,
        "role": "Super-Heavy Breakthrough Tank", "weight_t": 68.5, "gun": "88mm KwK 43 L/71",
        "armor_mm": 150, "speed_kmh": 38, "power_hp": 700, "crew": 5, "produced": 492,
        "x_offset": 0.25, "lane_offset": 0.22,
        "stats": {"firepower": 88, "armor": 88, "mobility": 32, "optics": 76, "impact": 86},
        "summary": "Combining the Panther's sloped armor geometry (150mm at 50°—never penetrated in combat from the front) with the devastating long-barreled 88mm KwK 43 L/71 gun, the 68.5-ton King Tiger could destroy any Allied tank at 2,500m, though its weight strained bridges and final drives from Normandy to Lake Balaton.",
        "innovations": ["150mm sloped glacis armor impervious to all WWII tank guns", "88mm KwK 43 L/71 long-barrel cannon"]
    },
    {
        "id": "t34_85", "name": "T-34-85", "nation": "SU_RU", "era": 4, "year": 1944,
        "role": "Medium Tank", "weight_t": 32.0, "gun": "85mm ZiS-S-53",
        "armor_mm": 90, "speed_kmh": 55, "power_hp": 500, "crew": 5, "produced": 48950,
        "x_offset": -0.2, "lane_offset": -0.18,
        "stats": {"firepower": 72, "armor": 68, "mobility": 70, "optics": 58, "impact": 99},
        "summary": "After Kursk showed the 76mm gun struggled against Tiger and Panther frontal armor, Soviet engineers gave the T-34 a roomy 3-man turret armed with an 85mm anti-aircraft-derived cannon. Spearheading Operation Bagration and the Battle of Berlin, it later fought in Korea, Vietnam, and the Middle East.",
        "innovations": ["Enlarged 3-man cast turret curing the T-34/76's ergonomic flaw", "85mm ZiS-S-53 gun capable of defeating Tigers and Panthers at combat range"]
    },
    {
        "id": "is2", "name": "IS-2 (Iosef Stalin-2)", "nation": "SU_RU", "era": 4, "year": 1944,
        "role": "Heavy Breakthrough Tank", "weight_t": 46.0, "gun": "122mm D-25T L/43",
        "armor_mm": 120, "speed_kmh": 37, "power_hp": 520, "crew": 4, "produced": 3854,
        "x_offset": 0.2, "lane_offset": 0.18,
        "stats": {"firepower": 86, "armor": 82, "mobility": 48, "optics": 56, "impact": 91},
        "summary": "Weighing less than a Panther (46 tons) yet packing a ferocious 122mm gun and 120mm sloped armor, the IS-2 smashed German defensive lines and duelled Tiger IIs in Poland and Hungary (1944–45). Its massive 25 kg shells could crack heavy German armor by sheer kinetic impact even without full penetration.",
        "innovations": ["122mm D-25T heavy breakthrough & anti-armor cannon", "46-ton weight profile lighter than Tiger I despite heavier armor and gun"]
    },
    {
        "id": "m4a3e8", "name": "M4A3E8 Sherman 'Easy Eight'", "nation": "US", "era": 4, "year": 1944,
        "role": "Medium Tank", "weight_t": 33.6, "gun": "76mm M1A2 (HVAP)",
        "armor_mm": 64, "speed_kmh": 45, "power_hp": 500, "crew": 5, "produced": 4542,
        "x_offset": -0.2, "lane_offset": -0.18,
        "stats": {"firepower": 72, "armor": 64, "mobility": 66, "optics": 68, "impact": 92},
        "summary": "The pinnacle of wartime Sherman evolution: Horizontal Volute Spring Suspension (HVSS) with wide tracks, a 500 hp Ford GAA V8 engine, 'wet' ammo stowage (reducing burn-out rates to under 15%), and a high-velocity 76mm gun firing tungsten-core HVAP rounds. Excelled in the Ardennes and Korea.",
        "innovations": ["HVSS wide-track suspension for low ground pressure", "Wet ammunition stowage drastically improving crew survival", "76mm M1A2 gun with HVAP tungsten sub-caliber rounds"]
    },
    {
        "id": "m26_pershing", "name": "M26 Pershing", "nation": "US", "era": 4, "year": 1945,
        "role": "Heavy / Medium Tank", "weight_t": 41.9, "gun": "90mm M3 L/53",
        "armor_mm": 102, "speed_kmh": 40, "power_hp": 500, "crew": 5, "produced": 2202,
        "x_offset": 0.2, "lane_offset": 0.18,
        "stats": {"firepower": 80, "armor": 76, "mobility": 54, "optics": 72, "impact": 91},
        "summary": "Armed with a potent 90mm M3 cannon and torsion-bar suspension, the M26 Pershing arrived in Europe in early 1945, famously duelling and destroying a German Panther right in front of Cologne Cathedral. It later countered North Korean T-34-85s in 1950 and birthed the entire Patton tank lineage.",
        "innovations": ["90mm M3 cannon matching the Tiger I's 88mm", "Torsion-bar chassis directly evolving into M46/M47/M48/M60 Patton series"]
    },

    # ERA 5: EARLY COLD WAR / 1st & 2nd GEN MBT (1946-1973)
    {
        "id": "chieftain", "name": "FV4201 Chieftain", "nation": "UK", "era": 5, "year": 1966,
        "role": "2nd Gen Main Battle Tank", "weight_t": 55.0, "gun": "120mm L11A5 rifled",
        "armor_mm": 195, "speed_kmh": 48, "power_hp": 750, "crew": 4, "produced": 2265,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 88, "armor": 84, "mobility": 50, "optics": 80, "impact": 88},
        "summary": "Rejecting the period philosophy of sacrificing armor for speed, Britain built the Chieftain with a supine (reclining) driver to lower hull height, heavily sloped cast armor, and the world's most powerful 1960s tank gun: the 120mm L11 rifled cannon. Fought extensively in the Iran–Iraq War and 1991 Gulf War (Kuwait).",
        "innovations": ["Supine reclining driver position reducing hull silhouette", "120mm L11 rifled gun with bag-charge separated ammunition", "Later upgraded with Stillbrew composite turret appliqué"]
    },
    {
        "id": "amx13_30", "name": "AMX-13 / AMX-30", "nation": "FR", "era": 5, "year": 1952,
        "role": "Light Oscillating-Turret / 2nd Gen MBT", "weight_t": 36.0, "gun": "75/90mm (AMX-13) / 105mm CN-105-F1 (AMX-30)",
        "armor_mm": 80, "speed_kmh": 65, "power_hp": 720, "crew": 4, "produced": 11200,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 82, "armor": 64, "mobility": 82, "optics": 78, "impact": 87},
        "summary": "The AMX-13 pioneered the two-piece oscillating turret with dual 6-round revolver autoloaders (fighting in Sinai 1956/1967 and Indo-Pak 1965), while the AMX-30 became France's highly mobile 2nd-generation MBT armed with the ingenious Obus G ball-bearing spin-stabilized HEAT shell and coaxial 20mm autocannon.",
        "innovations": ["AMX-13 FL-10 oscillating turret with revolver autoloader", "AMX-30 Obus G dual-shell ball-bearing HEAT round + 20mm coaxial autocannon"]
    },
    {
        "id": "leopard1", "name": "Leopard 1 (A1–A5)", "nation": "DE", "era": 5, "year": 1965,
        "role": "2nd Gen Main Battle Tank", "weight_t": 42.2, "gun": "105mm Royal Ordnance L7A3",
        "armor_mm": 70, "speed_kmh": 65, "power_hp": 830, "crew": 4, "produced": 6565,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 84, "armor": 66, "mobility": 85, "optics": 84, "impact": 93},
        "summary": "West Germany's return to tank design prioritized agility, precision stereoscopic rangefinders, and the British 105mm L7 gun over thick armor (believing HEAT warheads defeated all conventional steel). Standard tank of NATO European armies for decades and still seeing combat today in Ukraine (Leopard 1A5).",
        "innovations": ["Multi-fuel MTU powerpack exchangeable in the field in 20 minutes", "Precision optical coincidence/stereoscopic rangefinder & stabilized 105mm L7A3"]
    },
    {
        "id": "t54_55", "name": "T-54 / T-55", "nation": "SU_RU", "era": 5, "year": 1947,
        "role": "1st Gen Main Battle Tank", "weight_t": 36.0, "gun": "100mm D-10T rifled",
        "armor_mm": 200, "speed_kmh": 50, "power_hp": 580, "crew": 4, "produced": 100000,
        "x_offset": -0.22, "lane_offset": -0.18,
        "stats": {"firepower": 78, "armor": 76, "mobility": 72, "optics": 66, "impact": 100},
        "summary": "The most produced tank in human history (~100,000 built across the USSR, Poland, Czechoslovakia, and China as the Type 59). Evolving from the T-34-85 via the T-44, its low hemispherical 'frying-pan' turret, 100mm D-10T gun, and PAZ nuclear NBC protection fought in almost every Cold War conflict.",
        "innovations": ["Most produced tank in history (~100,000 units including Type 59)", "Hemispherical cast turret & PAZ pressurized NBC nuclear-fallout protection"]
    },
    {
        "id": "t62", "name": "T-62", "nation": "SU_RU", "era": 5, "year": 1961,
        "role": "2nd Gen Main Battle Tank", "weight_t": 40.0, "gun": "115mm U-5TS smoothbore",
        "armor_mm": 242, "speed_kmh": 50, "power_hp": 580, "crew": 4, "produced": 22700,
        "x_offset": 0.22, "lane_offset": 0.18,
        "stats": {"firepower": 84, "armor": 78, "mobility": 70, "optics": 70, "impact": 91},
        "summary": "The world's first production tank armed with a smoothbore cannon (115mm U-5TS) firing fin-stabilized armor-piercing sabot darts (APFSDS) at 1,615 m/s, plus an automatic spent-casing ejector out the rear of the turret. Clashed fiercely with Israeli Centurions and Pattons in the 1973 Yom Kippur War.",
        "innovations": ["World's first smoothbore tank cannon (115mm U-5TS) firing APFSDS fin-stabilized darts", "Automatic rear turret shell-casing ejection port"]
    },
    {
        "id": "m48_m60_patton", "name": "M48 / M60 Patton", "nation": "US", "era": 5, "year": 1952,
        "role": "1st & 2nd Gen Main Battle Tank", "weight_t": 52.6, "gun": "90mm M41 (M48) / 105mm M68 L7 (M60)",
        "armor_mm": 250, "speed_kmh": 48, "power_hp": 750, "crew": 4, "produced": 27000,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 84, "armor": 80, "mobility": 68, "optics": 82, "impact": 95},
        "summary": "America's Cold War backbone. Evolving from the M26 Pershing and M46/M47, the M48 fought in Vietnam and Indo-Pak 1965, while the M60 (armed with the 105mm M68/L7 gun and Continental diesel engine) fought in the 1973 Yom Kippur War, 1982 Lebanon, and 1991 Desert Storm.",
        "innovations": ["Boat-shaped cast hull for mine & ballistic deflection", "M60A1/A3 passive thermal sights, laser rangefinder & solid-state ballistic computer"]
    },
    {
        "id": "shot_magach", "name": "Sho't Kal (Centurion) / Magach", "nation": "IL", "era": 5, "year": 1967,
        "role": "Up-gunned Desert & Golan MBT", "weight_t": 52.0, "gun": "105mm Royal Ordnance L7",
        "armor_mm": 152, "speed_kmh": 43, "power_hp": 750, "crew": 4, "produced": 2600,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 85, "armor": 82, "mobility": 68, "optics": 84, "impact": 92},
        "summary": "Israel upgraded British Centurions ('Sho't Kal') and US M48/M60s ('Magach') with the 105mm L7 gun, US Continental AVDS-1790 diesel engines, and later Blazer Explosive Reactive Armor (ERA). In October 1973, ~105 Sho't Kal tanks held the 'Valley of Tears' on the Golan Heights against ~500 Syrian T-55/T-62s.",
        "innovations": ["105mm L7 + Continental diesel powerpack retrofit", "First combat use of Blazer Explosive Reactive Armor (ERA) in 1982"]
    },
    {
        "id": "type59_74_strv103", "name": "Type 59 (CN) / Type 74 (JP) / Strv 103 (SE)", "nation": "ASIA_OTHER", "era": 5, "year": 1959,
        "role": "Regional Cold War MBT Triad", "weight_t": 39.7, "gun": "100mm (Type 59) / 105mm L7 (Type 74 & Strv 103)",
        "armor_mm": 200, "speed_kmh": 55, "power_hp": 720, "crew": 3, "produced": 10900,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 82, "armor": 76, "mobility": 76, "optics": 80, "impact": 86},
        "summary": "While China mass-produced over 9,500 Type 59s (T-54A license) that fought in Vietnam, Indo-Pak 1971, and the Sino-Vietnamese & Gulf Wars, Japan's Type 74 and Sweden's turretless Strv 103 'S-Tank' pioneered hydropneumatic active kneeling suspension to aim over ridgelines.",
        "innovations": ["Hydropneumatic active suspension (Strv 103 & Type 74)", "Strv 103 turretless gas-turbine + diesel hybrid with 3-man crew and autoloader"]
    },

    # ERA 6: LATE COLD WAR / 3RD GEN MBT (1974-1991)
    {
        "id": "challenger1", "name": "FV4030 Challenger 1", "nation": "UK", "era": 6, "year": 1983,
        "role": "3rd Gen Composite-Armor MBT", "weight_t": 62.0, "gun": "120mm L11A5 rifled",
        "armor_mm": 650, "speed_kmh": 56, "power_hp": 1200, "crew": 4, "produced": 420,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 89, "armor": 94, "mobility": 72, "optics": 88, "impact": 89},
        "summary": "First tank designed around Britain's revolutionary 'Chobham' (Burlington) ceramic-matrix composite armor and hydropneumatic Hydrogas suspension. In the 1991 Gulf War, Challenger 1s destroyed ~300 Iraqi tanks without a single loss, scoring the longest tank-vs-tank kill at the time (4,700m).",
        "innovations": ["Chobham (Burlington) ceramic/metal composite armor array", "Hydrogas hydropneumatic suspension & 4,700m combat kill record in 1991"]
    },
    {
        "id": "leopard2_a4", "name": "Leopard 2 (A0–A4)", "nation": "DE", "era": 6, "year": 1979,
        "role": "3rd Gen Main Battle Tank", "weight_t": 55.1, "gun": "120mm Rheinmetall Rh-120 L/44 smoothbore",
        "armor_mm": 600, "speed_kmh": 68, "power_hp": 1500, "crew": 4, "produced": 3600,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 93, "armor": 90, "mobility": 92, "optics": 93, "impact": 98},
        "summary": "Born from lessons of the joint US-German MBT-70 project, the Leopard 2 combined the world-standard Rheinmetall 120mm L/44 smoothbore cannon, 1,500 hp MTU diesel engine, EMES-15 laser/thermal fire control, and composite armor—becoming the benchmark MBT adopted across 20+ nations.",
        "innovations": ["Rheinmetall 120mm L/44 smoothbore cannon (NATO standard)", "EMES-15 stabilized hunter-killer thermal/laser fire control & 1,500 hp MTU MB 873"]
    },
    {
        "id": "t64_t80", "name": "T-64 / T-80BV", "nation": "SU_RU", "era": 6, "year": 1966,
        "role": "High-End Soviet/Ukrainian Autoloader MBT", "weight_t": 42.5, "gun": "125mm 2A46 smoothbore + ATGM",
        "armor_mm": 550, "speed_kmh": 70, "power_hp": 1100, "crew": 3, "produced": 18500,
        "x_offset": -0.22, "lane_offset": -0.18,
        "stats": {"firepower": 90, "armor": 86, "mobility": 88, "optics": 82, "impact": 94},
        "summary": "Alexander Morozov's radical T-64 introduced the 3-man crew, vertical-carousel autoloader, 125mm smoothbore cannon, and 'Combination K' fiberglass/ceramic composite armor a decade before Western 3rd-gen MBTs. The T-80 added a 1,100+ hp gas turbine, and both T-64BV and T-80BVM clash fiercely in Ukraine.",
        "innovations": ["World's first composite armor ('Combination K') & 125mm 2A46 smoothbore", "3-man crew with korzina electro-hydraulic autoloader & gun-launched Kobra/Refleks ATGMs"]
    },
    {
        "id": "t72", "name": "T-72 (Ural / M1 / B)", "nation": "SU_RU", "era": 6, "year": 1973,
        "role": "Mass-Production 2nd/3rd Gen MBT", "weight_t": 41.5, "gun": "125mm 2A46 smoothbore",
        "armor_mm": 520, "speed_kmh": 60, "power_hp": 780, "crew": 3, "produced": 25000,
        "x_offset": 0.22, "lane_offset": 0.18,
        "stats": {"firepower": 88, "armor": 84, "mobility": 82, "optics": 76, "impact": 98},
        "summary": "Designed at Uralvagonzavod as a simpler, more rugged V-12 diesel alternative to the complex T-64, the T-72 became the most widely fielded 125mm MBT in the world. Fought in Lebanon (1982), Iran-Iraq, the 1991 & 2003 Gulf Wars, the Balkans (as M-84), Syria, and Ukraine.",
        "innovations": ["Compact horizontal-carousel AZ autoloader", "Kontakt-1 & Kontakt-5 Explosive Reactive Armor (T-72B) & 9K120 Svir laser-guided missiles"]
    },
    {
        "id": "m1_abrams", "name": "M1 / M1A1 HA Abrams", "nation": "US", "era": 6, "year": 1980,
        "role": "3rd Gen Gas-Turbine Composite MBT", "weight_t": 61.3, "gun": "120mm M256 smoothbore (M1A1)",
        "armor_mm": 680, "speed_kmh": 67, "power_hp": 1500, "crew": 4, "produced": 10400,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 94, "armor": 95, "mobility": 90, "optics": 95, "impact": 99},
        "summary": "Powered by a 1,500 hp Honeywell AGT1500 gas turbine, armored with Chobham + Depleted Uranium (DU) mesh, and storing all 120mm rounds behind blast doors with roof blow-out panels, the M1A1 HA Abrams dominated the Battle of 73 Easting and Medina Ridge (1991), destroying hundreds of Iraqi T-72s through sandstorms via FLIR thermals.",
        "innovations": ["Compartmentalized bustle ammo rack with blow-out panels (preventing turret toss)", "Depleted Uranium (DU) heavy armor mesh & M829A1 'Silver Bullet' DU APFSDS"]
    },
    {
        "id": "merkava_i_ii", "name": "Merkava Mk I / Mk II", "nation": "IL", "era": 6, "year": 1979,
        "role": "Crew-Survival Front-Engine MBT", "weight_t": 60.0, "gun": "105mm M68 rifled",
        "armor_mm": 580, "speed_kmh": 46, "power_hp": 908, "crew": 4, "produced": 830,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 86, "armor": 92, "mobility": 68, "optics": 88, "impact": 90},
        "summary": "Conceived by Gen. Israel Tal after the brutal casualties of the 1973 Yom Kippur War, the Merkava placed its engine and transmission at the very front to shield the crew, added a rear clamshell door to evacuate wounded soldiers or carry infantry, and defeated Syrian T-72s in the 1982 Lebanon War.",
        "innovations": ["Front-mounted engine block acting as secondary crew armor", "Rear clamshell access door for under-armor resupply & medevac", "Internal 60mm mortar for engaging hidden anti-tank infantry"]
    },

    # ERA 7: MODERN / DIGITAL & APS (1992-2026)
    {
        "id": "challenger2_3", "name": "Challenger 2 / Challenger 3", "nation": "UK", "era": 7, "year": 1998,
        "role": "Advanced Composite & Digital MBT", "weight_t": 64.0, "gun": "120mm L30A1 rifled (CR2) / L55A1 smoothbore (CR3)",
        "armor_mm": 850, "speed_kmh": 59, "power_hp": 1200, "crew": 4, "produced": 447,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 94, "armor": 98, "mobility": 76, "optics": 94, "impact": 91},
        "summary": "Protected by second-generation Dorchester composite armor, the Challenger 2 served in Bosnia, Kosovo, the 2003 Siege of Basra (where one survived 14–70 RPG hits and a MILAN missile), and with the Ukrainian Air Assault Forces since 2023. Challenger 3 upgrades to a 120mm L55A1 smoothbore gun and Trophy APS.",
        "innovations": ["Dorchester Level 2 composite armor + Streetfighter urban packages", "Challenger 3 digital turret with Rheinmetall 120mm L55A1 & Trophy APS"]
    },
    {
        "id": "leclerc", "name": "AMX-56 Leclerc XLR", "nation": "FR", "era": 7, "year": 1992,
        "role": "Autoloaded Digital 3rd+ Gen MBT", "weight_t": 57.4, "gun": "120mm GIAT CN120-26 L/52 smoothbore",
        "armor_mm": 780, "speed_kmh": 71, "power_hp": 1500, "crew": 3, "produced": 862,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 95, "armor": 91, "mobility": 96, "optics": 96, "impact": 90},
        "summary": "One of the first Western MBTs to adopt a bustle-mounted automatic loader (reducing crew to 3), hydropneumatic suspension, modular titanium/tungsten composite armor, and the SICS battlefield management network. Its hyperbar V8X engine accelerates 57 tons to 71 km/h.",
        "innovations": ["Bustle-mounted 22-round isolated belt autoloader (12 rounds/min)", "Hyperbar turbo-gas-turbine supercharged diesel & full digital databus"]
    },
    {
        "id": "leopard2_a7_kf51", "name": "Leopard 2A6 / 2A7V / 2A8", "nation": "DE", "era": 7, "year": 2001,
        "role": "Modern Benchmark NATO MBT", "weight_t": 66.5, "gun": "120mm Rheinmetall Rh-120 L/55A1 smoothbore",
        "armor_mm": 880, "speed_kmh": 63, "power_hp": 1500, "crew": 4, "produced": 1200,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 98, "armor": 96, "mobility": 88, "optics": 98, "impact": 98},
        "summary": "Featuring the longer 120mm L/55 high-pressure smoothbore barrel, wedge-shaped NERA spaced turret armor, 3rd-gen Attica thermals, programmable DM11 airburst ammunition, and Trophy APS (2A8), Leopard 2A4/2A6 tanks entered high-intensity combat in Ukraine in 2023–2024.",
        "innovations": ["120mm L/55A1 ultra-high-pressure barrel firing DM63/DM73 APFSDS", "Wedge NERA turret armor + EuroTrophy Active Protection System (2A8)"]
    },
    {
        "id": "t90m", "name": "T-90A / T-90M Proryv-3", "nation": "SU_RU", "era": 7, "year": 1992,
        "role": "Modernized Russian MBT", "weight_t": 48.0, "gun": "125mm 2A46M-5 smoothbore",
        "armor_mm": 800, "speed_kmh": 60, "power_hp": 1130, "crew": 3, "produced": 4000,
        "x_offset": -0.22, "lane_offset": -0.18,
        "stats": {"firepower": 93, "armor": 90, "mobility": 84, "optics": 90, "impact": 94},
        "summary": "Originally developed as the T-72BU combining the T-72B hull with the T-80U's advanced fire control, the T-90M 'Proryv-3' features a newly welded turret, Relikt heavy ERA, Kalina digital hunter-killer sights, and an isolated rear bustle compartment for spare rounds. Heavily engaged across the Ukrainian front.",
        "innovations": ["Welded turret with Relikt dual-flyer-plate ERA & Nakidka thermal/radar cloak", "Kalina hunter-killer digital FCS & 2A46M-5 gun firing Svinets-1/2 long-rod darts"]
    },
    {
        "id": "t84_oplot", "name": "T-64BV Zr.2017 / BM Oplot", "nation": "SU_RU", "era": 7, "year": 1999,
        "role": "Ukrainian Modernized MBT Lineage", "weight_t": 51.0, "gun": "125mm KBA-3 smoothbore + Kombat ATGM",
        "armor_mm": 800, "speed_kmh": 70, "power_hp": 1200, "crew": 3, "produced": 900,
        "x_offset": 0.22, "lane_offset": 0.18,
        "stats": {"firepower": 91, "armor": 88, "mobility": 86, "optics": 88, "impact": 89},
        "summary": "Ukraine's Kharkiv Morozov Design Bureau (birthplace of the T-34 and T-64) evolved the T-64/T-80UD lineage with 6TD-2 opposed-piston diesel engines, Nozh/Duplet tandem-shaped-charge ERA, and thermal sights—defending Chernihiv, Kyiv, Kharkiv, and Donbas against Russian T-72B3, T-80BVM, and T-90M armor.",
        "innovations": ["Nozh / Duplet linear shaped-charge ERA slicing incoming APFSDS rods", "6TD-2 1,200 hp opposed-piston diesel engine & PNK-6 panoramic sight"]
    },
    {
        "id": "m1a2_sepv3", "name": "M1A2 SEPv3 Abrams", "nation": "US", "era": 7, "year": 1999,
        "role": "Networked Heavy 3rd+ Gen MBT", "weight_t": 66.8, "gun": "120mm M256 smoothbore (M829A4 / AMP)",
        "armor_mm": 920, "speed_kmh": 67, "power_hp": 1500, "crew": 4, "produced": 3500,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 98, "armor": 98, "mobility": 86, "optics": 99, "impact": 98},
        "summary": "Equipped with Next-Generation Evolution Armor (NGAP), Trophy Active Protection System, 3rd-gen FLIR independent commander thermal viewer (CITV), Ammunition DataLink for programmable M1147 AMP rounds, and M829A4 depleted-uranium penetrators. M1A1/M1A2 variants fought in Iraq (2003), Yemen, and Ukraine (2024).",
        "innovations": ["M829A4 5th-gen DU APFSDS & M1147 Advanced Multi-Purpose programmable shell", "Integrated Trophy APS, CITV 3rd-gen FLIR & FBCB2/JBC-P digital battle command"]
    },
    {
        "id": "merkava_iv", "name": "Merkava Mk IVM Windbreaker / Barak", "nation": "IL", "era": 7, "year": 2004,
        "role": "APS-Protected Urban & Desert MBT", "weight_t": 65.0, "gun": "120mm MG253 smoothbore + LAHAT ATGM",
        "armor_mm": 860, "speed_kmh": 64, "power_hp": 1500, "crew": 4, "produced": 660,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 94, "armor": 97, "mobility": 82, "optics": 98, "impact": 94},
        "summary": "The first tank in history to enter combat with a battle-proven hard-kill Active Protection System: Rafael Trophy ('Windbreaker'), which uses four AESA radar panels to detect and intercept incoming ATGMs and RPGs in mid-air. The Mk IV Barak adds the IronVision 360° see-through-armor AI helmet.",
        "innovations": ["First operational hard-kill Active Protection System in combat (Trophy APS, 2011)", "IronVision 360° AR helmet seeing through the hull & AI target acquisition"]
    },
    {
        "id": "k2_type10_ztz99a", "name": "K2 Black Panther / Type 10 / ZTZ-99A", "nation": "ASIA_OTHER", "era": 7, "year": 2012,
        "role": "East Asian 3.5+ Gen Autoloaded MBTs", "weight_t": 55.0, "gun": "120mm L/55 (K2) / 120mm L/44 (Type 10) / 125mm (ZTZ-99A)",
        "armor_mm": 860, "speed_kmh": 70, "power_hp": 1500, "crew": 3, "produced": 1900,
        "x_offset": 0.0, "lane_offset": 0.0,
        "stats": {"firepower": 97, "armor": 94, "mobility": 96, "optics": 98, "impact": 95},
        "summary": "East Asia leads 21st-century tank innovation: South Korea's K2 Black Panther (adopted by Poland) combines a 120mm L/55 gun, bustle autoloader, In-arm Hydropneumatic Suspension (kneeling/tilting), and KSTAM top-attack smart munitions; Japan's 44-ton Type 10 features nano-crystal steel and CVT transmission; China's ZTZ-99A mounts a 1,500 hp engine and laser dazzler APS.",
        "innovations": ["K2 In-arm Hydropneumatic Suspension (ISU) & KSTAM parachute top-attack smart shells", "Type 10 C4I network sharing & hydromechanical continuously variable transmission (CVT)"]
    }
]

print(f"Total tanks defined: {len(TANKS)}")


# 3. RELATIONSHIPS / EDGES (3 Types: lineage, similarity, combat)
# type: "lineage" (direct evolution/chasis/doctrine successor)
# type: "similarity" (shared gun, license, suspension, or direct counter-design)
# type: "combat" (fought each other in historical battles)

EDGES = [
    # --- LINEAGE EDGES (Green/Cyan Solid Directional Flow) ---
    # UK Lineage
    {"source": "mark_i_iv", "target": "whippet", "type": "lineage", "label": "Heavy Trench → Fast Cavalry Split"},
    {"source": "mark_i_iv", "target": "matilda_ii", "type": "lineage", "label": "Heavy Infantry Armor Doctrine"},
    {"source": "whippet", "target": "vickers_6ton", "type": "lineage", "label": "Interwar Export & Light/Cruiser Chassis"},
    {"source": "vickers_6ton", "target": "crusader_valentine", "type": "lineage", "label": "Cruiser / Valentine Chassis Evolution"},
    {"source": "matilda_ii", "target": "crusader_valentine", "type": "lineage", "label": "Infantry Tank Line"},
    {"source": "crusader_valentine", "target": "cromwell_firefly", "type": "lineage", "label": "Christie Cruiser → Meteor-Powered Cromwell"},
    {"source": "cromwell_firefly", "target": "centurion_mk1", "type": "lineage", "label": "Cruiser + 17-pdr Merges into Universal Tank"},
    {"source": "centurion_mk1", "target": "chieftain", "type": "lineage", "label": "Heavy Gun & Armor MBT Doctrine"},
    {"source": "centurion_mk1", "target": "shot_magach", "type": "lineage", "label": "Up-gunned Israeli Sho't Kal (L7 + Diesel)"},
    {"source": "chieftain", "target": "challenger1", "type": "lineage", "label": "Shir 2 / Chobham Armor Evolution"},
    {"source": "challenger1", "target": "challenger2_3", "type": "lineage", "label": "Dorchester Armor & Digital Turret (CR2/CR3)"},

    # French Lineage
    {"source": "renault_ft", "target": "somua_s35", "type": "lineage", "label": "Turreted Cavalry Evolution"},
    {"source": "renault_ft", "target": "char_b1", "type": "lineage", "label": "French Infantry Breakthrough Line"},
    {"source": "somua_s35", "target": "amx13_30", "type": "lineage", "label": "High-Mobility French Post-War Armor"},
    {"source": "amx13_30", "target": "leclerc", "type": "lineage", "label": "Autoloaded High-Speed French MBT"},

    # German Lineage
    {"source": "a7v", "target": "panzer_ii", "type": "lineage", "label": "Rebirth of Panzerwaffe (Traktor Programs)"},
    {"source": "panzer_ii", "target": "panzer_iii", "type": "lineage", "label": "Blitzkrieg Medium Tank Core"},
    {"source": "panzer_ii", "target": "panzer_iv", "type": "lineage", "label": "Support Tank → Mainstay Medium"},
    {"source": "pz_38t", "target": "panzer_iii", "type": "lineage", "label": "Early Panzerwaffe Backbone Integration"},
    {"source": "panzer_iii", "target": "tiger_i", "type": "lineage", "label": "Henschel Breakthrough Heavy Evolution"},
    {"source": "panzer_iv", "target": "panther", "type": "lineage", "label": "Medium Tank Replacement (VK 30.02)"},
    {"source": "tiger_i", "target": "tiger_ii", "type": "lineage", "label": "Panther-Sloped Glacis + 88mm L/71"},
    {"source": "panther", "target": "tiger_ii", "type": "lineage", "label": "Shared Sloped Glacis & Maybach HL230"},
    {"source": "panther", "target": "leopard1", "type": "lineage", "label": "Post-War German High-Mobility Gunnery Doctrine"},
    {"source": "leopard1", "target": "leopard2_a4", "type": "lineage", "label": "MBT-70 Lessons → Composite 120mm MBT"},
    {"source": "leopard2_a4", "target": "leopard2_a7_kf51", "type": "lineage", "label": "L/55 Gun, Wedge NERA & Trophy APS"},

    # Soviet / Russian / Ukrainian Lineage
    {"source": "vickers_6ton", "target": "t26", "type": "lineage", "label": "Licensed Vickers 6-Ton → 11,000+ T-26s"},
    {"source": "christie_m2", "target": "bt7", "type": "lineage", "label": "Christie M1928 Purchased → BT Fast Series"},
    {"source": "bt7", "target": "t34_76", "type": "lineage", "label": "BT-7M Diesel + A-20/A-32 Sloped Hull → T-34"},
    {"source": "t26", "target": "kv1", "type": "lineage", "label": "Leningrad Kirov Breakthrough Line (SMK → KV-1)"},
    {"source": "t34_76", "target": "t34_85", "type": "lineage", "label": "3-Man Turret + 85mm Gun Upgrade"},
    {"source": "kv1", "target": "is2", "type": "lineage", "label": "KV-1S / KV-85 → IS-2 Heavy Breakthrough"},
    {"source": "t34_85", "target": "t54_55", "type": "lineage", "label": "T-44 Transverse Engine → T-54/55"},
    {"source": "t54_55", "target": "t62", "type": "lineage", "label": "Stretched Hull + 115mm Smoothbore"},
    {"source": "t54_55", "target": "t64_t80", "type": "lineage", "label": "Morozov Kharkiv Composite Autoloader Revolution"},
    {"source": "t62", "target": "t72", "type": "lineage", "label": "Uralvagonzavod Mobilization 125mm MBT"},
    {"source": "t72", "target": "t90m", "type": "lineage", "label": "T-72BU → T-90A → T-90M Proryv-3"},
    {"source": "t64_t80", "target": "t84_oplot", "type": "lineage", "label": "Kharkiv T-64BV / T-80UD → BM Oplot"},

    # US Lineage
    {"source": "renault_ft", "target": "m1917_light", "type": "lineage", "label": "US License Production of Renault FT"},
    {"source": "m1917_light", "target": "christie_m2", "type": "lineage", "label": "US Interwar Suspension & M2 Medium"},
    {"source": "christie_m2", "target": "m3_lee_grant", "type": "lineage", "label": "M2 Medium VVSS Chassis → M3 Lee"},
    {"source": "m3_lee_grant", "target": "m4_sherman", "type": "lineage", "label": "M3 Chassis + 75mm Rotating Turret → M4 Sherman"},
    {"source": "m4_sherman", "target": "m4a3e8", "type": "lineage", "label": "HVSS Suspension + 76mm M1A2 + Wet Stowage"},
    {"source": "m4a3e8", "target": "m26_pershing", "type": "lineage", "label": "T20/T26 Torsion-Bar 90mm Evolution"},
    {"source": "m26_pershing", "target": "m48_m60_patton", "type": "lineage", "label": "M26 → M46 → M47 → M48/M60 Patton Series"},
    {"source": "m48_m60_patton", "target": "m1_abrams", "type": "lineage", "label": "XM1 Chobham + Turbine Replacement"},
    {"source": "m1_abrams", "target": "m1a2_sepv3", "type": "lineage", "label": "CITV Digital Architecture, DU Gen-3 & Trophy"},

    # Israel & Asia Lineage
    {"source": "m48_m60_patton", "target": "shot_magach", "type": "lineage", "label": "US M48/M60 → Israeli Magach Series"},
    {"source": "shot_magach", "target": "merkava_i_ii", "type": "lineage", "label": "Golan/Sinai Lessons → Crew-First Merkava"},
    {"source": "merkava_i_ii", "target": "merkava_iv", "type": "lineage", "label": "120mm Smoothbore + Trophy APS + IronVision"},
    {"source": "type95_97", "target": "type59_74_strv103", "type": "lineage", "label": "Post-War Japanese Type 61 / Type 74 Diesel Lineage"},
    {"source": "t54_55", "target": "type59_74_strv103", "type": "lineage", "label": "Soviet T-54A Licensed as Chinese Type 59"},
    {"source": "type59_74_strv103", "target": "k2_type10_ztz99a", "type": "lineage", "label": "Asian Indigenous 3.5-Gen MBTs (Type 10 / ZTZ-99A)"},

    # --- SIMILARITY & TECH-TRANSFER EDGES (Dashed Indigo/Purple Links) ---
    {"source": "renault_ft", "target": "vickers_6ton", "type": "similarity", "label": "360° Turret + Rear Engine Blueprint"},
    {"source": "christie_m2", "target": "crusader_valentine", "type": "similarity", "label": "Shared Christie Coil-Spring Cruiser Suspension"},
    {"source": "vickers_6ton", "target": "type95_97", "type": "similarity", "label": "British Carden-Loyd / Vickers Interwar Influence"},
    {"source": "t34_76", "target": "panther", "type": "similarity", "label": "Direct Counter-Design: Panther Copied T-34 Sloped Glacis"},
    {"source": "m4_sherman", "target": "cromwell_firefly", "type": "similarity", "label": "US M4 Hull + British 17-Pounder Gun = Sherman Firefly"},
    {"source": "is2", "target": "chieftain", "type": "similarity", "label": "Heavy 120mm+ Gun & Sloped Cast Turret Philosophy"},
    {"source": "centurion_mk1", "target": "leopard1", "type": "similarity", "label": "Shared British 105mm Royal Ordnance L7 Gun"},
    {"source": "leopard1", "target": "m48_m60_patton", "type": "similarity", "label": "NATO Standardized 105mm L7 / M68 Gun"},
    {"source": "leopard1", "target": "amx13_30", "type": "similarity", "label": "Joint Franco-German Europanzer origins (Mobility > Armor)"},
    {"source": "shot_magach", "target": "type59_74_strv103", "type": "similarity", "label": "Shared 105mm L7 Rifled Gun Family"},
    {"source": "challenger1", "target": "m1_abrams", "type": "similarity", "label": "Shared British Chobham (Burlington) Composite Armor Tech"},
    {"source": "leopard2_a4", "target": "m1_abrams", "type": "similarity", "label": "Joint US-German MBT-70 Ancestor & Rheinmetall 120mm M256 Gun"},
    {"source": "t64_t80", "target": "t72", "type": "similarity", "label": "Shared 125mm 2A46 Smoothbore & Low-Profile Autoloaded Turret"},
    {"source": "m1a2_sepv3", "target": "k2_type10_ztz99a", "type": "similarity", "label": " Chrysler XM1 → K1 → K2 Lineage & 120mm NATO Smoothbore"},
    {"source": "merkava_iv", "target": "m1a2_sepv3", "type": "similarity", "label": "Shared Israeli Rafael Trophy Active Protection System"},
    {"source": "merkava_iv", "target": "leopard2_a7_kf51", "type": "similarity", "label": "Shared Trophy APS & 120mm Smoothbore Ammunition Compatibility"},

    # --- COMBAT ENGAGEMENT EDGES (Glowing Crimson Crossed-Swords Links) ---
    # WWI
    {"source": "mark_i_iv", "target": "a7v", "type": "combat", "label": "Villers-Bretonneux (Apr 1918): First Tank-vs-Tank Duel in History", "battles": ["villers_bretonneux_1918"]},
    {"source": "whippet", "target": "a7v", "type": "combat", "label": "Villers-Bretonneux (Apr 1918): A7V vs 7 Whippet Cavalry Tanks", "battles": ["villers_bretonneux_1918"]},

    # Interwar / 1939
    {"source": "bt7", "target": "type95_97", "type": "combat", "label": "Khalkhin Gol (1939): Zhukov's BT-7s Encircle Japanese Armor", "battles": ["khalkhin_gol_1939"]},
    {"source": "t26", "target": "type95_97", "type": "combat", "label": "Khalkhin Gol (1939) & Manchuria: 45mm T-26 vs Type 95/97", "battles": ["khalkhin_gol_1939"]},

    # Early WWII (1940-1942)
    {"source": "somua_s35", "target": "panzer_iii", "type": "combat", "label": "Battle of Hannut (May 1940): Largest Tank Clash of French Campaign", "battles": ["hannut_1940"]},
    {"source": "char_b1", "target": "panzer_iv", "type": "combat", "label": "Stonne & Flavion (May 1940): Char B1 'Eure' Destroys 13 Panzers", "battles": ["hannut_1940", "arras_1940"]},
    {"source": "matilda_ii", "target": "panzer_ii", "type": "combat", "label": "Battle of Arras (May 1940): Matilda II Shrugs Off 37mm/20mm Fire", "battles": ["arras_1940"]},
    {"source": "matilda_ii", "target": "pz_38t", "type": "combat", "label": "Arras (1940): British Counterattack Against Rommel's 7th Panzer", "battles": ["arras_1940"]},
    {"source": "t26", "target": "pz_38t", "type": "combat", "label": "Battle of Brody (Jun 1941): Massive Border Tank Clash", "battles": ["brody_1941"]},
    {"source": "t34_76", "target": "panzer_iii", "type": "combat", "label": "Brody, Moscow & Stalingrad (1941–42): T-34 Sloped Armor Shock", "battles": ["brody_1941", "kursk_1943"]},
    {"source": "kv1", "target": "panzer_iii", "type": "combat", "label": "Raseiniai & Brody (1941): KV-1 Impervious to 50mm Panzer III", "battles": ["brody_1941"]},
    {"source": "crusader_valentine", "target": "panzer_iii", "type": "combat", "label": "North Africa & El Alamein (1941–42): Desert Cruiser Duels", "battles": ["el_alamein_1942"]},
    {"source": "m3_lee_grant", "target": "panzer_iv", "type": "combat", "label": "Gazala & El Alamein (1942): 75mm Grant vs Panzer IV", "battles": ["el_alamein_1942"]},
    {"source": "m4_sherman", "target": "panzer_iv", "type": "combat", "label": "El Alamein, Tunisia, Italy & Normandy (1942–44)", "battles": ["el_alamein_1942", "normandy_1944", "arracourt_1944"]},
    {"source": "m4_sherman", "target": "type95_97", "type": "combat", "label": "Pacific Island Campaigns & Luzon (1943–45): Sherman Overwhelms Type 97", "battles": ["khalkhin_gol_1939"]},

    # Late WWII (1943-1945)
    {"source": "t34_76", "target": "tiger_i", "type": "combat", "label": "Kursk / Prokhorovka (Jul 1943): Close-Range Rush Against 88mm Tigers", "battles": ["kursk_1943"]},
    {"source": "t34_76", "target": "panther", "type": "combat", "label": "Kursk (Jul 1943): Panther Combat Debut vs T-34/76", "battles": ["kursk_1943"]},
    {"source": "cromwell_firefly", "target": "tiger_i", "type": "combat", "label": "Villers-Bocage & Goodwood (1944): 17-pdr Firefly vs Wittmann's Tigers", "battles": ["normandy_1944"]},
    {"source": "cromwell_firefly", "target": "panther", "type": "combat", "label": "Normandy Bocage & Operation Goodwood (1944)", "battles": ["normandy_1944"]},
    {"source": "m4a3e8", "target": "panther", "type": "combat", "label": "Arracourt & Battle of the Bulge (1944): 76mm Sherman vs Panther", "battles": ["arracourt_1944", "bulge_1944"]},
    {"source": "m4a3e8", "target": "tiger_ii", "type": "combat", "label": "Battle of the Bulge / Ardennes (Dec 1944): Easy Eight vs King Tiger", "battles": ["bulge_1944"]},
    {"source": "m26_pershing", "target": "panther", "type": "combat", "label": "Cologne Cathedral Duel (Mar 1945): M26 Pershing Destroys Panther", "battles": ["bulge_1944"]},
    {"source": "t34_85", "target": "panther", "type": "combat", "label": "Bagration, Vistula-Oder & Lake Balaton (1944–45)", "battles": ["balaton_1945"]},
    {"source": "is2", "target": "tiger_ii", "type": "combat", "label": "Sandomierz & Lake Balaton (1944–45): Heavy 122mm vs 88mm L/71 Clash", "battles": ["balaton_1945"]},

    # Cold War I & II (1950-1991)
    {"source": "t34_85", "target": "m4a3e8", "type": "combat", "label": "Korean War (1950): 70 Tank-vs-Tank Clashes along Nakdong & Chongchon", "battles": ["korea_1950"]},
    {"source": "t34_85", "target": "m26_pershing", "type": "combat", "label": "Pusan Perimeter & Seoul (1950): 90mm Pershing Outguns T-34-85", "battles": ["korea_1950"]},
    {"source": "centurion_mk1", "target": "m48_m60_patton", "type": "combat", "label": "Battle of Asal Uttar & Chawinda (1965): Indian Centurion vs Pakistani Patton", "battles": ["chawinda_1965"]},
    {"source": "amx13_30", "target": "m48_m60_patton", "type": "combat", "label": "Indo-Pak War (1965) & Six-Day War (1967): AMX-13 vs Patton", "battles": ["chawinda_1965", "sinai_1967"]},
    {"source": "shot_magach", "target": "t54_55", "type": "combat", "label": "Six-Day War (1967) & Valley of Tears (1973): Sho't/Magach vs T-55", "battles": ["sinai_1967", "valley_of_tears_1973", "chinese_farm_1973"]},
    {"source": "shot_magach", "target": "t62", "type": "combat", "label": "Valley of Tears & Chinese Farm (Oct 1973): 105mm L7 vs 115mm T-62", "battles": ["valley_of_tears_1973", "chinese_farm_1973"]},
    {"source": "m48_m60_patton", "target": "t54_55", "type": "combat", "label": "Vietnam (Ben Het 1969), Sinai (1973) & Desert Storm (1991)", "battles": ["chinese_farm_1973", "easting_1991"]},
    {"source": "chieftain", "target": "t62", "type": "combat", "label": "Battle of Dezful / Susangerd (1981): Iranian Chieftain vs Iraqi T-62", "battles": ["dezful_1981"]},
    {"source": "chieftain", "target": "t72", "type": "combat", "label": "Iran–Iraq War (1981–88) & Kuwait (1991): First T-72 vs 120mm Chieftain Duels", "battles": ["dezful_1981"]},
    {"source": "merkava_i_ii", "target": "t72", "type": "combat", "label": "Bekaa Valley / Lebanon (1982): Merkava Mk I vs Syrian T-72M", "battles": ["bekaa_1982"]},
    {"source": "m1_abrams", "target": "t72", "type": "combat", "label": "73 Easting & Medina Ridge (1991): M1A1 HA Thermal Dominance vs T-72M1", "battles": ["easting_1991", "baghdad_2003"]},
    {"source": "m1_abrams", "target": "type59_74_strv103", "type": "combat", "label": "Gulf War (1991): US M1A1 & Marine M60A1 vs Iraqi Type 59/69", "battles": ["easting_1991"]},
    {"source": "challenger1", "target": "t72", "type": "combat", "label": "Operation Granby / Norfolk (1991): ~300 Iraqi Tanks Destroyed (4.7km Record)", "battles": ["easting_1991"]},

    # Modern Era (1992-2026)
    {"source": "challenger2_3", "target": "t54_55", "type": "combat", "label": "Siege of Basra (2003): 14 Challenger 2s Destroy 14 Iraqi T-55s", "battles": ["baghdad_2003"]},
    {"source": "m1a2_sepv3", "target": "t72", "type": "combat", "label": "Karbala Gap & Baghdad (2003) + Avdiivka/Pokrovsk (2024)", "battles": ["baghdad_2003", "ukraine_2022_2024"]},
    {"source": "t84_oplot", "target": "t72", "type": "combat", "label": "Battle of Chernihiv & Donbas (2022–24): Ukrainian T-64BV vs Russian T-72B3", "battles": ["ukraine_2022_2024"]},
    {"source": "t84_oplot", "target": "t90m", "type": "combat", "label": "Kharkiv & Donbas (2022–24): T-64BV/T-84 vs T-90M Proryv", "battles": ["ukraine_2022_2024"]},
    {"source": "leopard2_a7_kf51", "target": "t90m", "type": "combat", "label": "Zaporizhzhia & Donbas (2023–24): Leopard 2A4/2A6 vs T-72B3/T-80BVM/T-90M", "battles": ["ukraine_2022_2024"]},
    {"source": "leopard2_a7_kf51", "target": "t64_t80", "type": "combat", "label": "Ukraine Counteroffensive (2023–24): Leopard 2A6 vs Russian T-80BVM", "battles": ["ukraine_2022_2024"]}
]

print(f"Total edges defined: {len(EDGES)}")


# 4. MAJOR WORLD TANK BATTLES (With Geocoordinates, Theatre Regions & Tactical Zoom Schematics)
BATTLES = [
    {
        "id": "cambrai_1917",
        "name": "Battle of Cambrai",
        "date": "Nov 20 – Dec 7, 1917",
        "year": 1917,
        "era": 1,
        "theatre": "EUROPE_WEST",
        "location": "Cambrai, Nord, France",
        "lat": 50.176, "lon": 3.235,
        "total_tanks": "476 British Tanks",
        "side_a": {"name": "British Empire (Royal Tank Corps)", "flag": "🇬🇧", "tanks": ["mark_i_iv"], "count": "378 Mark IV combat tanks + 98 support"},
        "side_b": {"name": "German Empire (2nd Army)", "flag": "🇩🇪", "tanks": ["a7v"], "count": "Field artillery, K-bullets & Sturmtruppen (A7V deployed shortly after)"},
        "outcome": "First massed combined-arms tank breakthrough in history; penetrated the Hindenburg Line 8 km on Day 1.",
        "tactical_zoom": {
            "terrain": "Chalk downs, Hindenburg Line triple trench network, Canal du Nord",
            "range_m": "50–300m point-blank trench suppression",
            "formations": [
                {"side": "A", "label": "378x Mark IV (Fascine Bundles)", "x": 22, "y": 50, "tx": 62, "ty": 48},
                {"side": "B", "label": "Hindenburg Trench & 77mm Direct-Fire Batteries", "x": 70, "y": 48, "tx": 55, "ty": 52}
            ],
            "key_lesson": "Proved tanks must be concentrated en masse with unpredicted artillery registration and infantry-aircraft cooperation."
        },
        "summary": "Instead of scattering tanks in small penny-packets in deep mud, Brig. Gen. Hugh Elles and Col. J.F.C. Fuller massed 378 Mark IV tanks carrying giant brushwood fascines to bridge the 4-meter-wide Hindenburg Line trenches. In six hours, British armor advanced further than in three months at Passchendaele."
    },
    {
        "id": "villers_bretonneux_1918",
        "name": "Second Battle of Villers-Bretonneux",
        "date": "April 24, 1918",
        "year": 1918,
        "era": 1,
        "theatre": "EUROPE_WEST",
        "location": "Villers-Bretonneux (Somme), France",
        "lat": 49.867, "lon": 2.517,
        "total_tanks": "33 Tanks (20 UK, 13 DE)",
        "side_a": {"name": "British Army (1st Tank Brigade)", "flag": "🇬🇧", "tanks": ["mark_i_iv", "whippet"], "count": "3 Mark IVs + 7 Medium Mark A Whippets"},
        "side_b": {"name": "German Empire (Abteilung 1–3)", "flag": "🇩🇪", "tanks": ["a7v"], "count": "13 Sturmpanzerwagen A7Vs (incl. 'Nixe')"},
        "outcome": "First tank-versus-tank battle in world history; Lt. Frank Mitchell's Male Mark IV disabled A7V 'Nixe' with three 6-pounder hits.",
        "tactical_zoom": {
            "terrain": "Morning mist over Cachy switch-line fields & Bois d'Aquenne",
            "range_m": "180–400m direct gunnery duel",
            "formations": [
                {"side": "A", "label": "Lt. Mitchell's Mark IV Male (6-pdr)", "x": 25, "y": 40, "tx": 52, "ty": 45},
                {"side": "A", "label": "7x Whippet Cavalry Tanks", "x": 28, "y": 72, "tx": 60, "ty": 68},
                {"side": "B", "label": "Lt. Biltz's A7V 'Nixe' (57mm)", "x": 75, "y": 46, "tx": 48, "ty": 45}
            ],
            "key_lesson": "Immediately demonstrated that tanks needed armor-piercing high-velocity cannons, not just machine guns—two Female (MG-only) Mark IVs were forced to retreat before the Male Mark IV defeated the A7V."
        },
        "summary": "When three German A7V groups attacked toward Amiens, three British Mark IVs (one Male with 57mm 6-pounders, two Females with machine guns) intercepted A7V 'Nixe'. After 'Nixe' damaged both Female tanks, Lt. Frank Mitchell halted his Male Mark IV to fire accurately, putting three 6-pounder shells through 'Nixe'. Soon after, 7 fast Whippet tanks decimated German infantry in the open."
    },
    {
        "id": "khalkhin_gol_1939",
        "name": "Battles of Khalkhin Gol (Nomonhan)",
        "date": "May 11 – Sep 16, 1939",
        "year": 1939,
        "era": 2,
        "theatre": "ASIA_EAST",
        "location": "Khalkhin Gol River, Mongolia / Manchuria",
        "lat": 47.728, "lon": 118.590,
        "total_tanks": "~600 Armored Vehicles",
        "side_a": {"name": "Soviet Union (57th Special Corps / Gen. Zhukov)", "flag": "☭", "tanks": ["bt7", "t26"], "count": "498 Tanks (BT-5, BT-7, T-26, OT-26)"},
        "side_b": {"name": "Imperial Japanese Kwantung Army (Yasuoka Detachment)", "flag": "🇯🇵", "tanks": ["type95_97"], "count": "73–120 Tanks (Type 89, Type 95 Ha-Go, Type 97 Chi-Ha)"},
        "outcome": "Decisive Soviet double-envelopment victory under Georgy Zhukov; shaped WWII Soviet deep-battle doctrine and deterred Japan from invading Siberia in 1941.",
        "tactical_zoom": {
            "terrain": "Open steppe dunes along the Halha (Khalkhin Gol) River",
            "range_m": "400–900m open-steppe gunnery & encirclement",
            "formations": [
                {"side": "A", "label": "6th Tank Brigade (BT-7 Northern Hook)", "x": 25, "y": 24, "tx": 68, "ty": 30},
                {"side": "A", "label": "11th Tank Brigade (BT-5/T-26 Southern Hook)", "x": 25, "y": 76, "tx": 68, "ty": 70},
                {"side": "B", "label": "Japanese 23rd Div & Yasuoka Type 95/97s", "x": 62, "y": 50, "tx": 45, "ty": 50}
            ],
            "key_lesson": "Exposed the fire vulnerability of gasoline-powered BT-7s to Molotov cocktails and 37mm guns—directly accelerating adoption of the V-2 diesel engine and thicker sloped armor on the T-34."
        },
        "summary": "On the treeless steppes of eastern Mongolia, Georgy Zhukov orchestrated his first classic double-envelopment using two fast armored wings of BT-5, BT-7, and T-26 tanks to encircle the Japanese 23rd Division. While Soviet 45mm guns outranged Japanese 57mm low-velocity guns, heavy losses to close-range anti-tank fire convinced Red Army designers to build the diesel-powered, heavily armored T-34."
    },
    {
        "id": "hannut_1940",
        "name": "Battle of Hannut & Gembloux Gap",
        "date": "May 12–14, 1940",
        "year": 1940,
        "era": 3,
        "theatre": "EUROPE_WEST",
        "location": "Hannut, Liège Province, Belgium",
        "lat": 50.672, "lon": 5.078,
        "total_tanks": "~1,220 Tanks (600 FR, 618 DE)",
        "side_a": {"name": "French Cavalry Corps (2nd & 3rd DLM)", "flag": "🇫🇷", "tanks": ["somua_s35", "char_b1", "renault_ft"], "count": "~600 Tanks (176 SOMUA S35, Hotchkiss H35/H39)"},
        "side_b": {"name": "German XVI Panzer Corps (3rd & 4th Panzer Divs)", "flag": "🇩🇪", "tanks": ["panzer_ii", "panzer_iii", "panzer_iv"], "count": "618 Tanks (Panzer I, II, III, IV)"},
        "outcome": "Tactical draw on the field (French S35s destroyed more Panzers than they lost), but strategically pinned Allied mobile forces in Belgium while Guderian crossed the Ardennes at Sedan.",
        "tactical_zoom": {
            "terrain": "Rolling Belgian farmland around Crehen, Thisnes & Merdorp",
            "range_m": "400–800m ridge-to-ridge duels",
            "formations": [
                {"side": "A", "label": "French 2nd/3rd DLM (SOMUA S35 Hull-Down)", "x": 30, "y": 48, "tx": 52, "ty": 48},
                {"side": "B", "label": "German 3rd & 4th Panzer Divs (Radio Swarm)", "x": 75, "y": 48, "tx": 45, "ty": 48}
            ],
            "key_lesson": "Proved that superior individual tank armor and gun (SOMUA S35) can be defeated by 3-man turrets, universal onboard radios, and Luftwaffe Stuka integration."
        },
        "summary": "The largest tank battle of the 1940 Western Campaign. French SOMUA S35 cavalry tanks—with 47mm cast armor immune to German 37mm guns—knocked out scores of Panzer IIIs and IVs around Crehen and Merdorp. However, French commanders sat alone in one-man turrets (acting as commander, gunner, and loader simultaneously) without radios, allowing radio-coordinated German Panzers to outflank them."
    },
    {
        "id": "arras_1940",
        "name": "Battle of Arras",
        "date": "May 21, 1940",
        "year": 1940,
        "era": 3,
        "theatre": "EUROPE_WEST",
        "location": "Arras, Pas-de-Calais, France",
        "lat": 50.291, "lon": 2.777,
        "total_tanks": "~300 Tanks (74 UK + 60 FR vs ~220 DE)",
        "side_a": {"name": "Anglo-French Frankforce (4th & 7th RTR + 3rd DLM)", "flag": "🇬🇧", "tanks": ["matilda_ii", "somua_s35", "char_b1"], "count": "58 Matilda I, 16 Matilda II + ~60 French S35/B1"},
        "side_b": {"name": "German 7th Panzer Division (Erwin Rommel) & SS Totenkopf", "flag": "🇩🇪", "tanks": ["panzer_ii", "pz_38t", "panzer_iii", "panzer_iv"], "count": "~220 Panzer II, 38(t), III, IV + 88mm Flak"},
        "outcome": "British Matilda IIs overran German 37mm anti-tank lines until Rommel personally directed 88mm Flak anti-aircraft guns in direct fire; shocked German High Command into halting for 24 hours before Dunkirk.",
        "tactical_zoom": {
            "terrain": "Telegraph Hill & Wailly ridges south of Arras",
            "range_m": "200–1,000m (37mm bounced; 88mm Flak engaged at 1,000m)",
            "formations": [
                {"side": "A", "label": "4th & 7th RTR Matilda II Columns", "x": 32, "y": 28, "tx": 55, "ty": 65},
                {"side": "B", "label": "Rommel's Panzer 38(t) & 88mm Flak Gun Line", "x": 65, "y": 72, "tx": 48, "ty": 52}
            ],
            "key_lesson": "Established the 88mm Flak anti-aircraft gun as Germany's premier heavy tank killer—a direct ancestor of the Tiger I's 88mm KwK 36."
        },
        "summary": "Charging south from Arras, 74 British Matilda I and Matilda II infantry tanks smashed straight through Erwin Rommel's 7th Panzer Division flank. German 37mm Pak 36 shells bounced harmlessly off the Matilda II's 78mm cast armor. In desperation, Rommel formed a last-ditch gun line of 88mm Flak anti-aircraft guns and 105mm howitzers to stop the British armor—contributing to Hitler's famous halt order that helped save the BEF at Dunkirk."
    },
    {
        "id": "brody_1941",
        "name": "Battle of Brody / Dubno-Lutsk",
        "date": "June 23–30, 1941",
        "year": 1941,
        "era": 3,
        "theatre": "EUROPE_EAST",
        "location": "Brody & Dubno, Western Ukraine",
        "lat": 50.083, "lon": 25.148,
        "total_tanks": "~4,300 Tanks (3,500 SU vs 800 DE)",
        "side_a": {"name": "Soviet Southwestern Front (5 Mechanized Corps)", "flag": "☭", "tanks": ["t26", "bt7", "t34_76", "kv1"], "count": "~3,500 Tanks (T-26, BT-7, plus ~350 new T-34 & KV-1)"},
        "side_b": {"name": "German 1st Panzer Group (Gen. von Kleist)", "flag": "🇩🇪", "tanks": ["panzer_ii", "pz_38t", "panzer_iii", "panzer_iv"], "count": "~800 Tanks (Panzer III, IV, II, 38(t))"},
        "outcome": "German operational victory due to Luftwaffe air supremacy and logistics, but Soviet T-34 and KV-1 tanks triggered the 'T-34 Crisis' in Berlin.",
        "tactical_zoom": {
            "terrain": "River Ikva marshes, Dubno crossroads & rolling Ukrainian plains",
            "range_m": "300–1,000m (German 37mm/50mm failed against KV-1/T-34 glacis)",
            "formations": [
                {"side": "A", "label": "8th & 15th Mech Corps (KV-1 & T-34 Counterattack)", "x": 72, "y": 55, "tx": 46, "ty": 48},
                {"side": "B", "label": "11th & 16th Panzer Divisions Spearhead", "x": 25, "y": 45, "tx": 55, "ty": 48}
            ],
            "key_lesson": "Encountering sloped-armor T-34s and 45-ton KV-1s that ignored 37mm and short 50mm/75mm hits forced Germany to rush long-barreled 75mm guns onto the Panzer IV and launch the Panther/Tiger programs."
        },
        "summary": "In the opening week of Operation Barbarossa, five Soviet Mechanized Corps counterattacked von Kleist's 1st Panzer Group with over 3,500 tanks. While thousands of older T-26 and BT-7 tanks broke down or fell to Luftwaffe Stukas, the combat debut of the T-34/76 and KV-1 stunned German tank crews, whose shells shattered against Soviet sloped and heavy armor."
    },
    {
        "id": "el_alamein_1942",
        "name": "Second Battle of El Alamein",
        "date": "Oct 23 – Nov 11, 1942",
        "year": 1942,
        "era": 3,
        "theatre": "NORTH_AFRICA",
        "location": "El Alamein & Tel el Aqqaqir, Egypt",
        "lat": 30.833, "lon": 28.950,
        "total_tanks": "1,576 Tanks (1,029 Allied vs 547 Axis)",
        "side_a": {"name": "British Eighth Army (Gen. Bernard Montgomery)", "flag": "🇬🇧/🇺🇸", "tanks": ["m4_sherman", "m3_lee_grant", "crusader_valentine"], "count": "1,029 Tanks (252 M4 Shermans, 170 Grants, 294 Crusaders, 194 Valentines)"},
        "side_b": {"name": "Panzerarmee Afrika (Field Marshal Erwin Rommel)", "flag": "🇩🇪/🇮🇹", "tanks": ["panzer_iii", "panzer_iv"], "count": "547 Tanks (211 German Panzer III/IV + 336 Italian M13/40 & Semovente)"},
        "outcome": "Decisive Allied victory; combat debut of the M4 Sherman turned the tide in North Africa.",
        "tactical_zoom": {
            "terrain": "Mediterranean coastal desert bottleneck north of Qattara Depression",
            "range_m": "800–1,500m desert gunnery across Kidney Ridge & Tel el Aqqaqir",
            "formations": [
                {"side": "A", "label": "X Corps Armored Breakthrough (M4 Sherman & Crusader III)", "x": 75, "y": 46, "tx": 42, "ty": 46},
                {"side": "B", "label": "15th & 21st Panzer Divs + 88mm Screen (Devil's Garden)", "x": 28, "y": 46, "tx": 48, "ty": 46}
            ],
            "key_lesson": "The M4 Sherman's turreted dual-purpose 75mm gun could engage both Axis tanks with AP and deadly 88mm anti-tank gun screens with high-explosive shells from hull-down positions."
        },
        "summary": "Bounded by the Mediterranean Sea to the north and the impassable Qattara Depression to the south, El Alamein had no open desert flank. Rushed personally from US assembly lines by President Roosevelt after Tobruk fell, 252 new M4 Shermans gave Montgomery's Eighth Army a turreted 75mm tank that matched the long-barreled Panzer IV Ausf. F2 and shattered Rommel's Panzerarmee during Operation Supercharge."
    },
    {
        "id": "kursk_1943",
        "name": "Battle of Kursk & Prokhorovka",
        "date": "July 5–16, 1943",
        "year": 1943,
        "era": 4,
        "theatre": "EUROPE_EAST",
        "location": "Kursk Salient & Prokhorovka, Russia",
        "lat": 51.036, "lon": 36.731,
        "total_tanks": "~8,000 Tanks (5,128 SU vs 2,928 DE)",
        "side_a": {"name": "Soviet Central, Voronezh & Steppe Fronts (Zhukov / Vatutin / Rotmistrov)", "flag": "☭", "tanks": ["t34_76", "kv1"], "count": "5,128 Tanks (~850 at Prokhorovka in 5th Guards Tank Army)"},
        "side_b": {"name": "German Army Groups Center & South (Model / Manstein / II SS Panzer Corps)", "flag": "🇩🇪", "tanks": ["tiger_i", "panther", "panzer_iv", "panzer_iii"], "count": "2,928 Tanks (Tiger I, Panther Ausf. D debut, Panzer IV H, Ferdinand)"},
        "outcome": "Largest tank battle in human history; permanently broke Germany's strategic offensive capability on the Eastern Front.",
        "tactical_zoom": {
            "terrain": "8-belt fortified salient, Psel River bottleneck & Prokhorovka railway embankment",
            "range_m": "Closed from 1,500m (88mm Tiger kill zone) to 100–400m point-blank brawl",
            "formations": [
                {"side": "A", "label": "5th Guards Tank Army (Rotmistrov's High-Speed T-34 Charge)", "x": 76, "y": 35, "tx": 46, "ty": 52},
                {"side": "B", "label": "II SS Panzer Corps (Leibstandarte, Das Reich, Totenkopf Tigers & Pz IVs)", "x": 26, "y": 65, "tx": 52, "ty": 48}
            ],
            "key_lesson": "Demonstrated that 76.2mm guns could no longer reliably penetrate Tiger I and Panther frontal armor at normal ranges—directly triggering production of the T-34-85 and IS-2."
        },
        "summary": "Forewarned by intelligence, the Red Army turned the Kursk salient into eight concentric defensive belts laced with over 500,000 anti-tank mines. In the south on July 12 at Prokhorovka, Pavel Rotmistrov's 5th Guards Tank Army charged II SS Panzer Corps at full speed to get inside the long-range kill zone of the Tiger I's 88mm gun. Though Soviet tank losses were heavy, Operation Citadel collapsed and the Red Army seized the strategic initiative for the rest of the war."
    },
    {
        "id": "normandy_1944",
        "name": "Normandy Bocage, Villers-Bocage & Operation Goodwood",
        "date": "June 13 – July 20, 1944",
        "year": 1944,
        "era": 4,
        "theatre": "EUROPE_WEST",
        "location": "Caen, Villers-Bocage & Bourguébus Ridge, France",
        "lat": 49.146, "lon": -0.305,
        "total_tanks": "~2,100 Tanks (1,300 Allied vs 750 German)",
        "side_a": {"name": "British Second Army & Canadian II Corps", "flag": "🇬🇧/🇺🇸", "tanks": ["cromwell_firefly", "m4_sherman"], "count": "1,100+ Cromwell, M4 Sherman & 17-pdr Sherman Firefly"},
        "side_b": {"name": "Panzer Group West & I SS Panzer Corps (Wittmann / 21st Panzer)", "flag": "🇩🇪", "tanks": ["tiger_i", "panther", "panzer_iv", "tiger_ii"], "count": "~750 Tanks (Tiger I, Panther, Panzer IV, first Western Front Tiger IIs)"},
        "outcome": "Fierce attritional battles around Caen pinned 7 of 8 German Panzer divisions in the east, enabling the US Operation Cobra breakout at Saint-Lô.",
        "tactical_zoom": {
            "terrain": "Sunken Normandy hedgerows (bocage) & open Bourguébus wheatfields",
            "range_m": "100m bocage ambushes to 1,200m open-ridge 17-pdr/88mm duels",
            "formations": [
                {"side": "A", "label": "7th/11th/Guards Armoured Divs (3 Shermans + 1 Firefly Troop)", "x": 30, "y": 25, "tx": 55, "ty": 58},
                {"side": "B", "label": "s.SS-Pz.Abt 101 Tigers & 1st SS Panthers on Bourguébus Ridge", "x": 65, "y": 72, "tx": 50, "ty": 52}
            ],
            "key_lesson": "Validated the 17-pounder Sherman Firefly (which killed Michael Wittmann's Tiger 007 near Cintheaux on Aug 8, 1944) and proved the urgent need for the Centurion Universal Tank."
        },
        "summary": "At Villers-Bocage (June 13), SS-Obersturmführer Michael Wittmann's Tiger I ambushed the British 7th Armoured Division column before being driven off by 6-pounder AT guns and Sherman Fireflies. A month later in Operation Goodwood, over 1,100 British tanks charged across the Orne bridges, grinding down Germany's last armored reserves around Caen while Trooper Joe Ekins' Sherman Firefly later knocked out three Tigers (including Wittmann's) in 12 minutes."
    },
    {
        "id": "arracourt_1944",
        "name": "Battle of Arracourt",
        "date": "September 18–29, 1944",
        "year": 1944,
        "era": 4,
        "theatre": "EUROPE_WEST",
        "location": "Arracourt, Lorraine, France",
        "lat": 48.723, "lon": 6.533,
        "total_tanks": "~500 Tanks (US CCA 4th Armored vs 5th Panzer Army)",
        "side_a": {"name": "US Third Army — 4th Armored Division (Col. Bruce Clarke / Lt. Col. Creighton Abrams)", "flag": "🇺🇸", "tanks": ["m4_sherman", "m4a3e8"], "count": "~200 M4/M4A3 Shermans (75mm & 76mm) + M18 Hellcat Tank Destroyers"},
        "side_b": {"name": "German 5th Panzer Army (111th & 113th Panzer Brigades)", "flag": "🇩🇪", "tanks": ["panther", "panzer_iv"], "count": "262 Brand-New Panthers, Panzer IVs & StuG IIIs"},
        "outcome": "Resounding US tactical triumph: 4th Armored Division destroyed or disabled ~200 German Panthers and Panzer IVs for the loss of only 25 Shermans.",
        "tactical_zoom": {
            "terrain": "Foggy rolling Lorraine valleys & reverse-slope ridge lines",
            "range_m": "300–700m flank shots out of morning fog",
            "formations": [
                {"side": "A", "label": "Creighton Abrams' 37th Tank Bn (Reverse-Slope & Flank Maneuver)", "x": 28, "y": 45, "tx": 54, "ty": 38},
                {"side": "B", "label": "111th/113th Panzer Brigades (Panthers Skylined on Ridges)", "x": 74, "y": 55, "tx": 48, "ty": 48}
            ],
            "key_lesson": "Proved that superior crew training, powered turret traverse, gyrostabilizers, and tactical mobility allowed M4 Shermans to defeat heavier Panthers at a 4:1 ratio."
        },
        "summary": "Often cited to debunk myths about the M4 Sherman: when Hitler ordered two newly equipped Panzer brigades armed with brand-new Panther tanks to destroy Patton's bridgehead in Lorraine, Lt. Col. Creighton Abrams (future namesake of the M1 Abrams) and Col. Bruce Clarke used thick autumn fog, fast powered turret traverse, gyrostabilizers, and reverse-slope ambushes to hit the Panthers' thin 40mm side armor—destroying over 85 tanks and disabling another 115 for just 25 Shermans lost."
    },
    {
        "id": "bulge_1944",
        "name": "Battle of the Bulge (Ardennes) & Cologne Follow-Up",
        "date": "Dec 16, 1944 – Jan 25, 1945 (Cologne: Mar 6, 1945)",
        "year": 1944,
        "era": 4,
        "theatre": "EUROPE_WEST",
        "location": "Bastogne, La Gleize (Belgium) & Cologne (Germany)",
        "lat": 50.000, "lon": 5.718,
        "total_tanks": "~3,800 Tanks (2,400 US/UK vs 1,400 DE)",
        "side_a": {"name": "US First & Third Armies (4th, 7th, 9th, 3rd Armored Divs)", "flag": "🇺🇸", "tanks": ["m4a3e8", "m4_sherman", "m26_pershing"], "count": "~2,400 Shermans (incl. M4A3E8 Easy Eight, M4A3E2 Jumbo) & M26 Pershing"},
        "side_b": {"name": "German 6th SS & 5th Panzer Armies (Kampfgruppe Peiper / Manteuffel)", "flag": "🇩🇪", "tanks": ["tiger_ii", "panther", "panzer_iv"], "count": "~1,400 Tanks & Assault Guns (Tiger II King Tiger, Panther, Jagdpanther)"},
        "outcome": "Allied victory; exhausted Germany's last Western Front Panzer reserves and saw the combat debut of the M4A3E8 'Easy Eight' and M26 Pershing.",
        "tactical_zoom": {
            "terrain": "Snow-covered Ardennes forests, narrow Amblève river bridges & Bastogne perimeter",
            "range_m": "200–900m snowbound road & forest corridor duels",
            "formations": [
                {"side": "A", "label": "Patton's 4th Armored Relief Spearhead (M4A3E8 Easy Eight & Jumbo)", "x": 30, "y": 75, "tx": 48, "ty": 48},
                {"side": "B", "label": "Kampfgruppe Peiper (King Tigers & Panthers towards Meuse)", "x": 72, "y": 35, "tx": 45, "ty": 42}
            ],
            "key_lesson": "The 68.5-ton Tiger II proved too heavy for Ardennes bridges and fuel-starved mountain roads, while the 90mm M26 Pershing proved a true match for the Panther at Cologne."
        },
        "summary": "Spearheaded by Kampfgruppe Peiper's 68.5-ton Tiger II 'King Tigers' and Panthers, Hitler's winter offensive gambled on capturing Allied fuel depots. Instead, stubborn US defenses at St. Vith and Bastogne and Patton's rapid relief counterattack with M4A3E2 'Jumbos' and 76mm M4A3E8 'Easy Eights' trapped the Panzers out of fuel at La Gleize. Two months later at Cologne Cathedral, a 90mm M26 Pershing (T26E3 'Eagle 7') famously outduelled a Panther on camera."
    },
    {
        "id": "balaton_1945",
        "name": "Operation Spring Awakening (Lake Balaton)",
        "date": "March 6–16, 1945",
        "year": 1945,
        "era": 4,
        "theatre": "EUROPE_EAST",
        "location": "Lake Balaton, Western Hungary",
        "lat": 46.917, "lon": 18.083,
        "total_tanks": "~1,300 Tanks (877 DE vs 407 SU + 900 SU Counteroffensive)",
        "side_a": {"name": "Soviet 3rd Ukrainian Front & 6th Guards Tank Army", "flag": "☭", "tanks": ["is2", "t34_85"], "count": "T-34-85, IS-2 Heavy Tanks, SU-100 & ISU-152"},
        "side_b": {"name": "German 6th SS Panzer Army (Sepp Dietrich)", "flag": "🇩🇪", "tanks": ["tiger_ii", "panther", "panzer_iv"], "count": "877 Tanks (incl. 56 Tiger IIs of s.SS-Pz.Abt 501 & FG 1250 IR Panthers)"},
        "outcome": "Germany's final major armored offensive of WWII crushed in deep mud and Soviet anti-tank defense belts, opening the road to Vienna.",
        "tactical_zoom": {
            "terrain": "Thawing springtime mud between Lake Balaton and Lake Velence",
            "range_m": "600–1,400m heavy 122mm IS-2 / 100mm SU-100 vs Tiger II duels",
            "formations": [
                {"side": "A", "label": "Soviet Deep Anti-Tank Belts + IS-2 / T-34-85 Reserves", "x": 72, "y": 48, "tx": 46, "ty": 48},
                {"side": "B", "label": "6th SS Panzer Army (Tiger II & Night-Vision Panthers)", "x": 26, "y": 48, "tx": 52, "ty": 48}
            ],
            "key_lesson": "Even equipped with infrared night-vision sights (Sperber FG 1250) and King Tigers, heavy German armor could not overcome Soviet 100mm/122mm defense-in-depth and 46-ton IS-2 counterattacks."
        },
        "summary": "To protect Hungary's Nagykanizsa oilfields, Hitler committed the elite 6th SS Panzer Army—fresh from the Ardennes and equipped with Tiger IIs and the world's first infrared night-vision Panthers. Marshal Tolbukhin replicated the Kursk defense-in-depth with 66 anti-tank guns per kilometer, backed by 122mm IS-2 heavy tanks and T-34-85s that shattered the SS Panzer divisions and captured Vienna weeks later."
    },
    {
        "id": "korea_1950",
        "name": "Korean War Tank Battles (Pusan Perimeter, Inchon & Chipyong-ni)",
        "date": "July – November 1950",
        "year": 1950,
        "era": 5,
        "theatre": "ASIA_EAST",
        "location": "Nakdong River / Bowling Alley & Seoul, Korea",
        "lat": 35.995, "lon": 128.564,
        "total_tanks": "~650 Tanks (500 UN vs 150+ KPA)",
        "side_a": {"name": "UN Command (US Army / USMC / British 8th King's Royal Irish Hussars)", "flag": "🇺🇸/🇬🇧", "tanks": ["m4a3e8", "m26_pershing", "m48_m60_patton", "centurion_mk1"], "count": "~500 Tanks (M4A3E8 Easy Eight, M26 Pershing, M46 Patton, Centurion Mk 3)"},
        "side_b": {"name": "Korean People's Army (105th Armored Division)", "flag": "🇰🇵/☭", "tanks": ["t34_85"], "count": "258 T-34-85 Medium Tanks & SU-76M"},
        "outcome": "Across 119 tank actions in 1950, US M26 Pershings, M46 Pattons, and M4A3E8 Easy Eights destroyed 97 T-34-85s in direct tank-vs-tank duels for 34 US tanks lost.",
        "tactical_zoom": {
            "terrain": "Steep mountain valleys ('The Bowling Alley' north of Taegu) & Nakdong River crossings",
            "range_m": "300–1,100m valley road duels with 90mm & 76mm HVAP",
            "formations": [
                {"side": "A", "label": "USMC M26 Pershings & Army M4A3E8 Easy Eights", "x": 50, "y": 72, "tx": 50, "ty": 42},
                {"side": "B", "label": "KPA 105th Armored Div (T-34-85 Spearheads)", "x": 50, "y": 24, "tx": 50, "ty": 52}
            ],
            "key_lesson": "While T-34-85s easily overran light M24 Chaffees in July 1950, the arrival of 90mm M26 Pershings, M46 Pattons, and HVAP-armed M4A3E8s decisively reversed the armor balance."
        },
        "summary": "In June–July 1950, North Korea's Soviet-supplied T-34-85s spearheaded the rapid capture of Seoul against South Korean infantry and US light M24 Chaffee tanks. Rush-shipped to the Pusan Perimeter in August, US M26 Pershings, M46 Pattons, M4A3E8 Easy Eights, and British Centurion Mk 3s turned the 'Bowling Alley' into a graveyard for KPA armor, winning nearly 3-to-1 in tank-on-tank engagements."
    },
    {
        "id": "chawinda_1965",
        "name": "Battles of Asal Uttar & Chawinda (Indo-Pakistani War)",
        "date": "September 8–22, 1965",
        "year": 1965,
        "era": 5,
        "theatre": "SOUTH_ASIA",
        "location": "Khem Karan (Punjab, India) & Chawinda (Sialkot, Pakistan)",
        "lat": 32.345, "lon": 74.715,
        "total_tanks": "~1,100 Tanks across Both Sectors",
        "side_a": {"name": "Indian Army (1st Armoured Division & 2nd Independent Armoured Brigade)", "flag": "🇮🇳", "tanks": ["centurion_mk1", "m4_sherman", "amx13_30"], "count": "Centurion Mk 7 (20-pdr), M4A3E8 Sherman, AMX-13"},
        "side_b": {"name": "Pakistan Army (1st & 6th Armoured Divisions)", "flag": "🇵🇰", "tanks": ["m48_m60_patton"], "count": "M47 & M48 Patton (90mm), M36B2, M24 Chaffee"},
        "outcome": "At Asal Uttar, Indian Centurions and flooded sugarcane fields trapped 97 Pakistani Pattons ('Patton Nagar'); at Chawinda, Pakistani Pattons and tank destroyers blunted India's 1st Armoured Division drive.",
        "tactical_zoom": {
            "terrain": "Flooded Punjab sugarcane fields (Asal Uttar horseshoe) & Sialkot plains (Chawinda)",
            "range_m": "500–1,200m ambush gunnery (20-pounder APDS vs 90mm HEAT)",
            "formations": [
                {"side": "A", "label": "Indian 3rd Cavalry Centurion Mk 7 Horseshoe Ambush", "x": 70, "y": 46, "tx": 48, "ty": 48},
                {"side": "B", "label": "Pakistani 1st/6th Armoured Div M47/M48 Pattons", "x": 26, "y": 48, "tx": 52, "ty": 48}
            ],
            "key_lesson": "Showed that older, simpler Centurion Mk 7 tanks with well-trained crews using terrain (flooded irrigation canals) could defeat technologically complex M48 Pattons whose computer rangefinders confused crews at close range."
        },
        "summary": "The largest tank clashes since Kursk. At Asal Uttar (Sep 8–10), Indian Brig. Thomas Theograj flooded the tall sugarcane fields overnight and arrayed his 20-pounder Centurion Mk 7s, Shermans, and AMX-13s in a U-shaped trap, capturing or destroying 97 Pakistani M47/M48 Pattons. Days later at Chawinda, over 500 tanks clashed around Sialkot as Pakistani M48s held the railway line until the UN ceasefire."
    },
    {
        "id": "sinai_1967",
        "name": "Battle of Abu-Ageila & Sinai Campaign (Six-Day War)",
        "date": "June 5–8, 1967",
        "year": 1967,
        "era": 5,
        "theatre": "MIDDLE_EAST",
        "location": "Abu-Ageila & Bir Gifgafa, Sinai Peninsula, Egypt",
        "lat": 30.830, "lon": 34.070,
        "total_tanks": "~1,650 Tanks (700 IL vs 950 EG)",
        "side_a": {"name": "Israel Defense Forces (Ugda Tal, Sharon & Yoffe)", "flag": "🇮🇱", "tanks": ["shot_magach", "centurion_mk1", "m48_m60_patton", "amx13_30"], "count": "~700 Tanks (Sho't Centurion, Magach M48, M50/M51 Super Sherman, AMX-13)"},
        "side_b": {"name": "Egyptian Armed Forces (Field Marshal Amer — 7 Divisions)", "flag": "🇪🇬", "tanks": ["t54_55", "t34_85"], "count": "~950 Tanks (T-54, T-55, T-34-85, IS-3M Heavy Tanks)"},
        "outcome": "Decisive Israeli breakthrough; long-range 105mm gunnery and night combined-arms assault destroyed or captured over 600 Egyptian tanks in four days.",
        "tactical_zoom": {
            "terrain": "Sand dunes (considered impassable), fortified Umm Qatef ridges & Mitla Pass",
            "range_m": "1,500–2,500m desert gunnery",
            "formations": [
                {"side": "A", "label": "Gen. Israel Tal & Ariel Sharon (Centurion/Patton Dune Outflanking)", "x": 76, "y": 35, "tx": 35, "ty": 52},
                {"side": "B", "label": "Egyptian Fortified Abu-Ageila Hedgehog (T-54/55 & IS-3M)", "x": 45, "y": 50, "tx": 55, "ty": 46}
            ],
            "key_lesson": "Long-range tank gunnery (105mm L7 and French CN-105-F1 on M51 Super Shermans) defeated heavily armored Soviet IS-3M and T-54/55 tanks from beyond their effective return-fire envelope."
        },
        "summary": "Crossing 'impassable' northern coastal dunes at Khan Yunis and executing a textbook night combined-arms encirclement at Abu-Ageila, Israeli armored divisions under Israel Tal, Avraham Yoffe, and Ariel Sharon shattered Egypt's Sinai defense network. Israeli 105mm-armed Centurions and M51 Super Shermans knocked out even Soviet IS-3M heavy tanks before racing to seal the Mitla and Gidi Passes."
    },
    {
        "id": "valley_of_tears_1973",
        "name": "Battle of the Valley of Tears (Golan Heights)",
        "date": "October 6–9, 1973",
        "year": 1973,
        "era": 5,
        "theatre": "MIDDLE_EAST",
        "location": "Kuneitra & Northern Golan Heights",
        "lat": 33.128, "lon": 35.815,
        "total_tanks": "~1,400 Tanks in Golan (~177 IL vs ~1,200 SY)",
        "side_a": {"name": "IDF 7th Armored Brigade (Avigdor Kahalani) & 188th Barak Brigade", "flag": "🇮🇱", "tanks": ["shot_magach"], "count": "105 Sho't Kal (Up-gunned Centurions) in 7th Brigade"},
        "side_b": {"name": "Syrian Arab Army (7th Infantry & 1st/3rd Armored Divisions)", "flag": "🇸🇾", "tanks": ["t54_55", "t62"], "count": "~500–700 Syrian T-55 & T-62 Tanks in the northern sector"},
        "outcome": "One of the most extraordinary defensive tank stands in history: ~105 Israeli Centurions held off 500+ Syrian T-55/T-62s for four days and nights, leaving 260 Syrian tanks and 240 APCs burning in the valley.",
        "tactical_zoom": {
            "terrain": "Black basalt volcanic boulders, anti-tank ditch & Booster Ridge overlook",
            "range_m": "2,000m daytime sniping down to 50m pitch-black night brawls",
            "formations": [
                {"side": "A", "label": "7th Armored Brigade (Kahalani's Sho't Kal on Booster Ramp)", "x": 28, "y": 50, "tx": 42, "ty": 50},
                {"side": "B", "label": "Syrian 7th Div & 3rd Armored Div (T-55/T-62 Infrared Night Waves)", "x": 78, "y": 50, "tx": 46, "ty": 50}
            ],
            "key_lesson": "The Centurion's superior -10° gun depression (vs -4° on the T-55/T-62) allowed Israeli tanks to fire down from basalt ridges while exposing only their turret roofs."
        },
        "summary": "Outnumbered nearly 5-to-1 and lacking infrared night-vision sights against Syrian T-55s and 115mm smoothbore T-62s that had them, Lt. Col. Avigdor Kahalani's 77th Battalion and the 7th Armored Brigade fought non-stop for 75 hours along a volcanic ridge overlooking Kuneitra. Exploiting the Centurion's -10° gun depression, the last 7 operational Israeli tanks charged the ridge crest on October 9 just as Syrian forces—convinced Israel had reinforced—retreated, abandoning 260 knocked-out tanks."
    },
    {
        "id": "chinese_farm_1973",
        "name": "Battle of the Chinese Farm & Sinai Crossing",
        "date": "October 14–18, 1973",
        "year": 1973,
        "era": 5,
        "theatre": "MIDDLE_EAST",
        "location": "Deversoir / Great Bitter Lake (East Bank Suez Canal), Egypt",
        "lat": 30.435, "lon": 32.355,
        "total_tanks": "~1,700 Tanks across Sinai Crossing (Oct 14–18)",
        "side_a": {"name": "IDF Southern Command (Sharon's 143rd & Adan's 162nd Armored Divs)", "flag": "🇮🇱", "tanks": ["shot_magach", "m48_m60_patton"], "count": "~750 Magach 3/6 (M48/M60) & Sho't Kal Centurions"},
        "side_b": {"name": "Egyptian Second & Third Armies (21st & 4th Armored Divs)", "flag": "🇪🇬", "tanks": ["t54_55", "t62"], "count": "~800–1,000 T-55 & T-62 Tanks + 9M14 Malyutka (AT-3 Sagger) ATGM Teams"},
        "outcome": "After defeating Egypt's October 14 armored push (destroying ~250 Egyptian tanks), Israeli armor fought through the lethal Chinese Farm strongpoint to bridge the Suez Canal and encircle the Egyptian Third Army.",
        "tactical_zoom": {
            "terrain": "Irrigation canals of former Japanese agricultural station ('Chinese Farm') & Suez approaches",
            "range_m": "Point-blank 30–300m night tank-and-ATGM melee",
            "formations": [
                {"side": "A", "label": "Sharon & Adan Magach (M60) / Centurion Canal Corridor Push", "x": 74, "y": 46, "tx": 28, "ty": 52},
                {"side": "B", "label": "Egyptian 21st Armored Div (T-62/T-55) & Sagger ATGM Trenches", "x": 45, "y": 38, "tx": 48, "ty": 48}
            ],
            "key_lesson": "Exposed the vulnerability of conventional steel armor and hydraulic turret fluid (in early M60s) to wire-guided HEAT missiles (AT-3 Sagger) and RPG-7s—directly driving the invention of Chobham composite armor, Blazer ERA, and the front-engine Merkava."
        },
        "summary": "After Egyptian infantry armed with AT-3 Sagger missiles decimated unescorted Israeli tank charges in the opening days, Egypt launched a massive 1,000-tank offensive out from under its SAM umbrella on October 14—losing ~250 T-55/T-62s to hull-down Israeli M60s and Centurions. Immediately, Gen. Ariel Sharon exploited the seam between Egypt's Second and Third Armies at the 'Chinese Farm,' fighting a brutal 72-hour point-blank night tank battle to haul pontoon bridges to the Suez Canal."
    },
    {
        "id": "dezful_1981",
        "name": "Battle of Dezful / Susangerd (Iran–Iraq War)",
        "date": "January 5–8, 1981",
        "year": 1981,
        "era": 6,
        "theatre": "MIDDLE_EAST",
        "location": "Susangerd & Dezful, Khuzestan Province, Iran",
        "lat": 31.560, "lon": 48.183,
        "total_tanks": "~600 Tanks (~300 IR vs ~300 IQ)",
        "side_a": {"name": "Islamic Republic of Iran Army (16th & 92nd Armored Divisions)", "flag": "🇮🇷", "tanks": ["chieftain", "m48_m60_patton"], "count": "~300 British Chieftain Mk 5P & US M60A1 Tanks"},
        "side_b": {"name": "Iraqi Army (9th Armored Division)", "flag": "🇮🇶", "tanks": ["t62", "t72"], "count": "~300 Soviet T-62 & early T-72 Ural Tanks"},
        "outcome": "Iraqi defensive victory; mud bogged down heavy 55-ton Iranian Chieftains in a three-sided T-62/T-72 horseshoe ambush, though Chieftain 120mm guns later exacted revenge in Operation Tariq al-Quds.",
        "tactical_zoom": {
            "terrain": "Waterlogged Karkheh River floodplains near Susangerd",
            "range_m": "1,000–1,800m hull-down T-62/T-72 ambush vs bogged Chieftains",
            "formations": [
                {"side": "A", "label": "Iranian 16th Armored Div (Chieftain Mk 5P Column in Mud)", "x": 72, "y": 48, "tx": 46, "ty": 48},
                {"side": "B", "label": "Iraqi 9th Armored Div (Hull-Down T-62 & T-72 Ural Horseshoe)", "x": 32, "y": 48, "tx": 48, "ty": 48}
            ],
            "key_lesson": "First major combat clash between the British 120mm-armed Chieftain and Soviet 115mm T-62 / 125mm T-72; highlighted the Chieftain's Leyland L60 engine reliability issues in deep mud and homogeneous steel vulnerability to 115mm/125mm APFSDS."
        },
        "summary": "During Operation Nasr near Susangerd and Dezful, three brigades of Iranian Chieftain Mk 5P and M60A1 tanks advanced across winter-rain-soaked floodplains without infantry or artillery coordination. Iraqi T-62s and newly delivered T-72 Urals waited in prepared three-sided hull-down revetments, knocking out over 100 bogged-down Iranian tanks while suffering ~45 T-62 losses to the Chieftain's formidable 120mm L11 rifled gun."
    },
    {
        "id": "bekaa_1982",
        "name": "Battles of the Bekaa Valley & Sultan Yacoub (1982 Lebanon War)",
        "date": "June 9–11, 1982",
        "year": 1982,
        "era": 6,
        "theatre": "MIDDLE_EAST",
        "location": "Bekaa Valley & Sultan Yacoub, Lebanon",
        "lat": 33.685, "lon": 35.862,
        "total_tanks": "~800 Tanks (~400 IL vs ~400 SY)",
        "side_a": {"name": "Israel Defense Forces (Ben-Gal's Northern Corps)", "flag": "🇮🇱", "tanks": ["merkava_i_ii", "shot_magach"], "count": "Merkava Mk I (combat debut), Magach 6 (M60 with Blazer ERA), Sho't Kal"},
        "side_b": {"name": "Syrian Arab Army (1st & 3rd Armored Divisions)", "flag": "🇸🇾", "tanks": ["t72", "t62"], "count": "T-72M (125mm) & T-62 Medium Tanks + Gazelle Attack Helicopters"},
        "outcome": "Successful combat debut of the Israeli Merkava Mk I, Blazer Explosive Reactive Armor (ERA), and M111 'Hetz' 105mm tungsten fin-stabilized APFSDS round.",
        "tactical_zoom": {
            "terrain": "Narrow mountain highway corridor between Mount Lebanon and Anti-Lebanon ranges",
            "range_m": "1,200–2,500m valley-floor and mountain-terrace gunnery",
            "formations": [
                {"side": "A", "label": "Merkava Mk I & Blazer-ERA Magach 6 Advancing North", "x": 48, "y": 76, "tx": 48, "ty": 42},
                {"side": "B", "label": "Syrian 3rd Armored Div (T-72M & T-62 Counterattack)", "x": 48, "y": 22, "tx": 48, "ty": 48}
            ],
            "key_lesson": "First combat deployment of Explosive Reactive Armor (Blazer ERA defeated RPGs/ATGMs) and first Western 105mm APFSDS ('Hetz' M111) penetration of T-72 frontal glacis—which soon prompted the USSR to weld an extra 16mm steel plate and Kontakt-1 ERA onto all T-72s."
        },
        "summary": "The 1982 Bekaa Valley campaign marked three historic milestones in tank warfare: the combat debut of Gen. Israel Tal's front-engine Merkava Mk I, the first battlefield use of Explosive Reactive Armor (Blazer tiles on Magach M60s and Centurions), and the first clash between Western 105mm M111 'Hetz' tungsten APFSDS darts and Soviet-built Syrian T-72M tanks."
    },
    {
        "id": "easting_1991",
        "name": "Battle of 73 Easting, Medina Ridge & Norfolk (Gulf War)",
        "date": "February 26–27, 1991",
        "year": 1991,
        "era": 6,
        "theatre": "MIDDLE_EAST",
        "location": "Al-Busayyah / 73 Easting Gridline, Southern Iraq",
        "lat": 29.545, "lon": 46.625,
        "total_tanks": "~1,800 Tanks across VII Corps Sector",
        "side_a": {"name": "US VII Corps (2nd ACR, 1st & 3rd Armored, 1st Inf) & UK 1st Armoured Div", "flag": "🇺🇸/🇬🇧", "tanks": ["m1_abrams", "challenger1", "m48_m60_patton"], "count": "M1A1 HA Abrams (120mm DU), UK Challenger 1, USMC M60A1 RISE"},
        "side_b": {"name": "Iraqi Republican Guard (Tawakalna, Medina & Hammurabi Divisions)", "flag": "🇮🇶", "tanks": ["t72", "t62", "t54_55", "type59_74_strv103"], "count": "T-72M/M1, T-62, T-55 & Chinese Type 59/69"},
        "outcome": "One-sided technological rout: at 73 Easting and Medina Ridge, US M1A1 Abrams and M2 Bradleys destroyed over 340 Republican Guard T-72s and T-62s without a single M1A1 destroyed by enemy tank fire.",
        "tactical_zoom": {
            "terrain": "Featureless Iraqi desert swept by blinding Shamal sandstorms along UTM North-South Gridline 73",
            "range_m": "2,400–3,500m (Abrams thermal sights saw through sandstorm; Iraqi optics blinded beyond 1,000m)",
            "formations": [
                {"side": "A", "label": "Eagle Troop / 2nd ACR & 1st Armored (M1A1 HA Abrams + M3 Bradley)", "x": 22, "y": 48, "tx": 60, "ty": 48},
                {"side": "B", "label": "Republican Guard Tawakalna & Medina Divs (Dug-In T-72M1 Berm Line)", "x": 74, "y": 48, "tx": 55, "ty": 48}
            ],
            "key_lesson": "Demonstrated the overwhelming generational leap of 3rd-Gen MBTs: GPS navigation across featureless desert, FLIR thermal sights piercing sandstorms at 3,000m, Chobham/DU armor, and M829A1 depleted-uranium darts punching straight through sand berms into T-72 hulls."
        },
        "summary": "Charging east through a blinding Shamal sandstorm using GPS receivers, Capt. H.R. McMaster's Eagle Troop (2nd Armored Cavalry Regiment) crested the 70 Easting rise and overran the Iraqi Republican Guard's Tawakalna Division along the 73 Easting gridline in 23 minutes. The next day at Medina Ridge, over 300 M1A1 HA Abrams engaged the Medina Division at 3,000m—destroying 186 Iraqi tanks while British Challenger 1s destroyed ~300 Iraqi tanks including a 4,700m world-record kill."
    },
    {
        "id": "baghdad_2003",
        "name": "Battle of the Karbala Gap, Baghdad Thunder Runs & Basra (2003 Iraq War)",
        "date": "March 23 – April 7, 2003",
        "year": 2003,
        "era": 7,
        "theatre": "MIDDLE_EAST",
        "location": "Karbala, Mahmoudiyah, Baghdad & Basra, Iraq",
        "lat": 33.150, "lon": 44.360,
        "total_tanks": "~650 Coalition Tanks vs ~450 Iraqi Tanks",
        "side_a": {"name": "US 3rd Infantry Div, 1st Marine Div & UK 7th Armoured Brigade (Desert Rats)", "flag": "🇺🇸/🇬🇧", "tanks": ["m1a2_sepv3", "m1_abrams", "challenger2_3"], "count": "M1A1 AIM / M1A2 Abrams & 120x British Challenger 2"},
        "side_b": {"name": "Iraqi Republican Guard (Medina & Nebuchadnezzar Divs) & 6th Armored Div", "flag": "🇮🇶", "tanks": ["t72", "t54_55"], "count": "T-72M1 / Lion of Babylon & T-55 Enigma (spaced armor)"},
        "outcome": "Rapid Coalition armored dash to Baghdad; outside Basra on March 27, 14 British Challenger 2s destroyed 14 Iraqi T-55s without loss, while US 3rd ID's 'Thunder Runs' collapsed Baghdad's defenses.",
        "tactical_zoom": {
            "terrain": "Euphrates palm groves, Highway 8 urban highway overpasses & Basra outskirts",
            "range_m": "50m urban overpass RPG ambushes to 2,200m T-72/T-55 engagements",
            "formations": [
                {"side": "A", "label": "TF 1-64 Armor 'Thunder Run' (M1A1/A2 Abrams Column into Baghdad)", "x": 30, "y": 74, "tx": 52, "ty": 30},
                {"side": "B", "label": "Medina Div T-72s (Mahmoudiyah) & Highway Ambush Bunkers", "x": 54, "y": 46, "tx": 48, "ty": 52}
            ],
            "key_lesson": "Proved modern composite MBTs could survive high-intensity urban 'Thunder Runs' when kept moving, while spawning TUSK (Tank Urban Survival Kit) and Dorchester Streetfighter upgrades against side/rear RPG-29s and IEDs."
        },
        "summary": "After smashing Republican Guard T-72s around the Karbala Gap and Mahmoudiyah (where 2nd Bn, 70th Armor destroyed 7 T-72s at point-blank range in a dust storm), Col. David Perkins and Lt. Col. Eric Schwartz launched two daring 'Thunder Runs'—driving columns of M1A1/A2 Abrams and Bradleys straight into the heart of Baghdad. Meanwhile in the south at Basra, Royal Scots Dragoon Guards Challenger 2s won a 14-to-0 tank duel against Iraqi T-55s."
    },
    {
        "id": "ukraine_2022_2024",
        "name": "Russo-Ukrainian War Tank Battles (Chernihiv, Vuhledar, Zaporizhzhia & Pokrovsk)",
        "date": "Feb 2022 – 2026",
        "year": 2023,
        "era": 7,
        "theatre": "EUROPE_EAST",
        "location": "Chernihiv, Vuhledar, Robotyne & Donbas, Ukraine",
        "lat": 47.781, "lon": 37.248,
        "total_tanks": "4,000+ Tanks Engaged Across Theatre",
        "side_a": {"name": "Armed Forces of Ukraine (1st Tank Brigade, 47th & 33rd Mech Brigades)", "flag": "🇺🇦", "tanks": ["t84_oplot", "t64_t80", "leopard2_a7_kf51", "m1a2_sepv3", "challenger2_3"], "count": "T-64BV Zr.2017, T-84 Oplot, Leopard 2A4/2A6, M1A1 SA Abrams, Challenger 2"},
        "side_b": {"name": "Russian Armed Forces (1st Guards Tank Army, 90th Tank Div)", "flag": "🇷🇺", "tanks": ["t72", "t64_t80", "t90m"], "count": "T-72B3M, T-80BVM, T-90M Proryv-3, modernized T-62M"},
        "outcome": "First high-intensity conflict combining Soviet-lineage and Western 3rd-Gen MBTs under omnipresent UAV recon, FPV kamikaze drones, dense minefields, and top-attack ATGMs.",
        "tactical_zoom": {
            "terrain": "Donbas & Zaporizhzhia open steppes divided by dense tree-line windbreaks (posadkas) & minefields",
            "range_m": "800–2,500m tree-line duels + 5–15km indirect drone-corrected tank fire & FPV drone defense",
            "formations": [
                {"side": "A", "label": "Ukrainian T-64BV / Leopard 2A6 / M1A1 Abrams Tree-Line Defense & Counter-Push", "x": 28, "y": 48, "tx": 48, "ty": 48},
                {"side": "B", "label": "Russian T-90M Proryv & T-80BVM Mechanized Columns", "x": 74, "y": 48, "tx": 52, "ty": 48}
            ],
            "key_lesson": "Redefined 21st-century armor: Western MBTs (Leopard 2, Abrams, Challenger 2) demonstrated dramatically higher crew survival rates due to isolated ammo blow-out panels (vs carousel autoloader detonations), while FPV drones forced all tanks to adopt roof cages, EW jammers, and multi-hemisphere Active Protection."
        },
        "summary": "In Feb–March 2022 at the Battle of Chernihiv, Ukraine's 1st Tank Brigade (equipped with modernized T-64BV tanks using Nozh ERA and thermal sights) ambushed larger Russian T-72B3 columns in forests and towns. In 2023–2024 around Vuhledar, Robotyne, and Avdiivka/Pokrovsk, Leopard 2A4/2A6, M1A1 Abrams, and Challenger 2 fought alongside T-64BVs against Russian T-90M Proryv and T-80BVM tanks—ushering in the era of drone-networked armor warfare."
    }
]

# Validate all node and battle references!
tank_ids = {t["id"] for t in TANKS}
battle_ids = {b["id"] for b in BATTLES}

for e in EDGES:
    assert e["source"] in tank_ids, f"Missing edge source: {e['source']}"
    assert e["target"] in tank_ids, f"Missing edge target: {e['target']}"
    for b_id in e.get("battles", []):
        assert b_id in battle_ids, f"Missing edge battle: {b_id}"

for b in BATTLES:
    for tid in b["side_a"]["tanks"] + b["side_b"]["tanks"]:
        assert tid in tank_ids, f"Missing battle tank: {tid} in {b['id']}"

print(f"VALIDATION PASSED: {len(TANKS)} Tanks, {len(EDGES)} Edges, {len(BATTLES)} Battles all cross-linked with 0 broken IDs!")

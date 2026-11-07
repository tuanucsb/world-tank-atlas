# Forensic Destruction Breakdown & Chronological Battle Timelines for all 27 Battles
# Special ultra-detailed historical choreography for Battle of Raseiniai (994 tanks) and all major battles.

BATTLE_FORENSICS = {
    "raseiniai_1941": {
        "total_tanks": "994 Tanks Involved (749 Soviet 3rd & 12th Mechanized Corps vs 245 German 6th & 1st Panzer Divisions)",
        "numeric_a": 749,
        "numeric_b": 245,
        "numeric_lost_a": 704,
        "numeric_lost_b": 45,
        "side_a_count": "749 Tanks (~52 KV-1 & KV-2 Heavy, ~415 T-26 Light, ~282 BT-7 Fast Cavalry Tanks)",
        "side_b_count": "245 Tanks (114 Panzer 35(t)/38(t), 47 Panzer IV, 45 Panzer III, 39 Panzer II + 88mm Flak batteries)",
        "losses_a": "704 of 749 Soviet tanks destroyed/abandoned (~430 T-26/BT-7 penetrated by 37mm/50mm AP; ~29 KV-1/KV-2 knocked out by 88mm Flak & 105mm guns; ~195 out of fuel/ammo & scuttled in pocket; ~50 mechanical breakdown)",
        "losses_b": "~45 German Panzers & 35+ Pak/Flak guns destroyed (~28 Panzers penetrated by 76.2mm KV-1 & 45mm BT-7 fire; ~12 Panzers & 35+ AT guns crushed directly under KV-1/2 tracks; ~5 shattered by 152mm KV-2 HE)",
        "destruction_a": [
            {"cause": "37mm & 50mm Panzer / Pak Crossfire on Light Armor", "pct": 61, "count": "~430 T-26 & BT-7 Light Tanks", "color": "#f43f5e", "detail": "Thin 15–22mm armor on Soviet T-26 and BT-7 light tanks (23rd & 28th Tank Divs) was easily penetrated at 300–800m by German Panzer 35(t)/38(t) 37mm, Panzer III 50mm L/42, and 50mm Pak 38 ambushes along forest roads."},
            {"cause": "Fuel & Ammo Exhaustion inside Encirclement Pocket", "pct": 28, "count": "~195 KV-1, KV-2, BT-7 & T-26", "color": "#f59e0b", "detail": "After 1st & 6th Panzer Divisions closed the ring east of the Dubysa River and Luftwaffe Stukas bombed Red Army fuel trains, ~195 tanks ran dry of diesel and shells in the marshes and were blown up by their crews."},
            {"cause": "Mechanical Breakdown on 150km Forced Marches", "pct": 7, "count": "~50 T-26 & BT-7 Tanks", "color": "#a855f7", "detail": "12th Mechanized Corps marched 120–150 km under constant air attack without recovery tractors; worn clutches and tracks forced crews to abandon ~50 vehicles."},
            {"cause": "88mm Flak 18/36 Heavy AA Guns, 105mm Howitzers & Pioneers", "pct": 4, "count": "~29 KV-1 & KV-2 Heavy Tanks", "color": "#38bdf8", "detail": "Because 37mm & 50mm tank shells bounced off the KV-1/KV-2's 75–90mm armor, Germans could only destroy them by towing high-velocity 88mm Flak AA guns to 600m, firing 105mm howitzers point-blank, and sending sappers with satchel charges against their tracks."}
        ],
        "destruction_b": [
            {"cause": "76.2mm L-11/F-32 (KV-1) & 45mm 20-K (BT-7/T-26) Gunfire", "pct": 62, "count": "~28 Panzer 35(t)/38(t), III & IV", "color": "#38bdf8", "detail": "Penetrated at 400–900m during Maj. Gen. Solyankin's 2nd Tank Division counterattack south of Raseiniai on June 23–24."},
            {"cause": "Crushed Directly Under KV-1 & KV-2 Heavy Tracks", "pct": 27, "count": "~12 Panzers & 35+ Pak 36/38 Guns", "color": "#f59e0b", "detail": "When German 37mm 'door-knocker' shells bounced off Soviet KV-1s, Soviet crews drove their 45-ton tanks straight over German anti-tank batteries, supply trucks, and immobilized Panzers."},
            {"cause": "152mm M-10 Howitzer Concussion (KV-2 Dreadnoughts)", "pct": 11, "count": "~5 Panzer III / IV", "color": "#f43f5e", "detail": "Shattered by massive 48.8 kg high-explosive shells fired by KV-2 heavy assault tanks."}
        ],
        "phases": [
            {
                "phase": 1,
                "time": "June 23, 1941 (04:00–16:00)",
                "title": "XLI Panzer Corps Crosses the Dubysa River & Seizes Raseiniai",
                "desc": "German 6th Panzer Division (114 Panzer 35(t)/38(t), 47 Panzer IV) captures Raseiniai and forms two bridgeheads across the Dubysa River: KG Raus in the north and KG Seckendorff in the south. Soviet Northwestern Front orders 3rd & 12th Mechanized Corps (749 tanks) to counterattack.",
                "lost_a_pct": 0.05,
                "lost_b_pct": 0.02,
                "focus_event": "Dubysa River Bridgeheads Established"
            },
            {
                "phase": 2,
                "time": "June 23–24, 1941 (Morning)",
                "title": "Solyankin's 2nd Tank Div (50+ KV-1/KV-2) Smashes KG Seckendorff",
                "desc": "Maj. Gen. Solyankin's Soviet 2nd Tank Division charges KG Seckendorff south of Raseiniai. German 37mm Pak 36 and 50mm Panzer III shells bounce harmlessly off the 75–90mm armor of Soviet KV-1 and KV-2 heavy tanks! KV-1s crush German Pak batteries and trucks under their tracks.",
                "lost_a_pct": 0.16,
                "lost_b_pct": 0.55,
                "focus_event": "KV-1 Armor Shock — 37mm/50mm Shells Ricochet!"
            },
            {
                "phase": 3,
                "time": "June 24 (14:00) – June 25 (16:00)",
                "title": "The Lone KV Tank on the Crossroads Blocks KG Raus for 26 Hours",
                "desc": "A single Soviet KV-1/KV-2 occupies the sole supply road behind KG Raus's northern bridgehead, burning 12 supply trucks, destroying four 50mm Pak 38s and an 88mm Flak gun, and shrugging off midnight sapper bombs. On June 25, 13 Panzer 35(t)s swarm in a distraction circle while two 88mm Flak guns fire 7 AP rounds into its rear/side to finally silence it.",
                "lost_a_pct": 0.34,
                "lost_b_pct": 0.75,
                "focus_event": "Lone KV Holds Crossroads for 26h vs Half a Panzer Division"
            },
            {
                "phase": 4,
                "time": "June 25–26, 1941",
                "title": "1st Panzer Division Flanks from Kelmė — 430 BT-7 & T-26 Light Tanks Burned",
                "desc": "While 88mm Flak guns stem the KV-1 advance, the German 1st Panzer Division (Panzer III & IV) hooks north from Kelmė into the Soviet flank. Caught on forest roads, ~430 thin-armored Soviet T-26 (15mm) and BT-7 (22mm) tanks of the 12th Mechanized Corps are penetrated and burned by German 37mm/50mm crossfire.",
                "lost_a_pct": 0.72,
                "lost_b_pct": 0.92,
                "focus_event": "1st Panzer Flank Hook — Light BT-7/T-26 Columns Ambushed"
            },
            {
                "phase": 5,
                "time": "June 26–27, 1941",
                "title": "Pocket Closes East of Raseiniai — Fuel Starvation & Final Collapse",
                "desc": "1st and 6th Panzer Divisions link up in the Soviet rear, encircling the 2nd, 23rd, and 28th Tank Divisions. Gen. Solyankin is killed in action; with fuel convoys bombed by the Luftwaffe, ~195 remaining KV-1, KV-2, BT-7, and T-26 tanks run out of diesel and ammo in the swamps and are scuttled. 704 of 749 Soviet tanks are lost.",
                "lost_a_pct": 0.94,
                "lost_b_pct": 1.0,
                "focus_event": "Raseiniai Pocket Closed — 704 of 749 Soviet Tanks Lost"
            }
        ]
    },
    "kursk_1943": {
        "total_tanks": "1,460 Tanks at Prokhorovka / ~6,000 in Kursk Salient (850 Soviet 5th Guards Tank Army vs 610 German II SS Panzer Corps)",
        "numeric_a": 850,
        "numeric_b": 610,
        "numeric_lost_a": 334,
        "numeric_lost_b": 85,
        "side_a_count": "850 Tanks at Prokhorovka (500+ T-34/76, 260 T-70, 35 Churchill, KV-1, SU-122 & SU-152 'Zveroboy')",
        "side_b_count": "610 Tanks & Assault Guns (Panzer IV L/48, Panzer III, StuG III, ~42 Tiger I; ~200 Panther & 90 Ferdinand on Salient)",
        "losses_a": "334–400 Soviet tanks destroyed/damaged at Prokhorovka on July 12 (~220 burned by 88mm Tiger I & 75mm Panzer IV L/48 fire; ~65 fell into anti-tank ditch & shot; ~50 hit by StuG III & Marder III)",
        "losses_b": "70–85 German tanks & StuGs destroyed/damaged at Prokhorovka (~45 Panzer IV/III & StuG III penetrated at close range by T-34/76 & SU-152; ~25 immobilized in Soviet minefields & Pakfronts)",
        "destruction_a": [
            {"cause": "Long-Range 88mm KwK 36 (Tiger I) & 75mm L/48 (Panzer IV) Gunnery", "pct": 64, "count": "~215 T-34/76 & T-70 Tanks", "color": "#f43f5e", "detail": "German Tiger I (100mm armor, 88mm gun) and Panzer IV Ausf. G/H outranged Soviet 76.2mm F-34 guns across the open steppe between the Psel River and railway embankment at 1,000–1,800m."},
            {"cause": "Oktiabrskii State Farm Anti-Tank Ditch Bottleneck", "pct": 21, "count": "~70 T-34 & T-70 Tanks", "color": "#f59e0b", "detail": "Racing forward at 40 km/h to close range, lead brigades of 18th & 29th Tank Corps tumbled into a 4.5m-deep anti-tank ditch and were picked off by SS Leibstandarte Panzer IVs and StuGs."},
            {"cause": "Luftwaffe Hs 129 (30mm MK 103) & Stuka / Artillery Strikes", "pct": 15, "count": "~49 Tanks", "color": "#a855f7", "detail": "Cannon-armed Henschel Hs 129 and Ju 87G tank-busters struck engine decks of massed Soviet reserve waves."}
        ],
        "destruction_b": [
            {"cause": "Close-Range (100–400m) T-34/76 Flank Shots & SU-152 152mm Hits", "pct": 58, "count": "~49 Panzer IV, Panzer III & StuG III", "color": "#38bdf8", "detail": "Once Rotmistrov's T-34s closed inside 400m amidst dust and smoke, 76.2mm AP shells penetrated Panzer III/IV side and frontal plates, while SU-152s shattered heavy armor."},
            {"cause": "Deep Red Army Minefields (3,000 Mines/km) & 8 Defense Belts", "pct": 27, "count": "~23 Tanks & Ferdinands Disabled", "color": "#f59e0b", "detail": "Sappers laid over 500,000 mines across the Kursk salient, blowing tracks off Panthers, Tigers, and Ferdinands so Soviet Pakfronts could finish them."},
            {"cause": "Early Panther Mechanical/Engine Fires & Breakdowns", "pct": 15, "count": "~13 Panthers / Tigers Disabled", "color": "#a855f7", "detail": "Rushed to Kursk without field trials, many early Panther Ausf. D tanks suffered fuel-pump fires and final-drive failures."}
        ],
        "phases": [
            {"phase": 1, "time": "July 5–10, 1943", "title": "Operation Citadel Opens — German Spearheads Grind Through 8 Soviet Defense Belts", "desc": "II SS Panzer Corps (LSSAH, Das Reich, Totenkopf) and XLVIII Panzer Corps breach the outer Soviet minefields and Pakfronts slowly while Ferdinand tank destroyers assault Ponyri in the north.", "lost_a_pct": 0.15, "lost_b_pct": 0.25, "focus_event": "Minefield Breaching & Pakfront Attrition"},
            {"phase": 2, "time": "July 12, 1943 (08:30)", "title": "Rotmistrov's 5th Guards Tank Army (850 Tanks) Charges at Prokhorovka", "desc": "With the battle cry 'Stal! Stal! Stal!', 18th and 29th Tank Corps charge down the narrow 6km corridor between the Psel River and railway embankment with the rising sun behind them.", "lost_a_pct": 0.35, "lost_b_pct": 0.42, "focus_event": "850 Soviet Tanks Launch High-Speed Charge"},
            {"phase": 3, "time": "July 12, 1943 (10:00–14:00)", "title": "The Anti-Tank Ditch Bottleneck & Point-Blank Brawl Around Hill 252.2", "desc": "Wittmann's 4 Tiger Is and SS Leibstandarte Panzer IVs engage at 1,500m, but surviving T-34/76s close to 100–300m around Hill 252.2 and Oktiabrskii State Farm, neutralizing the Tiger's range advantage.", "lost_a_pct": 0.72, "lost_b_pct": 0.78, "focus_event": "Point-Blank Melee at Hill 252.2 (100–300m)"},
            {"phase": 4, "time": "July 12, 1943 (14:00–20:00)", "title": "Flanking Clashes on the Psel River & Das Reich Sector", "desc": "Tank-on-tank fighting rages across the southern and northern shoulders until a summer thunderstorm turns the steppe into mud. Over 400 burned-out hulls litter the Prokhorovka corridor.", "lost_a_pct": 0.92, "lost_b_pct": 0.94, "focus_event": "400+ Burning Hulls Across Prokhorovka Steppe"},
            {"phase": 5, "time": "July 13–16, 1943", "title": "Citadel Cancelled — Strategic Initiative Passes Permanently to the Red Army", "desc": "Exhausted by attrition and with Allied landings in Sicily, Hitler cancels Operation Citadel; the Red Army launches Operations Kutuzov and Rumyantsev.", "lost_a_pct": 1.0, "lost_b_pct": 1.0, "focus_event": "German Offensive Halted Forever"}
        ]
    },
    "an_loc_dong_ha_1972": {
        "total_tanks": "520 Tanks Involved (120 ARVN M48A3 Patton & M41 Bulldog vs 400 PAVN/NVA T-54, Type 59 & PT-76)",
        "numeric_a": 120,
        "numeric_b": 400,
        "numeric_lost_a": 42,
        "numeric_lost_b": 250,
        "side_a_count": "120 Tanks (ARVN 20th Tank Regt M48A3 Pattons & M41A3 Walker Bulldogs + US UH-1B TOW helicopters)",
        "side_b_count": "400+ Tanks (PAVN 201st, 202nd & 203rd Armored Regiments: T-54, Type 59, PT-76 & T-34-85)",
        "losses_a": "~42 ARVN M41 Bulldogs & M48A3 Pattons lost during the initial Quảng Trị overrun and street defense",
        "losses_b": "250+ PAVN T-54, Type 59 & PT-76 tanks destroyed (~95 by M48A3/M41 tank fire at Dong Ha/Kontum; ~80 by M72 LAW & TOW missiles inside An Loc; ~75 by US/VNAF air strikes)",
        "destruction_a": [
            {"cause": "NVA 100mm D-10T (T-54/Type 59) & AT-3 Sagger Missile Hits", "pct": 58, "count": "~24 M41 Bulldogs & M48A3s", "color": "#f43f5e", "detail": "In May 1972, PAVN deployed 9M14 Malyutka (AT-3 Sagger) wire-guided missiles for the first time in Vietnam alongside 100mm T-54 guns along Highway 1."},
            {"cause": "130mm M-46 Artillery Barrages & Bridge Demolition Traps", "pct": 42, "count": "~18 Tanks Lost on Retreat from Quang Tri", "color": "#f59e0b", "detail": "Caught north of destroyed bridges during the April 28 collapse of Quang Tri perimeter."}
        ],
        "destruction_b": [
            {"cause": "Long-Range 90mm M48A3 Patton Optical Rangefinder Sniping (2,500–2,800m)", "pct": 38, "count": "~95 T-54, Type 59 & PT-76 Tanks", "color": "#38bdf8", "detail": "At Dong Ha (April 2 & April 27, 1972), ARVN 20th Tank Regiment M48A3s used coincidence optical rangefinders from hull-down ridges to destroy NVA T-54s and PT-76s long before NVA crews spotted them."},
            {"cause": "BGM-71 TOW Missiles (First Combat Use) & Close-Range M72 LAW Teams", "pct": 34, "count": "~85 T-54 & Type 59 Tanks (An Loc & Kontum)", "color": "#10b981", "detail": "Inside An Loc, NVA tanks attacked without infantry protection and were stalked from rooftops by ARVN paratroopers firing M72 66mm HEAT rockets; at Kontum, two US UH-1B TOW helicopters destroyed 24 NVA tanks."},
            {"cause": "USAF / USMC / VNAF Skyraider, Phantom & B-52 Strikes", "pct": 28, "count": "~70 NVA Tanks", "color": "#f59e0b", "detail": "Rockeye cluster munitions and laser-guided bombs destroyed staged NVA armor columns in rubber plantations."}
        ],
        "phases": [
            {"phase": 1, "time": "April 2, 1972 (11:30)", "title": "Battle of Dong Ha Bridge — ARVN M48A3 Pattons Ambush NVA 203rd Armored Regt at 2,800m", "desc": "As PAVN T-54 and PT-76 tanks roll down Highway 1 toward Dong Ha Bridge, Lt. Col. Nguyen Trong Luat's ARVN 20th Tank Regiment M48A3 Pattons open fire from hull-down ridge positions at 2,500–2,800m, knocking out 9 T-54s and 2 PT-76s with zero M48 losses before Capt. John Ripley blows the bridge.", "lost_a_pct": 0.05, "lost_b_pct": 0.16, "focus_event": "Dong Ha Ridge Snipe: 11 NVA Tanks Destroyed at 2,800m"},
            {"phase": 2, "time": "April 13 – May 11, 1972", "title": "Siege of An Loc — NVA T-54s & Type 59s Roll Into the Streets Without Infantry", "desc": "Over 40 PAVN T-54, Type 59, and PT-76 tanks breach An Loc from the north, but their supporting infantry is stripped away by artillery and B-52 strikes. Blinded inside the town, NVA tanks are hunted block-by-block by ARVN soldiers with M72 LAWs.", "lost_a_pct": 0.35, "lost_b_pct": 0.52, "focus_event": "An Loc Urban Tank Trap — 30+ T-54s Knocked Out in Streets"},
            {"phase": 3, "time": "April 27–30, 1972", "title": "First Combat Use of AT-3 Sagger vs M48A3s at Dong Ha", "desc": "PAVN fires 9M14 Malyutka (Sagger) wire-guided missiles in combat for the first time, knocking out several M48A3s, while surviving ARVN Pattons destroy another 15+ NVA T-54s in fierce close-range duels.", "lost_a_pct": 0.72, "lost_b_pct": 0.72, "focus_event": "First Sagger ATGM vs M48A3 Tank Duel"},
            {"phase": 4, "time": "May 14–28, 1972", "title": "Battle of Kontum — First Combat Debut of the BGM-71 TOW Missile", "desc": "In the Central Highlands at Kontum, two experimental US Army UH-1B Hueys fitted with XM26 BGM-71 TOW missiles and ARVN M41/M48 tanks smash a two-regiment NVA T-54 assault, destroying 24+ NVA tanks from the air.", "lost_a_pct": 0.90, "lost_b_pct": 0.90, "focus_event": "BGM-71 TOW Debut Destroys 24 NVA Tanks at Kontum"},
            {"phase": 5, "time": "June 1972", "title": "Easter Offensive Contained — Over 250 NVA Tanks Destroyed Across 3 Fronts", "desc": "An Loc and Kontum hold firm and ARVN counterattacks recapture Quang Tri Citadel; PAVN loses over 250 tanks and learns combined-arms lessons that shape the 1975 campaign.", "lost_a_pct": 1.0, "lost_b_pct": 1.0, "focus_event": "250+ NVA Tanks Destroyed — An Loc & Kontum Held"}
        ]
    }
}

def generate_default_forensics(b):
    """Generates historically grounded 5-phase timeline & forensic destruction breakdown for any battle not manually overridden."""
    bid = b["id"]
    if bid in BATTLE_FORENSICS:
        return BATTLE_FORENSICS[bid]

    # Parse approximate numeric tank counts from strings
    import re
    def extract_num(s, default_val):
        nums = [int(x.replace(",", "")) for x in re.findall(r"\d[\d,]*", str(s))]
        # Pick largest plausible tank count (< 10000, not a year like 1943 unless it's the only number)
        non_years = [n for n in nums if not (1914 <= n <= 2026)]
        if non_years:
            return max(non_years)
        return default_val

    num_a = extract_num(b["side_a"]["count"], 250)
    num_b = extract_num(b["side_b"]["count"], 250)
    lost_a = extract_num(b.get("losses_a", ""), int(num_a * (0.25 if b.get("winner_side") == "A" else 0.68)))
    lost_b = extract_num(b.get("losses_b", ""), int(num_b * (0.72 if b.get("winner_side") == "A" else 0.30)))
    lost_a = min(num_a, max(1, lost_a))
    lost_b = min(num_b, max(1, lost_b))

    year = b["year"]
    if year <= 1918:
        da = [
            {"cause": "Direct 77mm Field Artillery & 57mm Tank/Fortress Fire", "pct": 54, "count": b.get("losses_a", "Primary Combat Losses"), "color": "#f43f5e", "detail": "Thin 12–16mm riveted boiler-plate armor penetrated by direct-fire German 77mm FK 96 field guns, 57mm Maxim-Nordenfelt cannons, and K-bullet armor-piercing rifle fire."},
            {"cause": "Mechanical Breakdown, Trench Bogging & Mud Immobilization", "pct": 34, "count": "Ditched / Mechanical Losses", "color": "#f59e0b", "detail": "Early unsprung rhomboid hulls and overloaded transmissions broke down or bellied out across deep Hindenburg Line trenches and shell craters."},
            {"cause": "Internal Fuel Fire & Bundled Grenade Demolition", "pct": 12, "count": "Close-Assault Losses", "color": "#a855f7", "detail": "Internal gravity-fed petrol tanks ignited or tracks blown by stormtrooper Geballte Ladung bundled grenades."}
        ]
        db = [
            {"cause": "6-Pounder (57mm) Male Tank & Artillery Direct Hits", "pct": 65, "count": b.get("losses_b", "Armor Losses"), "color": "#38bdf8", "detail": "Hit by British 57mm 6-pounder sponson guns and concentrated field artillery barrages."},
            {"cause": "Chassis Rollover / Engine Overheating & Abandonment", "pct": 35, "count": "Terrain / Mechanical Losses", "color": "#f59e0b", "detail": "High center of gravity and short Holt bogie tracks caused bogging in cratered no-man's-land, forcing crew demolition."}
        ]
    elif year <= 1945:
        da = [
            {"cause": "High-Velocity Tank Gun AP / APCR Penetrations (75mm / 88mm / 50mm)", "pct": 56, "count": "Primary Tank-on-Tank Kills", "color": "#f43f5e", "detail": f"Direct kinetic penetrations across {b['tactical_zoom']['range_m']} engagement envelopes, igniting internal ammunition racks and fuel."},
            {"cause": "Towed Anti-Tank Pakfronts (88mm Flak / 75mm Pak 40) & Minefields", "pct": 28, "count": "AT Screen & Mine Losses", "color": "#f59e0b", "detail": "Camouflaged anti-tank gun belts and Tellermine/TM-35 minefields blew off tracks first, leaving immobilized tanks exposed to flank shots."},
            {"cause": "Fuel/Ammo Exhaustion, Air Interdiction & Mechanical Breakdown", "pct": 16, "count": "Operational Attrition", "color": "#a855f7", "detail": "Cut-off spearheads and final-drive/transmission failures under combat maneuver stress."}
        ]
        db = [
            {"cause": "Allied/Soviet Tank & Tank Destroyer AP/HVAP/APDS Fire", "pct": 58, "count": "Direct Tank Duel Kills", "color": "#38bdf8", "detail": f"Flanking maneuvers and concentrated volley fire penetrated hull sides and turret mantlets ({b['losses_b']})."},
            {"cause": "Artillery Barrages, Close-Support Aircraft & Anti-Tank Guns", "pct": 24, "count": "Combined-Arms Kills", "color": "#10b981", "detail": "Heavy artillery concentrations, anti-tank guns, and rocket/bomb strikes shattered tracks and engine decks."},
            {"cause": "Fuel Starvation & Final-Drive Breakdowns (Scuttled by Crews)", "pct": 18, "count": "Logistical / Mechanical Losses", "color": "#f59e0b", "detail": "Heavy tanks running dry of fuel or suffering transmission failures during retreat were blown up by their own crews."}
        ]
    elif year <= 1975:
        da = [
            {"cause": "High-Velocity 90mm / 100mm / 105mm APDS & HEAT Tank Duels", "pct": 55, "count": "Tank-on-Tank Gun Kills", "color": "#f43f5e", "detail": f"Long-range optical rangefinder and stabilized gun duels across {b['tactical_zoom']['range_m']} ({b['losses_a']})."},
            {"cause": "Early ATGMs (Sagger / TOW), RPG-7 / M72 LAW & Recoilless Rifles", "pct": 30, "count": "Infantry & Missile Ambush Kills", "color": "#f59e0b", "detail": "Shaped-charge warheads from infantry ambushes, wire-guided ATGMs, and recoilless rifles."},
            {"cause": "Anti-Tank Mines, Air Strikes & Terrain Bogging", "pct": 15, "count": "Mine & Air Losses", "color": "#a855f7", "detail": "Heavy anti-tank mines, close air support (napalm/CBU/cluster), and river/jungle/sand immobilization."}
        ]
        db = [
            {"cause": "Precision 90mm / 105mm L7 / 20-pdr Hull-Down Tank Gunnery", "pct": 62, "count": "Primary Tank Duel Kills", "color": "#38bdf8", "detail": f"Superior gun depression (-10°), APDS/HEAT velocity, and optical fire control destroyed advancing columns ({b['losses_b']})."},
            {"cause": "BGM-71 TOW Missiles, Tactical Airpower & M72 LAW / RPG Teams", "pct": 26, "count": "Air & Missile Kills", "color": "#10b981", "detail": "Guided anti-tank missiles and close air support devastated road-bound armor formations."},
            {"cause": "Fuel/Ammo Cut-Off & Crew Abandonment Under Fire", "pct": 12, "count": "Captured / Abandoned", "color": "#f59e0b", "detail": "Spearheads isolated from supply echelons or trapped inside kill sacks."}
        ]
    else:
        da = [
            {"cause": "120mm / 125mm APFSDS Long-Rod Kinetic Penetrators", "pct": 42, "count": "Direct Tank Fire Losses", "color": "#f43f5e", "detail": "Fin-stabilized tungsten/DU darts fired at 1,500–1,750 m/s using thermal sights and laser rangefinders."},
            {"cause": "Top-Attack ATGMs (Javelin/TOW-2B/Kornet) & FPV Loitering Drones", "pct": 38, "count": "Precision Missile & Drone Kills", "color": "#f59e0b", "detail": "Tandem-warhead missiles and FPV strike drones targeting thinner turret roof and engine deck armor."},
            {"cause": "Dense Anti-Tank Minefields (TM-62) & Precision Artillery", "pct": 20, "count": "Mine & Artillery Immobilizations", "color": "#a855f7", "detail": "Mobility kills (M-Kills) from stacked anti-tank mines followed by artillery or drone finish-offs."}
        ]
        db = [
            {"cause": "Long-Range 120mm / 125mm Thermal-Sighted APFSDS Duels", "pct": 58, "count": "Tank & IFV Kills", "color": "#38bdf8", "detail": f"FLIR thermal optics and stabilized fire control achieved first-round hits through dust, smoke, and night ({b['losses_b']})."},
            {"cause": "Autoloader Carousel Cook-Offs from ATGM / Drone / Sabot Hits", "pct": 28, "count": "Catastrophic Hull/Turret Losses", "color": "#f43f5e", "detail": "Penetration of hull ammo carousels triggered sympathetic propellant detonation ('turret toss')."},
            {"cause": "Minefield Breaching & Air/Artillery Interdiction", "pct": 14, "count": "Breaching & Air Losses", "color": "#f59e0b", "detail": "Immobilized in contested grey-zone minefields and abandoned by crews."}
        ]

    phases = [
        {
            "phase": 1,
            "time": "Phase 1 (00%–20%) — Reconnaissance & Approach March",
            "title": f"Opening Contact & Deployment at {b['location']}",
            "desc": f"{b['side_a']['name']} ({b['side_a']['count']}) and {b['side_b']['name']} ({b['side_b']['count']}) deploy into {b['tactical_zoom']['terrain']}. Vanguard recon platoons establish contact.",
            "lost_a_pct": 0.08,
            "lost_b_pct": 0.08,
            "focus_event": "Vanguard Recon Contact & Deployment"
        },
        {
            "phase": 2,
            "time": "Phase 2 (20%–45%) — Long-Range Gunnery & First Wave Clash",
            "title": f"Long-Range Firefight Opens Across {b['tactical_zoom']['range_m']}",
            "desc": f"Main armor formations open fire at {b['tactical_zoom']['range_m']}. Long-range guns and hull-down batteries test frontal glacis armor while flanking squadrons maneuver for side shots.",
            "lost_a_pct": 0.32,
            "lost_b_pct": 0.35,
            "focus_event": f"Main Gun Exchange at {b['tactical_zoom']['range_m']}"
        },
        {
            "phase": 3,
            "time": "Phase 3 (45%–70%) — Climax Maneuver, Flank Hook & Close Brawl",
            "title": "Decisive Armored Thrust & Kill-Sack Engagement",
            "desc": f"Both sides commit their heavy reserves. {b['tactical_zoom']['key_lesson']}",
            "lost_a_pct": 0.68,
            "lost_b_pct": 0.72,
            "focus_event": "Peak Attrition & Flanking Envelopment"
        },
        {
            "phase": 4,
            "time": "Phase 4 (70%–90%) — Breakthrough & Collapse of Defeated Wing",
            "title": f"{b['winner']} Shatters Opposing Armor Line",
            "desc": f"Cumulative tank losses ({b['losses_b'] if b.get('winner_side')=='A' else b['losses_a']}) and ammunition/fuel depletion force the losing side's formations to fracture.",
            "lost_a_pct": 0.90,
            "lost_b_pct": 0.92,
            "focus_event": "Defensive Line Fractures — Heavy Losses"
        },
        {
            "phase": 5,
            "time": "Phase 5 (90%–100%) — Final Outcome & Battlefield Aftermath",
            "title": f"Outcome: {b['outcome']}",
            "desc": f"Final tally: Side A Losses: {b['losses_a']} | Side B Losses: {b['losses_b']}.",
            "lost_a_pct": 1.0,
            "lost_b_pct": 1.0,
            "focus_event": f"Battle Concluded — {b['winner']}"
        }
    ]

    return {
        "total_tanks": b["total_tanks"],
        "numeric_a": num_a,
        "numeric_b": num_b,
        "numeric_lost_a": lost_a,
        "numeric_lost_b": lost_b,
        "side_a_count": b["side_a"]["count"],
        "side_b_count": b["side_b"]["count"],
        "losses_a": b["losses_a"],
        "losses_b": b["losses_b"],
        "destruction_a": da,
        "destruction_b": db,
        "phases": phases
    }

BATTLE_REAL_MAPS_AND_WRECKAGE = {
    "raseiniai_1941": {
        "real_map_url": "https://upload.wikimedia.org/wikipedia/commons/d/d8/Battle_of_Raseiniai_Battle_Map.jpg",
        "real_map_alt_url": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Battle_of_Raseiniai.png",
        "real_map_caption": "Official Historical Operational Map of the Battle of Raseiniai (June 23–27, 1941): German XLI Panzer Corps (6th & 1st Panzer Divisions) crossing the Dubysa River vs. Soviet 3rd & 12th Mechanized Corps (749 Soviet vs. 245 German tanks).",
        "map_zoom": 11,
        "wreckage_photos": [
            {
                "url": "https://upload.wikimedia.org/wikipedia/commons/f/fc/The_Germans_inspect_the_damaged_Soviet_KV-2_near_Raseiniai_during_the_World_War_II.jpg",
                "title": "Knocked-Out Soviet KV-2 Heavy Tank Near Raseiniai (June 1941)",
                "how_destroyed": "Withstood dozens of 37mm Pak 36 and 50mm KwK 38 hits before being penetrated by horizontal 88mm Flak 36 APBC fire and finished by German pioneer satchel charges on the turret ring."
            },
            {
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/68/Bundesarchiv_Bild_101I-209-0091-11%2C_Russland-Nord%2C_russischer_Panzer_KW-2.jpg",
                "title": "Bundesarchiv: Destroyed 52-Ton KV-2 of 2nd Tank Division (Baltic Sector, June 1941)",
                "how_destroyed": "Immobilized after running out of fuel and 152mm ammunition inside the Raseiniai pocket; internal demolition charge detonated by crew."
            },
            {
                "url": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Kowno_Panzerschlacht_1941_01_%28RaBoe%29.jpg",
                "title": "Catastrophic Ammunition Cook-Off in the Raseiniai–Kaunas Panzer Battle (June 1941)",
                "how_destroyed": "50mm PzGr.39 AP shell pierced the thin 15–22mm hull armor, igniting stowed 45mm ammunition and aviation gasoline, blowing the turret and hull roof apart."
            },
            {
                "url": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Bundesarchiv_Bild_101I-020-1268-36%2C_Russland%2C_russischer_Gefallener%2C_Panzer_BT_7%2C.jpg",
                "title": "Burned-Out Soviet BT-7 Fast Tank (12th Mechanized Corps, June 1941)",
                "how_destroyed": "Struck in the flank by 37mm KwK 38(t) / 50mm Panzer III crossfire during 1st Panzer Division's Kelmė hook; M-17T gasoline engine erupted in flames."
            }
        ],
        "combat_videos": [
            {
                "title": "WWII Anti-Tank & Armor Penetration Footage ('Crack That Tank' 1943 Archival Film)",
                "source": "U.S. War Department / Wikimedia Commons Public Domain Film",
                "video_url": "https://upload.wikimedia.org/wikipedia/commons/7/77/%22CRACK_THAT_TANK%22_RESTRICTED_WWII_INFANTRY_TRAINING_FILM_1943_ANTI-TANK_WARFARE.webm",
                "yt_url": "https://www.youtube.com/results?search_query=Battle+of+Raseiniai+1941+KV-1+KV-2+lone+tank+documentary"
            },
            {
                "title": "Soviet T-34 & Heavy Armor Live Mobility & Firing Footage",
                "source": "Wikimedia Commons Armor Archive",
                "video_url": "https://upload.wikimedia.org/wikipedia/commons/6/6c/T-34-85_tanks_in_Alabino_%2831-03-2020%29.webm",
                "yt_url": "https://www.youtube.com/results?search_query=Raseiniai+1941+900+tanks+Eastern+Front+animated+map"
            }
        ],
        "killcam_scenarios": [
            {
                "id": "raseiniai_88mm_kv",
                "title": "88mm Flak 36 Direct Fire vs. Lone KV-1/KV-2 at Raseiniai Crossroads",
                "attacker": "8.8cm Flak 18/36 & Pz.38(t) (Kampfgruppe Raus)",
                "defender": "KV-2 / KV-1 Heavy Tank (2nd Tank Div)",
                "attacker_id": "pz_38t",
                "defender_id": "kv2",
                "shell": "88mm PzGr.39 APBC (810 m/s, 10.2 kg)",
                "pen_mm": 110,
                "armor_mm": 75,
                "result": "CATASTROPHIC PENETRATION & AMMO COOK-OFF",
                "turret_blow": True,
                "desc": "After 37mm and 50mm AT guns bounced harmlessly off the KV's 75–90mm armor for 26 hours, two 88mm Flak guns crept within 600m while Panzer 38(t)s distracted the crew. Six 88mm APBC rounds smashed into the turret ring and hull side, penetrating the 75mm plate and detonating internal charges."
            },
            {
                "id": "raseiniai_37mm_ricochet",
                "title": "37mm Pak 36 & Pz.38(t) vs. KV-1 Frontal Glacis (June 23–24)",
                "attacker": "Panzer 38(t) & 3.7cm Pak 36 Battery",
                "defender": "KV-1 Model 1940 (90mm Frontal Armor)",
                "attacker_id": "pz_38t",
                "defender_id": "kv1",
                "shell": "37mm PzGr.18 AP (762 m/s) / 50mm PzGr.38",
                "pen_mm": 38,
                "armor_mm": 90,
                "result": "RICOCHET",
                "turret_blow": False,
                "desc": "German gunners scored 14 direct hits at 200–400m on advancing 2nd Tank Division KV-1s. With only 38–55mm penetration against 90mm of Soviet rolled homogeneous armor, every shell shattered or ricocheted into the sky before the 45-ton KV-1s crushed the guns under their tracks."
            },
            {
                "id": "raseiniai_bt7_cookoff",
                "title": "50mm Panzer III & 37mm Panzer 38(t) Crossfire vs. BT-7 & T-26 (~430 Lost)",
                "attacker": "Panzer III Ausf. H (5cm KwK 38)",
                "defender": "BT-7 / T-26 Light Tank (15–22mm Armor)",
                "attacker_id": "panzer_iii",
                "defender_id": "bt7",
                "shell": "50mm PzGr.39 APHE (685 m/s)",
                "pen_mm": 62,
                "armor_mm": 20,
                "result": "HULL OVERMATCH, GASOLINE FIRE & TURRET BLOW-OFF",
                "turret_blow": True,
                "desc": "Over 80% of the Soviet 3rd and 12th Mechanized Corps consisted of thin-skinned BT-7 (22mm) and T-26 (15mm) light tanks powered by volatile aviation gasoline. German 37mm and 50mm APHE shells easily overmatched their hulls at 800m, igniting fuel tanks and 45mm ammo racks in seconds."
            },
            {
                "id": "raseiniai_pioneer_satchel",
                "title": "Panzer IV 75mm & Pioneer Satchel Charge Assault on KV Tracks & Engine",
                "attacker": "Panzer IV Ausf. E & Combat Pioneers (6kg TNT)",
                "defender": "KV-1 / KV-2 Heavy Tank",
                "attacker_id": "panzer_iv",
                "defender_id": "kv1",
                "shell": "6kg Bundled TNT Satchel & 75mm KwK 37 HEAT",
                "pen_mm": 85,
                "armor_mm": 40,
                "result": "TRACKS BLOWN OFF & ENGINE LOUVERS SHATTERED",
                "turret_blow": False,
                "desc": "Unable to pierce the KV frontal armor with tank guns, German pioneers crawled onto the tanks at night to plant demolition charges on the tracks, gun barrel, and 30–40mm rear engine louvers, immobilizing 18 KV heavy tanks."
            }
        ]
    },
    "kursk_1943": {
        "real_map_url": "https://upload.wikimedia.org/wikipedia/commons/6/65/Prokhorovka%2C_Battle_of_Kursk%2C_night_11_July.png",
        "real_map_alt_url": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Battle_of_Kursk_%28map%29.jpg",
        "real_map_caption": "Official Operational Map of the Battle of Prokhorovka / Kursk Southern Sector (July 11–12, 1943): 5th Guards Tank Army charging II SS-Panzer Corps in the narrow corridor between the Psel River and the railway.",
        "map_zoom": 12,
        "wreckage_photos": [
            {
                "url": "https://upload.wikimedia.org/wikipedia/commons/9/93/Bundesarchiv_Bild_101I-219-0553A-36%2C_Russland%2C_bei_Pokrowka%2C_russischer_Panzer_T34.jpg",
                "title": "Bundesarchiv: Knocked-Out Soviet T-34/76 near Prokhorovka (July 1943)",
                "how_destroyed": "Struck at 1,200m by an 88mm KwK 36 shell from a Tiger I while charging across the open steppe toward Hill 252.2; hull penetrated and burned out."
            },
            {
                "url": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Bundesarchiv_B_145_Bild-F016199-10%2C_Zerst%C3%B6rter_sowjetischer_Panzer.jpg",
                "title": "Catastrophic Turret Blow-Off after Internal 76.2mm Ammo Detonation",
                "how_destroyed": "75mm KwK 40 L/48 APCR round penetrated the T-34 hull side above the Christie suspension rollers, detonating floor ammunition bins and hurling the turret meters away."
            }
        ],
        "combat_videos": [
            {
                "title": "T-34 Tank Live Mobility & Firing Demonstration",
                "source": "Wikimedia Commons Armor Archive",
                "video_url": "https://upload.wikimedia.org/wikipedia/commons/6/6c/T-34-85_tanks_in_Alabino_%2831-03-2020%29.webm",
                "yt_url": "https://www.youtube.com/results?search_query=Battle+of+Prokhorovka+Kursk+1943+tank+battle+documentary"
            },
            {
                "title": "WWII Anti-Tank Warfare & Armor Penetration Archival Film (1943)",
                "source": "Wikimedia Commons Public Domain Film",
                "video_url": "https://upload.wikimedia.org/wikipedia/commons/7/77/%22CRACK_THAT_TANK%22_RESTRICTED_WWII_INFANTRY_TRAINING_FILM_1943_ANTI-TANK_WARFARE.webm",
                "yt_url": "https://www.youtube.com/results?search_query=Kursk+1943+Tiger+vs+T-34+combat+footage"
            }
        ]
    }
}

DEFAULT_BATTLE_MAPS = {
    "cambrai_1917": ("https://upload.wikimedia.org/wikipedia/commons/4/4e/Battle_of_cambrai_1_-_front_lines.png", "https://upload.wikimedia.org/wikipedia/commons/4/4d/Bundesarchiv_Bild_104-0941A%2C_Bei_Cambrai%2C_zerst%C3%B6rter_englischer_Panzer_Mark_I.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9b/Tanks_of_WWI.ogv"),
    "villers_bretonneux_1918": ("https://upload.wikimedia.org/wikipedia/commons/0/04/Battle_of_Amiens_Hundred_Days_Offensive.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c4/Bundesarchiv_Bild_146-1998-098-10%2C_Bei_Cambrai%2C_erbeuteter_englischer_Panzer.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9b/Tanks_of_WWI.ogv"),
    "khalkhin_gol_1939": ("https://upload.wikimedia.org/wikipedia/commons/5/57/Battle_of_Khalkhin_Gol-Japanese_soldiers_and_captured_Soviet_AFVs.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/57/Battle_of_Khalkhin_Gol-Japanese_soldiers_and_captured_Soviet_AFVs.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/77/%22CRACK_THAT_TANK%22_RESTRICTED_WWII_INFANTRY_TRAINING_FILM_1943_ANTI-TANK_WARFARE.webm"),
    "hannut_1940": ("https://upload.wikimedia.org/wikipedia/commons/b/b5/16May-21May_Battle_of_Belgium.PNG", "https://upload.wikimedia.org/wikipedia/commons/a/aa/Battle_of_Arras_%2821_May_1940%29.png", "https://upload.wikimedia.org/wikipedia/commons/7/77/%22CRACK_THAT_TANK%22_RESTRICTED_WWII_INFANTRY_TRAINING_FILM_1943_ANTI-TANK_WARFARE.webm"),
    "arras_1940": ("https://upload.wikimedia.org/wikipedia/commons/a/aa/Battle_of_Arras_%2821_May_1940%29.png", "https://upload.wikimedia.org/wikipedia/commons/b/b5/16May-21May_Battle_of_Belgium.PNG", "https://upload.wikimedia.org/wikipedia/commons/7/77/%22CRACK_THAT_TANK%22_RESTRICTED_WWII_INFANTRY_TRAINING_FILM_1943_ANTI-TANK_WARFARE.webm"),
    "brody_1941": ("https://upload.wikimedia.org/wikipedia/commons/1/11/Battle_of_Dubno.svg", "https://upload.wikimedia.org/wikipedia/commons/4/4a/Bundesarchiv_B_145_Bild-F016199-10%2C_Zerst%C3%B6rter_sowjetischer_Panzer.jpg", "https://upload.wikimedia.org/wikipedia/commons/7/77/%22CRACK_THAT_TANK%22_RESTRICTED_WWII_INFANTRY_TRAINING_FILM_1943_ANTI-TANK_WARFARE.webm"),
    "el_alamein_1942": ("https://upload.wikimedia.org/wikipedia/commons/0/01/2_Battle_of_El_Alamein_001.png", "https://upload.wikimedia.org/wikipedia/commons/3/3e/2_Battle_of_El_Alamein_002.png", "https://upload.wikimedia.org/wikipedia/commons/4/45/Fury_Tank_tankfest_2021.webm"),
    "normandy_1944": ("https://upload.wikimedia.org/wikipedia/commons/7/7b/Tanksgoodwood.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9d/Turretless_King_Tiger_Normandy.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/45/Fury_Tank_tankfest_2021.webm"),
    "arracourt_1944": ("https://upload.wikimedia.org/wikipedia/commons/4/48/Arracourt_%28M-et-M%29_tank_%2801%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9d/Turretless_King_Tiger_Normandy.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/45/Fury_Tank_tankfest_2021.webm"),
    "bulge_1944": ("https://upload.wikimedia.org/wikipedia/commons/5/50/Wacht_am_Rhein_map_%28Opaque%29.svg", "https://upload.wikimedia.org/wikipedia/commons/a/a2/Destroyed_German_Tiger_II_tank_at_Moinet%2C_Belgium%2C_23_January_1945_%28111-SC-199473%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/4/45/Fury_Tank_tankfest_2021.webm"),
    "balaton_1945": ("https://upload.wikimedia.org/wikipedia/commons/9/97/Plattensee-op.png", "https://upload.wikimedia.org/wikipedia/commons/a/a2/Destroyed_German_Tiger_II_tank_at_Moinet%2C_Belgium%2C_23_January_1945_%28111-SC-199473%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/6c/T-34-85_tanks_in_Alabino_%2831-03-2020%29.webm"),
    "lang_vei_ben_het_1968": ("https://upload.wikimedia.org/wikipedia/commons/a/af/Destroyed_PT76_tank_at_Ben_Het.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/05/PT-76_monument.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/1c/M48_Patton.webm"),
    "an_loc_dong_ha_1972": ("https://upload.wikimedia.org/wikipedia/commons/7/7f/1975_Spring_offensive.svg", "https://upload.wikimedia.org/wikipedia/commons/2/29/An_Loc2.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/1c/M48_Patton.webm"),
    "xuan_loc_saigon_1975": ("https://upload.wikimedia.org/wikipedia/commons/7/7f/1975_Spring_offensive.svg", "https://upload.wikimedia.org/wikipedia/commons/2/29/An_Loc2.jpg", "https://upload.wikimedia.org/wikipedia/commons/1/1c/M48_Patton.webm"),
    "valley_of_tears_1973": ("https://upload.wikimedia.org/wikipedia/commons/3/35/Destroyed_Syrian_T-62_with_Fallen_Crew_Member_Somewhere_in_the_Golan_Sector%2C_Yom_Kippur_War%2C_8_October_1973.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/35/Destroyed_Syrian_T-62_with_Fallen_Crew_Member_Somewhere_in_the_Golan_Sector%2C_Yom_Kippur_War%2C_8_October_1973.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/55/Tank_museum%2C_Latrun._Part_3.webm"),
    "chinese_farm_1973": ("https://upload.wikimedia.org/wikipedia/commons/0/03/Destroyed_tank_of_the_Egyptian_army_on_the_Sinai%2C_1973_%282%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/03/Destroyed_tank_of_the_Egyptian_army_on_the_Sinai%2C_1973_%282%29.jpg", "https://upload.wikimedia.org/wikipedia/commons/5/55/Tank_museum%2C_Latrun._Part_3.webm"),
    "easting_1991": ("https://upload.wikimedia.org/wikipedia/commons/0/03/Type_69_Operation_Desert_Storm.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c7/T-72_tank_of_the_Iraqi_army%2C_destroyed_by_Coalition_forces_during_Gulf_war%2C_1991.jpg", "https://upload.wikimedia.org/wikipedia/commons/b/b8/M1A2_Abrams_tank_B12_%28%22Leeroy_Jenkins%22%29_shooting_live_fire_at_NTC_at_night_%28January_2023%29.webm"),
    "baghdad_2003": ("https://upload.wikimedia.org/wikipedia/commons/c/c3/An_Iraqi_T-72_main_battle_tank_destroyed_in_southern_Iraq_during_Operation_Desert_Storm_DA-ST-92-08908.jpg", "https://upload.wikimedia.org/wikipedia/commons/6/6c/Destroyed_Iraqi_T-72_tank_during_the_Gulf_War.JPEG", "https://upload.wikimedia.org/wikipedia/commons/a/a7/Australian_M1_Abrams_tank_conducting_target_practice_in_May_2017.webm"),
    "ukraine_2022_2024": ("https://upload.wikimedia.org/wikipedia/commons/0/0b/Vuhledar_%282024-09-25%29_01.jpg", "https://upload.wikimedia.org/wikipedia/commons/c/c7/T-72_tank_of_the_Iraqi_army%2C_destroyed_by_Coalition_forces_during_Gulf_war%2C_1991.jpg", "https://upload.wikimedia.org/wikipedia/commons/0/0b/K2_Black_Panther_tank_firing_while_maneuvering.webm")
}

def enrich_all_battles_with_forensics(battles):
    for b in battles:
        f = generate_default_forensics(b)
        b["total_tanks"] = f["total_tanks"]
        b["side_a"]["count"] = f["side_a_count"]
        b["side_b"]["count"] = f["side_b_count"]
        b["losses_a"] = f["losses_a"]
        b["losses_b"] = f["losses_b"]
        b["numeric_a"] = f["numeric_a"]
        b["numeric_b"] = f["numeric_b"]
        b["numeric_lost_a"] = f["numeric_lost_a"]
        b["numeric_lost_b"] = f["numeric_lost_b"]
        b["side_a_num"] = f["numeric_a"]
        b["side_b_num"] = f["numeric_b"]
        b["loss_a_num"] = f["numeric_lost_a"]
        b["loss_b_num"] = f["numeric_lost_b"]
        b["destruction_a"] = f["destruction_a"]
        b["destruction_b"] = f["destruction_b"]

        raw_phases = f["phases"]
        n_ph = max(1, len(raw_phases))
        # Phases whose own text describes night fighting (1-based): the simulator darkens them
        NIGHT_PHASES = {
            ("lang_vei_ben_het_1968", 2), ("lang_vei_ben_het_1968", 4),  # night jungle gunnery; Ben Het night tank duel
            ("chinese_farm_1973", 2), ("chinese_farm_1973", 5),          # night tank-and-ATGM melee
            ("valley_of_tears_1973", 2),                                 # pitch-black night brawls
            ("balaton_1945", 3),                                         # infrared night-vision sights
            ("sinai_1967", 5),                                           # night combined-arms assault
        }
        norm_phases = []
        for idx, ph in enumerate(raw_phases):
            ph_copy = dict(ph)
            if isinstance(ph_copy.get("phase"), int):
                ph_copy["phase"] = f"Phase {ph_copy['phase']}"
            elif not ph_copy.get("phase"):
                ph_copy["phase"] = f"Phase {idx + 1}"
            if "range" not in ph_copy or not isinstance(ph_copy["range"], list):
                ph_copy["range"] = [round(idx / n_ph, 2), round((idx + 1) / n_ph, 2)]
            if "losses_note" not in ph_copy or not ph_copy["losses_note"]:
                la = int(round(f["numeric_lost_a"] * ph_copy.get("lost_a_pct", (idx + 1) / n_ph)))
                lb = int(round(f["numeric_lost_b"] * ph_copy.get("lost_b_pct", (idx + 1) / n_ph)))
                fe = ph_copy.get("focus_event", "Armored engagement")
                ph_copy["losses_note"] = f"{fe} · Losses so far: {la} vs {lb}"
            ph_copy["night"] = (b["id"], idx + 1) in NIGHT_PHASES
            norm_phases.append(ph_copy)
        b["phases"] = norm_phases

        bid = b["id"]
        if bid in BATTLE_REAL_MAPS_AND_WRECKAGE:
            mw = BATTLE_REAL_MAPS_AND_WRECKAGE[bid]
            b["real_map_url"] = mw["real_map_url"]
            b["real_map_alt_url"] = mw["real_map_alt_url"]
            b["real_map_caption"] = mw["real_map_caption"]
            b["map_zoom"] = mw.get("map_zoom", 11)
            b["wreckage_photos"] = mw["wreckage_photos"]
            b["combat_videos"] = mw["combat_videos"]
            b["killcam_scenarios"] = mw.get("killcam_scenarios")
        else:
            m_url, w_url, v_url = DEFAULT_BATTLE_MAPS.get(
                bid,
                (
                    "https://upload.wikimedia.org/wikipedia/commons/d/d8/Battle_of_Raseiniai_Battle_Map.jpg",
                    "https://upload.wikimedia.org/wikipedia/commons/4/4a/Bundesarchiv_B_145_Bild-F016199-10%2C_Zerst%C3%B6rter_sowjetischer_Panzer.jpg",
                    "https://upload.wikimedia.org/wikipedia/commons/7/77/%22CRACK_THAT_TANK%22_RESTRICTED_WWII_INFANTRY_TRAINING_FILM_1943_ANTI-TANK_WARFARE.webm"
                )
            )
            b["real_map_url"] = m_url
            b["real_map_alt_url"] = w_url
            b["real_map_caption"] = f"Archival Operational Map & Battlefield Reconnaissance: {b['name']} ({b['date']}) at {b['location']}."
            b["map_zoom"] = 11
            b["wreckage_photos"] = [
                {
                    "url": w_url,
                    "title": f"Knocked-Out Armor Wreckage — {b['name']} ({b['year']})",
                    "how_destroyed": b["destruction_a"][0]["detail"] if b.get("destruction_a") else "Penetrated by direct armor-piercing fire and internal ammunition detonation."
                },
                {
                    "url": m_url,
                    "title": f"Archival Battle Map & Tactical Sector — {b['location']}",
                    "how_destroyed": b["destruction_b"][0]["detail"] if b.get("destruction_b") else "Knocked out during armored counter-offensive maneuvers."
                }
            ]
            q_b = b["name"].replace(" ", "+")
            b["combat_videos"] = [
                {
                    "title": f"Archival Tank Combat & Anti-Armor Footage: {b['name']}",
                    "source": "Wikimedia Commons Public Domain Military Film",
                    "video_url": v_url,
                    "yt_url": f"https://www.youtube.com/results?search_query={q_b}+tank+battle+combat+footage+documentary"
                }
            ]

        if not b.get("killcam_scenarios"):
            da0 = b["destruction_a"][0] if b.get("destruction_a") else {"cause": "Direct AP Penetration", "detail": "High-velocity armor-piercing shell penetrated the hull and ignited stowed ammunition."}
            db0 = b["destruction_b"][0] if b.get("destruction_b") else {"cause": "Counter-Battery Tank Fire", "detail": "Flanking fire penetrated turret side armor."}
            tid_a = b["side_a"]["tanks"][0] if b["side_a"].get("tanks") else "t34_76"
            tid_b = b["side_b"]["tanks"][0] if b["side_b"].get("tanks") else "panzer_iv"
            b["killcam_scenarios"] = [
                {
                    "id": f"{bid}_kill_1",
                    "title": f"{b['side_b']['name']} Fire vs. {b['side_a']['name']} ({da0['cause']})",
                    "attacker": b["side_b"]["name"],
                    "defender": b["side_a"]["name"],
                    "attacker_id": tid_b,
                    "defender_id": tid_a,
                    "shell": da0["cause"],
                    "pen_mm": 125,
                    "armor_mm": 80,
                    "result": "ARMOR PENETRATION & INTERNAL AMMO COOK-OFF",
                    "turret_blow": True,
                    "desc": da0["detail"]
                },
                {
                    "id": f"{bid}_kill_2",
                    "title": f"{b['side_a']['name']} Fire vs. {b['side_b']['name']} ({db0['cause']})",
                    "attacker": b["side_a"]["name"],
                    "defender": b["side_b"]["name"],
                    "attacker_id": tid_a,
                    "defender_id": tid_b,
                    "shell": db0["cause"],
                    "pen_mm": 110,
                    "armor_mm": 70,
                    "result": "HULL BREACH & FUEL / PROPELLANT DETONATION",
                    "turret_blow": False,
                    "desc": db0["detail"]
                }
            ]
    return battles

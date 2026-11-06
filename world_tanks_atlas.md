# Global Tank Lineage, Similarity & Combat Atlas (1916–2026) — v2 Complete Edition

## File Locations
- **Workspace Interactive Web App**: `/Users/tuandinh/Scifi/world-tank-atlas/world_tanks_atlas.html`
- **Artifact Preview Copy**: `/Users/tuandinh/.gemini/antigravity/brain/0bba3639-6aa1-4358-af48-fa98be8e3cf6/world_tanks_atlas.html`
- **Sister Sci-Fi AI Evolution Atlas**: `/Users/tuandinh/Scifi/index.html` (cross-linked in the top header of both files)

---

## Was the Vietnam War Involved in Any Tank Battles? — **YES!**
Despite its popular image as a jungle-infantry and helicopter conflict, **over 2,000 tanks** saw combat across South Vietnam, Laos, and Cambodia between 1965 and 1975:
- **US, ARVN & Allied Armor**: **M48A3 Patton** (90mm M41), **M41A3 Walker Bulldog** (76mm M32, backbone of the ARVN Armor Corps), **M551 Sheridan** (152mm gun/Shillelagh missile launcher), and **Australian Centurion Mk 5/1** (84mm 20-pdr).
- **North Vietnamese Army (PAVN / NVA) Armor**: **PT-76 Amphibious Light Tank** (76.2mm D-56T), **T-54 / T-55** (100mm D-10T), **Chinese Type 59** (100mm Type 59), and **T-34-85** (85mm ZiS-S-53).

### Major Vietnam War Tank Battles Included in the Atlas & Live Battle Simulator
1. **Lang Vei & Ben Het (`lang_vei_ben_het_1968`, Feb 1968 & Mar 1969)**
   - **Lang Vei (Feb 6–7, 1968)**: 13 NVA **PT-76** amphibious light tanks of the 198th Tank Battalion swam the Xe Pon River at night and overran the US Special Forces camp near Khe Sanh (6 PT-76s knocked out by M72 LAWs and 106mm recoilless rifles).
   - **Ben Het (March 3, 1969)**: The **only US-vs-NVA tank-on-tank battle** of the entire war. A platoon of US Army **M48A3 Pattons** (1st Battalion, 69th Armor) engaged ~10 NVA **PT-76** tanks and BTR-50PKs in pitch darkness at 900–1,100m, firing 90mm HEAT rounds at the PT-76 muzzle flashes and destroying 2 PT-76s and 1 BTR-50.
2. **Easter Offensive Armor Clashes: Dong Ha, Kontum & An Loc (`an_loc_dong_ha_1972`, April–June 1972)**
   - Following **Operation Lam Son 719 (Feb 1971)** in Laos—where ARVN 1st Armored Brigade **M41A3 Walker Bulldogs** destroyed 6 NVA **T-54s** and 16 **PT-76s**—North Vietnam launched a three-front conventional invasion in 1972 with **400+ T-54, Type 59, and PT-76 tanks**.
   - At **Dong Ha (April 2–9, 1972)**, newly formed **ARVN 20th Tank Regiment M48A3 Pattons** ambushed NVA 203rd Armored Regiment columns from hull-down ridge positions at 2,500–2,800m, destroying 9 **T-54s** and 2 **PT-76s** with zero M48 losses.
   - At **Kontum & An Loc**, US Army UH-1B helicopters achieved the first combat kills with the **BGM-71 TOW missile** (destroying 24 NVA tanks at Kontum), while defenders destroyed over 80 NVA T-54/Type 59/PT-76 tanks inside An Loc.
3. **Battle of Xuan Loc & Fall of Saigon (`xuan_loc_saigon_1975`, April 9–30, 1975)**
   - Five PAVN corps spearheaded by **~600 T-54, Type 59, and PT-76 tanks** fought ARVN 18th Division and 3rd Armored Cavalry Brigade **M48A3s and M41s** at Xuan Loc (37 NVA tanks destroyed in 12 days) before **NVA T-54B #843** and **Type 59 #390** crashed through the gates of Independence Palace in Saigon on April 30, 1975.

---

## Key Features in v2
1. **High-Contrast Tactical UI + Daylight/Dark Mode Toggle**: Explicit `:root` high-contrast variables (`#0b1120` deep slate background, `#f8fafc` crisp white typography, vivid color-coded lane & theatre headers) plus a one-click **☀️ Daylight / 🌙 Dark** button in the top bar.
2. **Area-Colored World Map + Interactive Battle Popup (`🌍 2. World Map & Battle Popups`)**:
   - Continents are color-coded by region and overlaid with **8 colored Strategic Theatre Polygons** (*Western Europe, British Isles, Eastern Front & Ukraine, North Africa/Sinai/Golan, Persian Gulf/Iraq, South Asia, Vietnam & SE Asia, East Asia & Korea*).
   - Clicking any of the **27 battle dots** on the World Map opens an **On-Map Battle Popup Card** showing **Who Won**, **Who Lost**, **Total Tanks Involved**, **Armor Losses**, **Historical Summary**, **clickable links for every participating tank**, and a button to launch the **Full Battle Page & Live Simulation**.
3. **67 Dedicated Tank Pages (`🛡️ 3. Tank Pages (67)`)**:
   - Every tank has a dedicated full-screen dossier (`openTankPage(id)`) featuring a **Wikimedia Commons historical/museum photograph**, an **interactive scaled SVG engineering blueprint**, **3 curated video links** (*The Tank Museum Tank Chats*, *Inside the Chieftain's Hatch*, and *Archival Combat Footage*), Wikipedia reference link, 5-axis performance bars, and clickable links to all ancestor, descendant, peer, and combat-opponent tanks and battles.
4. **27 Dedicated Battle Pages with Live Formation Simulator (`🎬 4. Battle Pages & Sim (27)`)**:
   - Every battle has a dedicated page (`openBattlePage(id)`) with a **Live Animated Battle & Formation Simulator** (`▶ Play / ⏸ Pause`, `↺ Reset`, `0.5× / 1× / 2× Speed`) that animates Side A and Side B tank platoons maneuvering in their historical formations (*Keil Wedge, Double Envelopment, Hull-Down Ridge Ambush, Night River Assault*, etc.), firing APFSDS/HEAT tracers, and tracking live armor attrition based on historical firepower, armor, optics, and outcome data.

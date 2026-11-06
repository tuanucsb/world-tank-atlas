#!/usr/bin/env python3
"""
Renders the complete World Tank Lineage, Similarity, Combat Graph & Battle Map Atlas HTML file.
"""
import json
import sys

sys.path.insert(0, "/Users/tuandinh/.gemini/antigravity/brain/0bba3639-6aa1-4358-af48-fa98be8e3cf6/scratch")
import build_tank_atlas_app as app
import generate_data as gd

# High-precision geographic coastline & inland sea polygons (lon, lat pairs) for crisp World & Theatre Zoom
WORLD_POLYGONS = [
    # UK & Ireland
    {"name": "Great Britain", "type": "land", "pts": [[-5.2,50.0],[-4.2,50.3],[-3.5,50.4],[-1.9,50.7],[0.2,50.8],[1.4,51.3],[1.0,51.8],[1.7,52.5],[0.2,53.0],[-0.1,53.6],[-1.1,54.6],[-1.6,55.6],[-3.1,56.0],[-2.0,57.0],[-2.0,57.7],[-4.0,57.8],[-3.1,58.6],[-5.0,58.6],[-5.8,57.0],[-5.5,55.3],[-4.8,54.7],[-3.1,54.1],[-3.1,53.3],[-4.6,53.3],[-4.5,52.8],[-4.1,52.5],[-5.2,51.8],[-3.2,51.4],[-5.2,50.0]]},
    {"name": "Ireland", "type": "land", "pts": [[-9.8,51.5],[-6.2,52.0],[-6.0,53.4],[-5.5,54.5],[-7.3,55.3],[-8.5,55.0],[-10.0,53.8],[-9.5,52.6],[-9.8,51.5]]},
    # Continental Europe & Eurasia
    {"name": "Eurasia", "type": "land", "pts": [
        [-9.2,38.7],[-8.8,41.8],[-9.2,43.0],[-1.8,43.4],[-1.2,44.6],[-2.2,47.2],[-4.7,48.4],[-1.8,48.6],[-1.6,49.6],[-0.1,49.3],[1.6,50.9],[3.4,51.4],[4.2,52.0],[4.8,53.0],[7.0,53.4],[8.6,53.9],[8.2,55.5],[8.6,57.1],[10.5,57.7],[10.2,56.1],[9.6,54.8],[10.9,54.0],[12.1,54.2],[14.2,53.9],[16.5,54.5],[18.6,54.4],[19.9,54.5],[21.0,55.8],[22.5,57.8],[24.4,57.8],[23.5,59.0],[24.8,59.4],[28.2,59.6],[30.2,60.0],
        # Scandinavia
        [28.0,60.6],[24.0,60.1],[21.2,61.5],[21.5,63.2],[24.5,65.5],[22.2,65.8],[20.0,63.8],[18.0,62.5],[17.5,60.5],[18.8,59.4],[16.5,56.6],[14.2,55.4],[12.8,55.4],[12.6,56.3],[11.8,57.8],[10.8,59.9],[8.0,58.0],[5.2,59.0],[5.0,61.0],[6.0,62.5],[10.0,64.0],[14.0,67.5],[18.0,69.6],[25.5,71.1],[31.0,69.8],[33.5,69.3],[40.0,67.5],[44.0,66.0],[43.0,68.5],[55.0,68.5],[60.0,70.0],[68.0,70.0],[70.0,73.0],[85.0,73.5],[105.0,77.0],[135.0,71.5],[160.0,69.5],[178.0,66.5],[163.0,60.0],[156.0,51.0],[143.0,59.0],[140.0,54.0],[135.0,45.0],[131.0,42.8],
        # Korea & East China Coast
        [129.5,39.0],[129.5,35.1],[126.5,34.3],[126.6,37.5],[125.0,39.8],[124.2,39.9],[121.2,38.9],[119.5,39.8],[117.8,38.9],[119.0,37.5],[122.6,37.4],[120.4,36.0],[119.5,34.5],[121.9,30.9],[121.5,28.5],[119.5,25.5],[116.5,23.0],[114.2,22.2],[110.0,20.2],[108.6,21.6],[106.6,20.8],[105.8,19.0],[108.2,16.0],[109.2,12.5],[106.8,10.3],[104.5,10.4],[103.5,1.3],[101.2,3.0],[100.0,6.5],[98.5,8.0],[97.6,16.5],[94.3,16.0],[92.2,21.5],[89.0,21.8],[87.0,20.8],[85.0,19.5],[80.3,13.1],[79.8,10.3],[77.5,8.1],[76.2,10.0],[74.8,13.0],[72.8,19.0],[72.6,21.6],[69.0,22.2],[70.0,23.8],[67.0,24.9],[61.5,25.2],[57.0,25.8],[56.3,26.3],
        # Persian Gulf & Arabian Peninsula
        [55.0,25.1],[51.5,25.3],[50.0,26.5],[48.5,29.9],[47.8,30.0],[49.0,30.3],[50.2,29.9],[51.5,27.8],[54.8,26.6],[56.4,27.1],[57.8,25.6],[59.8,22.5],[58.0,20.5],[54.0,17.0],[48.0,14.0],[43.3,12.6],[42.6,15.5],[41.0,18.0],[39.1,21.5],[37.0,25.0],[34.9,29.5],[34.5,28.0],[32.5,29.9],
        # Levant, Turkey, Black Sea, Greece, Italy, Iberia
        [32.3,31.3],[34.2,31.3],[34.9,32.8],[35.1,33.1],[35.8,34.4],[35.9,35.9],[36.2,36.8],[35.4,36.8],[34.0,36.2],[32.0,36.5],[30.5,36.8],[29.0,36.5],[27.2,37.5],[26.2,39.5],[26.8,40.4],[29.0,41.0],[28.0,41.5],[27.5,42.5],[28.6,44.2],[29.6,45.2],[30.8,46.4],[32.0,46.6],[33.5,46.0],[33.5,44.4],[36.5,45.2],[38.8,47.2],[39.2,47.0],[37.5,44.8],[39.5,43.5],[41.6,41.6],[38.0,41.0],[35.0,42.0],[32.0,41.5],[29.2,41.2],[26.0,40.8],[24.0,40.3],[22.9,40.5],[23.8,38.0],[22.5,36.4],[21.2,37.8],[20.0,39.5],[19.4,41.0],[18.5,42.4],[16.5,43.5],[14.5,45.3],[13.6,45.6],[12.3,45.4],[12.5,44.0],[13.9,42.8],[16.1,41.9],[15.8,41.4],[18.4,40.1],[16.8,39.8],[16.1,38.0],[15.6,38.2],[15.9,39.5],[14.0,40.8],[12.2,41.8],[10.3,43.7],[8.9,44.4],[7.5,43.8],[5.4,43.3],[3.2,42.4],[2.1,41.4],[0.8,40.8],[-0.3,39.5],[-0.7,37.6],[-2.2,36.7],[-4.4,36.7],[-5.6,36.0],[-6.3,36.5],[-7.4,37.2],[-8.9,37.0],[-9.2,38.7]
    ]},
    # Africa
    {"name": "Africa", "type": "land", "pts": [
        [-5.8,35.8],[-2.2,35.2],[0.0,35.8],[3.0,36.8],[8.5,37.0],[10.2,37.2],[11.0,37.0],[10.6,35.8],[10.1,33.5],[11.5,33.1],[15.2,32.4],[20.0,31.0],[20.1,32.1],[23.9,32.1],[25.2,31.6],[27.2,31.4],[28.9,30.8],[29.9,31.2],[31.5,31.5],[32.3,31.3],
        [32.5,29.9],[33.8,27.8],[35.5,24.0],[37.2,21.0],[38.8,18.0],[39.5,15.5],[43.1,12.5],[44.0,11.5],[49.0,11.5],[51.4,11.9],[50.0,8.0],[45.3,2.0],[41.0,-1.5],[39.5,-6.8],[40.5,-10.5],[40.6,-15.0],[35.0,-19.5],[35.5,-24.0],[32.6,-26.0],[31.0,-29.8],[28.0,-32.8],[25.5,-34.0],[20.0,-34.8],[18.4,-34.0],[17.9,-29.8],[15.0,-26.0],[14.5,-23.0],[11.8,-17.0],[13.2,-9.0],[12.2,-6.0],[9.4,0.5],[9.6,4.0],[5.5,4.3],[3.4,6.4],[0.0,5.8],[-4.0,5.2],[-7.7,4.4],[-10.8,6.3],[-13.5,8.5],[-16.7,12.3],[-17.5,14.7],[-16.5,19.5],[-17.0,20.8],[-14.5,26.0],[-10.0,29.8],[-9.4,32.3],[-5.8,35.8]
    ]},
    # Japan
    {"name": "Japan (Honshu/Kyushu/Hokkaido)", "type": "land", "pts": [[130.9,33.9],[132.5,34.4],[135.2,34.7],[136.9,34.5],[139.8,35.2],[140.9,35.8],[141.0,38.3],[142.0,39.6],[141.4,41.5],[140.3,41.2],[139.8,39.0],[138.9,37.8],[136.7,37.3],[135.5,35.6],[132.0,35.0],[130.9,33.9]]},
    {"name": "Hokkaido", "type": "land", "pts": [[140.5,41.8],[143.2,42.0],[145.5,43.4],[141.9,45.5],[140.5,41.8]]},
    {"name": "Taiwan", "type": "land", "pts": [[120.1,22.9],[121.9,25.1],[121.5,23.5],[120.8,21.9],[120.1,22.9]]},
    {"name": "Sri Lanka", "type": "land", "pts": [[79.8,9.5],[81.8,7.5],[80.5,5.9],[79.8,7.8],[79.8,9.5]]},
    {"name": "Sicily", "type": "land", "pts": [[12.5,37.8],[15.6,38.2],[15.1,36.7],[12.5,37.8]]},
    # North America
    {"name": "North America", "type": "land", "pts": [[-165.0,64.0],[-140.0,70.0],[-95.0,70.0],[-78.0,62.0],[-65.0,60.0],[-55.0,52.0],[-60.0,46.0],[-67.0,45.0],[-70.0,41.8],[-74.0,40.5],[-75.5,35.5],[-80.0,32.0],[-80.2,25.5],[-82.5,28.0],[-89.0,29.5],[-97.0,26.0],[-96.0,19.0],[-87.0,21.0],[-83.5,10.0],[-79.0,9.0],[-85.0,11.0],[-93.0,15.0],[-105.0,20.0],[-110.0,24.0],[-117.0,32.5],[-122.5,37.8],[-124.5,48.0],[-135.0,57.0],[-150.0,60.0],[-162.0,55.0],[-165.0,64.0]]},
    # South America
    {"name": "South America", "type": "land", "pts": [[-79.0,9.0],[-72.0,11.5],[-62.0,10.5],[-50.0,1.0],[-35.0,-6.0],[-38.5,-13.0],[-43.0,-23.0],[-52.0,-32.0],[-58.0,-38.0],[-65.0,-42.0],[-68.0,-54.0],[-74.0,-52.0],[-73.0,-40.0],[-71.5,-30.0],[-70.5,-18.0],[-81.0,-5.0],[-78.0,2.0],[-79.0,9.0]]},
    # Australia
    {"name": "Australia", "type": "land", "pts": [[114.0,-22.0],[122.0,-18.0],[131.0,-12.0],[136.5,-12.5],[136.0,-16.0],[142.5,-11.0],[145.5,-16.0],[150.0,-23.0],[153.5,-28.0],[150.0,-37.5],[145.0,-38.5],[138.5,-35.5],[135.5,-34.5],[129.0,-31.8],[122.0,-34.0],[115.0,-34.0],[114.0,-22.0]]}
]

print(f"World coastline polygons ready: {len(WORLD_POLYGONS)}")


HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>World Tank Lineage, Similarity, Combat Graph &amp; Battle Map Atlas (1916–2026)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    * { box-sizing: border-box; }
    .custom-scroll::-webkit-scrollbar { width: 7px; height: 7px; }
    .custom-scroll::-webkit-scrollbar-track { background: transparent; }
    .custom-scroll::-webkit-scrollbar-thumb { background: rgba(148, 163, 184, 0.35); border-radius: 9999px; }
    .custom-scroll::-webkit-scrollbar-thumb:hover { background: rgba(148, 163, 184, 0.65); }
    canvas { user-select: none; }

    /* 2d-panning modern web guidance: unrestricted 2D scroll container without axis-locking railing */
    .pan-viewport {
      overflow: auto;
      scroll-axis-lock: none;
      overscroll-behavior: none;
    }
    .pan-viewport:focus-visible {
      outline: 3px solid #38bdf8;
      outline-offset: 2px;
    }
    @supports not (scroll-axis-lock: none) {
      .pan-viewport {
        touch-action: none;
      }
    }
  </style>
</head>
<body class="bg-[var(--background)] text-[var(--foreground)] antialiased min-h-screen flex flex-col">

  <!-- Top Header & Navigation Controls -->
  <header class="bg-[var(--card)] border-b border-[var(--border)] px-5 py-3.5 sticky top-0 z-30 shadow-sm">
    <div class="max-w-[1800px] mx-auto flex flex-col gap-3">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="flex items-center gap-2.5">
            <span class="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 font-bold text-sm border border-amber-500/30">🛡️</span>
            <h1 class="text-lg font-bold tracking-tight text-[var(--foreground)]">
              World Tank Lineage, Design Similarity, Combat Duels &amp; Battle Map Atlas (1916–2026)
            </h1>
          </div>
          <p class="text-xs text-[var(--muted-foreground)] mt-0.5">
            7 Historical Eras • __NUM_TANKS__ Iconic Tanks • __NUM_EDGES__ Lineage, Tech-Similarity &amp; Combat Links • __NUM_BATTLES__ Georeferenced World Tank Battles with Tactical Zoom-In
          </p>
        </div>

        <!-- 4-Tab View Switcher -->
        <div class="flex flex-wrap items-center gap-1.5 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)]">
          <button id="tab-graph" onclick="switchMainView('graph')" class="px-3 py-1.5 rounded-md text-xs font-semibold transition bg-amber-600 text-white shadow-sm">
            🕸️ Lineage, Similarity &amp; Combat Graph
          </button>
          <button id="tab-map" onclick="switchMainView('map')" class="px-3 py-1.5 rounded-md text-xs font-semibold transition text-[var(--muted-foreground)] hover:text-[var(--foreground)]">
            🌍 World Tank Battles Map (+ Tactical Zoom)
          </button>
          <button id="tab-duel" onclick="switchMainView('duel')" class="px-3 py-1.5 rounded-md text-xs font-semibold transition text-[var(--muted-foreground)] hover:text-[var(--foreground)]">
            ⚔️ Head-to-Head Tank Duel Comparator
          </button>
          <button id="tab-matrix" onclick="switchMainView('matrix')" class="px-3 py-1.5 rounded-md text-xs font-semibold transition text-[var(--muted-foreground)] hover:text-[var(--foreground)]">
            📐 2D Tech-Tree Blueprint &amp; Catalog (__NUM_TANKS__)
          </button>
        </div>
      </div>

      <!-- Row 2: Relationship Filters, Conflict Presets & Search -->
      <div class="flex flex-wrap items-center justify-between gap-2 pt-2.5 border-t border-[var(--border)]">
        <div class="flex flex-wrap items-center gap-1.5">
          <span class="text-xs font-semibold text-[var(--muted-foreground)] mr-1">Edge Layers:</span>
          <button onclick="toggleEdgeLayer('lineage')" id="layer-lineage" class="px-2.5 py-1 rounded-md text-xs font-semibold border border-emerald-500/60 bg-emerald-500/15 text-emerald-300 transition">
            🟢 Lineage Evolution: ON
          </button>
          <button onclick="toggleEdgeLayer('similarity')" id="layer-similarity" class="px-2.5 py-1 rounded-md text-xs font-semibold border border-sky-500/60 bg-sky-500/15 text-sky-300 transition">
            🔵 Design Similarity / Tech Transfer: ON
          </button>
          <button onclick="toggleEdgeLayer('combat')" id="layer-combat" class="px-2.5 py-1 rounded-md text-xs font-semibold border border-rose-500/60 bg-rose-500/15 text-rose-300 transition">
            ⚔️ 🔴 Fought Each Other (Combat): ON
          </button>

          <span class="text-[var(--muted-foreground)] mx-1">|</span>
          <span class="text-xs font-semibold text-[var(--muted-foreground)]">Conflict &amp; Saga Focus:</span>
          <button onclick="setConflictFilter('all')" id="cf-all" class="cf-btn px-2 py-1 rounded text-xs font-semibold border border-amber-500 bg-amber-500/15 text-[var(--foreground)]">All Eras</button>
          <button onclick="setConflictFilter('ww1_interwar')" id="cf-ww1_interwar" class="cf-btn px-2 py-1 rounded text-xs font-medium border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]">WWI &amp; Interwar</button>
          <button onclick="setConflictFilter('ww2')" id="cf-ww2" class="cf-btn px-2 py-1 rounded text-xs font-medium border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]">WWII Duels (1939–45)</button>
          <button onclick="setConflictFilter('arab_israeli')" id="cf-arab_israeli" class="cf-btn px-2 py-1 rounded text-xs font-medium border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Sinai, Golan &amp; Bekaa</button>
          <button onclick="setConflictFilter('gulf')" id="cf-gulf" class="cf-btn px-2 py-1 rounded text-xs font-medium border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Gulf Wars (1991/2003)</button>
          <button onclick="setConflictFilter('ukraine')" id="cf-ukraine" class="cf-btn px-2 py-1 rounded text-xs font-medium border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Ukraine (2022–26)</button>
        </div>

        <!-- Nation Filter + Search -->
        <div class="flex flex-wrap items-center gap-2">
          <select id="nation-select" onchange="setNationFilter(this.value)" class="px-2.5 py-1 rounded-lg text-xs bg-[var(--background)] border border-[var(--border)] text-[var(--foreground)]">
            <option value="all">🌐 All 7 Nations / Blocs</option>
            <option value="UK">🇬🇧 United Kingdom</option>
            <option value="FR">🇫🇷 France</option>
            <option value="DE">🇩🇪 Germany</option>
            <option value="SU_RU">☭/🇷🇺/🇺🇦 USSR / Russia / Ukraine</option>
            <option value="US">🇺🇸 United States</option>
            <option value="IL">🇮🇱 Israel</option>
            <option value="ASIA_OTHER">🌏 Japan / China / S. Korea / Sweden</option>
          </select>

          <div class="relative">
            <input
              id="search-input"
              type="text"
              oninput="handleSearch(this.value)"
              placeholder="Search tank, gun, battle (Tiger, T-34, Kursk, 73 Easting)..."
              class="w-64 pl-3 pr-7 py-1 rounded-lg text-xs bg-[var(--background)] border border-[var(--border)] text-[var(--foreground)] placeholder-[var(--muted-foreground)] focus:outline-none focus:border-amber-500"
            />
            <button id="clear-search" onclick="clearSearch()" class="hidden absolute right-2 top-1/2 -translate-y-1/2 text-xs text-[var(--muted-foreground)] hover:text-[var(--foreground)]">✕</button>
          </div>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Workspace Container -->
  <main class="flex-1 max-w-[1800px] w-full mx-auto p-4 flex flex-col gap-4">

    <!-- ===================================================================== -->
    <!-- VIEW 1: INTERACTIVE TANK LINEAGE, SIMILARITY & COMBAT GRAPH           -->
    <!-- ===================================================================== -->
    <section id="view-graph" class="flex flex-col gap-3">
      <!-- 7-Era Interactive Stepper Bar -->
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-3 shadow-sm flex flex-col gap-2">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div class="flex flex-wrap items-center gap-2 text-xs">
            <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold border border-amber-500/30">HOW TO READ THE GRAPH</span>
            <span class="text-[var(--foreground)] font-medium">1. Left → Right = 7 Historical Eras (1916–2026)</span>
            <span class="text-[var(--muted-foreground)]">•</span>
            <span class="text-[var(--foreground)] font-medium">2. <span class="text-emerald-400">Solid Green = Lineage</span> | <span class="text-sky-400">Dashed Blue = Tech Similarity</span> | <span class="text-rose-400">Crimson ⚔️ = Fought Each Other</span></span>
            <span class="text-[var(--muted-foreground)]">•</span>
            <span class="text-[var(--foreground)] font-medium">3. Click any Tank to inspect its Combat Duels &amp; jump to the World Map!</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="text-xs text-[var(--muted-foreground)]">Y-Axis Layout:</span>
            <button onclick="setGraphYMode('nation')" id="ymode-nation" class="px-2.5 py-1 rounded text-xs font-semibold bg-amber-600 text-white">By Nation / Bloc</button>
            <button onclick="setGraphYMode('weight')" id="ymode-weight" class="px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]">By Combat Weight (t)</button>
          </div>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-1.5 pt-1" id="era-stepper-bar"></div>
      </div>

      <!-- Split Grid: Graph Canvas (7 cols) + Deep Tank & Combat Duel Inspector (5 cols) -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 items-start">
        <div class="lg:col-span-7 bg-[var(--card)] border border-[var(--border)] rounded-xl overflow-hidden shadow-sm flex flex-col">
          <div class="px-4 py-2.5 border-b border-[var(--border)] flex flex-wrap items-center justify-between gap-2 bg-[var(--background)]/40">
            <div class="flex flex-wrap items-center gap-2 text-xs">
              <span class="font-semibold text-[var(--foreground)]">Interactive Armor Network:</span>
              <span class="text-[var(--muted-foreground)]" id="graph-status-label">Showing all tanks &amp; links</span>
            </div>
            <div class="flex items-center gap-1.5">
              <button onclick="stepTank(-1)" class="px-2.5 py-1 rounded border border-[var(--border)] bg-[var(--card)] hover:border-amber-500 text-xs font-medium transition">◀ Prev Tank</button>
              <button onclick="stepTank(1)" class="px-2.5 py-1 rounded border border-[var(--border)] bg-[var(--card)] hover:border-amber-500 text-xs font-medium transition">Next Tank ▶</button>
              <button onclick="zoomGraph(1.25)" class="px-2 py-1 rounded border border-[var(--border)] bg-[var(--card)] hover:bg-[var(--background)] text-xs font-bold transition">+</button>
              <button onclick="zoomGraph(0.8)" class="px-2 py-1 rounded border border-[var(--border)] bg-[var(--card)] hover:bg-[var(--background)] text-xs font-bold transition">−</button>
              <button onclick="resetGraphCamera()" class="px-2.5 py-1 rounded border border-[var(--border)] bg-[var(--card)] hover:bg-[var(--background)] text-xs font-medium transition">Reset View</button>
            </div>
          </div>

          <div class="relative w-full h-[720px] bg-[var(--background)]" id="graph-canvas-wrap">
            <canvas id="tank-graph-canvas" class="w-full h-full block cursor-grab active:cursor-grabbing"></canvas>

            <!-- Floating Legend Bottom-Left -->
            <div class="absolute bottom-3 left-3 bg-[var(--card)]/95 backdrop-blur border border-[var(--border)] rounded-lg p-2.5 shadow-md flex flex-wrap items-center gap-3 text-xs pointer-events-none max-w-[96%]">
              <div class="flex items-center gap-1.5"><span class="w-5 h-0.5 bg-emerald-400 inline-block"></span><span>Lineage / Evolution</span></div>
              <div class="flex items-center gap-1.5"><span class="w-5 h-0.5 border-b-2 border-dashed border-sky-400 inline-block"></span><span>Design Similarity / Shared Gun-Armor</span></div>
              <div class="flex items-center gap-1.5"><span class="w-5 h-0.5 bg-rose-500 inline-block"></span><span>⚔️ Fought Each Other in Combat</span></div>
            </div>

            <!-- Floating Hint Top-Right -->
            <div class="absolute top-3 right-3 bg-[var(--card)]/90 backdrop-blur border border-[var(--border)] rounded-lg px-3 py-1.5 text-xs text-[var(--muted-foreground)] pointer-events-none">
              Click any tank node • Drag to pan • Scroll to zoom
            </div>
          </div>
        </div>

        <!-- Right-Side Deep Tank & Combat Inspector -->
        <div class="lg:col-span-5 bg-[var(--card)] border border-[var(--border)] rounded-xl shadow-sm flex flex-col h-[770px]">
          <div id="tank-inspector" class="flex-1 overflow-y-auto custom-scroll p-5 flex flex-col gap-4"></div>
        </div>
      </div>
    </section>

    <!-- ===================================================================== -->
    <!-- VIEW 2: WORLD TANK BATTLES MAP & TACTICAL BATTLEFIELD ZOOM-IN         -->
    <!-- ===================================================================== -->
    <section id="view-map" class="hidden flex-col gap-3">
      <!-- Theatre Quick-Zoom Bar -->
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-3 shadow-sm flex flex-wrap items-center justify-between gap-2">
        <div class="flex flex-wrap items-center gap-1.5">
          <span class="text-xs font-bold text-amber-400 mr-1">🌍 THEATRE ZOOM PRESETS:</span>
          <button onclick="flyToTheatre('WORLD')" class="px-2.5 py-1 rounded-md text-xs font-semibold bg-amber-600 text-white hover:bg-amber-500 transition">🌐 Full World (__NUM_BATTLES__ Battles)</button>
          <button onclick="flyToTheatre('EUROPE_WEST')" class="px-2.5 py-1 rounded-md text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-amber-500 transition">🇫🇷🇧🇪 Western Front &amp; Normandy (7)</button>
          <button onclick="flyToTheatre('EUROPE_EAST')" class="px-2.5 py-1 rounded-md text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-amber-500 transition">🇺🇦🇷🇺 Eastern Front, Kursk &amp; Ukraine (5)</button>
          <button onclick="flyToTheatre('NORTH_AFRICA_SINAI')" class="px-2.5 py-1 rounded-md text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-amber-500 transition">🇪🇬🇮🇱 El Alamein, Sinai &amp; Golan (5)</button>
          <button onclick="flyToTheatre('GULF_ME')" class="px-2.5 py-1 rounded-md text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-amber-500 transition">🇮🇶🇮🇷 Persian Gulf &amp; Iraq (3)</button>
          <button onclick="flyToTheatre('ASIA')" class="px-2.5 py-1 rounded-md text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-amber-500 transition">🇲🇳🇰🇷🇮🇳 Khalkhin Gol, Korea &amp; Chawinda (3)</button>
        </div>

        <div class="flex items-center gap-1.5">
          <button onclick="zoomMapBy(1.4)" class="px-2.5 py-1 rounded border border-[var(--border)] bg-[var(--background)] hover:border-amber-500 text-xs font-bold">🔍 Zoom In (+)</button>
          <button onclick="zoomMapBy(0.7)" class="px-2.5 py-1 rounded border border-[var(--border)] bg-[var(--background)] hover:border-amber-500 text-xs font-bold">Zoom Out (−)</button>
          <button onclick="toggleTacticalZoomModal()" id="btn-tactical-toggle" class="px-3 py-1 rounded-md bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold shadow-sm transition">
            🎯 Open Tactical Battlefield Schematic Zoom
          </button>
        </div>
      </div>

      <!-- Map Canvas (7 cols) + Battle Inspector & Tactical Schematic (5 cols) -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 items-start">
        <div class="lg:col-span-7 bg-[var(--card)] border border-[var(--border)] rounded-xl overflow-hidden shadow-sm flex flex-col">
          <div class="px-4 py-2 border-b border-[var(--border)] flex flex-wrap items-center justify-between gap-2 bg-[var(--background)]/40 text-xs">
            <span class="font-semibold text-[var(--foreground)]" id="map-zoom-readout">World Map Camera: 1.0x • Click any pulsing battle marker to zoom in</span>
            <span class="text-[var(--muted-foreground)]">Scroll wheel to zoom up to 18x • Drag to pan</span>
          </div>

          <div class="relative w-full h-[720px] bg-[#07111e]" id="map-canvas-wrap">
            <canvas id="world-map-canvas" class="w-full h-full block cursor-grab active:cursor-grabbing"></canvas>

            <!-- Interactive Tactical Battlefield Zoom-In Overlay (Shown when Tactical Zoom is toggled) -->
            <div id="tactical-zoom-overlay" class="hidden absolute inset-4 bg-[var(--card)]/95 backdrop-blur-md border-2 border-amber-500/60 rounded-xl shadow-2xl flex flex-col overflow-hidden z-20">
              <div class="px-4 py-3 border-b border-[var(--border)] flex items-center justify-between bg-[var(--background)]/70">
                <div>
                  <span class="px-2 py-0.5 rounded text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40 mr-2">TACTICAL BATTLEFIELD ZOOM-IN</span>
                  <span class="font-bold text-sm text-[var(--foreground)]" id="tac-overlay-title">Battle Schematic</span>
                </div>
                <button onclick="toggleTacticalZoomModal(false)" class="px-3 py-1 rounded-lg bg-[var(--card)] border border-[var(--border)] hover:border-amber-500 text-xs font-semibold">
                  ✕ Back to World Map
                </button>
              </div>
              <div class="flex-1 relative bg-[#091520]">
                <canvas id="tactical-schematic-canvas" class="w-full h-full block"></canvas>
              </div>
              <div class="px-4 py-2.5 border-t border-[var(--border)] bg-[var(--background)]/80 text-xs text-[var(--muted-foreground)] flex flex-wrap items-center justify-between gap-2" id="tac-overlay-footer"></div>
            </div>

            <!-- Timeline Battle Scrubber Bottom Bar -->
            <div class="absolute bottom-3 left-3 right-3 bg-[var(--card)]/95 backdrop-blur border border-[var(--border)] rounded-lg p-2 shadow-lg flex items-center gap-2 overflow-x-auto custom-scroll" id="map-battle-strip"></div>
          </div>
        </div>

        <!-- Battle Inspector & Tactical Breakdown Column (5 cols) -->
        <div class="lg:col-span-5 bg-[var(--card)] border border-[var(--border)] rounded-xl shadow-sm flex flex-col h-[765px]">
          <div id="battle-inspector" class="flex-1 overflow-y-auto custom-scroll p-5 flex flex-col gap-4"></div>
        </div>
      </div>
    </section>

    <!-- ===================================================================== -->
    <!-- VIEW 3: HEAD-TO-HEAD TANK DUEL COMPARATOR                             -->
    <!-- ===================================================================== -->
    <section id="view-duel" class="hidden flex-col gap-4">
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-5 shadow-sm flex flex-col gap-4">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-[var(--border)] pb-4">
          <div>
            <h2 class="text-base font-bold text-[var(--foreground)]">⚔️ Head-to-Head Tank Duel Comparator &amp; Historical Clash Analyzer</h2>
            <p class="text-xs text-[var(--muted-foreground)] mt-0.5">Select any two tanks from 1916–2026 or click a famous historical duel preset below:</p>
          </div>
          <div class="flex flex-wrap items-center gap-1.5">
            <button onclick="setDuelPair('mark_i_iv','a7v')" class="px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1918: Mark IV vs A7V</button>
            <button onclick="setDuelPair('somua_s35','panzer_iii')" class="px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1940: SOMUA S35 vs Pz III</button>
            <button onclick="setDuelPair('t34_76','tiger_i')" class="px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1943: T-34/76 vs Tiger I</button>
            <button onclick="setDuelPair('cromwell_firefly','tiger_i')" class="px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1944: Firefly vs Tiger I</button>
            <button onclick="setDuelPair('m4a3e8','panther')" class="px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1944: Easy Eight vs Panther</button>
            <button onclick="setDuelPair('is2','tiger_ii')" class="px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1945: IS-2 vs King Tiger</button>
            <button onclick="setDuelPair('shot_magach','t62')" class="px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1973: Sho't Kal vs T-62</button>
            <button onclick="setDuelPair('m1_abrams','t72')" class="px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1991: M1A1 Abrams vs T-72</button>
            <button onclick="setDuelPair('leopard2_a7_kf51','t90m')" class="px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">2024: Leopard 2A6 vs T-90M</button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-1 rounded bg-sky-500/20 text-sky-400 font-bold text-xs border border-sky-500/30">TANK A</span>
            <select id="duel-select-a" onchange="updateDuelView()" class="flex-1 px-3 py-2 rounded-lg text-xs font-semibold bg-[var(--background)] border border-[var(--border)] text-[var(--foreground)]"></select>
          </div>
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-1 rounded bg-rose-500/20 text-rose-400 font-bold text-xs border border-rose-500/30">TANK B</span>
            <select id="duel-select-b" onchange="updateDuelView()" class="flex-1 px-3 py-2 rounded-lg text-xs font-semibold bg-[var(--background)] border border-[var(--border)] text-[var(--foreground)]"></select>
          </div>
        </div>

        <div id="duel-comparison-body" class="grid grid-cols-1 lg:grid-cols-12 gap-5 pt-2"></div>
      </div>
    </section>

    <!-- ===================================================================== -->
    <!-- VIEW 4: 2D SCROLLABLE TECH-TREE BLUEPRINT BOARD & ENCYCLOPEDIA        -->
    <!-- ===================================================================== -->
    <section id="view-matrix" class="hidden flex-col gap-4">
      <!-- 2D Scrollable Blueprint Matrix (Implements modern-web-guidance `2d-panning`) -->
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 shadow-sm flex flex-col gap-3">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 class="text-base font-bold text-[var(--foreground)]">📐 2D Panning National Tech-Tree Matrix (1916–2026)</h2>
            <p class="text-xs text-[var(--muted-foreground)]">Freely pan diagonally or with Arrow keys across all 7 Nations × 7 Eras (`scroll-axis-lock: none`). Click any tank card to inspect.</p>
          </div>
          <span class="text-xs text-amber-400 font-semibold">Tip: Focus board &amp; use Arrow keys or drag/scroll in any 2D direction</span>
        </div>

        <div
          id="blueprint-pan-viewport"
          class="pan-viewport w-full h-[520px] bg-[var(--background)] border border-[var(--border)] rounded-xl p-4"
          tabindex="0"
          role="region"
          aria-label="Interactive 2D Tank Lineage Matrix across 7 Eras and 7 Nations"
        >
          <div id="blueprint-pan-surface" class="min-w-[1680px] min-h-[760px]"></div>
        </div>
      </div>

      <!-- Full Filterable Encyclopedia Grid -->
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 shadow-sm flex flex-col gap-3">
        <h3 class="text-sm font-bold text-[var(--foreground)]">📚 Complete World Tank Encyclopedia (__NUM_TANKS__ Iconic Vehicles)</h3>
        <div id="catalog-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3"></div>
      </div>
    </section>

  </main>

  <script>
    const ERAS = __ERAS_JSON__;
    const NATIONS = __NATIONS_JSON__;
    const TANKS = __TANKS_JSON__;
    const EDGES = __EDGES_JSON__;
    const BATTLES = __BATTLES_JSON__;
    const WORLD_POLYGONS = __POLYGONS_JSON__;
'''

print("HTML header & body template prepared.")

JS_ENGINE = r'''
    // Lookup Maps
    const TANK_MAP = Object.fromEntries(TANKS.map(t => [t.id, t]));
    const NATION_MAP = Object.fromEntries(NATIONS.map(n => [n.id, n]));
    const BATTLE_MAP = Object.fromEntries(BATTLES.map(b => [b.id, b]));
    const ERA_MAP = Object.fromEntries(ERAS.map(e => [e.id, e]));

    // Application State
    const state = {
      mainView: 'graph',
      selectedTankId: 't34_76',
      hoveredTankId: null,
      selectedBattleId: 'kursk_1943',
      hoveredBattleId: null,
      tacticalZoomOpen: false,
      layers: { lineage: true, similarity: true, combat: true },
      conflictFilter: 'all',
      nationFilter: 'all',
      eraFilter: null,
      searchQuery: '',
      yMode: 'nation', // 'nation' or 'weight'
      // Graph camera
      gCam: { x: 0, y: 0, k: 1.0, dragging: false, sx: 0, sy: 0, moved: false },
      // Map camera (center lon, lat, zoom)
      mCam: { lon: 25.0, lat: 36.0, k: 1.85, targetLon: 25.0, targetLat: 36.0, targetK: 1.85, dragging: false, sx: 0, sy: 0 },
      duelA: 't34_76',
      duelB: 'tiger_i',
      animTick: 0
    };

    // Conflict Preset Tank Sets
    const CONFLICT_SETS = {
      ww1_interwar: new Set(TANKS.filter(t => t.era <= 2).map(t => t.id)),
      ww2: new Set(TANKS.filter(t => t.era === 3 || t.era === 4 || t.id === 'matilda_ii' || t.id === 'somua_s35' || t.id === 'char_b1' || t.id === 'panzer_ii' || t.id === 'pz_38t' || t.id === 't26' || t.id === 'bt7' || t.id === 'type95_97').map(t => t.id)),
      arab_israeli: new Set(['centurion_mk1','shot_magach','m48_m60_patton','amx13_30','t34_85','is3','t54_55','t62','t72','merkava_i_ii','merkava_iv']),
      gulf: new Set(['m1_abrams','m1a2_sepv3','challenger1','challenger2_3','m48_m60_patton','amx30','chieftain','t72','t62','t54_55','type59_69']),
      ukraine: new Set(['t64_t80','t80bvm','t84_oplot','t72','t90m','leopard1','leopard2_a4','leopard2_a7_kf51','m1_abrams','m1a2_sepv3','challenger2_3'])
    };

    function isTankVisible(t) {
      if (state.eraFilter && t.era !== state.eraFilter) return false;
      if (state.nationFilter !== 'all' && t.nation !== state.nationFilter) return false;
      if (state.conflictFilter !== 'all' && CONFLICT_SETS[state.conflictFilter] && !CONFLICT_SETS[state.conflictFilter].has(t.id)) return false;
      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase();
        const inBattles = BATTLES.some(b => (b.side_a.tanks.includes(t.id) || b.side_b.tanks.includes(t.id)) && (b.name.toLowerCase().includes(q) || b.location.toLowerCase().includes(q)));
        const match = t.name.toLowerCase().includes(q) || t.gun.toLowerCase().includes(q) || t.role.toLowerCase().includes(q) || t.summary.toLowerCase().includes(q) || inBattles;
        if (!match) return false;
      }
      return true;
    }

    // Compute world coordinates for each tank node on the graph canvas
    function getGraphNodePos(t, W, H) {
      const padLeft = 145, padRight = 55, padTop = 78, padBottom = 42;
      const usableW = Math.max(800, W) - padLeft - padRight;
      const usableH = Math.max(520, H) - padTop - padBottom;
      const colW = usableW / 7;
      const x = padLeft + (t.era - 0.5) * colW + (t.x_offset || 0) * (colW * 0.52);
      let y;
      if (state.yMode === 'nation') {
        const lane = NATION_MAP[t.nation]?.lane ?? 0;
        const laneH = usableH / 7;
        y = padTop + (lane + 0.5) * laneH + (t.lane_offset || 0) * (laneH * 0.58);
      } else {
        // Weight mode: 6t at bottom to 70t at top
        const normW = Math.min(1, Math.max(0, (t.weight_t - 5) / 65));
        y = padTop + (1 - normW) * usableH;
      }
      return { x, y };
    }

    // Build Era Stepper Bar
    function renderEraStepper() {
      const el = document.getElementById('era-stepper-bar');
      el.innerHTML = ERAS.map(e => {
        const active = state.eraFilter === e.id;
        return `<button onclick="toggleEraFilter(${e.id})" class="text-left p-2 rounded-lg border transition ${active ? 'border-amber-500 bg-amber-500/20' : 'border-[var(--border)] bg-[var(--background)]/60 hover:border-amber-500/50'}">
          <div class="text-[11px] font-bold ${active ? 'text-amber-300' : 'text-[var(--foreground)]'} truncate">${e.short}</div>
          <div class="text-[10px] text-[var(--muted-foreground)] truncate mt-0.5">${e.desc}</div>
        </button>`;
      }).join('');
    }

    function toggleEraFilter(eraId) {
      state.eraFilter = (state.eraFilter === eraId) ? null : eraId;
      renderEraStepper();
      renderCatalogAndMatrix();
    }

    function toggleEdgeLayer(layer) {
      state.layers[layer] = !state.layers[layer];
      const btn = document.getElementById('layer-' + layer);
      const labels = {
        lineage: ['🟢 Lineage Evolution: ON', '⚪ Lineage Evolution: OFF', 'emerald'],
        similarity: ['🔵 Design Similarity / Tech Transfer: ON', '⚪ Design Similarity: OFF', 'sky'],
        combat: ['⚔️ 🔴 Fought Each Other (Combat): ON', '⚪ Fought Each Other: OFF', 'rose']
      };
      const [onTxt, offTxt, col] = labels[layer];
      if (state.layers[layer]) {
        btn.textContent = onTxt;
        btn.className = `px-2.5 py-1 rounded-md text-xs font-semibold border border-${col}-500/60 bg-${col}-500/15 text-${col}-300 transition`;
      } else {
        btn.textContent = offTxt;
        btn.className = `px-2.5 py-1 rounded-md text-xs font-medium border border-[var(--border)] bg-[var(--background)] text-[var(--muted-foreground)] transition`;
      }
    }

    function setConflictFilter(cf) {
      state.conflictFilter = cf;
      document.querySelectorAll('.cf-btn').forEach(b => {
        b.className = 'cf-btn px-2 py-1 rounded text-xs font-medium border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]';
      });
      const activeBtn = document.getElementById('cf-' + cf);
      if (activeBtn) activeBtn.className = 'cf-btn px-2 py-1 rounded text-xs font-semibold border border-amber-500 bg-amber-500/15 text-[var(--foreground)]';
      renderCatalogAndMatrix();
    }

    function setNationFilter(nat) {
      state.nationFilter = nat;
      renderCatalogAndMatrix();
    }

    function handleSearch(val) {
      state.searchQuery = val.trim();
      document.getElementById('clear-search').classList.toggle('hidden', !state.searchQuery);
      renderCatalogAndMatrix();
    }

    function clearSearch() {
      document.getElementById('search-input').value = '';
      handleSearch('');
    }

    function setGraphYMode(mode) {
      state.yMode = mode;
      document.getElementById('ymode-nation').className = mode === 'nation'
        ? 'px-2.5 py-1 rounded text-xs font-semibold bg-amber-600 text-white'
        : 'px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)]';
      document.getElementById('ymode-weight').className = mode === 'weight'
        ? 'px-2.5 py-1 rounded text-xs font-semibold bg-amber-600 text-white'
        : 'px-2.5 py-1 rounded text-xs font-medium bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)]';
    }

    function switchMainView(view) {
      state.mainView = view;
      ['graph', 'map', 'duel', 'matrix'].forEach(v => {
        const sec = document.getElementById('view-' + v);
        const tab = document.getElementById('tab-' + v);
        if (v === view) {
          sec.classList.remove('hidden');
          sec.classList.add('flex');
          tab.className = 'px-3 py-1.5 rounded-md text-xs font-semibold transition bg-amber-600 text-white shadow-sm';
        } else {
          sec.classList.add('hidden');
          sec.classList.remove('flex');
          tab.className = 'px-3 py-1.5 rounded-md text-xs font-semibold transition text-[var(--muted-foreground)] hover:text-[var(--foreground)]';
        }
      });
      if (view === 'duel') updateDuelView();
      if (view === 'matrix') renderCatalogAndMatrix();
    }

    function selectTank(tankId, switchViewToGraph = false) {
      if (!TANK_MAP[tankId]) return;
      state.selectedTankId = tankId;
      if (switchViewToGraph) switchMainView('graph');
      renderTankInspector();
    }

    function stepTank(delta) {
      const visible = TANKS.filter(isTankVisible);
      if (!visible.length) return;
      const idx = visible.findIndex(t => t.id === state.selectedTankId);
      const next = visible[(idx + delta + visible.length) % visible.length];
      selectTank(next.id);
    }

    // Render Right-Side Tank & Combat Inspector
    function renderTankInspector() {
      const t = TANK_MAP[state.selectedTankId] || TANKS[0];
      const nat = NATION_MAP[t.nation];
      const era = ERA_MAP[t.era];

      // Gather connected edges
      const parents = EDGES.filter(e => e.type === 'lineage' && e.target === t.id).map(e => ({ tank: TANK_MAP[e.source], label: e.label }));
      const children = EDGES.filter(e => e.type === 'lineage' && e.source === t.id).map(e => ({ tank: TANK_MAP[e.target], label: e.label }));
      const similar = EDGES.filter(e => e.type === 'similarity' && (e.source === t.id || e.target === t.id)).map(e => {
        const otherId = e.source === t.id ? e.target : e.source;
        return { tank: TANK_MAP[otherId], label: e.label };
      });
      const combats = EDGES.filter(e => e.type === 'combat' && (e.source === t.id || e.target === t.id)).map(e => {
        const otherId = e.source === t.id ? e.target : e.source;
        return { tank: TANK_MAP[otherId], label: e.label, battles: (e.battles || []).map(bid => BATTLE_MAP[bid]).filter(Boolean) };
      });
      const battlesFought = BATTLES.filter(b => b.side_a.tanks.includes(t.id) || b.side_b.tanks.includes(t.id));

      const statBar = (label, val, color) => `
        <div class="flex items-center gap-2 text-xs">
          <span class="w-24 text-[var(--muted-foreground)]">${label}</span>
          <div class="flex-1 h-2 bg-[var(--background)] rounded-full overflow-hidden border border-[var(--border)]">
            <div class="h-full ${color} rounded-full" style="width:${val}%"></div>
          </div>
          <span class="w-8 text-right font-mono font-bold">${val}</span>
        </div>`;

      document.getElementById('tank-inspector').innerHTML = `
        <div class="border-b border-[var(--border)] pb-3">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold border" style="border-color:${nat.color}66; background:${nat.color}20; color:${nat.color}">
              ${nat.flag} ${nat.name} • ${t.year}
            </span>
            <span class="text-xs font-semibold text-amber-400">${era.short}</span>
          </div>
          <h2 class="text-xl font-bold text-[var(--foreground)] mt-2">${t.name}</h2>
          <p class="text-xs text-[var(--muted-foreground)] font-medium mt-0.5">${t.role} • Production: ~${t.produced.toLocaleString()} units</p>
          <p class="text-xs text-[var(--foreground)] leading-relaxed mt-2.5 bg-[var(--background)]/60 p-3 rounded-lg border border-[var(--border)]">${t.summary}</p>
        </div>

        <!-- Technical Specs Grid -->
        <div class="grid grid-cols-3 gap-2 text-xs">
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-2.5">
            <div class="text-[10px] text-[var(--muted-foreground)] uppercase">Main Armament</div>
            <div class="font-bold text-[var(--foreground)] mt-0.5 leading-snug">${t.gun}</div>
          </div>
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-2.5">
            <div class="text-[10px] text-[var(--muted-foreground)] uppercase">Frontal Armor</div>
            <div class="font-bold text-amber-400 mt-0.5">${t.armor_mm} mm RHAe</div>
          </div>
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-2.5">
            <div class="text-[10px] text-[var(--muted-foreground)] uppercase">Weight / Speed</div>
            <div class="font-bold text-emerald-400 mt-0.5">${t.weight_t}t • ${t.speed_kmh} km/h</div>
          </div>
        </div>

        <!-- 5-Axis Rating Bars -->
        <div class="bg-[var(--background)]/50 border border-[var(--border)] rounded-xl p-3 flex flex-col gap-1.5">
          <div class="text-xs font-bold text-[var(--foreground)] mb-1">Performance &amp; Historical Impact Index</div>
          ${statBar('Firepower', t.stats.firepower, 'bg-rose-500')}
          ${statBar('Armor / Protection', t.stats.armor, 'bg-amber-500')}
          ${statBar('Mobility', t.stats.mobility, 'bg-emerald-500')}
          ${statBar('Optics & Fire Ctrl', t.stats.optics, 'bg-sky-500')}
          ${statBar('Historical Impact', t.stats.impact, 'bg-purple-500')}
        </div>

        <!-- Combat Opponents ("Fought Against") -->
        <div class="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3.5 flex flex-col gap-2.5">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-rose-400 uppercase tracking-wider">⚔️ Fought Against in Combat (${combats.length} Rivals)</span>
            <button onclick="state.duelA='${t.id}'; state.duelB='${combats[0]?.tank?.id || 'tiger_i'}'; switchMainView('duel')" class="px-2 py-0.5 rounded bg-rose-600 text-white text-[11px] font-semibold hover:bg-rose-500">
              ⚔️ Open Duel Simulator
            </button>
          </div>
          ${combats.length ? combats.map(c => `
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-lg p-2.5 flex flex-col gap-1.5">
              <div class="flex items-center justify-between gap-2">
                <button onclick="selectTank('${c.tank.id}')" class="text-xs font-bold text-rose-300 hover:underline text-left">
                  ⚔️ vs. ${NATION_MAP[c.tank.nation].flag} ${c.tank.name} (${c.tank.year})
                </button>
                <button onclick="setDuelPair('${t.id}','${c.tank.id}'); switchMainView('duel')" class="px-2 py-0.5 rounded border border-rose-500/40 text-[10px] text-rose-300 hover:bg-rose-500/20">
                  Compare Stats
                </button>
              </div>
              <div class="text-[11px] text-[var(--muted-foreground)]">${c.label}</div>
              ${c.battles.length ? `<div class="flex flex-wrap gap-1 pt-0.5">
                ${c.battles.map(b => `<button onclick="jumpToBattleOnMap('${b.id}')" class="px-2 py-0.5 rounded bg-amber-500/15 border border-amber-500/40 text-amber-300 text-[10px] font-semibold hover:bg-amber-500/30">
                  🌍 Map Zoom: ${b.name} (${b.year})
                </button>`).join('')}
              </div>` : ''}
            </div>
          `).join('') : '<div class="text-xs text-[var(--muted-foreground)]">Deterrence / post-war deployment without recorded direct tank-on-tank duel in dataset.</div>'}
        </div>

        <!-- Lineage Evolution Chain -->
        <div class="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-3.5 flex flex-col gap-2">
          <div class="text-xs font-bold text-emerald-400 uppercase tracking-wider">🟢 Lineage &amp; Evolutionary Chain</div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <div>
              <div class="text-[11px] font-semibold text-[var(--muted-foreground)] mb-1">⬅️ Evolved From (Ancestors):</div>
              ${parents.length ? parents.map(p => `
                <button onclick="selectTank('${p.tank.id}')" class="w-full text-left p-2 rounded bg-[var(--card)] border border-[var(--border)] hover:border-emerald-500 mb-1 block">
                  <div class="text-xs font-bold text-emerald-300">${NATION_MAP[p.tank.nation].flag} ${p.tank.name}</div>
                  <div class="text-[10px] text-[var(--muted-foreground)]">${p.label}</div>
                </button>
              `).join('') : '<div class="text-xs text-[var(--muted-foreground)] italic">Foundational 1st-Gen Design</div>'}
            </div>
            <div>
              <div class="text-[11px] font-semibold text-[var(--muted-foreground)] mb-1">➡️ Evolved Into (Successors):</div>
              ${children.length ? children.map(c => `
                <button onclick="selectTank('${c.tank.id}')" class="w-full text-left p-2 rounded bg-[var(--card)] border border-[var(--border)] hover:border-emerald-500 mb-1 block">
                  <div class="text-xs font-bold text-emerald-300">${NATION_MAP[c.tank.nation].flag} ${c.tank.name}</div>
                  <div class="text-[10px] text-[var(--muted-foreground)]">${c.label}</div>
                </button>
              `).join('') : '<div class="text-xs text-[var(--muted-foreground)] italic">Current-Generation Pinnacle</div>'}
            </div>
          </div>
        </div>

        <!-- Design Similarity & Tech Transfer -->
        <div class="bg-sky-500/10 border border-sky-500/30 rounded-xl p-3.5 flex flex-col gap-2">
          <div class="text-xs font-bold text-sky-400 uppercase tracking-wider">🔵 Design Similarity, Shared Gun/Armor &amp; Counter-Designs</div>
          ${similar.length ? similar.map(s => `
            <button onclick="selectTank('${s.tank.id}')" class="w-full text-left p-2 rounded bg-[var(--card)] border border-[var(--border)] hover:border-sky-400 flex items-center justify-between gap-2">
              <div>
                <div class="text-xs font-bold text-sky-300">${NATION_MAP[s.tank.nation].flag} ${s.tank.name} (${s.tank.year})</div>
                <div class="text-[11px] text-[var(--muted-foreground)]">${s.label}</div>
              </div>
              <span class="text-xs text-sky-400 font-bold">Inspect →</span>
            </button>
          `).join('') : '<div class="text-xs text-[var(--muted-foreground)]">Unique indigenous architecture.</div>'}
        </div>

        <!-- Key Technical Innovations -->
        <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-3.5">
          <div class="text-xs font-bold text-amber-400 uppercase tracking-wider mb-1.5">🔧 Defining Engineering Innovations</div>
          <ul class="list-disc list-inside text-xs text-[var(--foreground)] space-y-1">
            ${(t.innovations || []).map(inv => `<li>${inv}</li>`).join('')}
          </ul>
        </div>
      `;
    }
'''

print("Appended JS part 1 to render_html.py")

JS_ENGINE_PART2 = r'''
    // =========================================================================
    // 1. INTERACTIVE GRAPH CANVAS (LINEAGE, SIMILARITY & COMBAT LINKS)
    // =========================================================================
    let graphNodeScreenPositions = [];

    function zoomGraph(factor) {
      state.gCam.k = Math.min(3.5, Math.max(0.55, state.gCam.k * factor));
    }

    function resetGraphCamera() {
      state.gCam.x = 0;
      state.gCam.y = 0;
      state.gCam.k = 1.0;
    }

    function setupGraphCanvas() {
      const canvas = document.getElementById('tank-graph-canvas');
      if (!canvas) return;

      canvas.addEventListener('mousedown', (e) => {
        state.gCam.dragging = true;
        state.gCam.moved = false;
        state.gCam.sx = e.clientX - state.gCam.x;
        state.gCam.sy = e.clientY - state.gCam.y;
      });

      window.addEventListener('mouseup', () => {
        state.gCam.dragging = false;
      });

      canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        if (state.gCam.dragging) {
          const dx = (e.clientX - state.gCam.sx) - state.gCam.x;
          const dy = (e.clientY - state.gCam.sy) - state.gCam.y;
          if (Math.hypot(dx, dy) > 4) state.gCam.moved = true;
          state.gCam.x = e.clientX - state.gCam.sx;
          state.gCam.y = e.clientY - state.gCam.sy;
          return;
        }

        // Hit-test nodes
        let hit = null;
        for (let i = graphNodeScreenPositions.length - 1; i >= 0; i--) {
          const n = graphNodeScreenPositions[i];
          if (mx >= n.sx - n.hw && mx <= n.sx + n.hw && my >= n.sy - n.hh && my <= n.sy + n.hh) {
            hit = n.id;
            break;
          }
        }
        state.hoveredTankId = hit;
        canvas.style.cursor = hit ? 'pointer' : (state.gCam.dragging ? 'grabbing' : 'grab');
      });

      canvas.addEventListener('click', (e) => {
        if (state.gCam.moved) return;
        if (state.hoveredTankId) {
          selectTank(state.hoveredTankId);
        }
      });

      canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        const factor = e.deltaY < 0 ? 1.12 : 0.89;
        const nextK = Math.min(3.5, Math.max(0.55, state.gCam.k * factor));
        const ratio = nextK / state.gCam.k;
        state.gCam.x = mx - (mx - state.gCam.x) * ratio;
        state.gCam.y = my - (my - state.gCam.y) * ratio;
        state.gCam.k = nextK;
      }, { passive: false });
    }

    function drawGraphCanvas() {
      const canvas = document.getElementById('tank-graph-canvas');
      if (!canvas || state.mainView !== 'graph') return;
      const rect = canvas.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;

      const dpr = window.devicePixelRatio || 1;
      if (canvas.width !== Math.floor(rect.width * dpr) || canvas.height !== Math.floor(rect.height * dpr)) {
        canvas.width = Math.floor(rect.width * dpr);
        canvas.height = Math.floor(rect.height * dpr);
      }

      const ctx = canvas.getContext('2d');
      ctx.save();
      ctx.scale(dpr, dpr);
      const W = rect.width;
      const H = rect.height;

      // Clear background
      ctx.fillStyle = '#090e17';
      ctx.fillRect(0, 0, W, H);

      // Apply camera transform
      ctx.save();
      ctx.translate(state.gCam.x, state.gCam.y);
      ctx.scale(state.gCam.k, state.gCam.k);

      const padLeft = 145, padRight = 55, padTop = 78, padBottom = 42;
      const usableW = Math.max(800, W) - padLeft - padRight;
      const usableH = Math.max(520, H) - padTop - padBottom;
      const colW = usableW / 7;

      // Draw Era Vertical Columns
      ERAS.forEach((era, idx) => {
        const x0 = padLeft + idx * colW;
        ctx.fillStyle = idx % 2 === 0 ? 'rgba(30, 41, 59, 0.24)' : 'rgba(15, 23, 42, 0.14)';
        ctx.fillRect(x0, padTop - 36, colW, usableH + 56);

        ctx.strokeStyle = 'rgba(148, 163, 184, 0.14)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(x0, padTop - 36);
        ctx.lineTo(x0, padTop + usableH + 20);
        ctx.stroke();

        // Era Header Label
        ctx.fillStyle = state.eraFilter === era.id ? '#fbbf24' : '#cbd5e1';
        ctx.font = 'bold 11px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(era.short.toUpperCase(), x0 + colW / 2, padTop - 20);
        ctx.fillStyle = '#64748b';
        ctx.font = '10px JetBrains Mono, monospace';
        ctx.fillText(era.years, x0 + colW / 2, padTop - 7);
      });

      // Draw Horizontal Lanes (Nations or Combat Weight)
      if (state.yMode === 'nation') {
        const laneH = usableH / 7;
        NATIONS.forEach((nat, idx) => {
          const y0 = padTop + idx * laneH;
          ctx.strokeStyle = 'rgba(148, 163, 184, 0.12)';
          ctx.beginPath();
          ctx.moveTo(12, y0);
          ctx.lineTo(padLeft + usableW + 25, y0);
          ctx.stroke();

          // Nation Pill on Left
          ctx.fillStyle = nat.color + '22';
          ctx.strokeStyle = nat.color + '88';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.roundRect(12, y0 + laneH / 2 - 15, 122, 30, 6);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = '#f8fafc';
          ctx.font = 'bold 11px Inter, sans-serif';
          ctx.textAlign = 'left';
          ctx.fillText(`${nat.flag} ${nat.short}`, 20, y0 + laneH / 2 + 4);
        });
      } else {
        // Weight bands (10t to 70t)
        [10, 25, 40, 55, 70].forEach(wt => {
          const normW = (wt - 5) / 65;
          const y = padTop + (1 - normW) * usableH;
          ctx.strokeStyle = 'rgba(148, 163, 184, 0.15)';
          ctx.setLineDash([4, 4]);
          ctx.beginPath();
          ctx.moveTo(padLeft - 40, y);
          ctx.lineTo(padLeft + usableW + 20, y);
          ctx.stroke();
          ctx.setLineDash([]);
          ctx.fillStyle = '#94a3b8';
          ctx.font = 'bold 11px JetBrains Mono, monospace';
          ctx.textAlign = 'right';
          ctx.fillText(`${wt} tons`, padLeft - 12, y + 4);
        });
      }

      // Compute visible tanks and node positions
      const focusId = state.hoveredTankId || state.selectedTankId;
      const posMap = {};
      const visMap = {};
      TANKS.forEach(t => {
        posMap[t.id] = getGraphNodePos(t, W, H);
        visMap[t.id] = isTankVisible(t);
      });

      // Determine neighbor set of focusId
      const neighborIds = new Set([focusId]);
      const combatRivalIds = new Set();
      EDGES.forEach(e => {
        if (!state.layers[e.type]) return;
        if (e.source === focusId) {
          neighborIds.add(e.target);
          if (e.type === 'combat') combatRivalIds.add(e.target);
        }
        if (e.target === focusId) {
          neighborIds.add(e.source);
          if (e.type === 'combat') combatRivalIds.add(e.source);
        }
      });

      // Update status label
      const visibleCount = TANKS.filter(t => visMap[t.id]).length;
      const activeEdgeCount = EDGES.filter(e => state.layers[e.type] && visMap[e.source] && visMap[e.target]).length;
      const statusEl = document.getElementById('graph-status-label');
      if (statusEl) {
        statusEl.textContent = `${visibleCount} tanks & ${activeEdgeCount} active relationships shown • Focus: ${TANK_MAP[focusId]?.name || ''}`;
      }

      // Draw Edges (Non-focused first, then focused on top)
      const sortedEdges = [...EDGES].sort((a, b) => {
        const aFocus = (a.source === focusId || a.target === focusId) ? 1 : 0;
        const bFocus = (b.source === focusId || b.target === focusId) ? 1 : 0;
        return aFocus - bFocus;
      });

      sortedEdges.forEach(e => {
        if (!state.layers[e.type]) return;
        if (!visMap[e.source] && !visMap[e.target]) return;
        const p1 = posMap[e.source];
        const p2 = posMap[e.target];
        if (!p1 || !p2) return;

        const isFocused = (e.source === focusId || e.target === focusId);
        const alpha = isFocused ? 0.96 : 0.22;

        ctx.save();
        ctx.beginPath();
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        const cx1 = p1.x + dx * 0.42;
        const cy1 = p1.y + (e.type === 'combat' ? -26 : 0);
        const cx2 = p1.x + dx * 0.58;
        const cy2 = p2.y + (e.type === 'combat' ? -26 : 0);

        ctx.moveTo(p1.x, p1.y);
        ctx.bezierCurveTo(cx1, cy1, cx2, cy2, p2.x, p2.y);

        if (e.type === 'lineage') {
          ctx.strokeStyle = isFocused ? '#34d399' : `rgba(52, 211, 153, ${alpha})`;
          ctx.lineWidth = isFocused ? 2.6 : 1.3;
          ctx.stroke();

          // Animated flow particle on focused lineage edges
          if (isFocused) {
            const tAnim = ((state.animTick * 0.012) % 1);
            const u = 1 - tAnim;
            const px = u*u*u*p1.x + 3*u*u*tAnim*cx1 + 3*u*tAnim*tAnim*cx2 + tAnim*tAnim*tAnim*p2.x;
            const py = u*u*u*p1.y + 3*u*u*tAnim*cy1 + 3*u*tAnim*tAnim*cy2 + tAnim*tAnim*tAnim*p2.y;
            ctx.fillStyle = '#a7f3d0';
            ctx.beginPath();
            ctx.arc(px, py, 3.2, 0, Math.PI * 2);
            ctx.fill();
          }
        } else if (e.type === 'similarity') {
          ctx.setLineDash([5, 4]);
          ctx.strokeStyle = isFocused ? '#38bdf8' : `rgba(56, 189, 248, ${alpha})`;
          ctx.lineWidth = isFocused ? 2.2 : 1.15;
          ctx.stroke();
          ctx.setLineDash([]);
        } else if (e.type === 'combat') {
          ctx.strokeStyle = isFocused ? '#f43f5e' : `rgba(244, 63, 94, ${alpha})`;
          ctx.lineWidth = isFocused ? 2.6 : 1.25;
          ctx.stroke();

          if (isFocused) {
            // Midpoint crossed-swords badge
            const mx = 0.125*p1.x + 0.375*cx1 + 0.375*cx2 + 0.125*p2.x;
            const my = 0.125*p1.y + 0.375*cy1 + 0.375*cy2 + 0.125*p2.y;
            ctx.fillStyle = '#881337';
            ctx.strokeStyle = '#fb7185';
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.arc(mx, my, 8.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = '#fff';
            ctx.font = '10px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('⚔', mx, my + 3.5);
          }
        }
        ctx.restore();
      });

      // Draw Tank Nodes
      graphNodeScreenPositions = [];
      TANKS.forEach(t => {
        if (!visMap[t.id]) return;
        const p = posMap[t.id];
        const nat = NATION_MAP[t.nation];
        const isSelected = t.id === state.selectedTankId;
        const isHovered = t.id === state.hoveredTankId;
        const isNeighbor = neighborIds.has(t.id);
        const isRival = combatRivalIds.has(t.id);

        const bw = isSelected || isHovered ? 112 : 98;
        const bh = isSelected || isHovered ? 38 : 33;
        const bx = p.x - bw / 2;
        const by = p.y - bh / 2;

        ctx.save();
        ctx.globalAlpha = isNeighbor ? 1.0 : 0.38;

        // Glow for selected or rival
        if (isSelected || isHovered) {
          ctx.shadowColor = '#f59e0b';
          ctx.shadowBlur = 16;
        } else if (isRival) {
          ctx.shadowColor = '#f43f5e';
          ctx.shadowBlur = 12;
        }

        ctx.fillStyle = isSelected ? '#1e293b' : '#0f172a';
        ctx.strokeStyle = isSelected ? '#fbbf24' : (isRival ? '#f43f5e' : nat.color);
        ctx.lineWidth = isSelected || isHovered ? 2.4 : (isRival ? 2.0 : 1.3);

        ctx.beginPath();
        ctx.roundRect(bx, by, bw, bh, 7);
        ctx.fill();
        ctx.stroke();
        ctx.shadowBlur = 0;

        // Top Nation Color Accent Bar
        ctx.fillStyle = nat.color;
        ctx.beginPath();
        ctx.roundRect(bx + 2, by + 2, bw - 4, 4, 2);
        ctx.fill();

        // Tank Name
        ctx.fillStyle = '#f8fafc';
        ctx.font = (isSelected || isHovered ? 'bold 10.5px' : 'bold 9.5px') + ' Inter, sans-serif';
        ctx.textAlign = 'center';
        const shortName = t.name.length > 15 ? t.name.slice(0, 14) + '…' : t.name;
        ctx.fillText(shortName, p.x, p.y + 1);

        // Year & Weight sub-label
        ctx.fillStyle = isRival ? '#fda4af' : '#94a3b8';
        ctx.font = '8.5px JetBrains Mono, monospace';
        ctx.fillText(`${t.year} • ${t.weight_t}t`, p.x, p.y + 12);

        // Rival Sword Badge
        if (isRival && !isSelected) {
          ctx.fillStyle = '#e11d48';
          ctx.beginPath();
          ctx.arc(bx + bw - 4, by + 4, 7.5, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#fff';
          ctx.font = '9px sans-serif';
          ctx.fillText('⚔', bx + bw - 4, by + 7);
        }

        ctx.restore();

        // Store screen space bounds for mouse hit testing
        const sx = p.x * state.gCam.k + state.gCam.x;
        const sy = p.y * state.gCam.k + state.gCam.y;
        graphNodeScreenPositions.push({
          id: t.id,
          sx,
          sy,
          hw: (bw / 2) * state.gCam.k + 4,
          hh: (bh / 2) * state.gCam.k + 4
        });
      });

      ctx.restore();
      ctx.restore();
    }

    // =========================================================================
    // 2. WORLD TANK BATTLES MAP & TACTICAL BATTLEFIELD SCHEMATIC ZOOM-IN
    // =========================================================================
    let mapBattleScreenPins = [];

    const THEATRE_PRESETS = {
      WORLD:              { lon: 25.0, lat: 34.0, k: 1.75 },
      EUROPE_WEST:        { lon: 3.5,  lat: 49.8, k: 8.5  },
      EUROPE_EAST:        { lon: 33.5, lat: 50.8, k: 6.2  },
      NORTH_AFRICA_SINAI: { lon: 32.2, lat: 31.2, k: 7.5  },
      GULF_ME:            { lon: 46.5, lat: 30.8, k: 7.8  },
      ASIA:               { lon: 105.0, lat: 37.5, k: 3.8 }
    };

    function lonLatToScreen(lon, lat, W, H) {
      const baseScale = (W / 360) * state.mCam.k;
      const x = W / 2 + (lon - state.mCam.lon) * baseScale;
      const y = H / 2 - (lat - state.mCam.lat) * baseScale * 1.18;
      return { x, y };
    }

    function flyToTheatre(key) {
      const p = THEATRE_PRESETS[key] || THEATRE_PRESETS.WORLD;
      state.mCam.targetLon = p.lon;
      state.mCam.targetLat = p.lat;
      state.mCam.targetK = p.k;
      state.tacticalZoomOpen = false;
      updateTacticalOverlayVisibility();
    }

    function zoomMapBy(factor) {
      state.mCam.targetK = Math.min(18.0, Math.max(1.1, state.mCam.targetK * factor));
    }

    function jumpToBattleOnMap(battleId) {
      const b = BATTLE_MAP[battleId];
      if (!b) return;
      switchMainView('map');
      selectBattle(battleId, true);
    }

    function selectBattle(battleId, zoomTo = false) {
      const b = BATTLE_MAP[battleId];
      if (!b) return;
      state.selectedBattleId = battleId;
      if (zoomTo) {
        state.mCam.targetLon = b.lon;
        state.mCam.targetLat = b.lat;
        state.mCam.targetK = Math.max(state.mCam.targetK, 7.2);
      }
      renderMapBattleStrip();
      renderBattleInspector();
      if (state.tacticalZoomOpen) {
        drawTacticalSchematic();
      }
    }

    function toggleTacticalZoomModal(forceState) {
      state.tacticalZoomOpen = typeof forceState === 'boolean' ? forceState : !state.tacticalZoomOpen;
      updateTacticalOverlayVisibility();
    }

    function updateTacticalOverlayVisibility() {
      const overlay = document.getElementById('tactical-zoom-overlay');
      const btn = document.getElementById('btn-tactical-toggle');
      if (!overlay || !btn) return;
      if (state.tacticalZoomOpen) {
        overlay.classList.remove('hidden');
        overlay.classList.add('flex');
        btn.textContent = '🌍 Return to World Map View';
        drawTacticalSchematic();
      } else {
        overlay.classList.add('hidden');
        overlay.classList.remove('flex');
        btn.textContent = '🎯 Open Tactical Battlefield Schematic Zoom';
      }
    }

    function setupMapCanvas() {
      const canvas = document.getElementById('world-map-canvas');
      if (!canvas) return;

      canvas.addEventListener('mousedown', (e) => {
        state.mCam.dragging = true;
        state.mCam.moved = false;
        state.mCam.sx = e.clientX;
        state.mCam.sy = e.clientY;
      });

      window.addEventListener('mouseup', () => {
        state.mCam.dragging = false;
      });

      canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        if (state.mCam.dragging) {
          const dx = e.clientX - state.mCam.sx;
          const dy = e.clientY - state.mCam.sy;
          if (Math.hypot(dx, dy) > 3) state.mCam.moved = true;
          const baseScale = (rect.width / 360) * state.mCam.k;
          state.mCam.lon -= dx / baseScale;
          state.mCam.lat += dy / (baseScale * 1.18);
          state.mCam.targetLon = state.mCam.lon;
          state.mCam.targetLat = state.mCam.lat;
          state.mCam.sx = e.clientX;
          state.mCam.sy = e.clientY;
          return;
        }

        // Hit-test battle markers
        let hit = null;
        for (let i = mapBattleScreenPins.length - 1; i >= 0; i--) {
          const pin = mapBattleScreenPins[i];
          if (Math.hypot(mx - pin.x, my - pin.y) <= pin.r + 6) {
            hit = pin.id;
            break;
          }
        }
        state.hoveredBattleId = hit;
        canvas.style.cursor = hit ? 'pointer' : (state.mCam.dragging ? 'grabbing' : 'grab');
      });

      canvas.addEventListener('click', () => {
        if (state.mCam.moved) return;
        if (state.hoveredBattleId) {
          selectBattle(state.hoveredBattleId, true);
        }
      });

      canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        const factor = e.deltaY < 0 ? 1.18 : 0.85;
        state.mCam.targetK = Math.min(18.0, Math.max(1.1, state.mCam.targetK * factor));
      }, { passive: false });
    }

    function drawWorldMap() {
      const canvas = document.getElementById('world-map-canvas');
      if (!canvas || state.mainView !== 'map') return;
      const rect = canvas.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;

      const dpr = window.devicePixelRatio || 1;
      if (canvas.width !== Math.floor(rect.width * dpr) || canvas.height !== Math.floor(rect.height * dpr)) {
        canvas.width = Math.floor(rect.width * dpr);
        canvas.height = Math.floor(rect.height * dpr);
      }

      // Smoothly interpolate map camera
      state.mCam.lon += (state.mCam.targetLon - state.mCam.lon) * 0.14;
      state.mCam.lat += (state.mCam.targetLat - state.mCam.lat) * 0.14;
      state.mCam.k += (state.mCam.targetK - state.mCam.k) * 0.14;

      const readout = document.getElementById('map-zoom-readout');
      if (readout) {
        const b = BATTLE_MAP[state.selectedBattleId];
        readout.textContent = `Camera Zoom: ${state.mCam.k.toFixed(1)}x • Focus: ${b ? b.name + ' (' + b.year + ')' : ''} [${state.mCam.lat.toFixed(1)}°N, ${state.mCam.lon.toFixed(1)}°E]`;
      }

      const ctx = canvas.getContext('2d');
      ctx.save();
      ctx.scale(dpr, dpr);
      const W = rect.width;
      const H = rect.height;

      // Deep Naval Ocean Gradient
      const grad = ctx.createLinearGradient(0, 0, 0, H);
      grad.addColorStop(0, '#06101e');
      grad.addColorStop(1, '#0a192f');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, W, H);

      // Draw Lat/Lon Graticule Grid
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.08)';
      ctx.lineWidth = 1;
      const stepDeg = state.mCam.k > 5 ? 5 : (state.mCam.k > 2.5 ? 10 : 20);
      for (let lon = -160; lon <= 180; lon += stepDeg) {
        const p = lonLatToScreen(lon, 0, W, H);
        if (p.x >= 0 && p.x <= W) {
          ctx.beginPath();
          ctx.moveTo(p.x, 0);
          ctx.lineTo(p.x, H);
          ctx.stroke();
          ctx.fillStyle = 'rgba(148, 163, 184, 0.35)';
          ctx.font = '9px JetBrains Mono, monospace';
          ctx.fillText(`${lon}°`, p.x + 3, 14);
        }
      }
      for (let lat = -60; lat <= 75; lat += stepDeg) {
        const p = lonLatToScreen(0, lat, W, H);
        if (p.y >= 0 && p.y <= H) {
          ctx.beginPath();
          ctx.moveTo(0, p.y);
          ctx.lineTo(W, p.y);
          ctx.stroke();
          ctx.fillStyle = 'rgba(148, 163, 184, 0.35)';
          ctx.font = '9px JetBrains Mono, monospace';
          ctx.fillText(`${lat}°`, 6, p.y - 3);
        }
      }

      // Draw World Landmass Polygons
      WORLD_POLYGONS.forEach(poly => {
        const pts = poly.pts || poly.points || [];
        ctx.beginPath();
        pts.forEach((pt, idx) => {
          const s = lonLatToScreen(pt[0], pt[1], W, H);
          if (idx === 0) ctx.moveTo(s.x, s.y);
          else ctx.lineTo(s.x, s.y);
        });
        ctx.closePath();
        ctx.fillStyle = '#13263b';
        ctx.fill();
        ctx.strokeStyle = '#2dd4bf55';
        ctx.lineWidth = 1.2;
        ctx.stroke();
      });

      // Draw Chronological Campaign Arcs between sequential battles
      ctx.save();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = 'rgba(251, 191, 36, 0.22)';
      ctx.lineWidth = 1.2;
      for (let i = 0; i < BATTLES.length - 1; i++) {
        const b1 = BATTLES[i];
        const b2 = BATTLES[i + 1];
        if (b1.era === b2.era) {
          const s1 = lonLatToScreen(b1.lon, b1.lat, W, H);
          const s2 = lonLatToScreen(b2.lon, b2.lat, W, H);
          ctx.beginPath();
          ctx.moveTo(s1.x, s1.y);
          ctx.lineTo(s2.x, s2.y);
          ctx.stroke();
        }
      }
      ctx.restore();

      // Draw Battle Markers
      mapBattleScreenPins = [];
      const pulse = (Math.sin(state.animTick * 0.08) + 1) * 0.5;

      BATTLES.forEach(b => {
        const s = lonLatToScreen(b.lon, b.lat, W, H);
        if (s.x < -60 || s.x > W + 60 || s.y < -60 || s.y > H + 60) return;

        const isSel = b.id === state.selectedBattleId;
        const isHov = b.id === state.hoveredBattleId;
        const r = isSel ? 9 : (isHov ? 8 : 6);

        // Pulsing Radar Ring
        if (isSel || isHov) {
          ctx.strokeStyle = isSel ? `rgba(251, 191, 36, ${0.8 - pulse * 0.55})` : 'rgba(244, 63, 94, 0.7)';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.arc(s.x, s.y, r + 5 + pulse * 11, 0, Math.PI * 2);
          ctx.stroke();
        }

        // Outer & Inner Pin
        ctx.fillStyle = isSel ? '#f59e0b' : '#e11d48';
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = isSel ? 2.2 : 1.4;
        ctx.beginPath();
        ctx.arc(s.x, s.y, r, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        // Label Pill
        if (state.mCam.k >= 2.2 || isSel || isHov) {
          const label = `${b.year} ${b.name.replace('Battle of ', '')}`;
          ctx.font = (isSel ? 'bold 11px' : '600 10px') + ' Inter, sans-serif';
          const tw = ctx.measureText(label).width;
          const px = s.x - tw / 2 - 6;
          const py = s.y - r - 22;

          ctx.fillStyle = isSel ? 'rgba(15, 23, 42, 0.95)' : 'rgba(15, 23, 42, 0.82)';
          ctx.strokeStyle = isSel ? '#fbbf24' : 'rgba(244, 63, 94, 0.6)';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.roundRect(px, py, tw + 12, 18, 4);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = isSel ? '#fde68a' : '#f1f5f9';
          ctx.textAlign = 'center';
          ctx.fillText(label, s.x, py + 12.5);
        }

        // High-Zoom On-Map Tactical Formation Callout (when zoomed >= 5.0x on selected battle)
        if (isSel && state.mCam.k >= 5.0) {
          ctx.fillStyle = 'rgba(15, 23, 42, 0.92)';
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 1.2;
          ctx.beginPath();
          ctx.roundRect(s.x - 135, s.y + 14, 270, 44, 6);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = '#38bdf8';
          ctx.font = 'bold 9.5px Inter, sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText(`🟦 ${b.side_a.flag || ''} ${b.side_a.name.slice(0,22)} vs 🟥 ${b.side_b.flag || ''} ${b.side_b.name.slice(0,22)}`, s.x, s.y + 29);
          ctx.fillStyle = '#fde68a';
          ctx.font = '9px JetBrains Mono, monospace';
          ctx.fillText(`Scale: ${(b.total_tanks || '').slice(0, 40)}`, s.x, s.y + 43);
        }

        mapBattleScreenPins.push({ id: b.id, x: s.x, y: s.y, r });
      });

      ctx.restore();
    }

    function renderMapBattleStrip() {
      const strip = document.getElementById('map-battle-strip');
      if (!strip) return;
      strip.innerHTML = BATTLES.map(b => {
        const active = b.id === state.selectedBattleId;
        return `
          <button onclick="selectBattle('${b.id}', true)" class="shrink-0 px-2.5 py-1.5 rounded-md border text-left transition ${
            active
              ? 'bg-amber-500/20 border-amber-400 text-amber-200 shadow-sm'
              : 'bg-[var(--background)]/90 border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]'
          }">
            <div class="text-[10px] font-mono font-bold text-rose-400">${b.year} • ${b.theatre}</div>
            <div class="text-xs font-bold whitespace-nowrap">${b.name.replace('Battle of ', '')}</div>
          </button>
        `;
      }).join('');
    }

    function renderBattleInspector() {
      const b = BATTLE_MAP[state.selectedBattleId] || BATTLES[0];
      const el = document.getElementById('battle-inspector');
      if (!el) return;

      const renderTankPills = (tankIds, colorCls) => tankIds.map(tid => {
        const t = TANK_MAP[tid];
        if (!t) return '';
        return `
          <button onclick="selectTank('${t.id}', true)" class="px-2.5 py-1 rounded-md bg-[var(--card)] border ${colorCls} text-xs font-semibold hover:scale-[1.02] transition flex items-center gap-1.5">
            <span>${NATION_MAP[t.nation]?.flag || ''} ${t.name}</span>
            <span class="text-[10px] opacity-75">(${t.gun.split(' ')[0]})</span>
          </button>`;
      }).join('');

      const leadA = b.side_a.tanks[0] || 't34_76';
      const leadB = b.side_b.tanks[0] || 'tiger_i';

      el.innerHTML = `
        <div class="border-b border-[var(--border)] pb-3">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">
              ⚔️ ${b.date} • ${b.theatre}
            </span>
            <span class="text-xs font-mono text-amber-400">[${b.lat.toFixed(2)}°N, ${b.lon.toFixed(2)}°E]</span>
          </div>
          <h2 class="text-xl font-bold text-[var(--foreground)] mt-2">${b.name}</h2>
          <p class="text-xs text-[var(--muted-foreground)] mt-0.5">📍 ${b.location}</p>
          <div class="mt-2.5 p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-xs font-semibold text-amber-300">
            📊 Scale: ${b.total_tanks}
          </div>
        </div>

        <!-- Action Buttons: Tactical Zoom-In & Duel -->
        <div class="grid grid-cols-2 gap-2">
          <button onclick="toggleTacticalZoomModal(true)" class="px-3 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold shadow-sm transition flex items-center justify-center gap-1.5">
            🎯 Tactical Battlefield Zoom-In
          </button>
          <button onclick="setDuelPair('${leadA}','${leadB}'); switchMainView('duel')" class="px-3 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold shadow-sm transition flex items-center justify-center gap-1.5">
            ⚔️ Compare Lead Tanks in Duel
          </button>
        </div>

        <!-- Opposing Armored Forces -->
        <div class="grid grid-cols-1 gap-3">
          <div class="bg-sky-500/10 border border-sky-500/30 rounded-xl p-3">
            <div class="flex items-center justify-between text-xs">
              <span class="font-bold text-sky-400">🟦 ${b.side_a.flag || ''} ${b.side_a.name}</span>
            </div>
            <div class="text-[11px] text-[var(--foreground)] font-medium mt-1">Order of Battle: ${b.side_a.count}</div>
            <div class="flex flex-wrap gap-1.5 mt-2">
              ${renderTankPills(b.side_a.tanks, 'border-sky-500/50 text-sky-200')}
            </div>
          </div>

          <div class="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3">
            <div class="flex items-center justify-between text-xs">
              <span class="font-bold text-rose-400">🟥 ${b.side_b.flag || ''} ${b.side_b.name}</span>
            </div>
            <div class="text-[11px] text-[var(--foreground)] font-medium mt-1">Order of Battle: ${b.side_b.count}</div>
            <div class="flex flex-wrap gap-1.5 mt-2">
              ${renderTankPills(b.side_b.tanks, 'border-rose-500/50 text-rose-200')}
            </div>
          </div>
        </div>

        <!-- Tactical Narrative & Outcome -->
        <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-3.5 flex flex-col gap-2">
          <div class="text-xs font-bold text-amber-400 uppercase tracking-wider">📖 Combat Engagement &amp; Tactical Analysis</div>
          <p class="text-xs text-[var(--foreground)] leading-relaxed">${b.summary}</p>
          <div class="pt-2 border-t border-[var(--border)] text-xs">
            <span class="font-bold text-emerald-400">Outcome:</span>
            <span class="text-[var(--foreground)]"> ${b.outcome}</span>
          </div>
        </div>

        <!-- Tactical Terrain & Engagement Parameters -->
        <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-3.5 text-xs flex flex-col gap-1.5">
          <div class="font-bold text-sky-400 uppercase tracking-wider">🗺️ Battlefield Terrain &amp; Engagement Range</div>
          <div><span class="text-[var(--muted-foreground)]">Terrain:</span> <span class="font-semibold">${b.tactical_zoom.terrain}</span></div>
          <div><span class="text-[var(--muted-foreground)]">Combat Range:</span> <span class="font-semibold text-amber-300">${b.tactical_zoom.range_m}</span></div>
          <div><span class="text-[var(--muted-foreground)]">Key Doctrinal Lesson:</span> <span>${b.tactical_zoom.key_lesson}</span></div>
        </div>
      `;
    }

    function drawTacticalSchematic() {
      const canvas = document.getElementById('tactical-schematic-canvas');
      if (!canvas || !state.tacticalZoomOpen) return;
      const b = BATTLE_MAP[state.selectedBattleId] || BATTLES[0];

      const titleEl = document.getElementById('tac-overlay-title');
      if (titleEl) titleEl.textContent = `${b.name} (${b.date}) — ${b.tactical_zoom.terrain}`;

      const footerEl = document.getElementById('tac-overlay-footer');
      if (footerEl) {
        footerEl.innerHTML = `
          <div><strong class="text-amber-400">Combat Range:</strong> ${b.tactical_zoom.range_m}</div>
          <div><strong class="text-emerald-400">Key Lesson:</strong> ${b.tactical_zoom.key_lesson}</div>
        `;
      }

      const rect = canvas.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;
      const dpr = window.devicePixelRatio || 1;
      canvas.width = Math.floor(rect.width * dpr);
      canvas.height = Math.floor(rect.height * dpr);

      const ctx = canvas.getContext('2d');
      ctx.save();
      ctx.scale(dpr, dpr);
      const W = rect.width;
      const H = rect.height;

      // Topographic Battlefield Background
      ctx.fillStyle = '#091622';
      ctx.fillRect(0, 0, W, H);

      // Tactical Grid Lines (1 km grid squares)
      ctx.strokeStyle = 'rgba(45, 212, 191, 0.11)';
      ctx.lineWidth = 1;
      for (let x = 0; x < W; x += 60) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
      }
      for (let y = 0; y < H; y += 60) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
      }

      // Topographic Elevation Contours
      ctx.strokeStyle = 'rgba(251, 191, 36, 0.14)';
      ctx.lineWidth = 1.2;
      [0.25, 0.5, 0.75].forEach((cxRatio, idx) => {
        ctx.beginPath();
        ctx.ellipse(W * cxRatio, H * (0.35 + (idx % 2) * 0.3), 130, 65, 0.3 * idx, 0, Math.PI * 2);
        ctx.stroke();
      });

      // Line of Contact / Front Line
      ctx.save();
      ctx.setLineDash([8, 6]);
      ctx.strokeStyle = 'rgba(244, 63, 94, 0.45)';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(W * 0.50, 20);
      ctx.bezierCurveTo(W * 0.44, H * 0.35, W * 0.56, H * 0.65, W * 0.49, H - 20);
      ctx.stroke();
      ctx.restore();

      // Draw Armored Units & Attack Vectors from b.tactical_zoom.formations
      const units = b.tactical_zoom.formations || [];
      const sideAUnits = units.filter(u => u.side === 'A');
      const sideBUnits = units.filter(u => u.side === 'B');

      // Draw animated tank-to-tank firing lines between Side A and Side B units
      if (sideAUnits.length && sideBUnits.length) {
        sideAUnits.forEach((ua, i) => {
          const ub = sideBUnits[i % sideBUnits.length];
          const x1 = (ua.x / 100) * W;
          const y1 = (ua.y / 100) * H;
          const x2 = (ub.x / 100) * W;
          const y2 = (ub.y / 100) * H;

          ctx.save();
          ctx.setLineDash([3, 5]);
          ctx.strokeStyle = 'rgba(251, 191, 36, 0.55)';
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(x1, y1);
          ctx.lineTo(x2, y2);
          ctx.stroke();
          ctx.restore();

          // Animated APFSDS / AP shell tracer
          const tTracer = ((state.animTick * 0.02 + i * 0.33) % 1);
          const sx = x1 + (x2 - x1) * tTracer;
          const sy = y1 + (y2 - y1) * tTracer;
          ctx.fillStyle = '#fde047';
          ctx.beginPath();
          ctx.arc(sx, sy, 3.8, 0, Math.PI * 2);
          ctx.fill();
        });
      }

      // Render Each Tactical Unit Block (NATO-style armor symbol + maneuver vector to tx,ty + label)
      units.forEach(u => {
        const ux = (u.x / 100) * W;
        const uy = (u.y / 100) * H;
        const tx = ((u.tx ?? (u.side === 'A' ? u.x + 15 : u.x - 15)) / 100) * W;
        const ty = ((u.ty ?? u.y) / 100) * H;
        const isA = u.side === 'A';
        const color = isA ? '#38bdf8' : '#f43f5e';
        const bg = isA ? 'rgba(14, 116, 144, 0.90)' : 'rgba(136, 19, 55, 0.90)';

        // Maneuver Vector Arrow from (ux, uy) to (tx, ty)
        const angle = Math.atan2(ty - uy, tx - ux);
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.6;
        ctx.beginPath();
        ctx.moveTo(ux, uy);
        ctx.lineTo(tx, ty);
        ctx.stroke();

        // Arrowhead at (tx, ty)
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(tx - 11 * Math.cos(angle - 0.4), ty - 11 * Math.sin(angle - 0.4));
        ctx.lineTo(tx - 11 * Math.cos(angle + 0.4), ty - 11 * Math.sin(angle + 0.4));
        ctx.closePath();
        ctx.fill();

        // NATO Armor Box
        ctx.fillStyle = bg;
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.roundRect(ux - 26, uy - 16, 52, 32, 5);
        ctx.fill();
        ctx.stroke();

        // NATO Tracked Oval inside box
        ctx.strokeStyle = '#fde68a';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.ellipse(ux, uy, 15, 8, 0, 0, Math.PI * 2);
        ctx.stroke();

        // Unit Caption Pill
        ctx.font = 'bold 11px Inter, sans-serif';
        const tw = ctx.measureText(u.label).width;
        ctx.fillStyle = 'rgba(15, 23, 42, 0.92)';
        ctx.strokeStyle = color;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.roundRect(ux - tw / 2 - 8, uy + 20, tw + 16, 20, 4);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#f8fafc';
        ctx.textAlign = 'center';
        ctx.fillText(u.label, ux, uy + 34);
      });

      ctx.restore();
    }

    // =========================================================================
    // 3. HEAD-TO-HEAD TANK DUEL COMPARATOR (VIEW 3)
    // =========================================================================
    function initDuelSelects() {
      const selA = document.getElementById('duel-select-a');
      const selB = document.getElementById('duel-select-b');
      if (!selA || !selB) return;

      const opts = TANKS.map(t => `<option value="${t.id}">${NATION_MAP[t.nation].flag} ${t.name} (${t.year}) — ${t.gun}</option>`).join('');
      selA.innerHTML = opts;
      selB.innerHTML = opts;
      selA.value = state.duelA;
      selB.value = state.duelB;
    }

    function setDuelPair(idA, idB) {
      if (TANK_MAP[idA]) state.duelA = idA;
      if (TANK_MAP[idB]) state.duelB = idB;
      const selA = document.getElementById('duel-select-a');
      const selB = document.getElementById('duel-select-b');
      if (selA) selA.value = state.duelA;
      if (selB) selB.value = state.duelB;
      updateDuelView();
    }

    function updateDuelView() {
      const selA = document.getElementById('duel-select-a');
      const selB = document.getElementById('duel-select-b');
      if (selA && selA.value) state.duelA = selA.value;
      if (selB && selB.value) state.duelB = selB.value;

      const tA = TANK_MAP[state.duelA] || TANKS[0];
      const tB = TANK_MAP[state.duelB] || TANKS[1];
      const container = document.getElementById('duel-comparison-body');
      if (!container) return;

      // Check direct historical combat edge & shared battles
      const directCombatEdge = EDGES.find(e => e.type === 'combat' && ((e.source === tA.id && e.target === tB.id) || (e.source === tB.id && e.target === tA.id)));
      const sharedBattles = BATTLES.filter(b =>
        (b.side_a.tanks.includes(tA.id) && b.side_b.tanks.includes(tB.id)) ||
        (b.side_b.tanks.includes(tA.id) && b.side_a.tanks.includes(tB.id))
      );

      // Build 5-axis SVG Radar Polygon
      const axes = [
        { key: 'firepower', label: 'Firepower' },
        { key: 'armor',     label: 'Armor' },
        { key: 'mobility',  label: 'Mobility' },
        { key: 'optics',    label: 'Optics/FCS' },
        { key: 'impact',    label: 'Impact' }
      ];
      const cx = 130, cy = 125, R = 86;
      const polyPoints = (t) => axes.map((ax, i) => {
        const angle = -Math.PI / 2 + (i * 2 * Math.PI) / axes.length;
        const val = (t.stats[ax.key] || 50) / 100;
        const x = cx + Math.cos(angle) * R * val;
        const y = cy + Math.sin(angle) * R * val;
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      }).join(' ');

      const axisLabelsSvg = axes.map((ax, i) => {
        const angle = -Math.PI / 2 + (i * 2 * Math.PI) / axes.length;
        const x = cx + Math.cos(angle) * (R + 24);
        const y = cy + Math.sin(angle) * (R + 18);
        return `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" fill="#cbd5e1" font-size="10" font-weight="bold" text-anchor="middle">${ax.label}</text>`;
      }).join('');

      const cardHtml = (t, badgeColor, tag) => {
        const nat = NATION_MAP[t.nation];
        return `
          <div class="lg:col-span-4 bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 flex flex-col gap-3">
            <div class="flex items-center justify-between">
              <span class="px-2 py-0.5 rounded text-xs font-bold ${badgeColor}">${tag} • ${nat.flag} ${nat.short}</span>
              <span class="text-xs font-mono text-[var(--muted-foreground)]">${t.year} • ${t.role}</span>
            </div>
            <h3 class="text-lg font-bold text-[var(--foreground)]">${t.name}</h3>
            <p class="text-xs text-[var(--muted-foreground)] leading-relaxed">${t.summary}</p>
            <div class="grid grid-cols-2 gap-2 text-xs mt-auto pt-2 border-t border-[var(--border)]">
              <div><span class="text-[var(--muted-foreground)]">Main Gun:</span> <div class="font-bold">${t.gun}</div></div>
              <div><span class="text-[var(--muted-foreground)]">Frontal Armor:</span> <div class="font-bold text-amber-400">${t.armor_mm} mm RHAe</div></div>
              <div><span class="text-[var(--muted-foreground)]">Combat Weight:</span> <div class="font-bold">${t.weight_t} tons</div></div>
              <div><span class="text-[var(--muted-foreground)]">Top Speed:</span> <div class="font-bold text-emerald-400">${t.speed_kmh} km/h</div></div>
            </div>
          </div>
        `;
      };

      container.innerHTML = `
        ${cardHtml(tA, 'bg-sky-500/20 text-sky-300 border border-sky-500/40', 'TANK A')}

        <div class="lg:col-span-4 bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 flex flex-col items-center justify-between gap-3">
          <div class="text-xs font-bold uppercase tracking-wider text-amber-400">5-Axis Telemetry Overlay</div>
          <svg viewBox="0 0 260 250" class="w-full max-w-[260px] h-auto">
            <circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="rgba(148,163,184,0.2)" stroke-dasharray="3,3"/>
            <circle cx="${cx}" cy="${cy}" r="${R*0.66}" fill="none" stroke="rgba(148,163,184,0.15)"/>
            <circle cx="${cx}" cy="${cy}" r="${R*0.33}" fill="none" stroke="rgba(148,163,184,0.15)"/>
            <polygon points="${polyPoints(tA)}" fill="rgba(56, 189, 248, 0.28)" stroke="#38bdf8" stroke-width="2.2"/>
            <polygon points="${polyPoints(tB)}" fill="rgba(244, 63, 94, 0.28)" stroke="#f43f5e" stroke-width="2.2"/>
            ${axisLabelsSvg}
          </svg>

          <!-- Historical Combat Verification Record -->
          <div class="w-full p-3 rounded-lg border ${directCombatEdge || sharedBattles.length ? 'bg-rose-500/15 border-rose-500/40' : 'bg-[var(--card)] border-[var(--border)]'} text-xs">
            <div class="font-bold ${directCombatEdge || sharedBattles.length ? 'text-rose-300' : 'text-[var(--muted-foreground)]'}">
              ${directCombatEdge || sharedBattles.length ? '⚔️ VERIFIED HISTORICAL COMBAT OPPONENTS' : '📐 Cross-Era / Theoretical Technical Comparison'}
            </div>
            <div class="text-[11px] text-[var(--foreground)] mt-1">
              ${directCombatEdge ? directCombatEdge.label : (sharedBattles.length ? 'Fought on opposing sides in recorded armored battles.' : 'No direct historical tank-vs-tank duel recorded between these two specific models.')}
            </div>
            ${sharedBattles.length ? `
              <div class="flex flex-wrap gap-1.5 mt-2">
                ${sharedBattles.map(b => `
                  <button onclick="jumpToBattleOnMap('${b.id}')" class="px-2 py-0.5 rounded bg-amber-500/20 border border-amber-500/40 text-amber-300 text-[10px] font-bold hover:bg-amber-500/30">
                    🌍 Zoom Battle: ${b.name} (${b.year})
                  </button>
                `).join('')}
              </div>
            ` : ''}
          </div>
        </div>

        ${cardHtml(tB, 'bg-rose-500/20 text-rose-300 border border-rose-500/40', 'TANK B')}
      `;
    }

    // =========================================================================
    // 4. 2D PANNING TECH-TREE MATRIX & ENCYCLOPEDIA GRID (VIEW 4)
    // =========================================================================
    function renderCatalogAndMatrix() {
      const surface = document.getElementById('blueprint-pan-surface');
      const grid = document.getElementById('catalog-grid');
      if (!surface || !grid) return;

      // Render 7 Nations x 7 Eras 2D Matrix Table
      surface.innerHTML = `
        <div class="grid grid-cols-8 gap-2 text-xs">
          <div class="p-2.5 rounded-lg bg-[var(--card)] border border-[var(--border)] font-bold text-amber-400">
            Nation \\ Era
          </div>
          ${ERAS.map(e => `
            <div class="p-2.5 rounded-lg bg-[var(--card)] border border-[var(--border)]">
              <div class="font-bold text-[var(--foreground)]">${e.short}</div>
              <div class="text-[10px] font-mono text-[var(--muted-foreground)]">${e.years}</div>
            </div>
          `).join('')}

          ${NATIONS.map(nat => `
            <div class="p-2.5 rounded-lg bg-[var(--card)] border border-[var(--border)] flex flex-col justify-center" style="border-left: 4px solid ${nat.color}">
              <div class="font-bold text-[var(--foreground)]">${nat.flag} ${nat.short}</div>
              <div class="text-[10px] text-[var(--muted-foreground)]">${nat.name}</div>
            </div>
            ${ERAS.map(era => {
              const cellTanks = TANKS.filter(t => t.nation === nat.id && t.era === era.id);
              return `
                <div class="p-2 rounded-lg bg-[var(--card)]/60 border border-[var(--border)] flex flex-col gap-1.5 min-h-[92px]">
                  ${cellTanks.map(t => {
                    const rivals = EDGES.filter(e => e.type === 'combat' && (e.source === t.id || e.target === t.id)).length;
                    return `
                      <button onclick="selectTank('${t.id}', true)" class="p-1.5 rounded bg-[var(--background)] border border-[var(--border)] hover:border-amber-400 text-left transition">
                        <div class="font-bold text-[11px] text-[var(--foreground)]">${t.name}</div>
                        <div class="flex items-center justify-between text-[10px] text-[var(--muted-foreground)] mt-0.5">
                          <span>${t.year} • ${t.weight_t}t</span>
                          ${rivals ? `<span class="text-rose-400 font-bold">⚔️${rivals}</span>` : ''}
                        </div>
                      </button>
                    `;
                  }).join('')}
                </div>
              `;
            }).join('')}
          `).join('')}
        </div>
      `;

      // Render Filtered Encyclopedia Cards
      const visibleTanks = TANKS.filter(isTankVisible);
      grid.innerHTML = visibleTanks.map(t => {
        const nat = NATION_MAP[t.nation];
        const rivals = EDGES.filter(e => e.type === 'combat' && (e.source === t.id || e.target === t.id));
        return `
          <div class="bg-[var(--background)] border border-[var(--border)] hover:border-amber-500/60 rounded-xl p-3.5 flex flex-col justify-between gap-2.5 transition">
            <div>
              <div class="flex items-center justify-between text-xs">
                <span class="font-bold" style="color:${nat.color}">${nat.flag} ${nat.short} • ${t.year}</span>
                <span class="px-2 py-0.5 rounded bg-[var(--card)] border border-[var(--border)] text-[10px] font-mono">${t.weight_t}t • ${t.armor_mm}mm</span>
              </div>
              <h4 class="text-sm font-bold text-[var(--foreground)] mt-1.5">${t.name}</h4>
              <div class="text-[11px] text-amber-400 font-medium">${t.gun}</div>
              <p class="text-xs text-[var(--muted-foreground)] mt-1 line-clamp-3">${t.summary}</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] flex items-center justify-between gap-2">
              <span class="text-[11px] text-rose-400 font-semibold">⚔️ ${rivals.length} Combat Rivals</span>
              <button onclick="selectTank('${t.id}', true)" class="px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold">
                Inspect on Graph →
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    // Modern Web Guidance `2d-panning` fallback for browsers without native `scroll-axis-lock: none`
    function setup2DPanningFallback() {
      if (typeof CSS !== 'undefined' && CSS.supports('scroll-axis-lock', 'none')) return;
      const viewport = document.getElementById('blueprint-pan-viewport');
      if (!viewport) return;
      viewport.addEventListener('wheel', (e) => {
        if (e.ctrlKey) return;
        e.preventDefault();
        viewport.scrollLeft += e.deltaX;
        viewport.scrollTop += e.deltaY;
      }, { passive: false });
    }

    // =========================================================================
    // 5. INITIALIZATION & ANIMATION LOOP
    // =========================================================================
    function refreshAll() {
      renderEraStepper();
      renderTankInspector();
      if (state.mainView === 'duel') updateDuelView();
      if (state.mainView === 'matrix') renderCatalogAndMatrix();
    }

    function tick() {
      state.animTick++;
      if (state.mainView === 'graph') {
        drawGraphCanvas();
      } else if (state.mainView === 'map') {
        drawWorldMap();
        if (state.tacticalZoomOpen) drawTacticalSchematic();
      }
      requestAnimationFrame(tick);
    }

    window.addEventListener('DOMContentLoaded', () => {
      renderEraStepper();
      renderTankInspector();
      renderMapBattleStrip();
      renderBattleInspector();
      initDuelSelects();
      setupGraphCanvas();
      setupMapCanvas();
      setup2DPanningFallback();
      requestAnimationFrame(tick);
    });
  </script>
</body>
</html>
'''

# Assemble full HTML and write to /Users/tuandinh/Scifi/world-tank-atlas/world_tanks_atlas.html
full_html = (
    HTML_TEMPLATE
    .replace('__ERAS_JSON__', json.dumps(gd.ERAS))
    .replace('__NATIONS_JSON__', json.dumps(gd.NATIONS))
    .replace('__TANKS_JSON__', json.dumps(app.ALL_TANKS))
    .replace('__EDGES_JSON__', json.dumps(app.ALL_EDGES))
    .replace('__BATTLES_JSON__', json.dumps(app.ALL_BATTLES))
    .replace('__POLYGONS_JSON__', json.dumps(WORLD_POLYGONS))
    .replace('__NUM_TANKS__', str(len(app.ALL_TANKS)))
    .replace('__NUM_EDGES__', str(len(app.ALL_EDGES)))
    .replace('__NUM_BATTLES__', str(len(app.ALL_BATTLES)))
    + JS_ENGINE
    + JS_ENGINE_PART2
)

output_workspace_path = '/Users/tuandinh/Scifi/world-tank-atlas/world_tanks_atlas.html'
with open(output_workspace_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Successfully generated {output_workspace_path} ({len(full_html):,} bytes)")

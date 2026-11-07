# Part 1 of HTML v3 generator: Starts on World Map, includes Universal Tank Popup Modal, 85 Real Tank Photos, and Raseiniai 994-Tank Timeline & Destruction Forensics
HTML_HEAD_AND_BODY = r"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>World Tank Atlas</title>
  <meta name="description" content="__N_TANKS__ tanks and __N_BATTLES__ tank battles, 1916–2026, with a battle simulator." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <!-- Fonts load without blocking the scripts below; text renders in the fallback face until they arrive -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" media="print" onload="this.media='all'" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    // Design tokens (DESIGN.md): Tailwind palettes resolve to theme-aware CSS variables
    const tokenRamp = (name) => Object.fromEntries(
      [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950].map(s => [s, `rgb(var(--${name}-${s}) / <alpha-value>)`])
    );
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            white: 'rgb(var(--n-50) / <alpha-value>)',
            slate: tokenRamp('n'), gray: tokenRamp('n'), zinc: tokenRamp('n'),
            amber: tokenRamp('acc'), yellow: tokenRamp('acc'), orange: tokenRamp('acc'),
            sky: tokenRamp('sa'), cyan: tokenRamp('sa'), blue: tokenRamp('sa'),
            indigo: tokenRamp('sa'), violet: tokenRamp('sa'), purple: tokenRamp('sa'), fuchsia: tokenRamp('sa'), pink: tokenRamp('sa'),
            rose: tokenRamp('sb'), red: tokenRamp('sb'),
            emerald: tokenRamp('ok'), green: tokenRamp('ok'), teal: tokenRamp('ok'), lime: tokenRamp('ok'),
          },
          fontFamily: {
            sans: ['"IBM Plex Sans"', 'sans-serif'],
            display: ['"Barlow Condensed"', '"IBM Plex Sans"', 'sans-serif'],
          },
          fontSize: {
            xs: ['0.875rem', { lineHeight: '1.25rem' }],
          },
        },
      },
    };
  </script>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    /* Token ramps (RGB triplets). n = neutral, acc = accent, sa = Side A, sb = Side B, ok = winner/success */
    :root {
      --ok-50: 233 248 240; --ok-100: 205 238 221; --ok-200: 159 220 191; --ok-300: 115 203 161; --ok-400: 76 195 138; --ok-500: 54 168 115; --ok-600: 42 134 92; --ok-700: 33 103 71; --ok-800: 25 76 53; --ok-900: 17 52 35; --ok-950: 10 32 22;
      --n-50: 246 247 242; --n-100: 236 239 230; --n-200: 216 221 209; --n-300: 196 203 187; --n-400: 169 178 160; --n-500: 111 124 105; --n-600: 74 87 70; --n-700: 46 58 46; --n-800: 36 48 36; --n-900: 26 33 26; --n-950: 17 22 17;
      --acc-50: 253 243 225; --acc-100: 251 228 189; --acc-200: 248 208 138; --acc-300: 245 189 95; --acc-400: 242 169 59; --acc-500: 224 149 42; --acc-600: 194 125 29; --acc-700: 154 98 22; --acc-800: 111 71 16; --acc-900: 74 47 11; --acc-950: 46 29 6;
      --sa-50: 234 242 253; --sa-100: 211 227 251; --sa-200: 169 200 245; --sa-300: 126 172 239; --sa-400: 79 143 232; --sa-500: 58 120 212; --sa-600: 44 96 176; --sa-700: 34 73 138; --sa-800: 26 54 102; --sa-900: 18 37 74; --sa-950: 11 23 46;
      --sb-50: 253 236 234; --sb-100: 250 211 208; --sb-200: 244 168 163; --sb-300: 237 125 118; --sb-400: 229 83 75; --sb-500: 207 63 55; --sb-600: 172 50 43; --sb-700: 133 39 34; --sb-800: 95 28 24; --sb-900: 64 19 16; --sb-950: 39 11 9;

      --surface: rgb(var(--n-950));
      --surface-raised: rgb(var(--n-900));
      --text: rgb(var(--n-100));
      --text-muted: rgb(var(--n-400));
      --border-token: rgb(var(--n-700));
      --accent: rgb(var(--acc-400));
      --focus: rgb(var(--acc-400));
      --side-a: rgb(var(--sa-400));
      --side-b: rgb(var(--sb-400));
      --tint-east: #8a3b3b33;
      --tint-desert: #8a733b33;
      --tint-asia: #3b7a5a33;

      /* Legacy names used across the markup, now aliases of the tokens */
      --background: var(--surface);
      --card: var(--surface-raised);
      --card-elevated: rgb(var(--n-800));
      --foreground: var(--text);
      --muted-foreground: var(--text-muted);
      --border: var(--border-token);
      --canvas-bg: #0b0f0b;
    }
    html.light-theme {
      --ok-50: 12 51 32; --ok-100: 16 64 42; --ok-200: 22 82 54; --ok-300: 29 100 67; --ok-400: 47 122 82; --ok-500: 58 138 96; --ok-600: 76 154 112; --ok-700: 205 233 218; --ok-800: 223 241 231; --ok-900: 239 248 243; --ok-950: 247 252 249;
      --n-50: 17 22 15; --n-100: 27 33 24; --n-200: 43 51 40; --n-300: 61 71 57; --n-400: 79 90 74; --n-500: 111 122 104; --n-600: 154 163 146; --n-700: 201 207 194; --n-800: 227 231 221; --n-900: 255 255 255; --n-950: 238 240 234;
      --acc-50: 74 44 0; --acc-100: 90 53 0; --acc-200: 111 66 0; --acc-300: 127 76 0; --acc-400: 147 90 0; --acc-500: 154 92 0; --acc-600: 138 82 0; --acc-700: 245 217 168; --acc-800: 249 230 196; --acc-900: 252 241 221; --acc-950: 254 248 238;
      --sa-50: 11 42 92; --sa-100: 15 54 117; --sa-200: 22 68 144; --sa-300: 27 82 168; --sa-400: 31 95 191; --sa-500: 42 108 204; --sa-600: 58 120 212; --sa-700: 201 220 246; --sa-800: 221 232 249; --sa-900: 237 243 252; --sa-950: 246 249 254;
      --sb-50: 77 19 15; --sb-100: 99 24 19; --sb-200: 125 30 24; --sb-300: 158 39 32; --sb-400: 192 52 43; --sb-500: 204 64 56; --sb-600: 212 82 74; --sb-700: 246 207 204; --sb-800: 249 224 222; --sb-900: 252 239 238; --sb-950: 254 247 246;
      --tint-east: #c0342b1f;
      --tint-desert: #b86e001f;
      --tint-asia: #2f7a521f;
      --canvas-bg: #0b0f0b;
    }
    * { box-sizing: border-box; }
    html { scrollbar-color: rgb(var(--n-600)) rgb(var(--n-900)); }
    body {
      background-color: var(--background);
      color: var(--foreground);
      font-family: "IBM Plex Sans", sans-serif;
      font-size: 16px;
      line-height: 1.5;
      caret-color: var(--accent);
    }
    ::selection { background: rgb(var(--acc-400) / 0.3); }
    :focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
    .tabular-nums, [data-num] { font-variant-numeric: tabular-nums; }
    .custom-scroll::-webkit-scrollbar { width: 8px; height: 8px; }
    .custom-scroll::-webkit-scrollbar-track { background: rgb(var(--n-900) / 0.3); }
    .custom-scroll::-webkit-scrollbar-thumb { background: rgb(var(--n-600) / 0.6); border-radius: 9999px; }
    .custom-scroll::-webkit-scrollbar-thumb:hover { background: rgb(var(--acc-400) / 0.8); }
    canvas { user-select: none; }

    /* App bar tabs and filter chips */
    .app-tab {
      display: inline-flex; align-items: center; padding: 0 12px; white-space: nowrap;
      font-size: 15px; font-weight: 600; color: var(--muted-foreground);
      border-bottom: 2px solid transparent; transition: color 150ms ease-out, border-color 150ms ease-out;
    }
    .app-tab:hover { color: var(--foreground); }
    .app-tab[aria-current="page"] { color: var(--foreground); border-bottom-color: var(--accent); }
    .cf-btn {
      height: 28px; padding: 0 10px; border-radius: 6px; font-size: 14px; font-weight: 500;
      color: var(--muted-foreground); border: 1px solid var(--border);
      transition: color 150ms ease-out, background-color 150ms ease-out;
    }
    .cf-btn:hover { color: var(--foreground); }
    .cf-btn[aria-pressed="true"] { color: var(--foreground); border-color: var(--accent); background: rgb(var(--acc-400) / 0.18); font-weight: 600; }
    /* Battle theater: battlefield fills the screen under the app bar, battle header and force bar */
    .sim-stage { height: calc(100vh - 260px); min-height: 420px; }
    .sim-panel { height: calc(100vh - 260px + 56px); min-height: 476px; }
    .sim-notch {
      position: absolute; top: 0; transform: translateX(-1px); height: 18px; min-width: 18px; padding: 0 4px;
      font-size: 12px; line-height: 18px; border-left: 2px solid var(--border); color: var(--muted-foreground);
    }
    .sim-notch:hover { color: var(--foreground); }
    .sim-notch[aria-current="step"] { color: var(--accent); border-left-color: var(--accent); font-weight: 600; }

    /* ---- Responsive: phones < 768px, tablets 768-1023px, desktop >= 1024px ---- */
    .mobile-only { display: none; }
    /* Photos: tinted placeholder while loading; blueprint fallback when they fail */
    main img, #tank-popup-modal img { background-color: var(--surface-raised); }
    .photo-fallback { position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; background: var(--surface-raised); }
    .photo-fallback > svg { width: 100%; height: 100%; }
    .photo-fallback-caption { position: absolute; left: 6px; bottom: 4px; font-size: 12px; line-height: 1.3; padding: 1px 6px; border-radius: 4px; color: var(--muted-foreground); background: rgb(var(--n-950) / 0.85); }
    .photo-fallback:not(:has(svg)) .photo-fallback-caption { position: static; background: none; }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; }
    }
    .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0; }
    .app-tab[aria-selected="true"] { color: var(--foreground); border-bottom-color: var(--accent); }
    kbd { font-family: inherit; font-size: 13px; padding: 1px 6px; border: 1px solid var(--border); border-bottom-width: 2px; border-radius: 4px; color: var(--foreground); background: var(--background); }
    select { max-width: 100%; min-width: 0; }
    #filter-row select { flex-shrink: 0; max-width: none; } /* the row scrolls sideways instead */
    .sheet-handle { display: none; }
    .view-menu-item { display: block; width: 100%; text-align: left; padding: 10px 12px; font-size: 15px; color: var(--muted-foreground); }
    .view-menu-item:hover, .view-menu-item[aria-current="page"] { color: var(--foreground); background: var(--background); }

    /* Bottom sheet (map battle panel, battle story panel): peeks at 30%, opens to 90% */
    @media (max-width: 1023px) {
      .sheet {
        position: fixed !important; left: 0; right: 0; bottom: var(--sheet-bottom, 0px);
        height: 90vh !important; min-height: 0 !important; z-index: 35; margin: 0 !important;
        border-radius: 10px 10px 0 0 !important; box-shadow: 0 -4px 16px rgb(0 0 0 / 0.35);
        transform: translateY(60vh); transition: transform 200ms ease-out;
      }
      .sheet.sheet-full { transform: translateY(0); }
      .sheet.sheet-dragging { transition: none; }
      .sheet-handle {
        display: flex; align-items: center; justify-content: center; flex-shrink: 0;
        width: 100%; height: 32px; touch-action: none; cursor: grab;
      }
      .sheet-handle::before { content: ''; width: 40px; height: 4px; border-radius: 2px; background: var(--border); }
      body[data-view="battle-page"] main, body.map-panel-open main { padding-bottom: calc(30vh + 72px) !important; }
      .sim-stage { height: calc(70vh - 236px) !important; min-height: 260px !important; }
    }

    @media (max-width: 767px) {
      .mobile-only { display: flex; }
      #app-bar > div:first-child { height: 48px; gap: 4px; padding-left: 12px; padding-right: 8px; }
      #view-tabs, #app-search { display: none; }
      #app-bar.search-open #app-search {
        display: block; position: absolute; left: 0; right: 0; top: 48px; z-index: 45;
        padding: 8px 12px; background: var(--card); border-bottom: 1px solid var(--border);
      }
      #app-bar.search-open #app-search input { width: 100%; height: 44px; }
      #app-bar h1 { font-size: 20px; }
      main { padding: 8px !important; }
      #map-canvas-wrap { height: calc(100vh - 48px - 44px - 64px - 24px) !important; min-height: 320px; }
      /* sim controls fixed at the bottom, within thumb reach; the story sheet sits on top of them */
      #sim-controls { position: fixed; left: 0; right: 0; bottom: 0; z-index: 40; height: 60px; min-height: 0; padding-top: 0; padding-bottom: 0; gap: 8px; }
      #sim-time-readout, #sim-replay-btn, .sim-loss-strip { display: none !important; }
      .sim-scale-note { font-size: 12px; }
      .sim-panel.sheet { --sheet-bottom: 60px; }
      .sim-stage { height: calc(70vh - 244px) !important; min-height: 220px !important; }
      /* battle header wraps: back + title on one row, switcher + Details on the next */
      #battle-header { height: auto; flex-wrap: wrap; row-gap: 4px; }
      #battle-header h2 { flex: 1 1 0; min-width: 0; font-size: 20px; }
      #battle-header > div:last-child { margin-left: 0; width: 100%; }
      #battle-page-select { flex: 1 1 0; min-width: 0; max-width: none; }
      #sim-controls > div.relative { min-width: 0; }
    }
    @media (max-width: 479px) {
      #sim-speed-group { display: none !important; }
    }
    @media (pointer: coarse) {
      .cf-btn, #nation-select { min-height: 44px; }
      .app-tab { min-width: 44px; }
      #filter-row > div { height: auto; padding-top: 4px; padding-bottom: 4px; }
    }

    /* 2d-panning modern web guidance: unrestricted 2D scroll container without axis-locking railing */
    .pan-viewport {
      overflow: auto;
      scroll-axis-lock: none;
      overscroll-behavior: none;
    }
    .pan-viewport:focus-visible {
      outline: 2px solid var(--focus);
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

  <!-- ======================================================================= -->
  <!-- UNIVERSAL INTERACTIVE TANK POPUP MODAL (Opens over ANY view on click!)  -->
  <!-- ======================================================================= -->
  <div id="tank-popup-modal" class="hidden fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm items-center justify-center p-3 sm:p-6 overflow-y-auto" onclick="if(event.target===this) closeTankPopup()">
    <div id="tank-popup-card" class="bg-slate-900 border-2 border-amber-400 rounded-2xl max-w-4xl w-full max-h-[92vh] overflow-y-auto custom-scroll shadow-2xl p-4 sm:p-6 text-slate-100 flex flex-col gap-4">
      <!-- Populated dynamically by openTankPopup(tankId) -->
    </div>
  </div>

  <!-- App bar (56px) + per-view filter row (40px). Counts __N_TANKS__ / __N_BATTLES__ are filled by assemble_v2.py -->
  <header id="app-bar" class="sticky top-0 z-40 bg-[var(--card)] border-b border-[var(--border)]">
    <div class="max-w-[1860px] mx-auto h-14 px-4 flex items-center gap-4">
      <!-- Wordmark + site switcher -->
      <div class="relative shrink-0">
        <button id="site-switcher-btn" onclick="toggleSiteMenu()" aria-haspopup="menu" aria-expanded="false" aria-controls="site-menu"
          class="h-11 flex items-center gap-2 px-1 rounded-md hover:bg-[var(--background)]">
          <svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-amber-400"><path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6l8-3z"/></svg>
          <h1 class="font-display text-[22px] leading-none tracking-wide text-[var(--foreground)] whitespace-nowrap">World Tank Atlas</h1>
          <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-[var(--muted-foreground)]"><path d="M6 9l6 6 6-6"/></svg>
        </button>
        <div id="site-menu" role="menu" class="hidden absolute left-0 top-12 w-56 rounded-[10px] border border-[var(--border)] bg-[var(--card)] shadow-lg py-1 z-50">
          <span role="menuitem" aria-current="page" class="flex items-center justify-between px-3 py-2.5 text-sm font-semibold text-[var(--foreground)]">World Tank Atlas <span class="text-amber-400 text-xs">current</span></span>
          <a role="menuitem" href="../scifi-ai-atlas/index.html" class="block px-3 py-2.5 text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--background)]">Sci-Fi AI Atlas</a>
        </div>
      </div>

      <!-- View tabs -->
      <nav id="view-tabs" role="tablist" aria-label="Views" class="flex-1 min-w-0 h-full flex items-stretch gap-1 overflow-x-auto">
        <button id="tab-map" role="tab" aria-selected="true" aria-controls="view-map" tabindex="0" onclick="switchMainView('map')" class="app-tab" aria-current="page">Map</button>
        <button id="tab-battle-page" role="tab" aria-selected="false" aria-controls="view-battle-page" tabindex="-1" onclick="switchMainView('battle-page')" class="app-tab">Battles</button>
        <button id="tab-tank-page" role="tab" aria-selected="false" aria-controls="view-tank-page" tabindex="-1" onclick="switchMainView('tank-page')" class="app-tab">Tanks</button>
        <button id="tab-graph" role="tab" aria-selected="false" aria-controls="view-graph" tabindex="-1" onclick="switchMainView('graph')" class="app-tab">Lineage</button>
        <button id="tab-duel" role="tab" aria-selected="false" aria-controls="view-duel" tabindex="-1" onclick="switchMainView('duel')" class="app-tab">Compare</button>
        <button id="tab-matrix" role="tab" aria-selected="false" aria-controls="view-matrix" tabindex="-1" onclick="switchMainView('matrix')" class="app-tab">Tech tree</button>
      </nav>

      <!-- Search + theme (phones: search behind an icon, views behind a menu) -->
      <div class="mobile-only flex-1"></div>
      <button onclick="toggleMobileSearch()" aria-label="Search" aria-expanded="false" id="mobile-search-btn"
        class="mobile-only shrink-0 w-11 h-11 rounded-md items-center justify-center text-[var(--muted-foreground)] hover:text-[var(--foreground)]">
        <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      </button>
      <div id="app-search" class="relative shrink-0">
        <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="absolute left-2.5 top-1/2 -translate-y-1/2 text-[var(--muted-foreground)]"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
        <input
          id="search-input"
          type="search"
          aria-label="Search tanks or battles"
          oninput="handleSearch(this.value)"
          placeholder="Search tanks or battles"
          class="w-56 h-9 pl-8 pr-8 rounded-md text-sm bg-[var(--background)] border border-[var(--border)] text-[var(--foreground)] placeholder-[var(--muted-foreground)] focus:border-amber-400"
        />
        <button id="clear-search" onclick="clearSearch()" aria-label="Clear search" class="hidden absolute right-1 top-1/2 -translate-y-1/2 w-7 h-7 rounded text-[var(--muted-foreground)] hover:text-[var(--foreground)]">
          <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mx-auto"><path d="M6 6l12 12M18 6L6 18"/></svg>
        </button>
      </div>
      <div class="mobile-only relative shrink-0">
        <button onclick="toggleViewMenu()" id="view-menu-btn" aria-label="Views" aria-haspopup="menu" aria-expanded="false" aria-controls="view-menu"
          class="w-11 h-11 rounded-md flex items-center justify-center text-[var(--muted-foreground)] hover:text-[var(--foreground)]">
          <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        </button>
        <div id="view-menu" role="menu" class="hidden absolute right-0 top-12 w-52 rounded-[10px] border border-[var(--border)] bg-[var(--card)] shadow-lg py-1 z-50">
          <button role="menuitem" data-view-link="map" onclick="switchMainView('map')" class="view-menu-item">Map</button>
          <button role="menuitem" data-view-link="battle-page" onclick="switchMainView('battle-page')" class="view-menu-item">Battles</button>
          <button role="menuitem" data-view-link="tank-page" onclick="switchMainView('tank-page')" class="view-menu-item">Tanks</button>
          <button role="menuitem" data-view-link="graph" onclick="switchMainView('graph')" class="view-menu-item">Lineage</button>
          <button role="menuitem" data-view-link="duel" onclick="switchMainView('duel')" class="view-menu-item">Compare</button>
          <button role="menuitem" data-view-link="matrix" onclick="switchMainView('matrix')" class="view-menu-item">Tech tree</button>
        </div>
      </div>
      <button onclick="toggleTheme()" id="theme-toggle-btn" aria-label="Switch light or dark theme" title="Switch light or dark theme"
        class="shrink-0 w-11 h-11 rounded-md flex items-center justify-center text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--background)]">
        <svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 000 18z" fill="currentColor"/></svg>
      </button>
    </div>

    <!-- Filter row: shown only on Map, Tanks and Lineage (switchMainView) -->
    <div id="filter-row" class="border-t border-[var(--border)]">
      <div class="max-w-[1860px] mx-auto h-10 px-4 flex items-center gap-1.5 overflow-x-auto whitespace-nowrap">
        <span class="text-xs font-semibold text-[var(--muted-foreground)] mr-1">Era</span>
        <button onclick="setConflictFilter('all')" id="cf-all" class="cf-btn" aria-pressed="true">All eras</button>
        <button onclick="setConflictFilter('ww1_interwar')" id="cf-ww1_interwar" class="cf-btn" aria-pressed="false">WWI &amp; interwar</button>
        <button onclick="setConflictFilter('ww2')" id="cf-ww2" class="cf-btn" aria-pressed="false">WWII</button>
        <button onclick="setConflictFilter('vietnam')" id="cf-vietnam" class="cf-btn" aria-pressed="false">Vietnam</button>
        <button onclick="setConflictFilter('arab_israeli')" id="cf-arab_israeli" class="cf-btn" aria-pressed="false">Arab-Israeli</button>
        <button onclick="setConflictFilter('gulf')" id="cf-gulf" class="cf-btn" aria-pressed="false">Gulf</button>
        <button onclick="setConflictFilter('ukraine')" id="cf-ukraine" class="cf-btn" aria-pressed="false">Ukraine</button>
        <select id="nation-select" onchange="setNationFilter(this.value)" aria-label="Nation"
          class="ml-2 h-8 px-2 rounded-md text-xs font-semibold bg-[var(--background)] border border-[var(--border)] text-[var(--foreground)]">
          <option value="all">All nations</option>
          <option value="UK">🇬🇧 United Kingdom</option>
          <option value="FR">🇫🇷 France</option>
          <option value="DE">🇩🇪 Germany</option>
          <option value="SU_RU">🇷🇺 USSR / Russia / Ukraine</option>
          <option value="US">🇺🇸 United States</option>
          <option value="IL">🇮🇱 Israel</option>
          <option value="ASIA_OTHER">Japan / China / S. Korea / Sweden</option>
        </select>
        <select id="theatre-select" onchange="flyToTheatre(this.value)" aria-label="Theatre"
          class="ml-2 h-8 px-2 rounded-md text-xs font-semibold bg-[var(--background)] border border-[var(--border)] text-[var(--foreground)]">
          <option value="WORLD">Whole world</option>
          <option value="EUROPE_EAST">Eastern Front</option>
          <option value="EUROPE_WEST">Western Europe</option>
          <option value="NORTH_AFRICA_SINAI">North Africa, Sinai &amp; Golan</option>
          <option value="GULF_ME">Persian Gulf &amp; Iraq</option>
          <option value="VIETNAM_SEA">Vietnam &amp; SE Asia</option>
          <option value="ASIA">East &amp; South Asia</option>
        </select>
        <span id="atlas-summary" class="ml-auto pl-4 text-xs text-[var(--muted-foreground)] tabular-nums">__N_TANKS__ tanks and __N_BATTLES__ battles, 1916–2026</span>
      </div>
    </div>
  </header>

  <!-- Main Workspace Container -->
  <main class="flex-1 max-w-[1860px] w-full mx-auto p-4 flex flex-col gap-4">
    <!-- Screen-reader announcements for the battle (phase changes, knock-outs), throttled in JS -->
    <div id="sim-announcer" class="sr-only" aria-live="polite" aria-atomic="true"></div>
    <!-- Shown by the router when a link points at a battle or tank that doesn't exist -->
    <div id="route-notice" role="status" class="hidden flex flex-col gap-1 rounded-[10px] border border-amber-400 bg-[var(--card)] p-4"></div>

    <!-- ===================================================================== -->
    <!-- VIEW 1 (DEFAULT): WORLD TANK BATTLES & 85 TANKS MAP + POPUPS          -->
    <!-- ===================================================================== -->
    <section id="view-map" role="tabpanel" aria-labelledby="tab-map" class="flex flex-col gap-3">
      <!-- Map toolbar: what to show + zoom. Theatre jumps live in the filter row. -->
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-[10px] px-3 py-2 flex flex-wrap items-center gap-2">
        <span class="text-xs font-semibold text-[var(--muted-foreground)]">Show</span>
        <button id="mpm-both" onclick="setMapPinMode('both')" class="px-2.5 py-1 rounded text-xs font-extrabold bg-amber-500 text-slate-950">Battles and tanks</button>
        <button id="mpm-battles" onclick="setMapPinMode('battles')" class="px-2.5 py-1 rounded text-xs font-semibold bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Battles</button>
        <button id="mpm-tanks" onclick="setMapPinMode('tanks')" class="px-2.5 py-1 rounded text-xs font-semibold bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Tanks</button>
        <div class="ml-auto flex items-center gap-1">
          <button onclick="zoomMapBy(1.4)" aria-label="Zoom in" class="w-9 h-9 rounded-md border border-[var(--border)] bg-[var(--background)] hover:border-amber-400 text-base font-semibold">+</button>
          <button onclick="zoomMapBy(0.7)" aria-label="Zoom out" class="w-9 h-9 rounded-md border border-[var(--border)] bg-[var(--background)] hover:border-amber-400 text-base font-semibold">−</button>
        </div>
      </div>

      <!-- Map (full width until a battle is clicked) + side panel for the selected battle -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 items-start">
        <div id="map-col" class="lg:col-span-12 bg-[var(--card)] border border-[var(--border)] rounded-xl overflow-hidden shadow-md flex flex-col">
          <div class="px-4 py-2 border-b border-[var(--border)] flex flex-wrap items-center justify-between gap-2 bg-[var(--background)]/60 text-xs">
            <span class="font-semibold text-[var(--foreground)]" id="map-zoom-readout">World map</span>
            <span class="text-[var(--muted-foreground)]">Scroll to zoom, drag to move</span>
          </div>

          <div class="relative w-full h-[690px] bg-[#06101e]" id="map-canvas-wrap">
            <canvas id="world-map-canvas" role="img" aria-label="World map of __N_BATTLES__ tank battles. Use the battle list along the bottom of the map to choose one." class="w-full h-full block cursor-grab active:cursor-grabbing"></canvas>

            <!-- Nothing matches the search/filters: shown by applyFilters() -->
            <div id="map-no-results" role="status" class="hidden absolute inset-x-4 top-1/3 z-20 mx-auto max-w-md flex flex-col gap-1 p-4 rounded-[10px] border border-amber-400 bg-[var(--card)] shadow-lg"></div>
            <!-- First-visit hint; hidden once a battle is selected -->
            <div id="map-hint" class="absolute top-3 left-3 z-20 px-3 py-1.5 rounded-md bg-[var(--card)]/95 border border-[var(--border)] text-sm text-[var(--foreground)] pointer-events-none">
              Click a battle to explore
            </div>

            <!-- Interactive Tactical Battlefield Zoom-In Overlay -->
            <div id="tactical-zoom-overlay" class="hidden absolute inset-4 bg-slate-900/95 backdrop-blur-md border-2 border-amber-500 rounded-xl shadow-2xl flex flex-col overflow-hidden z-30">
              <div class="px-4 py-3 border-b border-slate-700 flex items-center justify-between bg-slate-950/80">
                <div>
                  <span class="px-2 py-0.5 rounded text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40 mr-2">TACTICAL FORMATION SCHEMATIC</span>
                  <span class="font-bold text-sm text-white" id="tac-overlay-title">Battle Schematic</span>
                </div>
                <div class="flex items-center gap-2">
                  <button onclick="openBattlePage(state.selectedBattleId)" class="px-3 py-1 rounded-lg bg-amber-500 text-slate-950 text-xs font-extrabold hover:bg-amber-400">
                    🎬 Open Full 5-Phase Destruction Simulator →
                  </button>
                  <button onclick="toggleTacticalZoomModal(false)" class="px-3 py-1 rounded-lg bg-slate-800 border border-slate-600 text-white hover:border-amber-500 text-xs font-semibold">
                    ✕ Close
                  </button>
                </div>
              </div>
              <div class="flex-1 relative bg-[#091520]">
                <canvas id="tactical-schematic-canvas" class="w-full h-full block"></canvas>
              </div>
              <div class="px-4 py-2.5 border-t border-slate-700 bg-slate-950/90 text-xs text-slate-300 flex flex-wrap items-center justify-between gap-2" id="tac-overlay-footer"></div>
            </div>

            <!-- Timeline Battle Scrubber Bottom Bar -->
            <div class="absolute bottom-3 left-3 right-3 bg-slate-900/95 backdrop-blur border border-slate-700 rounded-lg p-2 shadow-xl flex items-center gap-2 overflow-x-auto custom-scroll" id="map-battle-strip"></div>
          </div>

          <!-- Visual Strip of Participating & World Tanks Below the Map (Click any tank for instant Tank Popup!) -->
          <div class="p-3 bg-[var(--background)] border-t border-[var(--border)] flex flex-col gap-2">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <span class="text-xs font-semibold text-[var(--foreground)]" id="map-tank-strip-title">All __N_TANKS__ tanks</span>
              <button onclick="switchMainView('tank-page')" class="text-xs font-semibold text-amber-400 hover:underline">Open the tank gallery</button>
            </div>
            <div id="map-tank-photo-strip" class="flex items-center gap-2.5 overflow-x-auto custom-scroll pb-1"></div>
          </div>
        </div>

        <!-- Side panel for the battle clicked on the map -->
        <aside id="map-panel" aria-label="Selected battle" class="sheet hidden lg:col-span-5 bg-[var(--card)] border border-[var(--border)] rounded-[10px] flex flex-col h-[820px]">
          <button class="sheet-handle" aria-label="Expand or collapse the battle panel"></button>
          <div class="flex items-center gap-2 px-5 py-3 border-b border-[var(--border)]">
            <button onclick="watchSelectedBattle()" class="h-10 px-4 rounded-md bg-amber-500 hover:bg-amber-400 text-slate-950 text-sm font-semibold">Watch battle</button>
            <button onclick="closeMapBattle()" aria-label="Close battle panel" class="ml-auto w-10 h-10 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--background)]">
              <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mx-auto"><path d="M6 6l12 12M18 6L6 18"/></svg>
            </button>
          </div>
          <div id="battle-inspector" class="flex-1 overflow-y-auto custom-scroll p-5 flex flex-col gap-4"></div>
        </aside>
      </div>
    </section>

    <!-- ===================================================================== -->
    <!-- VIEW 2: DEDICATED BATTLE PAGE, 5-PHASE TIMELINE & DESTRUCTION SIM     -->
    <!-- ===================================================================== -->
    <section id="view-battle-page" role="tabpanel" aria-labelledby="tab-battle-page" class="hidden flex-col gap-4">
      <!-- Battle header (48px): back to the map, title, battle switcher, jump to details -->
      <div id="battle-header" class="h-12 flex items-center gap-3 min-w-0">
        <button onclick="switchMainView('map')" class="shrink-0 h-10 px-2 rounded-md text-sm font-semibold text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--card)] flex items-center gap-1">
          <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
          All battles
        </button>
        <h2 id="battle-header-title" class="font-display text-[22px] leading-none tracking-wide text-[var(--foreground)] truncate"></h2>
        <div class="ml-auto shrink-0 flex items-center gap-1">
          <button onclick="stepBattlePage(-1)" aria-label="Previous battle" class="w-10 h-10 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--card)]">
            <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mx-auto"><path d="M15 18l-6-6 6-6"/></svg>
          </button>
          <select id="battle-page-select" onchange="openBattlePage(this.value)" aria-label="Choose a battle" class="h-9 max-w-[240px] px-2 rounded-md text-sm bg-[var(--card)] border border-[var(--border)] text-[var(--foreground)]"></select>
          <button onclick="stepBattlePage(1)" aria-label="Next battle" class="w-10 h-10 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--card)]">
            <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mx-auto"><path d="M9 6l6 6-6 6"/></svg>
          </button>
          <button onclick="document.getElementById('battle-details').scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth' })" class="ml-2 h-9 px-3 rounded-md text-sm font-semibold border border-[var(--border)] text-[var(--foreground)] hover:border-amber-400">
            Details
          </button>
        </div>
      </div>

      <!-- Dynamic Full-Page Battle Dossier + Multi-Platoon Historical Timeline & Destruction Canvas -->
      <div id="battle-page-content" class="flex flex-col gap-4"></div>
    </section>

    <!-- ===================================================================== -->
    <!-- VIEW 3: ALL 86 TANKS PHOTO GALLERY & DEDICATED TANK DOSSIER PAGE      -->
    <!-- ===================================================================== -->
    <section id="view-tank-page" role="tabpanel" aria-labelledby="tab-tank-page" class="hidden flex-col gap-4">
      <!-- Tank Selector & Quick Navigation Bar -->
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-3.5 shadow-md flex flex-wrap items-center justify-between gap-3">
        <div class="flex flex-wrap items-center gap-2 min-w-0 max-w-full">
          <span class="px-2.5 py-1 rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/40 text-xs font-extrabold">🛡️ ALL 86 TANKS GALLERY &amp; DOSSIER</span>
          <select id="tank-page-select" onchange="openTankPage(this.value)" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-[var(--background)] border border-[var(--border)] text-[var(--foreground)] min-w-[310px]"></select>
          <button onclick="stepTankPage(-1)" class="px-2.5 py-1.5 rounded-lg border border-[var(--border)] bg-[var(--background)] hover:border-amber-500 text-xs font-bold">◀ Prev Tank</button>
          <button onclick="stepTankPage(1)" class="px-2.5 py-1.5 rounded-lg border border-[var(--border)] bg-[var(--background)] hover:border-amber-500 text-xs font-bold">Next Tank ▶</button>
          <button onclick="openTankPopup(state.selectedTankId)" class="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-extrabold shadow">
            🔍 Open in Quick Popup Modal
          </button>
        </div>
        <div class="flex flex-wrap items-center gap-1.5">
          <span class="text-xs text-[var(--muted-foreground)] font-semibold">Raseiniai &amp; Vietnam Highlights:</span>
          <button onclick="openTankPage('kv1')" class="px-2 py-1 rounded text-xs font-semibold bg-rose-500/15 text-rose-300 border border-rose-500/40">KV-1</button>
          <button onclick="openTankPage('kv2')" class="px-2 py-1 rounded text-xs font-semibold bg-rose-500/15 text-rose-300 border border-rose-500/40">KV-2 (152mm)</button>
          <button onclick="openTankPage('pz_38t')" class="px-2 py-1 rounded text-xs font-semibold bg-amber-500/15 text-amber-300 border border-amber-500/40">Panzer 38(t)</button>
          <button onclick="openTankPage('m48_m60_patton')" class="px-2 py-1 rounded text-xs font-semibold bg-cyan-500/15 text-cyan-300 border border-cyan-500/40">M48A3 Patton</button>
          <button onclick="openTankPage('m60_patton')" class="px-2 py-1 rounded text-xs font-semibold bg-cyan-500/15 text-cyan-300 border border-cyan-500/40">M60 Patton</button>
          <button onclick="openTankPage('pt76')" class="px-2 py-1 rounded text-xs font-semibold bg-rose-500/15 text-rose-300 border border-rose-500/40">PT-76</button>
          <button onclick="openTankPage('t54_55')" class="px-2 py-1 rounded text-xs font-semibold bg-rose-500/15 text-rose-300 border border-rose-500/40">T-54/55</button>
        </div>
      </div>

      <!-- Visual Grid of ALL 85 Tanks (So the user sees all 85 tanks with real photographs at once!) -->
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-4 shadow-md flex flex-col gap-3">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h3 class="text-sm font-extrabold text-amber-400 uppercase tracking-wider">📸 Visual Roster of All 85 World Tanks (1916–2026) — Click Any Tank for Popup or Full Dossier Below</h3>
            <p class="text-xs text-[var(--muted-foreground)]">Every vehicle features a verified historical photograph from Wikimedia Commons, technical blueprint, and combat links.</p>
          </div>
          <span class="text-xs font-bold text-emerald-400" id="tank-gallery-count-badge">Showing 85 / 85 Tanks</span>
        </div>
        <div id="all-85-tanks-photo-grid" class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 xl:grid-cols-10 gap-2.5 max-h-[340px] overflow-y-auto custom-scroll p-1"></div>
      </div>

      <!-- Dynamic Full-Page Tank Dossier Content -->
      <div id="tank-page-content" class="flex flex-col gap-4"></div>
    </section>

    <!-- ===================================================================== -->
    <!-- VIEW 4: INTERACTIVE TANK LINEAGE, SIMILARITY & COMBAT GRAPH (85)      -->
    <!-- ===================================================================== -->
    <section id="view-graph" role="tabpanel" aria-labelledby="tab-graph" class="hidden flex-col gap-3">
      <!-- 7-Era Interactive Stepper Bar -->
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-3 shadow-md flex flex-col gap-2">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div class="flex flex-wrap items-center gap-2 text-xs">
            <span class="px-2.5 py-0.5 rounded bg-amber-500 text-slate-950 font-extrabold">85-TANK LINEAGE &amp; COMBAT GRAPH</span>
            <button onclick="toggleEdgeLayer('lineage')" id="layer-lineage" class="px-2 py-0.5 rounded text-xs font-bold border border-emerald-500/70 bg-emerald-500/20 text-emerald-300">🟢 Lineage: ON</button>
            <button onclick="toggleEdgeLayer('similarity')" id="layer-similarity" class="px-2 py-0.5 rounded text-xs font-bold border border-sky-500/70 bg-sky-500/20 text-sky-300">🔵 Similarity: ON</button>
            <button onclick="toggleEdgeLayer('combat')" id="layer-combat" class="px-2 py-0.5 rounded text-xs font-bold border border-rose-500/70 bg-rose-500/20 text-rose-300">⚔️ 🔴 Fought Each Other: ON</button>
            <span class="text-amber-300 font-semibold">Click any node to open its Tank Popup &amp; inspect its lineage!</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="text-xs font-semibold text-[var(--muted-foreground)]">Y-Axis Layout:</span>
            <button onclick="setGraphYMode('nation')" id="ymode-nation" class="px-2.5 py-1 rounded text-xs font-bold bg-amber-500 text-slate-950">By Nation / Bloc</button>
            <button onclick="setGraphYMode('weight')" id="ymode-weight" class="px-2.5 py-1 rounded text-xs font-semibold bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]">By Combat Weight (t)</button>
          </div>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-1.5 pt-1" id="era-stepper-bar"></div>
      </div>

      <!-- Split Grid: Graph Canvas (7 cols) + Deep Tank & Combat Duel Inspector (5 cols) -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 items-start">
        <div class="lg:col-span-7 bg-[var(--card)] border border-[var(--border)] rounded-xl overflow-hidden shadow-md flex flex-col">
          <div class="px-4 py-2.5 border-b border-[var(--border)] flex flex-wrap items-center justify-between gap-2 bg-[var(--background)]/60">
            <div class="flex flex-wrap items-center gap-2 text-xs">
              <span class="font-bold text-[var(--foreground)]">Interactive Armor Network:</span>
              <span class="text-amber-300 font-semibold" id="graph-status-label">Showing all 85 tanks &amp; 191 relationships</span>
            </div>
            <div class="flex flex-wrap items-center gap-1.5">
              <button onclick="openTankPopup(state.selectedTankId)" class="px-2.5 py-1 rounded bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-extrabold transition shadow-sm">
                🔍 Tank Popup
              </button>
              <button onclick="openTankPage(state.selectedTankId)" class="px-2.5 py-1 rounded bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold transition shadow-sm">
                📄 Full Tank Page
              </button>
              <button onclick="stepTank(-1)" class="px-2.5 py-1 rounded border border-[var(--border)] bg-[var(--card)] hover:border-amber-500 text-xs font-semibold transition">◀ Prev</button>
              <button onclick="stepTank(1)" class="px-2.5 py-1 rounded border border-[var(--border)] bg-[var(--card)] hover:border-amber-500 text-xs font-semibold transition">Next ▶</button>
              <button onclick="zoomGraph(1.25)" class="px-2.5 py-1 rounded border border-[var(--border)] bg-[var(--card)] hover:border-amber-500 text-xs font-bold transition">🔍 +</button>
              <button onclick="zoomGraph(0.8)" class="px-2.5 py-1 rounded border border-[var(--border)] bg-[var(--card)] hover:border-amber-500 text-xs font-bold transition">−</button>
              <button onclick="resetGraphCamera()" class="px-2.5 py-1 rounded border border-[var(--border)] bg-[var(--card)] hover:border-amber-500 text-xs font-semibold transition">Reset</button>
            </div>
          </div>

          <div class="relative w-full h-[740px] bg-[#070d19]" id="graph-canvas-wrap">
            <canvas id="tank-graph-canvas" class="w-full h-full block cursor-grab active:cursor-grabbing"></canvas>

            <!-- Floating Legend Bottom-Left -->
            <div class="absolute bottom-3 left-3 bg-slate-900/95 backdrop-blur border border-slate-700 rounded-lg p-2.5 shadow-xl flex flex-wrap items-center gap-3 text-xs text-slate-100 pointer-events-none max-w-[96%]">
              <div class="flex items-center gap-1.5"><span class="w-6 h-1 bg-emerald-400 inline-block rounded"></span><span class="font-semibold">Lineage / Evolution</span></div>
              <div class="flex items-center gap-1.5"><span class="w-6 h-0.5 border-b-2 border-dashed border-sky-400 inline-block"></span><span class="font-semibold">Design Similarity</span></div>
              <div class="flex items-center gap-1.5"><span class="w-6 h-1 bg-rose-500 inline-block rounded"></span><span class="font-semibold">⚔️ Fought Each Other</span></div>
            </div>

            <!-- Floating Hint Top-Right -->
            <div class="absolute top-3 right-3 bg-slate-900/90 backdrop-blur border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-amber-300 font-semibold pointer-events-none">
              Click any node for Tank Popup • Scroll to zoom
            </div>
          </div>
        </div>

        <!-- Right-Side Deep Tank & Combat Inspector -->
        <div class="lg:col-span-5 bg-[var(--card)] border border-[var(--border)] rounded-xl shadow-md flex flex-col h-[790px]">
          <div id="tank-inspector" class="flex-1 overflow-y-auto custom-scroll p-5 flex flex-col gap-4"></div>
        </div>
      </div>
    </section>

    <!-- ===================================================================== -->
    <!-- VIEW 5: HEAD-TO-HEAD TANK DUEL COMPARATOR                             -->
    <!-- ===================================================================== -->
    <section id="view-duel" role="tabpanel" aria-labelledby="tab-duel" class="hidden flex-col gap-4">
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-5 shadow-md flex flex-col gap-4">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-[var(--border)] pb-4">
          <div>
            <h2 class="text-base font-bold text-[var(--foreground)]">⚔️ Head-to-Head Tank Duel Comparator &amp; Historical Clash Analyzer</h2>
            <p class="text-xs text-[var(--muted-foreground)] mt-0.5">Select any two tanks from our 85-tank catalog or click a famous historical duel preset below:</p>
          </div>
          <div class="flex flex-wrap items-center gap-1.5">
            <button onclick="setDuelPair('kv1_kv2','pz_38t')" class="px-2.5 py-1 rounded text-xs font-extrabold bg-amber-500/20 text-amber-300 border border-amber-500/50">🔥 1941 Raseiniai: KV-1 vs Panzer 38(t)</button>
            <button onclick="setDuelPair('kv2','panzer_iv')" class="px-2.5 py-1 rounded text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/50">1941 Raseiniai: KV-2 (152mm) vs Panzer IV</button>
            <button onclick="setDuelPair('t34_76','tiger_i')" class="px-2.5 py-1 rounded text-xs font-semibold bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1943: T-34/76 vs Tiger I</button>
            <button onclick="setDuelPair('m4a3e8','panther')" class="px-2.5 py-1 rounded text-xs font-semibold bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1944: Easy Eight vs Panther</button>
            <button onclick="setDuelPair('m48_m60_patton','t54_55')" class="px-2.5 py-1 rounded text-xs font-bold bg-cyan-500/15 text-cyan-300 border border-cyan-500/40">🇻🇳 1972: M48A3 Patton vs NVA T-54</button>
            <button onclick="setDuelPair('shot_magach','t62')" class="px-2.5 py-1 rounded text-xs font-semibold bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1973: Sho't Kal vs T-62</button>
            <button onclick="setDuelPair('m1_abrams','t72')" class="px-2.5 py-1 rounded text-xs font-semibold bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">1991: M1A1 Abrams vs T-72</button>
            <button onclick="setDuelPair('leopard2_a7_kf51','t90m')" class="px-2.5 py-1 rounded text-xs font-semibold bg-[var(--background)] border border-[var(--border)] hover:border-rose-500">2024: Leopard 2A6 vs T-90M</button>
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
    <!-- VIEW 6: 2D TECH-TREE MATRIX, VIETNAM WAR SPECIAL DOSSIER & CATALOG    -->
    <!-- ===================================================================== -->
    <section id="view-matrix" role="tabpanel" aria-labelledby="tab-matrix" class="hidden flex-col gap-4">
      <!-- Special Feature Banner: Did the Vietnam War Involve Tank Battles? -->
      <div class="bg-gradient-to-r from-cyan-950/80 via-slate-900 to-rose-950/70 border-2 border-cyan-500/50 rounded-xl p-5 shadow-lg flex flex-col gap-3">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-1 rounded-md bg-cyan-500 text-slate-950 font-extrabold text-xs">🇻🇳 HISTORICAL DEEP-DIVE</span>
            <h2 class="text-base sm:text-lg font-extrabold text-white">Was the Vietnam War Involved in Any Tank Battles? — YES!</h2>
          </div>
          <button onclick="setConflictFilter('vietnam'); switchMainView('map'); flyToTheatre('VIETNAM_SEA');" class="px-3 py-1.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 text-xs font-extrabold transition shadow">
            🌍 View All 3 Vietnam War Tank Battles on Map →
          </button>
        </div>
        <p class="text-xs text-slate-200 leading-relaxed">
          Despite Vietnam's reputation as a helicopter and jungle-infantry conflict, over <strong>2,000 tanks</strong> fought across Vietnam, Laos, and Cambodia between 1965 and 1975. The North Vietnamese Army (PAVN/NVA) deployed Soviet <strong>PT-76 amphibious light tanks</strong>, <strong>T-34-85s</strong>, <strong>T-54/55s</strong>, and Chinese <strong>Type 59s</strong> against US Army/USMC <strong>M48A3 Pattons</strong>, <strong>M551 Sheridans</strong>, Australian <strong>Centurion Mk 5/1s</strong>, and South Vietnamese (ARVN) <strong>M41 Walker Bulldogs</strong>, <strong>M24 Chaffees</strong>, and <strong>M48A3s</strong>:
        </p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
          <div class="bg-slate-900/90 border border-cyan-500/40 rounded-lg p-3 flex flex-col justify-between gap-2">
            <div>
              <div class="text-xs font-bold text-cyan-300">1. Lang Vei (1968) &amp; Ben Het (1969)</div>
              <p class="text-xs text-slate-300 mt-1">In Feb 1968, 13 NVA <button onclick="openTankPopup('pt76')" class="text-amber-300 underline font-semibold">PT-76</button> tanks overran the US Green Beret camp at Lang Vei. On March 3, 1969 at <strong>Ben Het</strong>, US Army <button onclick="openTankPopup('m48_m60_patton')" class="text-amber-300 underline font-semibold">M48A3 Pattons</button> fought the <strong>only US-vs-NVA tank-on-tank night duel</strong> of the war, destroying 2 PT-76s by firing at their muzzle flashes.</p>
            </div>
            <button onclick="openBattlePage('lang_vei_ben_het_1968')" class="px-2.5 py-1.5 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold text-center">🎬 Open Battle Page &amp; Simulation</button>
          </div>
          <div class="bg-slate-900/90 border border-cyan-500/40 rounded-lg p-3 flex flex-col justify-between gap-2">
            <div>
              <div class="text-xs font-bold text-cyan-300">2. Operation Lam Son 719 (1971) &amp; Easter Offensive (1972)</div>
              <p class="text-xs text-slate-300 mt-1">In 1971, ARVN <button onclick="openTankPopup('m41_bulldog')" class="text-amber-300 underline font-semibold">M41 Walker Bulldogs</button> destroyed 6 T-54s &amp; 16 PT-76s in Laos. In April–June 1972 at <strong>Dong Ha, Kontum &amp; An Loc</strong>, 400+ NVA <button onclick="openTankPopup('t54_55')" class="text-amber-300 underline font-semibold">T-54</button> &amp; <button onclick="openTankPopup('type59_69')" class="text-amber-300 underline font-semibold">Type 59</button> tanks clashed with ARVN 20th Tank Regiment M48A3s at 2,800m and the first combat BGM-71 TOW missiles.</p>
            </div>
            <button onclick="openBattlePage('an_loc_dong_ha_1972')" class="px-2.5 py-1.5 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold text-center">🎬 Open Battle Page &amp; Simulation</button>
          </div>
          <div class="bg-slate-900/90 border border-cyan-500/40 rounded-lg p-3 flex flex-col justify-between gap-2">
            <div>
              <div class="text-xs font-bold text-cyan-300">3. Battle of Xuan Loc &amp; Fall of Saigon (April 1975)</div>
              <p class="text-xs text-slate-300 mt-1">Five NVA corps (~600 tanks) spearheaded the Ho Chi Minh Campaign. After fierce tank clashes against ARVN M48A3s and M41s at <strong>Xuan Loc</strong>, NVA <button onclick="openTankPopup('t54_55')" class="text-amber-300 underline font-semibold">T-54B #843</button> and <button onclick="openTankPopup('type59_69')" class="text-amber-300 underline font-semibold">Type 59 #390</button> crashed through the gates of Independence Palace on April 30, 1975.</p>
            </div>
            <button onclick="openBattlePage('xuan_loc_saigon_1975')" class="px-2.5 py-1.5 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold text-center">🎬 Open Battle Page &amp; Simulation</button>
          </div>
        </div>
      </div>

      <!-- 2D Scrollable Blueprint Matrix -->
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 shadow-md flex flex-col gap-3">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 class="text-base font-bold text-[var(--foreground)]">📐 2D Panning National Tech-Tree Matrix (85 Tanks, 1916–2026)</h2>
            <p class="text-xs text-[var(--muted-foreground)]">Freely pan diagonally across all 7 Nations × 7 Eras. Click any tank card to open its Tank Popup or Dedicated Page.</p>
          </div>
          <span class="text-xs text-amber-400 font-semibold">Tip: Click any tank to view its verified real photograph, blueprint &amp; videos</span>
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
      <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 shadow-md flex flex-col gap-3">
        <h3 class="text-sm font-bold text-[var(--foreground)]">📚 Complete World Tank Encyclopedia (85 Iconic Vehicles — Click Any Tank for Popup or Full Page)</h3>
        <div id="catalog-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3"></div>
      </div>
    </section>

  </main>
"""

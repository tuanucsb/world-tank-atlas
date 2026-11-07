# Part 2A of HTML v2 generator: State, Graph Canvas, Area-Colored World Map & Interactive Battle Popup
JS_PART_2A = r"""
    // Strategic Colored Geographic Areas on the World Map
    const STRATEGIC_REGIONS = [
      {
        id: "EUROPE_WEST",
        name: "Western Europe & Ardennes Theatre",
        fill: "rgba(16, 185, 129, 0.28)",
        stroke: "rgba(52, 211, 153, 0.85)",
        labelLon: 3.5, labelLat: 48.0,
        pts: [[-9.5,36.5],[-9.5,43.5],[-5.0,48.8],[1.8,51.2],[8.5,54.5],[14.8,54.2],[15.0,45.5],[16.5,38.0],[8.0,38.0],[-9.5,36.5]]
      },
      {
        id: "UK_ISLES",
        name: "British Isles (Birthplace of the Tank)",
        fill: "rgba(56, 189, 248, 0.30)",
        stroke: "rgba(56, 189, 248, 0.85)",
        labelLon: -3.5, labelLat: 55.2,
        pts: [[-10.5,50.0],[2.0,50.5],[2.0,59.0],[-10.5,59.0],[-10.5,50.0]]
      },
      {
        id: "EUROPE_EAST",
        name: "Eastern Front, Russia & Ukraine Steppe",
        fill: "rgba(244, 63, 94, 0.26)",
        stroke: "rgba(251, 113, 133, 0.85)",
        labelLon: 32.0, labelLat: 52.5,
        pts: [[15.0,45.5],[14.8,54.5],[21.0,56.5],[28.0,60.5],[48.0,60.0],[50.0,45.0],[38.0,44.0],[26.0,44.0],[15.0,45.5]]
      },
      {
        id: "NORTH_AFRICA_SINAI",
        name: "North Africa, Sinai & Golan Heights",
        fill: "rgba(245, 158, 11, 0.28)",
        stroke: "rgba(251, 191, 36, 0.88)",
        labelLon: 26.5, labelLat: 28.5,
        pts: [[-6.0,35.8],[10.5,37.2],[20.0,32.5],[32.5,31.5],[36.5,36.5],[38.5,33.5],[36.0,24.0],[20.0,23.5],[-6.0,25.0],[-6.0,35.8]]
      },
      {
        id: "GULF_ME",
        name: "Persian Gulf, Iraq & Khuzestan",
        fill: "rgba(249, 115, 22, 0.28)",
        stroke: "rgba(251, 146, 60, 0.88)",
        labelLon: 47.0, labelLat: 31.0,
        pts: [[38.5,33.5],[44.0,37.5],[52.0,35.0],[56.5,26.0],[46.0,24.0],[38.5,29.0],[38.5,33.5]]
      },
      {
        id: "SOUTH_ASIA",
        name: "South Asia / Indo-Pak Armor Theatre",
        fill: "rgba(236, 72, 153, 0.26)",
        stroke: "rgba(244, 114, 182, 0.85)",
        labelLon: 75.5, labelLat: 26.5,
        pts: [[66.0,24.0],[71.0,34.5],[80.0,32.0],[88.0,22.0],[77.5,8.0],[66.0,24.0]]
      },
      {
        id: "VIETNAM_SEA",
        name: "Vietnam, Laos & Southeast Asia Theatre",
        fill: "rgba(6, 182, 212, 0.34)",
        stroke: "rgba(34, 211, 238, 0.95)",
        labelLon: 106.5, labelLat: 15.5,
        pts: [[97.0,22.5],[109.8,22.0],[110.5,12.0],[104.5,8.5],[98.0,10.0],[97.0,22.5]]
      },
      {
        id: "EAST_ASIA",
        name: "East Asia, Khalkhin Gol & Korea",
        fill: "rgba(168, 85, 247, 0.26)",
        stroke: "rgba(192, 132, 252, 0.85)",
        labelLon: 121.0, labelLat: 42.0,
        pts: [[105.0,34.0],[112.0,50.5],[134.0,49.0],[142.0,38.0],[129.0,33.5],[118.0,29.0],[105.0,34.0]]
      }
    ];

    // Assign region colors to base continents so every continent has a rich area tint
    const CONTINENT_STYLES = {
      "Great Britain": { fill: "#163854", stroke: "#38bdf8" },
      "Ireland":       { fill: "#14354e", stroke: "#38bdf8" },
      "Eurasia":       { fill: "#182c42", stroke: "#475569" },
      "Africa":        { fill: "#292524", stroke: "#d9770688" },
      "North America": { fill: "#172554", stroke: "#60a5fa88" },
      "South America": { fill: "#14332a", stroke: "#34d39988" },
      "Australia":     { fill: "#2e1065", stroke: "#a78bfa88" },
      "Japan (Honshu/Kyushu/Hokkaido)": { fill: "#3b0764", stroke: "#c084fc" },
      "Hokkaido":      { fill: "#3b0764", stroke: "#c084fc" },
      "Taiwan":        { fill: "#164e63", stroke: "#22d3ee" },
      "Sri Lanka":     { fill: "#4a044e", stroke: "#f472b6" },
      "Sicily":        { fill: "#14532d", stroke: "#4ade80" }
    };

    // Lookup Maps
    const TANK_MAP = Object.fromEntries(TANKS.map(t => [t.id, t]));
    const NATION_MAP = Object.fromEntries(NATIONS.map(n => [n.id, n]));
    const BATTLE_MAP = Object.fromEntries(BATTLES.map(b => [b.id, b]));
    const ERA_MAP = Object.fromEntries(ERAS.map(e => [e.id, e]));

    // Application State (Starts on World Map with Battle of Raseiniai 1941 selected!)
    const state = {
      mainView: 'map',
      selectedTankId: 'kv1',
      hoveredTankId: null,
      selectedBattleId: 'raseiniai_1941',
      hoveredBattleId: null,
      hoveredMapTankId: null,
      mapPinMode: 'both', // 'both' | 'battles' | 'tanks'
      mapBattleId: null, // battle selected on the map (null on first load)
      tacticalZoomOpen: false,
      layers: { lineage: true, similarity: true, combat: true },
      conflictFilter: 'all',
      nationFilter: 'all',
      eraFilter: null,
      searchQuery: '',
      yMode: 'nation',
      gCam: { x: 0, y: 0, k: 1.0, dragging: false, sx: 0, sy: 0, moved: false },
      mCam: { lon: 25.0, lat: 46.5, k: 2.35, targetLon: 25.0, targetLat: 46.5, targetK: 2.35, dragging: false, sx: 0, sy: 0 },
      duelA: 'kv1',
      duelB: 'pz_38t',
      animTick: 0,
      // Live Battle Simulation State
      sim: {
        status: 'ready', // 'ready' | 'playing' | 'paused' | 'ended' (set via setSimStatus)
        stopAtPhases: true, // pause with a card at the start of each phase while playing
        phaseCard: null, // index of the phase whose card is showing
        playing: false,
        speed: 1.0,
        progress: 0.0, // 0.0 to 1.0
        showHulls: true,
        mapBgMode: 'historical', // 'historical' | 'topo' | 'satellite' | 'tactical'
        killcamIdx: 0,
        killcamTick: 0,
        logs: [],
        lastPhaseLogged: -1,
        hoveredAgentTankId: null
      }
    };

    // Real Tank Photograph & Historical Map Preload Cache for Canvas Sprites
    const TANK_IMG_CACHE = {};
    const URL_IMG_CACHE = {};
    function getTankImg(tankId) {
      const t = TANK_MAP[tankId];
      if (!t || !t.photo_url) return null;
      if (!TANK_IMG_CACHE[tankId]) {
        const img = new Image();
        img.src = t.photo_url;
        TANK_IMG_CACHE[tankId] = img;
      }
      const im = TANK_IMG_CACHE[tankId];
      return (im.complete && im.naturalWidth > 0) ? im : null;
    }
    function getUrlImg(url) {
      if (!url) return null;
      if (!URL_IMG_CACHE[url]) {
        const img = new Image();
        img.src = url;
        URL_IMG_CACHE[url] = img;
      }
      const im = URL_IMG_CACHE[url];
      return (im.complete && im.naturalWidth > 0) ? im : null;
    }

    // Conflict Preset Tank Sets (expanded for 85 tanks!)
    const CONFLICT_SETS = {
      ww1_interwar: new Set(TANKS.filter(t => t.era <= 2).map(t => t.id)),
      ww2: new Set(TANKS.filter(t => t.era === 3 || t.era === 4 || ['matilda_ii','valentine','somua_s35','char_b1','panzer_ii','pz_38t','t26','bt7','type95_hago','type95_97'].includes(t.id)).map(t => t.id)),
      vietnam: new Set(['m41_bulldog','pt76','m551_sheridan','m48_m60_patton','m60_patton','t54_55','type59_69','centurion_mk1','t34_85','m24_chaffee']),
      arab_israeli: new Set(['centurion_mk1','shot_magach','magach','m50_m51_sherman','m48_m60_patton','m60_patton','amx13_30','t34_85','is3','t54_55','t62','t72','bmp1','merkava_i_ii','merkava_iv','pt76']),
      gulf: new Set(['m1_abrams','m1a2_sepv3','m2_bradley','challenger1','challenger2_3','m48_m60_patton','m60_patton','amx30','chieftain','t72','t62','t54_55','type59_69','bmp1','m551_sheridan']),
      ukraine: new Set(['t64_t80','t80bvm','t84_oplot','t72','t90m','bmp1','m2_bradley','leopard1','leopard2_a4','leopard2_a7_kf51','m1_abrams','m1a2_sepv3','challenger2_3','pt76'])
    };

    function toggleTheme() {
      document.documentElement.classList.toggle('light-theme');
    }

    function toggleViewMenu(open) {
      const menu = document.getElementById('view-menu');
      const btn = document.getElementById('view-menu-btn');
      const show = open === undefined ? menu.classList.contains('hidden') : open;
      menu.classList.toggle('hidden', !show);
      btn.setAttribute('aria-expanded', show ? 'true' : 'false');
    }

    function toggleMobileSearch() {
      const bar = document.getElementById('app-bar');
      const open = !bar.classList.contains('search-open');
      bar.classList.toggle('search-open', open);
      document.getElementById('mobile-search-btn').setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) document.getElementById('search-input').focus();
    }

    // Bottom sheet (below 1024px): tap the handle to toggle, or drag it and let go to snap
    (() => {
      let drag = null;
      document.addEventListener('pointerdown', (e) => {
        const handle = e.target.closest('.sheet-handle');
        if (!handle || !matchMedia('(max-width: 1023px)').matches) return;
        const sheet = handle.closest('.sheet');
        drag = { sheet, startY: e.clientY, full: sheet.classList.contains('sheet-full'), moved: 0 };
        sheet.classList.add('sheet-dragging');
        handle.setPointerCapture(e.pointerId);
      });
      document.addEventListener('pointermove', (e) => {
        if (!drag) return;
        drag.moved = e.clientY - drag.startY;
        const peek = window.innerHeight * 0.6;
        const base = drag.full ? 0 : peek;
        drag.sheet.style.transform = `translateY(${Math.min(peek, Math.max(0, base + drag.moved))}px)`;
      });
      document.addEventListener('pointerup', () => {
        if (!drag) return;
        const { sheet, full, moved } = drag;
        sheet.classList.remove('sheet-dragging');
        sheet.style.transform = '';
        const open = Math.abs(moved) < 8 ? !full : moved < 0;
        sheet.classList.toggle('sheet-full', open);
        drag = null;
      });
    })();

    function toggleSiteMenu(open) {
      const menu = document.getElementById('site-menu');
      const btn = document.getElementById('site-switcher-btn');
      const show = open === undefined ? menu.classList.contains('hidden') : open;
      menu.classList.toggle('hidden', !show);
      btn.setAttribute('aria-expanded', show ? 'true' : 'false');
    }

    document.addEventListener('click', (e) => {
      if (!e.target.closest('#site-menu, #site-switcher-btn')) toggleSiteMenu(false);
      if (!e.target.closest('#view-menu-btn') || e.target.closest('#view-menu')) toggleViewMenu(false);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { toggleSiteMenu(false); toggleViewMenu(false); }
    });

    function setMapPinMode(mode) {
      state.mapPinMode = mode;
      ['both', 'battles', 'tanks'].forEach(m => {
        const el = document.getElementById('mpm-' + m);
        if (!el) return;
        el.className = m === mode
          ? 'px-2.5 py-1 rounded text-xs font-extrabold bg-amber-500 text-slate-950'
          : 'px-2.5 py-1 rounded text-xs font-semibold bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)]';
      });
    }

    // UNIVERSAL INTERACTIVE TANK POPUP MODAL (Opens over ANY screen when clicking a tank!)
    function openTankPopup(tankId) {
      const t = TANK_MAP[tankId];
      if (!t) return;
      state.selectedTankId = tankId;
      const modal = document.getElementById('tank-popup-modal');
      const card = document.getElementById('tank-popup-card');
      if (!modal || !card) return;

      const nat = NATION_MAP[t.nation] || { flag: '🛡️', name: '', color: '#38bdf8' };
      const era = ERA_MAP[t.era] || { short: '', name: '' };
      const battlesFought = BATTLES.filter(b => b.side_a.tanks.includes(t.id) || b.side_b.tanks.includes(t.id));
      const combats = EDGES.filter(e => e.type === 'combat' && (e.source === t.id || e.target === t.id)).map(e => {
        const otherId = e.source === t.id ? e.target : e.source;
        return { tank: TANK_MAP[otherId], label: e.label };
      }).filter(x => x.tank);
      const parents = EDGES.filter(e => e.type === 'lineage' && e.target === t.id).map(e => TANK_MAP[e.source]).filter(Boolean);
      const children = EDGES.filter(e => e.type === 'lineage' && e.source === t.id).map(e => TANK_MAP[e.target]).filter(Boolean);

      card.innerHTML = `
        <div class="flex flex-wrap items-start justify-between gap-3 border-b border-slate-700 pb-3">
          <div>
            <div class="flex flex-wrap items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-extrabold border" style="border-color:${nat.color}; background:${nat.color}25; color:${nat.color}">
                ${nat.flag} ${nat.name} • ${t.year}
              </span>
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">${era.name}</span>
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-800 text-slate-200 border border-slate-600">${t.role}</span>
            </div>
            <h2 class="text-xl sm:text-2xl font-extrabold text-white mt-1.5">${t.name}</h2>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="closeTankPopup(); openTankPage('${t.id}')" class="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-extrabold shadow">
              📄 Open Full Tank Page &amp; Gallery →
            </button>
            <button onclick="closeTankPopup()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-600 text-white text-xs font-extrabold">
              ✕ Close
            </button>
          </div>
        </div>

        <!-- Real Photograph + Technical Blueprint Side-by-Side -->
        <div class="grid grid-cols-1 md:grid-cols-12 gap-4 items-stretch">
          <div class="md:col-span-6 bg-slate-950 border border-slate-700 rounded-xl overflow-hidden flex flex-col justify-between">
            <div class="h-60 sm:h-64 w-full flex items-center justify-center bg-slate-950 overflow-hidden relative">
              <img src="${t.image_url}" alt="${t.name}" class="w-full h-full object-contain" />
            </div>
            <div class="px-3 py-2 bg-slate-900 border-t border-slate-800 flex items-center justify-between text-xs text-slate-300">
              <span>📸 Real Historical Photograph: <strong>${t.name}</strong></span>
              <a href="${t.image_url}" target="_blank" rel="noopener noreferrer" class="text-amber-400 hover:underline font-bold">Full Photo ↗</a>
            </div>
          </div>
          <div class="md:col-span-6 bg-slate-950 border border-slate-700 rounded-xl overflow-hidden flex flex-col justify-between">
            <div class="h-60 sm:h-64 w-full flex items-center justify-center p-2">
              ${typeof buildTankBlueprintSVG === 'function' ? buildTankBlueprintSVG(t) : ''}
            </div>
            <div class="px-3 py-2 bg-slate-900 border-t border-slate-800 flex items-center justify-between text-xs text-slate-300">
              <span>📐 Scaled Engineering Profile</span>
              <span class="font-mono text-emerald-400">${t.weight_t}t • ${t.armor_mm}mm RHAe • ${t.speed_kmh} km/h</span>
            </div>
          </div>
        </div>

        <p class="text-xs sm:text-sm text-slate-200 leading-relaxed bg-slate-950/80 p-3.5 rounded-xl border border-slate-800">${t.summary}</p>

        <!-- Key Specs Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
          <div class="bg-slate-950 border border-slate-800 rounded-lg p-2.5">
            <div class="text-xs text-slate-400 uppercase font-bold">Primary Armament</div>
            <div class="font-extrabold text-white mt-0.5">${t.gun}</div>
          </div>
          <div class="bg-slate-950 border border-slate-800 rounded-lg p-2.5">
            <div class="text-xs text-slate-400 uppercase font-bold">Frontal Armor</div>
            <div class="font-extrabold text-amber-400 mt-0.5">${t.armor_mm} mm RHAe</div>
          </div>
          <div class="bg-slate-950 border border-slate-800 rounded-lg p-2.5">
            <div class="text-xs text-slate-400 uppercase font-bold">Weight &amp; Mobility</div>
            <div class="font-extrabold text-emerald-400 mt-0.5">${t.weight_t}t • ${t.speed_kmh} km/h (${t.power_hp} hp)</div>
          </div>
          <div class="bg-slate-950 border border-slate-800 rounded-lg p-2.5">
            <div class="text-xs text-slate-400 uppercase font-bold">Crew &amp; Production</div>
            <div class="font-extrabold text-sky-400 mt-0.5">${t.crew} Crew • ~${t.produced.toLocaleString()} Built</div>
          </div>
        </div>

        <!-- Battles Fought & Combat Rivals -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div class="bg-amber-500/10 border border-amber-500/35 rounded-xl p-3 flex flex-col gap-2">
            <div class="font-extrabold text-amber-300 uppercase">🌍 Major Battles Fought (${battlesFought.length})</div>
            ${battlesFought.length ? battlesFought.map(b => `
              <div class="p-2 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <div class="font-bold text-white">${b.name} (${b.year})</div>
                  <div class="text-xs text-slate-400">${b.total_tanks}</div>
                </div>
                <div class="flex items-center gap-1 shrink-0">
                  <button onclick="closeTankPopup(); jumpToBattleOnMap('${b.id}')" class="px-2 py-1 rounded bg-amber-500/20 border border-amber-500/50 text-amber-300 text-xs font-bold">📍 Map</button>
                  <button onclick="closeTankPopup(); openBattlePage('${b.id}')" class="px-2 py-1 rounded bg-rose-600 text-white text-xs font-bold">🎬 Sim</button>
                </div>
              </div>
            `).join('') : '<div class="text-slate-400">Deterrence, evaluation, or secondary sectors.</div>'}
          </div>

          <div class="bg-rose-500/10 border border-rose-500/35 rounded-xl p-3 flex flex-col gap-2">
            <div class="font-extrabold text-rose-300 uppercase">⚔️ Direct Combat Rivals (${combats.length} — Click to Inspect)</div>
            ${combats.length ? `<div class="flex flex-col gap-1.5 max-h-44 overflow-y-auto custom-scroll pr-1">
              ${combats.map(c => `
                <button onclick="openTankPopup('${c.tank.id}')" class="p-2 rounded-lg bg-slate-950 border border-slate-800 hover:border-rose-400 text-left flex items-center justify-between gap-2 transition">
                  <div class="flex items-center gap-2">
                    <img src="${c.tank.image_url}" alt="${c.tank.name}" class="w-10 h-7 rounded object-cover bg-slate-900 border border-slate-700 shrink-0" />
                    <div>
                      <div class="font-bold text-rose-300">⚔️ ${NATION_MAP[c.tank.nation]?.flag || ''} ${c.tank.name} (${c.tank.year})</div>
                      <div class="text-xs text-slate-400 line-clamp-1">${c.label}</div>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-amber-300 shrink-0">Popup →</span>
                </button>
              `).join('')}
            </div>` : '<div class="text-slate-400">No direct tank duel in dataset.</div>'}
          </div>
        </div>

        <!-- Lineage & Video Links -->
        <div class="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-800 text-xs">
          <div class="flex flex-wrap items-center gap-1.5">
            <span class="font-bold text-emerald-400">🟢 Lineage:</span>
            ${parents.map(p => `<button onclick="openTankPopup('${p.id}')" class="px-2 py-0.5 rounded bg-emerald-950 border border-emerald-500/50 text-emerald-300 font-bold">⬅️ ${p.name}</button>`).join('')}
            ${children.map(c => `<button onclick="openTankPopup('${c.id}')" class="px-2 py-0.5 rounded bg-emerald-950 border border-emerald-500/50 text-emerald-300 font-bold">➡️ ${c.name}</button>`).join('')}
          </div>
          <div class="flex flex-wrap items-center gap-1.5">
            ${(t.videos || []).slice(0, 2).map(v => `
              <a href="${v.url}" target="_blank" rel="noopener noreferrer" class="px-2.5 py-1 rounded bg-red-600/20 border border-red-500/50 text-red-300 hover:bg-red-600 hover:text-white font-bold transition">
                ▶ ${v.title} ↗
              </a>
            `).join('')}
          </div>
        </div>
      `;

      modal.classList.remove('hidden');
      modal.classList.add('flex');
      renderTankInspector();
    }

    function closeTankPopup() {
      const modal = document.getElementById('tank-popup-modal');
      if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
      }
    }

    function isTankVisible(t) {
      if (state.eraFilter && t.era !== state.eraFilter) return false;
      if (state.nationFilter !== 'all' && t.nation !== state.nationFilter) return false;
      if (state.conflictFilter !== 'all' && CONFLICT_SETS[state.conflictFilter] && !CONFLICT_SETS[state.conflictFilter].has(t.id)) return false;
      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase();
        const inBattles = BATTLES.some(b => (b.side_a.tanks.includes(t.id) || b.side_b.tanks.includes(t.id)) && (b.name.toLowerCase().includes(q) || b.location.toLowerCase().includes(q) || b.theatre.toLowerCase().includes(q)));
        const match = t.name.toLowerCase().includes(q) || t.gun.toLowerCase().includes(q) || t.role.toLowerCase().includes(q) || t.summary.toLowerCase().includes(q) || inBattles;
        if (!match) return false;
      }
      return true;
    }

    function getGraphNodePos(t, W, H) {
      const padLeft = 152, padRight = 55, padTop = 78, padBottom = 42;
      const usableW = Math.max(850, W) - padLeft - padRight;
      const usableH = Math.max(540, H) - padTop - padBottom;
      const colW = usableW / 7;
      const x = padLeft + (t.era - 0.5) * colW + (t.x_offset || 0) * (colW * 0.54);
      let y;
      if (state.yMode === 'nation') {
        const lane = NATION_MAP[t.nation]?.lane ?? 0;
        const laneH = usableH / 7;
        y = padTop + (lane + 0.5) * laneH + (t.lane_offset || 0) * (laneH * 0.60);
      } else {
        const normW = Math.min(1, Math.max(0, (t.weight_t - 5) / 65));
        y = padTop + (1 - normW) * usableH;
      }
      return { x, y };
    }

    function renderEraStepper() {
      const el = document.getElementById('era-stepper-bar');
      if (!el) return;
      el.innerHTML = ERAS.map(e => {
        const active = state.eraFilter === e.id;
        return `<button onclick="toggleEraFilter(${e.id})" class="text-left p-2 rounded-lg border transition ${active ? 'border-amber-400 bg-amber-500/25 shadow' : 'border-[var(--border)] bg-[var(--background)]/70 hover:border-amber-500/60'}">
          <div class="text-xs font-extrabold ${active ? 'text-amber-300' : 'text-[var(--foreground)]'} truncate">${e.short}</div>
          <div class="text-xs text-[var(--muted-foreground)] truncate mt-0.5">${e.desc}</div>
        </button>`;
      }).join('');
    }

    function toggleEraFilter(eraId) {
      state.eraFilter = (state.eraFilter === eraId) ? null : eraId;
      renderEraStepper();
      renderMapTankPhotoStrip();
      if (typeof renderAll85TanksPhotoGrid === 'function') renderAll85TanksPhotoGrid();
      renderCatalogAndMatrix();
    }

    function toggleEdgeLayer(layer) {
      state.layers[layer] = !state.layers[layer];
      const btn = document.getElementById('layer-' + layer);
      const labels = {
        lineage: ['🟢 Lineage: ON', '⚪ Lineage: OFF', 'emerald'],
        similarity: ['🔵 Similarity: ON', '⚪ Similarity: OFF', 'sky'],
        combat: ['⚔️ 🔴 Fought Each Other: ON', '⚪ Fought Each Other: OFF', 'rose']
      };
      const [onTxt, offTxt, col] = labels[layer];
      if (state.layers[layer]) {
        btn.textContent = onTxt;
        btn.className = `px-2.5 py-1 rounded-md text-xs font-bold border border-${col}-500/70 bg-${col}-500/20 text-${col}-300 transition`;
      } else {
        btn.textContent = offTxt;
        btn.className = `px-2.5 py-1 rounded-md text-xs font-medium border border-[var(--border)] bg-[var(--background)] text-[var(--muted-foreground)] transition`;
      }
    }

    function setConflictFilter(cf) {
      state.conflictFilter = cf;
      document.querySelectorAll('.cf-btn').forEach(b => {
        b.setAttribute('aria-pressed', b.id === 'cf-' + cf ? 'true' : 'false');
      });
      renderMapTankPhotoStrip();
      if (typeof renderAll85TanksPhotoGrid === 'function') renderAll85TanksPhotoGrid();
      renderCatalogAndMatrix();
    }

    function setNationFilter(nat) {
      state.nationFilter = nat;
      renderMapTankPhotoStrip();
      if (typeof renderAll85TanksPhotoGrid === 'function') renderAll85TanksPhotoGrid();
      renderCatalogAndMatrix();
    }

    function handleSearch(val) {
      state.searchQuery = val.trim();
      document.getElementById('clear-search').classList.toggle('hidden', !state.searchQuery);
      renderMapTankPhotoStrip();
      if (typeof renderAll85TanksPhotoGrid === 'function') renderAll85TanksPhotoGrid();
      renderCatalogAndMatrix();
    }

    function clearSearch() {
      document.getElementById('search-input').value = '';
      handleSearch('');
    }

    function setGraphYMode(mode) {
      state.yMode = mode;
      document.getElementById('ymode-nation').className = mode === 'nation'
        ? 'px-2.5 py-1 rounded text-xs font-bold bg-amber-500 text-slate-950'
        : 'px-2.5 py-1 rounded text-xs font-semibold bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)]';
      document.getElementById('ymode-weight').className = mode === 'weight'
        ? 'px-2.5 py-1 rounded text-xs font-bold bg-amber-500 text-slate-950'
        : 'px-2.5 py-1 rounded text-xs font-semibold bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)]';
    }

    // Views that use the era/nation filter row under the app bar
    const FILTERED_VIEWS = ['map', 'tank-page', 'graph'];

    // Renders a view. Call switchMainView() instead, which routes through the URL hash.
    function showView(view) {
      if (view !== 'battle-page' && state.sim.status === 'playing') setSimStatus('paused');
      state.mainView = view;
      ['graph', 'map', 'tank-page', 'battle-page', 'duel', 'matrix'].forEach(v => {
        const sec = document.getElementById('view-' + v);
        const tab = document.getElementById('tab-' + v);
        if (!sec || !tab) return;
        if (v === view) {
          sec.classList.remove('hidden');
          sec.classList.add('flex');
          tab.setAttribute('aria-current', 'page');
        } else {
          sec.classList.add('hidden');
          sec.classList.remove('flex');
          tab.removeAttribute('aria-current');
        }
      });
      document.getElementById('filter-row').classList.toggle('hidden', !FILTERED_VIEWS.includes(view));
      document.body.dataset.view = view;
      document.querySelectorAll('[data-view-link]').forEach(b => {
        if (b.dataset.viewLink === view) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
      });
      document.getElementById('atlas-summary').classList.toggle('hidden', view !== 'map');
      document.getElementById('theatre-select').classList.toggle('hidden', view !== 'map');
      if (view === 'tank-page') {
        if (typeof renderAll85TanksPhotoGrid === 'function') renderAll85TanksPhotoGrid();
        renderTankPage();
      }
      if (view === 'battle-page') renderBattlePage();
      if (view === 'duel') updateDuelView();
      if (view === 'matrix') renderCatalogAndMatrix();
    }

    function showTankPage(tankId) {
      if (TANK_MAP[tankId]) {
        state.selectedTankId = tankId;
      }
      const sel = document.getElementById('tank-page-select');
      if (sel) sel.value = state.selectedTankId;
      showView('tank-page');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function showBattlePage(battleId, initialProgress = 0.05) {
      if (BATTLE_MAP[battleId]) {
        state.selectedBattleId = battleId;
      }
      const sel = document.getElementById('battle-page-select');
      if (sel) sel.value = state.selectedBattleId;
      state.sim.progress = initialProgress;
      state.sim.status = 'ready';
      state.sim.playing = false;
      state.sim.selectedAgentId = null;
      state.sim.statusBeforeSelect = null;
      state.sim.logs = [];
      state.sim.lastPhaseLogged = -1;
      showView('battle-page');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // =========================================================================
    // ROUTER: the URL hash is the single owner of navigation.
    // switchMainView / openTankPage / openBattlePage only change the hash;
    // applyRoute() reads it and calls the show*() renderers. Routes use data ids:
    //   #/map  #/battles  #/battles/<id>  #/tanks  #/tanks/<id>
    //   #/lineage  #/compare  #/tech-tree
    // =========================================================================
    const VIEW_ROUTES = {
      'map': 'map', 'battle-page': 'battles', 'tank-page': 'tanks',
      'graph': 'lineage', 'duel': 'compare', 'matrix': 'tech-tree'
    };
    const ROUTE_VIEWS = Object.fromEntries(Object.entries(VIEW_ROUTES).map(([v, r]) => [r, v]));
    let lastAppliedHash = null;
    let pendingBattleProgress = null;

    function navigate(hash) {
      if (location.hash !== hash) location.hash = hash;
      applyRoute();
    }

    function switchMainView(view) {
      navigate('#/' + (VIEW_ROUTES[view] || 'map'));
    }

    function openTankPage(tankId) {
      navigate('#/tanks/' + tankId);
    }

    function openBattlePage(battleId, initialProgress = 0.05) {
      pendingBattleProgress = initialProgress;
      navigate('#/battles/' + battleId);
    }

    function replaceRoute(hash) {
      history.replaceState(null, '', hash);
    }

    function applyRoute() {
      const hash = location.hash || '#/map';
      if (hash === lastAppliedHash && pendingBattleProgress === null) return;
      lastAppliedHash = hash;
      hideRouteNotice();
      const [path, query] = hash.split('?');
      const [section, id] = path.replace(/^#\/?/, '').split('/').map(decodeURIComponent);
      const t = parseFloat(new URLSearchParams(query || '').get('t'));

      if (section === 'battles' && id) {
        const progress = pendingBattleProgress !== null ? pendingBattleProgress
          : (t >= 0 && t <= 1 ? Math.min(0.999, t) : 0.05);
        pendingBattleProgress = null;
        if (BATTLE_MAP[id]) return showBattlePage(id, progress);
        replaceRoute(lastAppliedHash = '#/battles');
        showView('battle-page');
        return showRouteNotice('battle', id);
      }
      pendingBattleProgress = null;
      if (section === 'tanks' && id) {
        if (TANK_MAP[id]) return showTankPage(id);
        replaceRoute(lastAppliedHash = '#/tanks');
        showView('tank-page');
        return showRouteNotice('tank', id);
      }
      if (ROUTE_VIEWS[section]) return showView(ROUTE_VIEWS[section]);
      replaceRoute(lastAppliedHash = '#/map');
      showView('map');
    }

    // "Nothing matches" notice for links to a battle or tank that doesn't exist
    const ROUTE_SUGGESTIONS = [
      { label: 'Tiger I', hash: '#/tanks/tiger_i' },
      { label: 'Kursk 1943', hash: '#/battles/kursk_1943' },
      { label: 'T-34-85', hash: '#/tanks/t34_85' }
    ];

    function showRouteNotice(kind, id) {
      const el = document.getElementById('route-notice');
      const safeId = String(id).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
      el.innerHTML = `
        <p class="font-semibold text-[var(--foreground)]">No ${kind} matches "${safeId}"</p>
        <p class="text-sm text-[var(--muted-foreground)]">The link may be mistyped or out of date. Try one of these:</p>
        <div class="flex flex-wrap gap-2 mt-1">
          ${ROUTE_SUGGESTIONS.map(s => `<a href="${s.hash}" class="cf-btn inline-flex items-center">${s.label}</a>`).join('')}
          <button onclick="hideRouteNotice()" class="cf-btn">Dismiss</button>
        </div>`;
      el.classList.remove('hidden');
    }

    function hideRouteNotice() {
      const el = document.getElementById('route-notice');
      if (el) el.classList.add('hidden');
    }

    window.addEventListener('hashchange', applyRoute);

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

    function stepTankPage(delta) {
      const idx = TANKS.findIndex(t => t.id === state.selectedTankId);
      const next = TANKS[(idx + delta + TANKS.length) % TANKS.length];
      openTankPage(next.id);
    }

    function stepBattlePage(delta) {
      const idx = BATTLES.findIndex(b => b.id === state.selectedBattleId);
      const next = BATTLES[(idx + delta + BATTLES.length) % BATTLES.length];
      openBattlePage(next.id);
    }

    // Render Right-Side Tank & Combat Inspector (with direct links to Tank Page & Battle Page!)
    function renderTankInspector() {
      const t = TANK_MAP[state.selectedTankId] || TANKS[0];
      const nat = NATION_MAP[t.nation];
      const era = ERA_MAP[t.era];

      const parents = EDGES.filter(e => e.type === 'lineage' && e.target === t.id).map(e => ({ tank: TANK_MAP[e.source], label: e.label })).filter(x => x.tank);
      const children = EDGES.filter(e => e.type === 'lineage' && e.source === t.id).map(e => ({ tank: TANK_MAP[e.target], label: e.label })).filter(x => x.tank);
      const similar = EDGES.filter(e => e.type === 'similarity' && (e.source === t.id || e.target === t.id)).map(e => {
        const otherId = e.source === t.id ? e.target : e.source;
        return { tank: TANK_MAP[otherId], label: e.label };
      }).filter(x => x.tank);
      const combats = EDGES.filter(e => e.type === 'combat' && (e.source === t.id || e.target === t.id)).map(e => {
        const otherId = e.source === t.id ? e.target : e.source;
        return { tank: TANK_MAP[otherId], label: e.label, battles: (e.battles || []).map(bid => BATTLE_MAP[bid]).filter(Boolean) };
      }).filter(x => x.tank);
      const battlesFought = BATTLES.filter(b => b.side_a.tanks.includes(t.id) || b.side_b.tanks.includes(t.id));

      document.getElementById('tank-inspector').innerHTML = `
        <div class="border-b border-[var(--border)] pb-3">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold border" style="border-color:${nat.color}88; background:${nat.color}25; color:${nat.color}">
              ${nat.flag} ${nat.name} • ${t.year}
            </span>
            <span class="text-xs font-bold text-amber-400">${era.short}</span>
          </div>
          <div class="flex items-center justify-between gap-2 mt-2">
            <h2 class="text-xl font-extrabold text-[var(--foreground)]">${t.name}</h2>
            <button onclick="openTankPage('${t.id}')" class="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-extrabold shadow transition shrink-0">
              📄 Open Full Tank Page (Photos &amp; Videos) →
            </button>
          </div>
          <p class="text-xs text-[var(--muted-foreground)] font-semibold mt-0.5">${t.role} • Production: ~${t.produced.toLocaleString()} units</p>

          <!-- Thumbnail Photo + Quick Links -->
          <div class="mt-3 grid grid-cols-1 sm:grid-cols-12 gap-3 bg-[var(--background)] p-2.5 rounded-xl border border-[var(--border)] items-center">
            <div class="sm:col-span-5 h-28 rounded-lg overflow-hidden bg-slate-950 border border-slate-700 flex items-center justify-center relative">
              <img src="${t.image_url}" alt="${t.name}" class="w-full h-full object-cover" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
              <div class="hidden absolute inset-0 items-center justify-center text-xs text-slate-400 font-bold p-2 text-center">🛡️ ${t.name}</div>
            </div>
            <div class="sm:col-span-7 flex flex-col gap-1.5">
              <p class="text-xs text-[var(--foreground)] leading-relaxed line-clamp-3">${t.summary}</p>
              <div class="flex flex-wrap gap-1.5 pt-1">
                <button onclick="openTankPage('${t.id}')" class="px-2 py-1 rounded bg-sky-500/20 border border-sky-500/50 text-sky-300 text-xs font-bold hover:bg-sky-500/30">
                  📸 View High-Res Photo, Blueprint &amp; Videos
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Technical Specs Grid -->
        <div class="grid grid-cols-3 gap-2 text-xs">
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-2.5">
            <div class="text-xs text-[var(--muted-foreground)] uppercase font-bold">Main Gun</div>
            <div class="font-bold text-[var(--foreground)] mt-0.5 leading-snug">${t.gun}</div>
          </div>
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-2.5">
            <div class="text-xs text-[var(--muted-foreground)] uppercase font-bold">Frontal Armor</div>
            <div class="font-bold text-amber-400 mt-0.5">${t.armor_mm} mm RHAe</div>
          </div>
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-2.5">
            <div class="text-xs text-[var(--muted-foreground)] uppercase font-bold">Weight / Speed</div>
            <div class="font-bold text-emerald-400 mt-0.5">${t.weight_t}t • ${t.speed_kmh} km/h</div>
          </div>
        </div>

        <!-- Historic Battles Fought (Direct Links to Battle Pages & Map) -->
        <div class="bg-amber-500/10 border border-amber-500/40 rounded-xl p-3 flex flex-col gap-2">
          <div class="text-xs font-extrabold text-amber-300 uppercase tracking-wider">🌍 Battles Fought (${battlesFought.length} Recorded Battles)</div>
          ${battlesFought.length ? `<div class="flex flex-col gap-1.5">
            ${battlesFought.map(b => `
              <div class="p-2 rounded-lg bg-[var(--card)] border border-[var(--border)] flex flex-wrap items-center justify-between gap-2">
                <div>
                  <div class="text-xs font-bold text-[var(--foreground)]">${b.name} (${b.year})</div>
                  <div class="text-xs text-emerald-400 font-semibold">🏆 Winner: ${b.winner}</div>
                </div>
                <div class="flex items-center gap-1">
                  <button onclick="jumpToBattleOnMap('${b.id}')" class="px-2 py-1 rounded bg-amber-500/20 border border-amber-500/50 text-amber-300 text-xs font-bold hover:bg-amber-500/30">🌍 Map Popup</button>
                  <button onclick="openBattlePage('${b.id}')" class="px-2 py-1 rounded bg-rose-600 text-white text-xs font-bold hover:bg-rose-500">🎬 Battle Page &amp; Sim</button>
                </div>
              </div>
            `).join('')}
          </div>` : '<div class="text-xs text-[var(--muted-foreground)]">Deterrence / training / interwar prototype.</div>'}
        </div>

        <!-- Combat Opponents ("Fought Against") -->
        <div class="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3.5 flex flex-col gap-2">
          <div class="flex items-center justify-between">
            <span class="text-xs font-extrabold text-rose-400 uppercase tracking-wider">⚔️ Fought Against (${combats.length} Rivals)</span>
            <button onclick="state.duelA='${t.id}'; state.duelB='${combats[0]?.tank?.id || 'tiger_i'}'; switchMainView('duel')" class="px-2 py-0.5 rounded bg-rose-600 text-white text-xs font-bold hover:bg-rose-500">
              ⚔️ Compare in Duel View
            </button>
          </div>
          ${combats.length ? combats.map(c => `
            <div class="bg-[var(--card)] border border-[var(--border)] rounded-lg p-2.5 flex flex-col gap-1">
              <div class="flex items-center justify-between gap-2">
                <button onclick="selectTank('${c.tank.id}')" class="text-xs font-bold text-rose-300 hover:underline text-left">
                  ⚔️ vs. ${NATION_MAP[c.tank.nation].flag} ${c.tank.name} (${c.tank.year})
                </button>
                <button onclick="openTankPage('${c.tank.id}')" class="px-2 py-0.5 rounded bg-sky-500/20 border border-sky-500/40 text-xs text-sky-300 font-bold hover:bg-sky-500/30">
                  📄 Tank Page
                </button>
              </div>
              <div class="text-xs text-[var(--muted-foreground)]">${c.label}</div>
            </div>
          `).join('') : '<div class="text-xs text-[var(--muted-foreground)]">No direct tank-on-tank duel in dataset.</div>'}
        </div>

        <!-- Lineage Evolution Chain -->
        <div class="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-3.5 flex flex-col gap-2">
          <div class="text-xs font-extrabold text-emerald-400 uppercase tracking-wider">🟢 Lineage &amp; Evolutionary Chain</div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <div>
              <div class="text-xs font-bold text-[var(--muted-foreground)] mb-1">⬅️ Evolved From:</div>
              ${parents.length ? parents.map(p => `
                <div class="p-2 rounded bg-[var(--card)] border border-[var(--border)] mb-1 flex items-center justify-between gap-1">
                  <button onclick="selectTank('${p.tank.id}')" class="text-left text-xs font-bold text-emerald-300 hover:underline">${NATION_MAP[p.tank.nation].flag} ${p.tank.name}</button>
                  <button onclick="openTankPage('${p.tank.id}')" class="px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 text-xs font-bold">Page →</button>
                </div>
              `).join('') : '<div class="text-xs text-[var(--muted-foreground)] italic">Foundational 1st-Gen Design</div>'}
            </div>
            <div>
              <div class="text-xs font-bold text-[var(--muted-foreground)] mb-1">➡️ Evolved Into:</div>
              ${children.length ? children.map(c => `
                <div class="p-2 rounded bg-[var(--card)] border border-[var(--border)] mb-1 flex items-center justify-between gap-1">
                  <button onclick="selectTank('${c.tank.id}')" class="text-left text-xs font-bold text-emerald-300 hover:underline">${NATION_MAP[c.tank.nation].flag} ${c.tank.name}</button>
                  <button onclick="openTankPage('${c.tank.id}')" class="px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 text-xs font-bold">Page →</button>
                </div>
              `).join('') : '<div class="text-xs text-[var(--muted-foreground)] italic">Current-Gen Pinnacle</div>'}
            </div>
          </div>
        </div>
      `;
    }

    // =========================================================================
    // 1. INTERACTIVE GRAPH CANVAS (HIGH-CONTRAST NODES & LINKS)
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

      canvas.addEventListener('click', () => {
        if (state.gCam.moved) return;
        if (state.hoveredTankId) {
          selectTank(state.hoveredTankId);
          openTankPopup(state.hoveredTankId);
        }
      });

      canvas.addEventListener('dblclick', () => {
        if (state.hoveredTankId) {
          openTankPage(state.hoveredTankId);
        }
      });

      canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        const factor = e.deltaY < 0 ? 1.14 : 0.88;
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

      // High-contrast dark slate background
      ctx.fillStyle = '#080f1e';
      ctx.fillRect(0, 0, W, H);

      ctx.save();
      ctx.translate(state.gCam.x, state.gCam.y);
      ctx.scale(state.gCam.k, state.gCam.k);

      const padLeft = 152, padRight = 55, padTop = 78, padBottom = 42;
      const usableW = Math.max(850, W) - padLeft - padRight;
      const usableH = Math.max(540, H) - padTop - padBottom;
      const colW = usableW / 7;

      // Draw Era Vertical Columns
      ERAS.forEach((era, idx) => {
        const x0 = padLeft + idx * colW;
        ctx.fillStyle = idx % 2 === 0 ? 'rgba(30, 41, 59, 0.35)' : 'rgba(15, 23, 42, 0.20)';
        ctx.fillRect(x0, padTop - 38, colW, usableH + 58);

        ctx.strokeStyle = 'rgba(148, 163, 184, 0.22)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(x0, padTop - 38);
        ctx.lineTo(x0, padTop + usableH + 20);
        ctx.stroke();

        ctx.fillStyle = state.eraFilter === era.id ? '#fbbf24' : '#f1f5f9';
        ctx.font = 'bold 11.5px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(era.short.toUpperCase(), x0 + colW / 2, padTop - 21);
        ctx.fillStyle = '#94a3b8';
        ctx.font = 'bold 10px monospace';
        ctx.fillText(era.years, x0 + colW / 2, padTop - 7);
      });

      // Draw Horizontal Lanes
      if (state.yMode === 'nation') {
        const laneH = usableH / 7;
        NATIONS.forEach((nat, idx) => {
          const y0 = padTop + idx * laneH;
          ctx.strokeStyle = 'rgba(148, 163, 184, 0.18)';
          ctx.beginPath();
          ctx.moveTo(10, y0);
          ctx.lineTo(padLeft + usableW + 25, y0);
          ctx.stroke();

          ctx.fillStyle = nat.color + '33';
          ctx.strokeStyle = nat.color;
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.roundRect(10, y0 + laneH / 2 - 16, 132, 32, 7);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 11.5px Inter, sans-serif';
          ctx.textAlign = 'left';
          ctx.fillText(`${nat.flag} ${nat.short || nat.id}`, 18, y0 + laneH / 2 + 4);
        });
      } else {
        [10, 25, 40, 55, 70].forEach(wt => {
          const normW = (wt - 5) / 65;
          const y = padTop + (1 - normW) * usableH;
          ctx.strokeStyle = 'rgba(148, 163, 184, 0.25)';
          ctx.setLineDash([4, 4]);
          ctx.beginPath();
          ctx.moveTo(padLeft - 40, y);
          ctx.lineTo(padLeft + usableW + 20, y);
          ctx.stroke();
          ctx.setLineDash([]);
          ctx.fillStyle = '#e2e8f0';
          ctx.font = 'bold 11px monospace';
          ctx.textAlign = 'right';
          ctx.fillText(`${wt} tons`, padLeft - 12, y + 4);
        });
      }

      const focusId = state.hoveredTankId || state.selectedTankId;
      const posMap = {};
      const visMap = {};
      TANKS.forEach(t => {
        posMap[t.id] = getGraphNodePos(t, W, H);
        visMap[t.id] = isTankVisible(t);
      });

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

      const visibleCount = TANKS.filter(t => visMap[t.id]).length;
      const activeEdgeCount = EDGES.filter(e => state.layers[e.type] && visMap[e.source] && visMap[e.target]).length;
      const statusEl = document.getElementById('graph-status-label');
      if (statusEl) {
        statusEl.textContent = `${visibleCount} tanks & ${activeEdgeCount} links shown • Focus: ${TANK_MAP[focusId]?.name || ''}`;
      }

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
        const alpha = isFocused ? 0.98 : 0.28;

        ctx.save();
        ctx.beginPath();
        const dx = p2.x - p1.x;
        const cx1 = p1.x + dx * 0.42;
        const cy1 = p1.y + (e.type === 'combat' ? -26 : 0);
        const cx2 = p1.x + dx * 0.58;
        const cy2 = p2.y + (e.type === 'combat' ? -26 : 0);

        ctx.moveTo(p1.x, p1.y);
        ctx.bezierCurveTo(cx1, cy1, cx2, cy2, p2.x, p2.y);

        if (e.type === 'lineage') {
          ctx.strokeStyle = isFocused ? '#34d399' : `rgba(52, 211, 153, ${alpha})`;
          ctx.lineWidth = isFocused ? 2.8 : 1.5;
          ctx.stroke();

          if (isFocused) {
            const tAnim = ((state.animTick * 0.012) % 1);
            const u = 1 - tAnim;
            const px = u*u*u*p1.x + 3*u*u*tAnim*cx1 + 3*u*tAnim*tAnim*cx2 + tAnim*tAnim*tAnim*p2.x;
            const py = u*u*u*p1.y + 3*u*u*tAnim*cy1 + 3*u*tAnim*tAnim*cy2 + tAnim*tAnim*tAnim*p2.y;
            ctx.fillStyle = '#a7f3d0';
            ctx.beginPath();
            ctx.arc(px, py, 3.6, 0, Math.PI * 2);
            ctx.fill();
          }
        } else if (e.type === 'similarity') {
          ctx.setLineDash([5, 4]);
          ctx.strokeStyle = isFocused ? '#38bdf8' : `rgba(56, 189, 248, ${alpha})`;
          ctx.lineWidth = isFocused ? 2.4 : 1.3;
          ctx.stroke();
          ctx.setLineDash([]);
        } else if (e.type === 'combat') {
          ctx.strokeStyle = isFocused ? '#fb7185' : `rgba(244, 63, 94, ${alpha})`;
          ctx.lineWidth = isFocused ? 2.8 : 1.4;
          ctx.stroke();

          if (isFocused) {
            const mx = 0.125*p1.x + 0.375*cx1 + 0.375*cx2 + 0.125*p2.x;
            const my = 0.125*p1.y + 0.375*cy1 + 0.375*cy2 + 0.125*p2.y;
            ctx.fillStyle = '#881337';
            ctx.strokeStyle = '#fda4af';
            ctx.lineWidth = 1.4;
            ctx.beginPath();
            ctx.arc(mx, my, 9, 0, Math.PI * 2);
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

      graphNodeScreenPositions = [];
      TANKS.forEach(t => {
        if (!visMap[t.id]) return;
        const p = posMap[t.id];
        const nat = NATION_MAP[t.nation];
        const isSelected = t.id === state.selectedTankId;
        const isHovered = t.id === state.hoveredTankId;
        const isNeighbor = neighborIds.has(t.id);
        const isRival = combatRivalIds.has(t.id);

        const bw = isSelected || isHovered ? 128 : 114;
        const bh = isSelected || isHovered ? 44 : 38;
        const bx = p.x - bw / 2;
        const by = p.y - bh / 2;

        ctx.save();
        ctx.globalAlpha = isNeighbor ? 1.0 : 0.52;

        if (isSelected || isHovered) {
          ctx.shadowColor = '#fbbf24';
          ctx.shadowBlur = 18;
        } else if (isRival) {
          ctx.shadowColor = '#f43f5e';
          ctx.shadowBlur = 14;
        }

        ctx.fillStyle = isSelected ? '#1e293b' : '#0f172a';
        ctx.strokeStyle = isSelected ? '#fbbf24' : (isRival ? '#fb7185' : nat.color);
        ctx.lineWidth = isSelected || isHovered ? 2.6 : (isRival ? 2.2 : 1.6);

        ctx.beginPath();
        ctx.roundRect(bx, by, bw, bh, 7);
        ctx.fill();
        ctx.stroke();
        ctx.shadowBlur = 0;

        ctx.fillStyle = nat.color;
        ctx.beginPath();
        ctx.roundRect(bx + 2, by + 2, bw - 4, 4.5, 2);
        ctx.fill();

        // Draw real tank photo thumbnail on left of node
        const tImg = getTankImg(t.id);
        const thumbW = 30;
        const thumbH = bh - 10;
        if (tImg) {
          ctx.save();
          ctx.beginPath();
          ctx.roundRect(bx + 4, by + 7, thumbW, thumbH, 4);
          ctx.clip();
          ctx.drawImage(tImg, bx + 4, by + 7, thumbW, thumbH);
          ctx.restore();
          ctx.strokeStyle = 'rgba(255,255,255,0.28)';
          ctx.lineWidth = 0.8;
          ctx.strokeRect(bx + 4, by + 7, thumbW, thumbH);
        }

        const textCenterX = tImg ? (bx + 36 + (bw - 38) / 2) : p.x;
        ctx.fillStyle = '#ffffff';
        ctx.font = (isSelected || isHovered ? 'bold 10.5px' : 'bold 9.5px') + ' Inter, sans-serif';
        ctx.textAlign = 'center';
        const shortName = t.name.length > 13 ? t.name.slice(0, 12) + '…' : t.name;
        ctx.fillText(shortName, textCenterX, p.y + 1);

        ctx.fillStyle = isRival ? '#fecdd3' : '#cbd5e1';
        ctx.font = 'bold 8.5px monospace';
        ctx.fillText(`${t.year}•${t.weight_t}t`, textCenterX, p.y + 13);

        if (isRival && !isSelected) {
          ctx.fillStyle = '#e11d48';
          ctx.beginPath();
          ctx.arc(bx + bw - 4, by + 4, 8, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#fff';
          ctx.font = '9.5px sans-serif';
          ctx.fillText('⚔', bx + bw - 4, by + 7.5);
        }

        ctx.restore();

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
    // 2. WORLD TANK BATTLES & 85 TANKS MAP (AREA COLORING + INTERACTIVE POPUPS)
    // =========================================================================
    let mapBattleScreenPins = [];
    let mapTankScreenPins = [];

    // The 4 largest battles (by tanks involved) keep their label at any zoom
    // total_tanks is text like "~1,460 Tanks at Prokhorovka (...)": the first number is the total
    const firstNumber = (text) => parseInt((String(text).match(/\d[\d,]*/) || ['0'])[0].replace(/,/g, ''), 10);
    const LARGEST_BATTLE_IDS = new Set(
      [...BATTLES].sort((a, b) => firstNumber(b.total_tanks) - firstNumber(a.total_tanks)).slice(0, 4).map(b => b.id)
    );

    const THEATRE_PRESETS = {
      WORLD:              { lon: 23.12, lat: 55.38, k: 2.35 },
      EUROPE_WEST:        { lon: 3.5,  lat: 49.8, k: 8.5  },
      EUROPE_EAST:        { lon: 28.5, lat: 53.2, k: 6.2  },
      NORTH_AFRICA_SINAI: { lon: 32.2, lat: 31.2, k: 7.5  },
      GULF_ME:            { lon: 46.5, lat: 30.8, k: 7.8  },
      VIETNAM_SEA:        { lon: 106.8, lat: 14.5, k: 7.2 },
      ASIA:               { lon: 105.0, lat: 34.0, k: 3.2 }
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
      state.mapBattleId = battleId;
      if (zoomTo) {
        state.mCam.targetLon = b.lon;
        state.mCam.targetLat = b.lat;
        state.mCam.targetK = Math.max(state.mCam.targetK, 5.8);
      }
      renderMapBattleStrip();
      renderBattleInspector();
      setMapPanelOpen(true);
      if (state.tacticalZoomOpen) {
        drawTacticalSchematic();
      }
    }

    // Map side panel: hidden until a battle is clicked; map spans the full width meanwhile
    function setMapPanelOpen(open) {
      document.getElementById('map-panel').classList.toggle('hidden', !open);
      document.getElementById('map-col').classList.toggle('lg:col-span-7', open);
      document.getElementById('map-col').classList.toggle('lg:col-span-12', !open);
      document.getElementById('map-hint').classList.toggle('hidden', open);
      document.body.classList.toggle('map-panel-open', open);
      if (!open) document.getElementById('map-panel').classList.remove('sheet-full');
    }

    function closeMapBattle() {
      state.mapBattleId = null;
      setMapPanelOpen(false);
      renderMapBattleStrip();
    }

    function watchSelectedBattle() {
      if (state.mapBattleId) openBattlePage(state.mapBattleId);
    }

    function toggleTacticalZoomModal(forceState) {
      state.tacticalZoomOpen = typeof forceState === 'boolean' ? forceState : !state.tacticalZoomOpen;
      updateTacticalOverlayVisibility();
    }

    function updateTacticalOverlayVisibility() {
      const overlay = document.getElementById('tactical-zoom-overlay');
      if (!overlay) return;
      if (state.tacticalZoomOpen) {
        overlay.classList.remove('hidden');
        overlay.classList.add('flex');
        drawTacticalSchematic();
      } else {
        overlay.classList.add('hidden');
        overlay.classList.remove('flex');
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

        let hitBattle = null;
        if (state.mapPinMode !== 'tanks') {
          for (let i = mapBattleScreenPins.length - 1; i >= 0; i--) {
            const pin = mapBattleScreenPins[i];
            if (Math.hypot(mx - pin.x, my - pin.y) <= pin.r + 7) {
              hitBattle = pin.id;
              break;
            }
          }
        }
        let hitTank = null;
        if (!hitBattle && state.mapPinMode !== 'battles') {
          for (let i = mapTankScreenPins.length - 1; i >= 0; i--) {
            const pin = mapTankScreenPins[i];
            if (Math.hypot(mx - pin.x, my - pin.y) <= pin.r + 6) {
              hitTank = pin.id;
              break;
            }
          }
        }
        state.hoveredBattleId = hitBattle;
        state.hoveredMapTankId = hitTank;
        canvas.style.cursor = (hitBattle || hitTank) ? 'pointer' : (state.mCam.dragging ? 'grabbing' : 'grab');
      });

      canvas.addEventListener('click', () => {
        if (state.mCam.moved) return;
        if (state.hoveredBattleId) {
          selectBattle(state.hoveredBattleId, true);
        } else if (state.hoveredMapTankId) {
          openTankPopup(state.hoveredMapTankId);
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

      state.mCam.lon += (state.mCam.targetLon - state.mCam.lon) * 0.14;
      state.mCam.lat += (state.mCam.targetLat - state.mCam.lat) * 0.14;
      state.mCam.k += (state.mCam.targetK - state.mCam.k) * 0.14;

      const readout = document.getElementById('map-zoom-readout');
      if (readout) {
        const b = BATTLE_MAP[state.mapBattleId];
        readout.textContent = b ? `${b.name} (${b.year})` : 'World map';
      }

      const ctx = canvas.getContext('2d');
      ctx.save();
      ctx.scale(dpr, dpr);
      const W = rect.width;
      const H = rect.height;

      // Deep Naval Ocean Gradient
      const grad = ctx.createLinearGradient(0, 0, 0, H);
      grad.addColorStop(0, '#040b16');
      grad.addColorStop(1, '#09192f');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, W, H);

      // Graticule Grid
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.09)';
      ctx.lineWidth = 1;
      const stepDeg = state.mCam.k > 5 ? 5 : (state.mCam.k > 2.5 ? 10 : 20);
      for (let lon = -160; lon <= 180; lon += stepDeg) {
        const p = lonLatToScreen(lon, 0, W, H);
        if (p.x >= 0 && p.x <= W) {
          ctx.beginPath(); ctx.moveTo(p.x, 0); ctx.lineTo(p.x, H); ctx.stroke();
        }
      }
      for (let lat = -60; lat <= 75; lat += stepDeg) {
        const p = lonLatToScreen(0, lat, W, H);
        if (p.y >= 0 && p.y <= H) {
          ctx.beginPath(); ctx.moveTo(0, p.y); ctx.lineTo(W, p.y); ctx.stroke();
        }
      }

      // 1. Draw Continent Polygons with distinct area colors
      WORLD_POLYGONS.forEach(poly => {
        const pts = poly.pts || poly.points || [];
        const st = CONTINENT_STYLES[poly.name] || { fill: '#15283d', stroke: '#38bdf866' };
        ctx.beginPath();
        pts.forEach((pt, idx) => {
          const s = lonLatToScreen(pt[0], pt[1], W, H);
          if (idx === 0) ctx.moveTo(s.x, s.y);
          else ctx.lineTo(s.x, s.y);
        });
        ctx.closePath();
        ctx.fillStyle = st.fill;
        ctx.fill();
        ctx.strokeStyle = st.stroke;
        ctx.lineWidth = 1.4;
        ctx.stroke();
      });

      // 2. Draw Strategic Combat Area Zones (Color-Coded Regional Overlays!)
      STRATEGIC_REGIONS.forEach(reg => {
        ctx.save();
        ctx.beginPath();
        reg.pts.forEach((pt, idx) => {
          const s = lonLatToScreen(pt[0], pt[1], W, H);
          if (idx === 0) ctx.moveTo(s.x, s.y);
          else ctx.lineTo(s.x, s.y);
        });
        ctx.closePath();
        ctx.fillStyle = reg.fill;
        ctx.fill();
        ctx.setLineDash([5, 3]);
        ctx.strokeStyle = reg.stroke;
        ctx.lineWidth = 1.8;
        ctx.stroke();
        ctx.setLineDash([]);

        // Region Area Label
        const lblPos = lonLatToScreen(reg.labelLon, reg.labelLat, W, H);
        if (lblPos.x > 20 && lblPos.x < W - 20 && lblPos.y > 20 && lblPos.y < H - 50) {
          ctx.font = 'bold 10px Inter, sans-serif';
          ctx.fillStyle = reg.stroke;
          ctx.textAlign = 'center';
          ctx.fillText(reg.name.toUpperCase(), lblPos.x, lblPos.y);
        }
        ctx.restore();
      });

      // 3. Draw 85 Tank Pins (Green/Nation Shield Pins — Click for Tank Popup!)
      mapTankScreenPins = [];
      if (state.mapPinMode !== 'battles') {
        TANKS.forEach(t => {
          if (typeof t.origin_lon !== 'number' || typeof t.origin_lat !== 'number') return;
          const s = lonLatToScreen(t.origin_lon, t.origin_lat, W, H);
          if (s.x < -40 || s.x > W + 40 || s.y < -40 || s.y > H + 40) return;

          const isHov = t.id === state.hoveredMapTankId;
          const isSel = t.id === state.selectedTankId;
          const nat = NATION_MAP[t.nation] || { color: '#10b981', flag: '🛡️' };
          const r = isHov ? 8.5 : (isSel ? 7.5 : 5.5);

          ctx.save();
          ctx.fillStyle = isHov ? '#fbbf24' : '#10b981';
          ctx.strokeStyle = isHov ? '#ffffff' : nat.color;
          ctx.lineWidth = isHov ? 2.2 : 1.5;
          ctx.beginPath();
          ctx.roundRect(s.x - r, s.y - r, r * 2, r * 2, 3);
          ctx.fill();
          ctx.stroke();

          if (state.mCam.k >= 3.8 || isHov || (state.mapPinMode === 'tanks' && state.mCam.k >= 1.9)) {
            const lbl = `${nat.flag} ${t.name.slice(0, 15)}`;
            ctx.font = (isHov ? 'bold 10.5px' : 'bold 9px') + ' Inter, sans-serif';
            const tw = ctx.measureText(lbl).width;
            const px = s.x - tw / 2 - 4;
            const py = s.y + r + 3;
            ctx.fillStyle = isHov ? 'rgba(6, 78, 59, 0.96)' : 'rgba(15, 23, 42, 0.88)';
            ctx.strokeStyle = isHov ? '#fbbf24' : '#10b981';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.roundRect(px, py, tw + 8, 15, 3);
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = isHov ? '#fde68a' : '#a7f3d0';
            ctx.textAlign = 'center';
            ctx.fillText(lbl, s.x, py + 11);
          }
          ctx.restore();
          mapTankScreenPins.push({ id: t.id, x: s.x, y: s.y, r });
        });
      }

      // 4. Draw 27 Battle Markers (Color-coded by Victory / Era + Pulsing Ring)
      mapBattleScreenPins = [];
      const pulse = (Math.sin(state.animTick * 0.08) + 1) * 0.5;

      if (state.mapPinMode !== 'tanks') {
        BATTLES.forEach(b => {
          const s = lonLatToScreen(b.lon, b.lat, W, H);
          if (s.x < -60 || s.x > W + 60 || s.y < -60 || s.y > H + 60) return;

          const isSel = b.id === state.mapBattleId;
          const isHov = b.id === state.hoveredBattleId;
          const isVietnam = b.id.includes('1968') || b.id.includes('1972') || b.id.includes('1975');
          const r = isSel ? 11 : (isHov ? 9.5 : 7.2);

          // Pulsing Radar Ring
          if (isSel || isHov || isVietnam) {
            ctx.strokeStyle = isSel ? `rgba(251, 191, 36, ${0.9 - pulse * 0.55})` : (isVietnam ? 'rgba(34, 211, 238, 0.75)' : 'rgba(244, 63, 94, 0.75)');
            ctx.lineWidth = isSel ? 2.6 : 1.8;
            ctx.beginPath();
            ctx.arc(s.x, s.y, r + 5 + pulse * 11, 0, Math.PI * 2);
            ctx.stroke();
          }

          // Pin Circle
          ctx.fillStyle = isSel ? '#fbbf24' : (isVietnam ? '#06b6d4' : '#e11d48');
          ctx.strokeStyle = '#ffffff';
          ctx.lineWidth = isSel ? 2.4 : 1.6;
          ctx.beginPath();
          ctx.arc(s.x, s.y, r, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();

          // Label Pill
          if (state.mCam.k >= 5 || isSel || isHov || LARGEST_BATTLE_IDS.has(b.id)) {
            const shortBName = b.name.replace('Battle of ', '').replace('Battles of ', '').slice(0, 22);
            const label = `${b.year} ${shortBName}`;
            ctx.font = (isSel ? 'bold 11.5px' : 'bold 10px') + ' Inter, sans-serif';
            const tw = ctx.measureText(label).width;
            const px = s.x - tw / 2 - 6;
            const py = s.y - r - 23;

            ctx.fillStyle = isSel ? 'rgba(15, 23, 42, 0.96)' : 'rgba(15, 23, 42, 0.88)';
            ctx.strokeStyle = isSel ? '#fbbf24' : (isVietnam ? '#22d3ee' : 'rgba(244, 63, 94, 0.7)');
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.roundRect(px, py, tw + 12, 19, 4);
            ctx.fill();
            ctx.stroke();

            ctx.fillStyle = isSel ? '#fde68a' : (isVietnam ? '#a5f3fc' : '#ffffff');
            ctx.textAlign = 'center';
            ctx.fillText(label, s.x, py + 13);
          }

          mapBattleScreenPins.push({ id: b.id, x: s.x, y: s.y, r });
        });
      }

      ctx.restore();
    }

    function renderMapBattleStrip() {
      const strip = document.getElementById('map-battle-strip');
      if (!strip) return;
      strip.innerHTML = BATTLES.map(b => {
        const active = b.id === state.mapBattleId;
        const isVN = b.id.includes('1968') || b.id.includes('1972') || b.id.includes('1975');
        return `
          <button onclick="selectBattle('${b.id}', true)" class="shrink-0 px-2.5 py-1.5 rounded-md border text-left transition ${
            active
              ? 'bg-amber-500 text-slate-950 border-amber-300 font-extrabold shadow'
              : (isVN ? 'bg-cyan-950/90 border-cyan-500/60 text-cyan-200 hover:border-cyan-300' : 'bg-slate-900 border-slate-700 text-slate-300 hover:text-white')
          }">
            <div class="text-xs font-mono font-bold ${active ? 'text-slate-900' : (isVN ? 'text-cyan-300' : 'text-rose-400')}">${b.year} • ${b.theatre}</div>
            <div class="text-xs font-bold whitespace-nowrap">${b.name.replace('Battle of ', '')}</div>
          </button>
        `;
      }).join('');
    }

    function renderMapTankPhotoStrip() {
      const strip = document.getElementById('map-tank-photo-strip');
      if (!strip) return;
      strip.innerHTML = TANKS.map(t => {
        const nat = NATION_MAP[t.nation] || { flag: '🛡️' };
        return `
          <div onclick="openTankPopup('${t.id}')" class="shrink-0 w-36 rounded-lg bg-slate-950 border border-slate-700 hover:border-amber-400 p-1.5 cursor-pointer transition group flex flex-col gap-1 shadow" title="Click to open interactive Tank Popup for ${t.name}">
            <div class="relative w-full h-20 rounded overflow-hidden bg-slate-900 border border-slate-800">
              <img src="${t.photo_url}" alt="${t.name}" class="w-full h-full object-cover group-hover:scale-105 transition duration-200" loading="lazy" />
              <span class="absolute top-1 left-1 px-1.5 py-0.5 rounded bg-slate-950/85 text-xs font-mono font-bold text-amber-300">${t.year}</span>
              <span class="absolute bottom-1 right-1 px-1 py-0.5 rounded bg-slate-950/85 text-xs font-bold text-slate-200">${t.weight_t}t</span>
            </div>
            <div class="text-xs font-extrabold text-white group-hover:text-amber-300 truncate">${nat.flag} ${t.name}</div>
            <div class="text-xs text-slate-400 truncate">${t.gun} • ${t.armor_mm}mm</div>
          </div>
        `;
      }).join('');
    }

    function openBattlePageAtPhase(battleId, phaseIdx) {
      openBattlePage(battleId);
      setTimeout(() => {
        const b = BATTLE_MAP[battleId];
        if (b && b.phases && b.phases[phaseIdx]) {
          const p = b.phases[phaseIdx];
          const nPh = b.phases.length || 5;
          const r0 = (p.range && typeof p.range[0] === 'number') ? p.range[0] : (phaseIdx / nPh);
          const r1 = (p.range && typeof p.range[1] === 'number') ? p.range[1] : ((phaseIdx + 1) / nPh);
          setBattleSimProgress(Math.round(((r0 + r1) / 2) * 100));
        }
      }, 60);
    }

    function renderBattleInspector() {
      const b = BATTLE_MAP[state.selectedBattleId] || BATTLES[0];
      const el = document.getElementById('battle-inspector');
      if (!el) return;

      const renderTankCards = (tankIds, colorCls) => tankIds.map(tid => {
        const t = TANK_MAP[tid];
        if (!t) return '';
        return `
          <div onclick="openTankPopup('${t.id}')" class="p-2 rounded-lg bg-[var(--card)] hover:bg-slate-800/80 border ${colorCls} flex items-center justify-between gap-2.5 cursor-pointer transition group">
            <img src="${t.photo_url}" alt="${t.name}" class="w-16 h-11 object-cover rounded border border-slate-700 shrink-0" loading="lazy" />
            <div class="min-w-0 flex-1">
              <div class="text-xs font-extrabold text-[var(--foreground)] group-hover:text-amber-300 truncate">${NATION_MAP[t.nation]?.flag || ''} ${t.name} (${t.year})</div>
              <div class="text-xs text-[var(--muted-foreground)] truncate">${t.gun} • ${t.armor_mm}mm • ${t.weight_t}t</div>
            </div>
            <button onclick="event.stopPropagation(); openTankPopup('${t.id}')" class="px-2 py-1 rounded bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-extrabold shrink-0">
              🔍 Popup
            </button>
          </div>`;
      }).join('');

      const renderDestructionList = (items, sideLabel, barColor) => {
        if (!items || !items.length) return '';
        return `
          <div class="flex flex-col gap-1.5">
            <div class="text-xs font-extrabold text-slate-200">${sideLabel}</div>
            ${items.map(d => `
              <div class="p-2 rounded-lg bg-slate-950/90 border border-slate-800 flex flex-col gap-1">
                <div class="flex items-center justify-between gap-2 text-xs">
                  <span class="font-bold text-white">${d.cause}</span>
                  <span class="font-mono font-extrabold text-amber-300 shrink-0">${d.Share || d.count} (${d.pct}%)</span>
                </div>
                <div class="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                  <div class="h-full ${barColor}" style="width:${Math.min(100, d.pct)}%"></div>
                </div>
                <div class="text-xs text-slate-300 leading-snug">${d.detail}</div>
              </div>
            `).join('')}
          </div>
        `;
      };

      const renderTimelinePhases = () => {
        if (!b.phases || !b.phases.length) return '';
        return `
          <div class="bg-[var(--background)] border border-amber-500/40 rounded-xl p-3 flex flex-col gap-2">
            <div class="flex items-center justify-between">
              <div class="text-xs font-extrabold text-amber-400 uppercase">⏱️ 5-Phase Battle Timeline &amp; Destruction</div>
              <button onclick="openBattlePage('${b.id}')" class="text-xs font-extrabold text-rose-400 hover:underline">Run Full Sim →</button>
            </div>
            <div class="flex flex-col gap-1.5">
              ${b.phases.map((p, idx) => `
                <div onclick="openBattlePageAtPhase('${b.id}', ${idx})" class="p-2 rounded-lg bg-slate-950/90 hover:bg-slate-900 border border-slate-800 hover:border-amber-400/60 cursor-pointer transition flex flex-col gap-0.5">
                  <div class="flex items-center justify-between gap-1 text-xs font-mono font-bold text-amber-300">
                    <span>${p.phase}: ${p.time}</span>
                    <span>▶ Sim</span>
                  </div>
                  <div class="text-xs font-extrabold text-white">${p.title}</div>
                  <div class="text-xs text-rose-300 font-semibold">💥 ${p.losses_note}</div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      };

      el.innerHTML = `
        <div class="border-b border-[var(--border)] pb-3">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">
              ⚔️ ${b.date} • ${b.theatre}
            </span>
            <button onclick="openBattlePage('${b.id}')" class="px-3 py-1 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-extrabold shadow">
              🎬 5-Phase Battle Sim →
            </button>
          </div>
          <h2 class="text-xl font-extrabold text-[var(--foreground)] mt-2">${b.name}</h2>
          <p class="text-xs text-[var(--muted-foreground)] mt-0.5">📍 ${b.location}</p>
        </div>

        <!-- Winner / Loser / Scale Summary -->
        <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-3 flex flex-col gap-2 text-xs">
          <div class="flex items-start justify-between gap-2">
            <span class="text-emerald-400 font-extrabold uppercase shrink-0">🏆 Winner:</span>
            <span class="font-bold text-[var(--foreground)] text-right">${b.winner}</span>
          </div>
          <div class="flex items-start justify-between gap-2 border-t border-[var(--border)] pt-1.5">
            <span class="text-rose-400 font-extrabold uppercase shrink-0">💥 Defeated:</span>
            <span class="font-semibold text-[var(--muted-foreground)] text-right">${b.loser}</span>
          </div>
          <div class="flex items-start justify-between gap-2 border-t border-[var(--border)] pt-1.5">
            <span class="text-amber-400 font-extrabold uppercase shrink-0">📊 Total Involved:</span>
            <span class="font-bold text-amber-300 text-right">${b.total_tanks}</span>
          </div>
        </div>

        <!-- Opposing Armored Forces & Tank Photo Popup Cards -->
        <div class="grid grid-cols-1 gap-3">
          <div class="bg-sky-500/10 border border-sky-500/30 rounded-xl p-3 flex flex-col gap-2">
            <div class="flex items-center justify-between text-xs">
              <span class="font-extrabold text-sky-400">🟦 ${b.side_a.flag || ''} ${b.side_a.name}</span>
              <span class="text-xs font-bold text-rose-300">Losses: ${b.losses_a}</span>
            </div>
            <div class="text-xs text-[var(--foreground)] font-semibold">Strength: ${b.side_a.count}</div>
            <div class="flex flex-col gap-1.5">
              ${renderTankCards(b.side_a.tanks, 'border-sky-500/40')}
            </div>
          </div>

          <div class="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 flex flex-col gap-2">
            <div class="flex items-center justify-between text-xs">
              <span class="font-extrabold text-rose-400">🟥 ${b.side_b.flag || ''} ${b.side_b.name}</span>
              <span class="text-xs font-bold text-rose-300">Losses: ${b.losses_b}</span>
            </div>
            <div class="text-xs text-[var(--foreground)] font-semibold">Strength: ${b.side_b.count}</div>
            <div class="flex flex-col gap-1.5">
              ${renderTankCards(b.side_b.tanks, 'border-rose-500/40')}
            </div>
          </div>
        </div>

        <!-- Real Historical Operational Battle Map Card -->
        ${b.real_map_url ? `
        <div class="bg-[var(--background)] border border-amber-500/40 rounded-xl p-3.5 flex flex-col gap-2">
          <div class="flex items-center justify-between">
            <div class="text-xs font-extrabold text-amber-400 uppercase">🗺️ Real Historical Operational Battle Map</div>
            <a href="${b.real_map_url}" target="_blank" rel="noopener" class="text-xs font-bold text-sky-400 hover:underline">Full-Res Map ↗</a>
          </div>
          <div class="grid ${b.real_map_alt_url ? 'grid-cols-2' : 'grid-cols-1'} gap-2">
            <img src="${b.real_map_url}" alt="${b.name} Historical Map" onclick="openBattlePage('${b.id}')" class="w-full h-36 object-cover rounded-lg border border-slate-700 cursor-pointer hover:border-amber-400 transition" loading="lazy" />
            ${b.real_map_alt_url ? `<img src="${b.real_map_alt_url}" alt="${b.name} Operational Map 2" onclick="openBattlePage('${b.id}')" class="w-full h-36 object-cover rounded-lg border border-slate-700 cursor-pointer hover:border-amber-400 transition" loading="lazy" />` : ''}
          </div>
          <p class="text-xs text-[var(--muted-foreground)] leading-snug">${b.real_map_caption || ''}</p>
        </div>` : ''}

        <!-- How the Tanks Got Destroyed Forensic Section -->
        <div class="bg-[var(--background)] border border-rose-500/40 rounded-xl p-3.5 flex flex-col gap-3">
          <div class="text-xs font-extrabold text-rose-400 uppercase">💥 How the Tanks Got Destroyed — Forensic Breakdown</div>
          ${renderDestructionList(b.destruction_a, `🟦 ${b.side_a.name} Losses (${b.losses_a})`, 'bg-sky-400')}
          ${renderDestructionList(b.destruction_b, `🟥 ${b.side_b.name} Losses (${b.losses_b})`, 'bg-rose-500')}
        </div>

        <!-- Real Archival Wreckage Photos: How They Blew Up -->
        ${(b.wreckage_photos && b.wreckage_photos.length) ? `
        <div class="bg-[var(--background)] border border-rose-500/40 rounded-xl p-3.5 flex flex-col gap-2.5">
          <div class="text-xs font-extrabold text-rose-400 uppercase">🔥 Real Knocked-Out Tank Wreckage &amp; Blow-Up Forensics</div>
          <div class="flex flex-col gap-2.5">
            ${b.wreckage_photos.map(w => `
              <div class="bg-slate-950/80 border border-slate-800 rounded-lg overflow-hidden">
                <img src="${w.url}" alt="${w.title}" class="w-full h-36 object-cover border-b border-slate-800" loading="lazy" />
                <div class="p-2.5">
                  <div class="text-xs font-extrabold text-rose-300">${w.title}</div>
                  <p class="text-xs text-slate-300 mt-1 leading-relaxed">${w.how_destroyed}</p>
                </div>
              </div>
            `).join('')}
          </div>
        </div>` : ''}

        <!-- Inline Playable Archival Tank Combat & Anti-Tank Footage -->
        ${(b.combat_videos && b.combat_videos.length) ? `
        <div class="bg-[var(--background)] border border-amber-500/40 rounded-xl p-3.5 flex flex-col gap-2.5">
          <div class="text-xs font-extrabold text-amber-400 uppercase">🎬 Real Archival Combat &amp; Armor Penetration Footage</div>
          ${b.combat_videos.map(v => `
            <div class="bg-slate-950/90 border border-slate-800 rounded-lg p-2 flex flex-col gap-1.5">
              <div class="text-xs font-bold text-white">${v.title}</div>
              <div class="text-xs text-slate-400">${v.source}</div>
              ${v.video_url ? `<video controls preload="metadata" class="w-full rounded border border-slate-700 bg-black max-h-48"><source src="${v.video_url}" /></video>` : ''}
              ${v.yt_url ? `<a href="${v.yt_url}" target="_blank" rel="noopener" class="text-xs font-bold text-amber-400 hover:underline">▶ Watch Additional Historical Documentary Footage on YouTube ↗</a>` : ''}
            </div>
          `).join('')}
        </div>` : ''}

        <!-- 5-Phase Chronological Battle Timeline -->
        ${renderTimelinePhases()}

        <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-3.5 flex flex-col gap-2">
          <div class="text-xs font-extrabold text-amber-400 uppercase">📖 Battle Description &amp; Outcome</div>
          <p class="text-xs text-[var(--foreground)] leading-relaxed">${b.summary}</p>
          <div class="pt-2 border-t border-[var(--border)] text-xs">
            <span class="font-bold text-emerald-400">Decisive Outcome:</span> ${b.outcome}
          </div>
        </div>
      `;
    }
"""

# Part 2B of HTML v2 generator: Dedicated Tank Page, Dedicated Battle Page & Live Formation Simulator
JS_PART_2B = r"""
    // =========================================================================
    // 3. DEDICATED TANK DOSSIER PAGE (ALL 67 TANKS + PHOTOS, BLUEPRINT & VIDEOS)
    // =========================================================================
    function buildTankBlueprintSVG(t) {
      const nat = NATION_MAP[t.nation] || { color: '#38bdf8', flag: '🛡️', name: '' };
      const isRhomboid = t.id === 'mark_i_iv' || t.id === 'whippet' || t.id === 'a7v';
      const isOscillating = t.id.includes('amx13');
      const isModern = t.era >= 6;
      const wheels = t.era === 1 ? 8 : (t.weight_t > 48 ? 7 : (t.weight_t > 25 ? 6 : 5));
      const barrelLen = Math.min(185, 65 + (t.stats.firepower || 50) * 1.15);

      let wheelsSvg = '';
      for (let i = 0; i < wheels; i++) {
        const wx = 125 + i * (230 / Math.max(1, wheels - 1));
        wheelsSvg += `
          <circle cx="${wx.toFixed(1)}" cy="176" r="15" fill="#0f172a" stroke="${nat.color}" stroke-width="2.2"/>
          <circle cx="${wx.toFixed(1)}" cy="176" r="5" fill="${nat.color}"/>
        `;
      }

      const hullPath = isRhomboid
        ? `<polygon points="85,175 120,105 350,105 395,165 365,190 105,190" fill="${nat.color}22" stroke="${nat.color}" stroke-width="2.5"/>`
        : `<polygon points="85,152 135,124 385,124 405,154 385,172 95,172" fill="${nat.color}25" stroke="${nat.color}" stroke-width="2.5"/>`;

      const turretPath = isRhomboid
        ? `<rect x="185" y="88" width="95" height="24" rx="4" fill="${nat.color}38" stroke="#f8fafc" stroke-width="2"/>`
        : (isModern
          ? `<polygon points="165,124 195,86 315,86 335,124" fill="${nat.color}40" stroke="#f8fafc" stroke-width="2.2"/>`
          : `<path d="M 180 124 Q 190 82 245 82 L 295 82 Q 315 102 310 124 Z" fill="${nat.color}40" stroke="#f8fafc" stroke-width="2.2"/>`);

      return `
        <svg viewBox="0 0 540 235" class="w-full h-full select-none">
          <defs>
            <pattern id="bp-grid" width="24" height="24" patternUnits="userSpaceOnUse">
              <path d="M 24 0 L 0 0 0 24" fill="none" stroke="rgba(56,189,248,0.12)" stroke-width="1"/>
            </pattern>
          </defs>
          <rect width="540" height="235" fill="#06101f"/>
          <rect width="540" height="235" fill="url(#bp-grid)"/>

          <!-- Engineering Dimension Guides -->
          <line x1="80" y1="210" x2="415" y2="210" stroke="#64748b" stroke-width="1" stroke-dasharray="3,3"/>
          <text x="248" y="224" fill="#94a3b8" font-size="10" font-family="monospace" text-anchor="middle">COMBAT WEIGHT: ${t.weight_t} TONS • MAX SPEED: ${t.speed_kmh} KM/H • CREW: ${t.crew}</text>

          <!-- Track Loop -->
          <rect x="92" y="154" width="296" height="40" rx="20" fill="rgba(15,23,42,0.85)" stroke="#94a3b8" stroke-width="2.2" stroke-dasharray="6,3"/>
          ${wheelsSvg}

          <!-- Armored Hull & Glacis Plate -->
          ${hullPath}
          <!-- Highlighted Frontal Armor Glacis Slope -->
          <line x1="85" y1="152" x2="135" y2="124" stroke="#fbbf24" stroke-width="4"/>
          <text x="72" y="114" fill="#fbbf24" font-size="10.5" font-weight="bold" font-family="monospace">GLACIS: ${t.armor_mm}mm RHAe</text>

          <!-- Turret & Main Armament -->
          ${turretPath}
          <rect x="295" y="97" width="${barrelLen}" height="8" rx="3" fill="#e2e8f0" stroke="${nat.color}" stroke-width="1.6"/>
          <rect x="${295 + barrelLen * 0.55}" y="94.5" width="22" height="13" rx="3" fill="#94a3b8"/>

          <!-- Callout Labels -->
          <text x="16" y="24" fill="#f8fafc" font-size="12" font-weight="bold" font-family="monospace">${nat.flag} ${t.name.toUpperCase()} (${t.year}) — TECHNICAL PROFILE</text>
          <text x="16" y="42" fill="#38bdf8" font-size="10.5" font-family="monospace">MAIN GUN: ${t.gun}</text>
          <text x="16" y="58" fill="#34d399" font-size="10" font-family="monospace">ENGINE: ${t.power_hp} HP (${(t.power_hp / Math.max(1, t.weight_t)).toFixed(1)} HP/t) • BUILT: ~${t.produced.toLocaleString()}</text>
        </svg>
      `;
    }

    function renderAll85TanksPhotoGrid() {
      const grid = document.getElementById('all-85-tanks-photo-grid');
      if (!grid) return;
      grid.innerHTML = TANKS.map(t => {
        const nat = NATION_MAP[t.nation] || { flag: '🛡️', color: '#38bdf8' };
        const isSel = t.id === state.selectedTankId;
        const imgUrl = t.photo_url || t.image_url;
        return `
          <div onclick="openTankPopup('${t.id}')" class="rounded-xl overflow-hidden border ${isSel ? 'border-amber-400 ring-2 ring-amber-400/40 bg-slate-900' : 'border-slate-800 bg-slate-950 hover:border-amber-400/70'} transition cursor-pointer group flex flex-col justify-between shadow">
            <div>
              <div class="relative h-24 w-full bg-slate-900 overflow-hidden">
                <img src="${imgUrl}" alt="${t.name}" class="w-full h-full object-cover group-hover:scale-105 transition duration-200" loading="lazy" />
                <span class="absolute top-1 left-1 px-1.5 py-0.5 rounded bg-slate-950/90 text-xs font-mono font-extrabold text-amber-300">${nat.flag} ${t.year}</span>
                <span class="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-slate-950/90 text-xs font-mono font-bold text-slate-200">${t.weight_t}t</span>
              </div>
              <div class="p-2">
                <div class="text-xs font-extrabold text-white group-hover:text-amber-300 truncate">${t.name}</div>
                <div class="text-xs text-slate-400 truncate mt-0.5">${t.gun} • ${t.armor_mm}mm</div>
              </div>
            </div>
            <div class="px-2 pb-2 flex items-center gap-1">
              <button onclick="event.stopPropagation(); openTankPopup('${t.id}')" class="flex-1 py-1 rounded bg-amber-500/20 hover:bg-amber-500 hover:text-slate-950 text-amber-300 border border-amber-500/40 text-xs font-extrabold transition">🔍 Popup</button>
              <button onclick="event.stopPropagation(); state.selectedTankId='${t.id}'; renderTankPage(); renderAll85TanksPhotoGrid();" class="flex-1 py-1 rounded bg-slate-800 hover:bg-sky-500 hover:text-slate-950 text-sky-300 text-xs font-bold transition">📄 Below</button>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderTankPage() {
      const t = TANK_MAP[state.selectedTankId] || TANKS[0];
      const nat = NATION_MAP[t.nation];
      const era = ERA_MAP[t.era];
      const imgUrl = t.photo_url || t.image_url;
      const container = document.getElementById('tank-page-content');
      if (!container) return;

      const sel = document.getElementById('tank-page-select');
      if (sel && sel.value !== t.id) sel.value = t.id;

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

      const statBar = (label, val, color) => `
        <div class="flex items-center gap-2 text-xs">
          <span class="w-28 text-[var(--muted-foreground)] font-semibold">${label}</span>
          <div class="flex-1 h-2.5 bg-[var(--background)] rounded-full overflow-hidden border border-[var(--border)]">
            <div class="h-full ${color} rounded-full" style="width:${val}%"></div>
          </div>
          <span class="w-9 text-right font-mono font-extrabold">${val}/100</span>
        </div>`;

      container.innerHTML = `
        <!-- Top Hero Card: Title, Historical Photograph & Scaled Technical Blueprint -->
        <div class="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 shadow-lg flex flex-col gap-5">
          <div class="flex flex-wrap items-start justify-between gap-4 border-b border-[var(--border)] pb-4">
            <div>
              <div class="flex flex-wrap items-center gap-2">
                <span class="px-3 py-1 rounded-full text-xs font-extrabold border" style="border-color:${nat.color}; background:${nat.color}25; color:${nat.color}">
                  ${nat.flag} ${nat.name} • Service Entry: ${t.year}
                </span>
                <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">${era.name}</span>
                <span class="px-2.5 py-1 rounded-full text-xs font-bold bg-slate-800 text-slate-200 border border-slate-600">${t.role}</span>
              </div>
              <h2 class="text-2xl sm:text-3xl font-extrabold text-[var(--foreground)] mt-2">${t.name}</h2>
              <p class="text-sm text-[var(--muted-foreground)] mt-1 max-w-4xl leading-relaxed">${t.summary}</p>
            </div>
            <div class="flex flex-wrap items-center gap-2">
              <button onclick="selectTank('${t.id}', true)" class="px-3 py-2 rounded-lg bg-[var(--background)] border border-[var(--border)] hover:border-amber-400 text-xs font-bold">
                🕸️ Highlight on Lineage Graph
              </button>
              <a href="${t.wiki_url || '#'}" target="_blank" rel="noopener noreferrer" class="px-3 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold shadow">
                📖 Wikipedia Reference ↗
              </a>
            </div>
          </div>

          <!-- Dual Visual Showcase: Real Photograph (Left) + Engineering Blueprint SVG (Right) -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 items-stretch">
            <div class="lg:col-span-6 bg-slate-950 border border-slate-700 rounded-xl overflow-hidden flex flex-col justify-between">
              <div class="relative h-[300px] sm:h-[340px] w-full flex items-center justify-center bg-slate-950 overflow-hidden">
                <img
                  src="${imgUrl}"
                  alt="${t.name} historical photograph"
                  class="w-full h-full object-contain bg-slate-950"
                  onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
                />
                <div class="hidden absolute inset-0 flex-col items-center justify-center p-6 text-center bg-slate-900">
                  <div class="text-2xl mb-2">🛡️ ${t.name}</div>
                  <div class="text-xs text-slate-300">Historical Armor Archive Photograph (${t.year})</div>
                </div>
              </div>
              <div class="px-4 py-2.5 bg-slate-900 border-t border-slate-800 flex items-center justify-between text-xs text-slate-300">
                <span>📸 Historical Photograph: <strong>${t.name}</strong> (${nat.name}, ${t.year})</span>
                <a href="${imgUrl}" target="_blank" rel="noopener noreferrer" class="text-amber-400 hover:underline font-bold">Open Full Image ↗</a>
              </div>
            </div>

            <div class="lg:col-span-6 bg-slate-950 border border-slate-700 rounded-xl overflow-hidden flex flex-col justify-between">
              <div class="h-[300px] sm:h-[340px] w-full flex items-center justify-center p-2">
                ${buildTankBlueprintSVG(t)}
              </div>
              <div class="px-4 py-2.5 bg-slate-900 border-t border-slate-800 flex items-center justify-between text-xs text-slate-300">
                <span>📐 Scaled Engineering Profile &amp; Armor Protection Diagram</span>
                <span class="font-mono text-emerald-400">${t.weight_t}t • ${t.armor_mm}mm RHAe • ${t.speed_kmh} km/h</span>
              </div>
            </div>
          </div>

          <!-- Technical Specifications & 5-Axis Telemetry Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
            <div class="lg:col-span-7 grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
              <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-3">
                <div class="text-xs text-[var(--muted-foreground)] uppercase font-bold">Primary Armament</div>
                <div class="text-sm font-extrabold text-[var(--foreground)] mt-1">${t.gun}</div>
              </div>
              <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-3">
                <div class="text-xs text-[var(--muted-foreground)] uppercase font-bold">Frontal Armor (RHAe)</div>
                <div class="text-sm font-extrabold text-amber-400 mt-1">${t.armor_mm} mm等效</div>
              </div>
              <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-3">
                <div class="text-xs text-[var(--muted-foreground)] uppercase font-bold">Combat Weight</div>
                <div class="text-sm font-extrabold text-sky-400 mt-1">${t.weight_t} metric tons</div>
              </div>
              <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-3">
                <div class="text-xs text-[var(--muted-foreground)] uppercase font-bold">Road Speed &amp; Power</div>
                <div class="text-sm font-extrabold text-emerald-400 mt-1">${t.speed_kmh} km/h • ${t.power_hp} hp</div>
              </div>
              <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-3">
                <div class="text-xs text-[var(--muted-foreground)] uppercase font-bold">Power-to-Weight Ratio</div>
                <div class="text-sm font-extrabold text-purple-400 mt-1">${(t.power_hp / Math.max(1, t.weight_t)).toFixed(1)} hp / ton</div>
              </div>
              <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-3">
                <div class="text-xs text-[var(--muted-foreground)] uppercase font-bold">Crew &amp; Total Built</div>
                <div class="text-sm font-extrabold text-[var(--foreground)] mt-1">${t.crew} crew • ~${t.produced.toLocaleString()} units</div>
              </div>
            </div>

            <div class="lg:col-span-5 bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 flex flex-col justify-center gap-2">
              <div class="text-xs font-extrabold text-amber-400 uppercase tracking-wider mb-1">📊 Combat Capability &amp; Historical Impact Telemetry</div>
              ${statBar('Firepower', t.stats.firepower, 'bg-rose-500')}
              ${statBar('Armor Protection', t.stats.armor, 'bg-amber-500')}
              ${statBar('Tactical Mobility', t.stats.mobility, 'bg-emerald-500')}
              ${statBar('Optics & Fire Ctrl', t.stats.optics, 'bg-sky-500')}
              ${statBar('Historical Impact', t.stats.impact, 'bg-purple-500')}
            </div>
          </div>

          <!-- Curated Video Documentaries & Museum Walkarounds -->
          <div class="bg-gradient-to-r from-red-950/50 via-slate-900 to-slate-900 border border-red-500/40 rounded-xl p-4 flex flex-col gap-3">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded bg-red-600 text-white text-xs font-extrabold">▶ VIDEO ARCHIVE</span>
                <h3 class="text-sm font-extrabold text-white">Relevant Videos, Museum Walkarounds &amp; Combat History for ${t.name}</h3>
              </div>
              <span class="text-xs text-slate-300">Opens directly on YouTube in a new tab</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              ${(t.videos || []).map((v, idx) => `
                <a href="${v.url}" target="_blank" rel="noopener noreferrer" class="group p-3.5 rounded-xl bg-slate-950/90 border border-slate-700 hover:border-red-500 transition flex items-center justify-between gap-3 shadow">
                  <div class="flex items-center gap-3">
                    <span class="w-10 h-10 rounded-lg bg-red-600/20 border border-red-500/50 text-red-400 group-hover:bg-red-600 group-hover:text-white flex items-center justify-center font-extrabold text-base transition shrink-0">▶</span>
                    <div>
                      <div class="text-xs font-extrabold text-white group-hover:text-amber-300 transition">${v.title}</div>
                      <div class="text-xs text-slate-400 mt-0.5">${idx === 0 ? 'The Tank Museum (Bovington)' : (idx === 1 ? 'Technical Walkaround & Crew Hatch' : 'Combat Footage & Documentary')}</div>
                    </div>
                  </div>
                  <span class="text-xs text-red-400 font-bold shrink-0">Watch ↗</span>
                </a>
              `).join('')}
            </div>
          </div>
        </div>

        <!-- Bottom 3-Column Associated Links: Battles Fought, Combat Rivals, and Lineage/Similarity -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <!-- Column 1: Battles Fought -->
          <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 flex flex-col gap-3">
            <div class="text-sm font-extrabold text-amber-400 uppercase">🌍 Major Tank Battles Fought (${battlesFought.length})</div>
            ${battlesFought.length ? battlesFought.map(b => `
              <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col gap-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-extrabold text-amber-300">${b.date} • ${b.theatre}</span>
                  <button onclick="jumpToBattleOnMap('${b.id}')" class="text-xs text-sky-400 hover:underline font-bold">📍 View on Map</button>
                </div>
                <div class="text-sm font-extrabold text-[var(--foreground)]">${b.name}</div>
                <div class="text-xs text-emerald-400 font-semibold">🏆 Winner: ${b.winner}</div>
                <div class="text-xs text-[var(--muted-foreground)]">${b.total_tanks}</div>
                <button onclick="openBattlePage('${b.id}')" class="mt-1 px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-extrabold text-center">
                  🎬 Open Battle Page &amp; Formation Simulation →
                </button>
              </div>
            `).join('') : '<div class="text-xs text-[var(--muted-foreground)]">Served in deterrence, training, or secondary theatres without a dedicated battle pin.</div>'}
          </div>

          <!-- Column 2: Combat Rivals -->
          <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 flex flex-col gap-3">
            <div class="text-sm font-extrabold text-rose-400 uppercase">⚔️ Direct Combat Rivals (${combats.length})</div>
            ${combats.length ? combats.map(c => `
              <div class="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex flex-col gap-2">
                <div class="flex items-center justify-between gap-2">
                  <button onclick="openTankPage('${c.tank.id}')" class="text-sm font-extrabold text-rose-300 hover:underline text-left">
                    ⚔️ ${NATION_MAP[c.tank.nation].flag} ${c.tank.name} (${c.tank.year})
                  </button>
                  <button onclick="openTankPage('${c.tank.id}')" class="px-2 py-1 rounded bg-sky-500/20 border border-sky-500/40 text-sky-300 text-xs font-bold shrink-0">
                    Open Tank Page →
                  </button>
                </div>
                <div class="text-xs text-[var(--muted-foreground)]">${c.label}</div>
                <div class="text-xs font-mono text-amber-300">${c.tank.gun} • ${c.tank.armor_mm}mm • ${c.tank.weight_t}t</div>
              </div>
            `).join('') : '<div class="text-xs text-[var(--muted-foreground)]">No direct tank-on-tank duel recorded in dataset.</div>'}
          </div>

          <!-- Column 3: Lineage, Similarity & Engineering Innovations -->
          <div class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 flex flex-col gap-3">
            <div class="text-sm font-extrabold text-emerald-400 uppercase">🟢 Lineage, Similarity &amp; Innovations</div>
            <div>
              <div class="text-xs font-bold text-[var(--muted-foreground)] mb-1">⬅️ Evolved From (Ancestors):</div>
              ${parents.length ? parents.map(p => `
                <button onclick="openTankPage('${p.tank.id}')" class="w-full text-left p-2.5 rounded-lg bg-[var(--background)] border border-[var(--border)] hover:border-emerald-400 mb-1.5 flex items-center justify-between">
                  <div>
                    <div class="text-xs font-extrabold text-emerald-300">${NATION_MAP[p.tank.nation].flag} ${p.tank.name} (${p.tank.year})</div>
                    <div class="text-xs text-[var(--muted-foreground)]">${p.label}</div>
                  </div>
                  <span class="text-xs font-bold text-emerald-400">Page →</span>
                </button>
              `).join('') : '<div class="text-xs text-[var(--muted-foreground)] italic mb-2">Foundational 1st-Generation Design</div>'}
            </div>
            <div>
              <div class="text-xs font-bold text-[var(--muted-foreground)] mb-1">➡️ Evolved Into (Successors):</div>
              ${children.length ? children.map(c => `
                <button onclick="openTankPage('${c.tank.id}')" class="w-full text-left p-2.5 rounded-lg bg-[var(--background)] border border-[var(--border)] hover:border-emerald-400 mb-1.5 flex items-center justify-between">
                  <div>
                    <div class="text-xs font-extrabold text-emerald-300">${NATION_MAP[c.tank.nation].flag} ${c.tank.name} (${c.tank.year})</div>
                    <div class="text-xs text-[var(--muted-foreground)]">${c.label}</div>
                  </div>
                  <span class="text-xs font-bold text-emerald-400">Page →</span>
                </button>
              `).join('') : '<div class="text-xs text-[var(--muted-foreground)] italic mb-2">Current-Generation Pinnacle</div>'}
            </div>
            <div>
              <div class="text-xs font-bold text-sky-400 mb-1">🔵 Design Similarity &amp; Shared Tech:</div>
              ${similar.length ? similar.map(s => `
                <button onclick="openTankPage('${s.tank.id}')" class="w-full text-left p-2.5 rounded-lg bg-[var(--background)] border border-[var(--border)] hover:border-sky-400 mb-1.5 flex items-center justify-between">
                  <div>
                    <div class="text-xs font-extrabold text-sky-300">${NATION_MAP[s.tank.nation].flag} ${s.tank.name} (${s.tank.year})</div>
                    <div class="text-xs text-[var(--muted-foreground)]">${s.label}</div>
                  </div>
                  <span class="text-xs font-bold text-sky-400">Page →</span>
                </button>
              `).join('') : '<div class="text-xs text-[var(--muted-foreground)] italic">Indigenous design.</div>'}
            </div>
            <div class="pt-2 border-t border-[var(--border)]">
              <div class="text-xs font-extrabold text-amber-400 uppercase mb-1">🔧 Defining Innovations</div>
              <ul class="list-disc list-inside text-xs text-[var(--foreground)] space-y-1">
                ${(t.innovations || []).map(inv => `<li>${inv}</li>`).join('')}
              </ul>
            </div>
          </div>
        </div>
      `;
    }

    // =========================================================================
    // 4. DEDICATED BATTLE DOSSIER PAGE & LIVE FORMATION SIMULATOR (27 BATTLES)
    // =========================================================================
    const PLAY_ICON = '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M7 4l13 8-13 8z"/></svg>';
    const PAUSE_ICON = '<svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>';

    function syncPlayButton() {
      const btn = document.getElementById('sim-play-btn');
      if (!btn) return;
      btn.innerHTML = state.sim.playing ? PAUSE_ICON : PLAY_ICON;
      btn.setAttribute('aria-label', state.sim.playing ? 'Pause' : 'Play');
    }

    // Playback states: 'ready' (just opened, Play overlay), 'playing', 'paused', 'ended' (result overlay).
    // Every start/stop goes through setSimStatus so the button, overlay and loop agree.
    function setSimStatus(status) {
      if (status !== 'paused') state.sim.phaseCard = null;
      state.sim.status = status;
      state.sim.playing = status === 'playing';
      syncPlayButton();
      syncSimOverlay();
    }

    function syncSimOverlay() {
      const overlay = document.getElementById('sim-overlay');
      if (!overlay) return;
      const status = state.sim.status;
      const atPhase = status === 'paused' && state.sim.phaseCard != null;
      overlay.classList.toggle('hidden', status !== 'ready' && status !== 'ended' && !atPhase);
      document.getElementById('sim-overlay-ready').classList.toggle('hidden', status !== 'ready');
      document.getElementById('sim-overlay-ended').classList.toggle('hidden', status !== 'ended');
      const phaseCard = document.getElementById('sim-overlay-phase');
      phaseCard.classList.toggle('hidden', !atPhase);
      if (atPhase) renderPhaseCard(state.sim.phaseCard);
    }

    // "Stop at each phase": while playing, crossing into a new phase pauses there with a card
    function renderPhaseCard(idx) {
      const b = BATTLE_MAP[state.selectedBattleId] || BATTLES[0];
      const phases = b.phases || [];
      const ph = phases[idx];
      const card = document.getElementById('sim-overlay-phase');
      if (!ph || !card) return;
      card.innerHTML = `
        <div class="text-xs font-semibold uppercase tracking-wide text-amber-400">Phase ${idx + 1} of ${phases.length}${ph.night ? ' · Night' : ''}</div>
        <div class="text-sm text-[var(--muted-foreground)]">${ph.time || ''}</div>
        <h3 class="text-lg font-semibold text-[var(--foreground)] leading-snug">${ph.title || ''}</h3>
        <p class="text-sm text-[var(--muted-foreground)] leading-relaxed line-clamp-4">${ph.desc || ''}</p>
        <div class="text-sm text-rose-400">${ph.losses_note || ''}</div>
        <div class="flex flex-wrap items-center gap-2 pt-1">
          <button onclick="setSimStatus('playing')" class="h-11 px-4 rounded-md bg-amber-500 hover:bg-amber-400 text-slate-950 text-sm font-semibold">Continue</button>
          <button onclick="setStopAtPhases(false); setSimStatus('playing')" class="h-11 px-3 rounded-md text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Play without stopping</button>
        </div>`;
    }

    function phaseStartCrossed(b, fromP, toP) {
      const phases = b.phases || [];
      const n = Math.max(1, phases.length);
      for (let i = 1; i < phases.length; i++) {
        const r0 = (phases[i].range && typeof phases[i].range[0] === 'number') ? phases[i].range[0] : i / n;
        if (fromP < r0 && toP >= r0) return { idx: i, r0 };
      }
      return null;
    }

    function setStopAtPhases(on) {
      state.sim.stopAtPhases = on;
      const btn = document.getElementById('sim-stops-btn');
      if (btn) btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    }

    function toggleSimPlay() {
      if (state.sim.selectedAgentId != null) clearSimUnit(false);
      if (state.sim.status === 'ended') return restartBattleSim();
      setSimStatus(state.sim.playing ? 'paused' : 'playing');
    }

    function restartBattleSim() {
      state.sim.progress = 0.0;
      state.sim.logs = [];
      state.sim.lastPhaseLogged = -1;
      const scrub = document.getElementById('sim-scrubber');
      if (scrub) scrub.value = '0';
      setSimStatus('playing');
    }

    // Auto-pause: battlefield scrolled out of view, or the browser tab hidden
    let simStageObserver = null;
    function observeSimStage() {
      if (simStageObserver) simStageObserver.disconnect();
      const stage = document.querySelector('.sim-stage');
      if (!stage || !('IntersectionObserver' in window)) return;
      simStageObserver = new IntersectionObserver(entries => {
        entries.forEach(e => {
          if (!e.isIntersecting && state.sim.status === 'playing') setSimStatus('paused');
        });
      }, { threshold: 0.25 });
      simStageObserver.observe(stage);
    }
    document.addEventListener('visibilitychange', () => {
      if (document.hidden && state.sim.status === 'playing') setSimStatus('paused');
    });

    function setSimSpeed(spd) {
      state.sim.speed = spd;
      document.querySelectorAll('[data-sim-speed]').forEach(el => {
        el.setAttribute('aria-pressed', parseFloat(el.dataset.simSpeed) === spd ? 'true' : 'false');
      });
    }

    function scrubBattleSim(val) {
      state.sim.progress = parseFloat(val);
      state.sim.phaseCard = null;
      if (state.sim.status === 'ended') setSimStatus('paused'); else syncSimOverlay();
    }

    function setBattleSimProgress(pct) {
      state.sim.progress = Math.min(0.999, Math.max(0, pct / 100));
      state.sim.phaseCard = null;
      if (state.sim.status === 'ended') setSimStatus('paused'); else syncSimOverlay();
      const scrub = document.getElementById('sim-scrubber');
      if (scrub) scrub.value = state.sim.progress.toFixed(3);
    }

    function toggleSimHulls() {
      state.sim.showHulls = !state.sim.showHulls;
      const btn = document.getElementById('sim-hull-btn');
      if (btn) btn.setAttribute('aria-pressed', state.sim.showHulls ? 'true' : 'false');
    }

    let battleSimLeaflet = null;
    let battleSimTileLayer = null;

    function setSimMapBgMode(mode) {
      state.sim.mapBgMode = mode;
      ['historical', 'topo', 'satellite', 'tactical'].forEach(m => {
        const btn = document.getElementById('sim-bg-' + m);
        if (!btn) return;
        btn.setAttribute('aria-pressed', m === mode ? 'true' : 'false');
      });
      syncBattleSimMapLayers();
    }

    function syncBattleSimMapLayers() {
      const b = BATTLE_MAP[state.selectedBattleId] || BATTLES[0];
      const histImg = document.getElementById('battle-sim-hist-map');
      const leafDiv = document.getElementById('battle-sim-leaflet-map');
      const mode = state.sim.mapBgMode || 'historical';

      if (histImg) {
        if (mode === 'historical' && b.real_map_url) {
          histImg.src = b.real_map_url;
          histImg.classList.remove('hidden');
        } else {
          histImg.classList.add('hidden');
        }
      }

      if (leafDiv) {
        if (mode === 'topo' || mode === 'satellite') {
          leafDiv.classList.remove('hidden');
          if (typeof L !== 'undefined') {
            if (!battleSimLeaflet || battleSimLeaflet._container !== leafDiv) {
              battleSimLeaflet = L.map(leafDiv, {
                zoomControl: false,
                attributionControl: false,
                dragging: false,
                scrollWheelZoom: false,
                doubleClickZoom: false
              }).setView([b.lat, b.lon], b.id === 'raseiniai_1941' ? 11 : 11);
            } else {
              battleSimLeaflet.setView([b.lat, b.lon], b.id === 'raseiniai_1941' ? 11 : 11);
              battleSimLeaflet.invalidateSize();
            }
            if (battleSimTileLayer) {
              battleSimLeaflet.removeLayer(battleSimTileLayer);
            }
            const tileUrl = mode === 'satellite'
              ? 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
              : 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png';
            battleSimTileLayer = L.tileLayer(tileUrl, { maxZoom: 17 }).addTo(battleSimLeaflet);
          }
        } else {
          leafDiv.classList.add('hidden');
        }
      }
    }

    function selectKillCamScenario(idx) {
      state.sim.killcamIdx = idx;
      state.sim.killcamTick = 0;
      const b = BATTLE_MAP[state.selectedBattleId] || BATTLES[0];
      const scenarios = b.killcam_scenarios || [];
      scenarios.forEach((sc, i) => {
        const btn = document.getElementById('killcam-btn-' + i);
        if (btn) {
          btn.className = i === idx
            ? 'p-2.5 rounded-xl border-2 border-rose-400 bg-rose-500/20 text-left transition shadow-lg flex flex-col gap-1'
            : 'p-2.5 rounded-xl border border-slate-700 bg-slate-950 hover:border-rose-400/60 text-left transition opacity-80 hover:opacity-100 flex flex-col gap-1';
        }
      });
      const sc = scenarios[idx];
      const descEl = document.getElementById('killcam-scenario-desc');
      if (descEl && sc) {
        descEl.innerHTML = `<strong class="text-rose-300">💥 ${sc.title}:</strong> <span class="text-slate-200">${sc.desc}</span>`;
      }
    }

    function renderBattlePage() {
      const b = BATTLE_MAP[state.selectedBattleId] || BATTLES[0];
      const container = document.getElementById('battle-page-content');
      if (!container) return;

      const sel = document.getElementById('battle-page-select');
      if (sel && sel.value !== b.id) sel.value = b.id;

      state.sim.killcamIdx = 0;
      state.sim.killcamTick = 0;

      const phases = b.phases || [];
      const killScenarios = b.killcam_scenarios || [];
      const wreckPhotos = b.wreckage_photos || [];
      const combatVideos = b.combat_videos || [];

      const renderParticipTankCard = (tid, sideColor) => {
        const t = TANK_MAP[tid];
        if (!t) return '';
        const nat = NATION_MAP[t.nation] || { flag: '🛡️' };
        const imgUrl = t.photo_url || t.image_url;
        return `
          <div onclick="openTankPopup('${t.id}')" class="p-3 rounded-xl bg-[var(--background)] hover:bg-slate-900 border border-${sideColor}-500/40 flex items-center justify-between gap-3 cursor-pointer transition group">
            <div class="flex items-center gap-3 min-w-0">
              <img src="${imgUrl}" alt="${t.name}" class="w-20 h-14 rounded-lg object-cover bg-slate-950 border border-slate-700 shrink-0" loading="lazy" />
              <div class="min-w-0">
                <div class="text-sm font-extrabold text-[var(--foreground)] group-hover:text-amber-400 truncate">
                  ${nat.flag} ${t.name} (${t.year}) — ${t.role}
                </div>
                <div class="text-xs text-[var(--muted-foreground)] truncate">${t.gun} • ${t.armor_mm}mm RHAe • ${t.weight_t}t • ${t.speed_kmh} km/h</div>
              </div>
            </div>
            <div class="flex items-center gap-1.5 shrink-0">
              <button onclick="event.stopPropagation(); openTankPopup('${t.id}')" class="px-2.5 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-extrabold">
                🔍 Popup
              </button>
              <button onclick="event.stopPropagation(); openTankPage('${t.id}')" class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-sky-300 border border-sky-500/40 text-xs font-bold">
                📄 Page
              </button>
            </div>
          </div>
        `;
      };

      const renderForensicCard = (items, title, badgeCls, barCls) => {
        if (!items || !items.length) return '';
        return `
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 flex flex-col gap-3">
            <div class="flex items-center justify-between border-b border-[var(--border)] pb-2">
              <span class="text-sm font-extrabold ${badgeCls}">${title}</span>
              <span class="text-xs font-mono text-[var(--muted-foreground)]">Forensic Cause Breakdown</span>
            </div>
            <div class="flex flex-col gap-2.5">
              ${items.map(d => `
                <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 flex flex-col gap-1.5">
                  <div class="flex flex-wrap items-center justify-between gap-2 text-xs">
                    <span class="font-extrabold text-white min-w-0">${d.cause}</span>
                    <span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40 font-mono font-extrabold max-w-full">${d.Share || d.count} (${d.pct}%)</span>
                  </div>
                  <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div class="h-full ${barCls} rounded-full" style="width:${Math.min(100, d.pct)}%"></div>
                  </div>
                  <div class="text-xs text-slate-300 leading-relaxed">${d.detail}</div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      };

      // The simulator's units (deterministic), shared with the draw loop
      simBattleCache.battleId = b.id;
      simBattleCache.agents = buildBattleAgents(b);
      const countersA = simBattleCache.agents.filter(a => a.side === 'A').length;
      const countersB = simBattleCache.agents.filter(a => a.side === 'B').length;
      const lossStrip = renderLossStrip(simBattleCache.agents, 40);

      container.innerHTML = `
        <!-- Battle theater: force bar, battlefield + docked controls, story panel -->
        <div id="battle-theater" class="flex flex-col gap-2">
          <div class="grid grid-cols-2 gap-6 items-end text-sm">
            <div class="flex flex-col gap-1 min-w-0">
              <div class="flex items-center justify-between gap-2">
                <span class="font-semibold text-sky-400 truncate">${b.side_a.name}</span>
                <span class="tabular-nums text-[var(--muted-foreground)] shrink-0"><strong id="sim-count-a" class="text-[var(--foreground)]">${b.side_a_num || 749}</strong> active, <strong id="sim-lost-a" class="text-rose-400">0</strong> lost</span>
              </div>
              <div class="flex items-center gap-2">
                <div class="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden"><div id="sim-bar-a" class="h-full bg-sky-400 transition-all duration-150" style="width:100%"></div></div>
                <span id="sim-pct-a" class="tabular-nums text-xs text-sky-300 w-10 text-right">100%</span>
              </div>
            </div>
            <div class="flex flex-col gap-1 min-w-0">
              <div class="flex items-center justify-between gap-2">
                <span class="tabular-nums text-[var(--muted-foreground)] shrink-0"><strong id="sim-count-b" class="text-[var(--foreground)]">${b.side_b_num || 245}</strong> active, <strong id="sim-lost-b" class="text-rose-400">0</strong> lost</span>
                <span class="font-semibold text-rose-400 truncate text-right">${b.side_b.name}</span>
              </div>
              <div class="flex items-center gap-2 flex-row-reverse">
                <div class="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden flex justify-end"><div id="sim-bar-b" class="h-full bg-rose-500 transition-all duration-150" style="width:100%"></div></div>
                <span id="sim-pct-b" class="tabular-nums text-xs text-rose-300 w-10">100%</span>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-4 gap-3">
            <div class="lg:col-span-3 flex flex-col rounded-[10px] overflow-hidden border border-[var(--border)]">
              <div class="sim-stage relative bg-[var(--canvas-bg)] overflow-hidden">
                <div id="battle-sim-leaflet-map" class="absolute inset-0 z-0 hidden opacity-70"></div>
                <img id="battle-sim-hist-map" src="${b.real_map_url || ''}" alt="Historical map of ${b.name}" class="absolute inset-0 w-full h-full object-cover opacity-45 pointer-events-none z-0" />
                <div class="absolute inset-0 bg-slate-950/35 pointer-events-none z-[1]"></div>
                <canvas id="battle-sim-canvas" role="img" aria-label="${b.name}: battlefield" class="relative z-10 w-full h-full block cursor-pointer"></canvas>
                <div class="sim-scale-note absolute bottom-2 right-2 z-[15] max-w-[calc(100%-1rem)] px-2.5 py-1 rounded-md bg-[var(--card)]/90 border border-[var(--border)] text-xs text-[var(--muted-foreground)] pointer-events-auto"
                  title="Phases, tank counts and losses come from historical sources. Unit positions and movements on the map are illustrative.">
                  <span class="text-sky-400 tabular-nums">${countersA === b.side_a_num ? `${countersA} tanks, one counter each` : `${countersA} counters for ${b.side_a_num} tanks`}</span> ·
                  <span class="text-rose-400 tabular-nums">${countersB === b.side_b_num ? `${countersB} tanks, one counter each` : `${countersB} for ${b.side_b_num}`}</span> ·
                  positions are illustrative
                </div>

                <!-- Ready (Play) and Ended (result) overlay; shown by syncSimOverlay() -->
                <div id="sim-overlay" class="hidden absolute inset-0 z-20 flex items-center justify-center bg-slate-950/55 p-4">
                  <div id="sim-overlay-ready" class="hidden flex flex-col items-center gap-3 text-center">
                    <button onclick="setSimStatus('playing')" aria-label="Play the battle" class="w-20 h-20 rounded-full bg-amber-500 hover:bg-amber-400 text-slate-950 flex items-center justify-center shadow-lg">
                      <svg aria-hidden="true" width="34" height="34" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5l12 7-12 7z"/></svg>
                    </button>
                    <div class="text-lg font-semibold text-white">Play the battle</div>
                    <div class="text-sm text-slate-200">${phases.length} phases, ${b.date}</div>
                  </div>
                  <div id="sim-overlay-phase" role="status" class="hidden w-full max-w-md rounded-[10px] bg-[var(--card)] border border-[var(--border)] p-5 flex flex-col gap-2"></div>
                  <div id="sim-overlay-ended" role="status" class="hidden w-full max-w-md rounded-[10px] bg-[var(--card)] border border-[var(--border)] p-5 flex flex-col gap-3">
                    <div class="text-xs font-semibold uppercase tracking-wide text-amber-400">Battle over</div>
                    <div>
                      <div class="text-sm text-[var(--muted-foreground)]">Winner</div>
                      <div class="text-lg font-semibold text-[var(--foreground)] leading-snug">${b.winner}</div>
                    </div>
                    <dl class="grid grid-cols-1 gap-2 text-sm">
                      <div><dt class="font-semibold text-sky-400">${b.side_a.name} losses</dt><dd class="text-[var(--foreground)]">${b.losses_a}</dd></div>
                      <div><dt class="font-semibold text-rose-400">${b.side_b.name} losses</dt><dd class="text-[var(--foreground)]">${b.losses_b}</dd></div>
                    </dl>
                    <div class="flex gap-2 pt-1">
                      <button onclick="restartBattleSim()" class="h-11 px-4 rounded-md border border-[var(--border)] text-[var(--foreground)] hover:border-amber-400 text-sm font-semibold">Replay</button>
                      <button onclick="stepBattlePage(1)" class="h-11 px-4 rounded-md bg-amber-500 hover:bg-amber-400 text-slate-950 text-sm font-semibold">Next battle</button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Docked control bar -->
              <div id="sim-controls" class="flex items-center gap-3 px-3 min-h-14 py-2 bg-[var(--card)] border-t border-[var(--border)]">
                <button id="sim-play-btn" onclick="toggleSimPlay()" aria-label="Pause" class="shrink-0 w-11 h-11 rounded-md bg-amber-500 hover:bg-amber-400 text-slate-950 flex items-center justify-center"></button>
                <button id="sim-replay-btn" onclick="restartBattleSim()" aria-label="Replay from the start" title="Replay from the start" class="shrink-0 w-11 h-11 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--background)] flex items-center justify-center">
                  <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/></svg>
                </button>
                <button id="sim-link-btn" onclick="copySimMomentLink()" aria-label="Copy a link to this moment" title="Copy a link to this moment"
                  class="shrink-0 w-11 h-11 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--background)] flex items-center justify-center">
                  <svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/></svg>
                </button>
                <span id="sim-time-readout" class="shrink-0 w-44 truncate text-sm tabular-nums text-[var(--foreground)]">${(phases[0] && phases[0].time) || b.date}</span>
                <div class="relative flex-1 min-w-[160px] pt-5">
                  ${phases.map((ph, idx) => {
                    const nPh = Math.max(1, phases.length);
                    const r0 = (ph.range && typeof ph.range[0] === 'number') ? ph.range[0] : (idx / nPh);
                    const r1 = (ph.range && typeof ph.range[1] === 'number') ? ph.range[1] : ((idx + 1) / nPh);
                    const midPct = Math.round(((r0 + r1) / 2) * 100);
                    return `<button id="sim-notch-${idx}" class="sim-notch" style="left:${(r0 * 100).toFixed(1)}%" onclick="setBattleSimProgress(${midPct})" aria-label="Phase ${idx + 1}: ${(ph.title || '').replace(/"/g, '&quot;')}" title="Phase ${idx + 1}: ${(ph.title || '').replace(/"/g, '&quot;')}">${idx + 1}</button>`;
                  }).join('')}
                  <div class="sim-loss-strip" title="Tanks knocked out over time: Side A above, Side B below">${lossStrip}</div>
                  <input id="sim-scrubber" type="range" min="0" max="1" step="0.004" value="${state.sim.progress}" oninput="scrubBattleSim(this.value)" aria-label="Battle timeline" class="w-full accent-amber-400 cursor-pointer" />
                </div>
                <div class="relative shrink-0 hidden md:block">
                  <button id="sim-keys-btn" onclick="toggleSimKeys()" aria-label="Keyboard shortcuts" aria-expanded="false" aria-controls="sim-keys" title="Keyboard shortcuts"
                    class="w-9 h-9 rounded-md border border-[var(--border)] text-sm font-semibold text-[var(--muted-foreground)] hover:text-[var(--foreground)]">?</button>
                  <div id="sim-keys" role="dialog" aria-label="Keyboard shortcuts" class="hidden absolute bottom-12 right-0 w-64 rounded-[10px] border border-[var(--border)] bg-[var(--card)] shadow-lg p-3 z-30">
                    <dl class="grid grid-cols-[auto_1fr] gap-x-3 gap-y-2 text-sm text-[var(--foreground)]">
                      <dt><kbd>Space</kbd></dt><dd>Play or pause</dd>
                      <dt><kbd>←</kbd> <kbd>→</kbd></dt><dd>Previous or next phase</dd>
                      <dt><kbd>Esc</kbd></dt><dd>Close the tank card or this list</dd>
                      <dt><kbd>?</kbd></dt><dd>Show this list</dd>
                    </dl>
                  </div>
                </div>
                <div id="sim-speed-group" class="shrink-0 flex items-center gap-1" role="group" aria-label="Speed">
                  <button data-sim-speed="0.5" onclick="setSimSpeed(0.5)" class="cf-btn" aria-pressed="${state.sim.speed === 0.5}">0.5×</button>
                  <button data-sim-speed="1" onclick="setSimSpeed(1)" class="cf-btn" aria-pressed="${state.sim.speed === 1}">1×</button>
                  <button data-sim-speed="2" onclick="setSimSpeed(2)" class="cf-btn" aria-pressed="${state.sim.speed === 2}">2×</button>
                </div>
              </div>
            </div>

            <!-- Story panel: current phase + event feed -->
            <aside aria-label="Battle story" class="sim-panel sheet lg:col-span-1 bg-[var(--card)] border border-[var(--border)] rounded-[10px] flex flex-col min-w-0">
              <button class="sheet-handle" aria-label="Expand or collapse the story panel"></button>
              <div id="sim-unit-card" class="hidden flex-1 min-h-0 overflow-y-auto custom-scroll p-4 flex flex-col gap-3"></div>
              <div id="sim-story" class="flex-1 min-h-0 flex flex-col">
              <div class="p-4 border-b border-[var(--border)] flex flex-col gap-1">
                <div id="sim-phase-label" class="text-xs font-semibold uppercase tracking-wide text-amber-400"></div>
                <h3 id="sim-banner-title" class="text-base font-semibold text-[var(--foreground)] leading-snug"></h3>
                <p id="sim-banner-desc" class="text-sm text-[var(--muted-foreground)] leading-relaxed line-clamp-4"></p>
                <div id="sim-banner-losses" class="text-sm text-rose-400 tabular-nums"></div>
              </div>
              <div class="flex-1 min-h-0 overflow-y-auto custom-scroll p-4 flex flex-col gap-2">
                <div class="text-xs font-semibold text-[var(--muted-foreground)]">Events</div>
                <div id="sim-telemetry-log" aria-live="off" class="flex flex-col gap-2 text-sm text-[var(--foreground)]"></div>
              </div>
              </div>
              <div class="p-3 border-t border-[var(--border)] flex flex-wrap items-center gap-1.5">
                <span class="text-xs text-[var(--muted-foreground)] mr-1">Map</span>
                <button id="sim-bg-historical" onclick="setSimMapBgMode('historical')" class="cf-btn" aria-pressed="false">Historical</button>
                <button id="sim-bg-topo" onclick="setSimMapBgMode('topo')" class="cf-btn" aria-pressed="false">Terrain</button>
                <button id="sim-bg-satellite" onclick="setSimMapBgMode('satellite')" class="cf-btn" aria-pressed="false">Satellite</button>
                <button id="sim-bg-tactical" onclick="setSimMapBgMode('tactical')" class="cf-btn" aria-pressed="false">Grid</button>
                <button id="sim-hull-btn" onclick="toggleSimHulls()" class="cf-btn" aria-pressed="${state.sim.showHulls !== false}">Tank photos</button>
                <button id="sim-stops-btn" onclick="setStopAtPhases(state.sim.stopAtPhases === false)" class="cf-btn" aria-pressed="${state.sim.stopAtPhases !== false}" title="Pause at the start of each phase">Stop at each phase</button>
              </div>
            </aside>
          </div>
        </div>

        <!-- Battle details (below the fold): header, key facts, tanks, losses, kill-cam, media -->
        <section id="battle-details" aria-label="Battle details" class="scroll-mt-20 bg-[var(--card)] border border-[var(--border)] rounded-[10px] p-5 flex flex-col gap-4">
          <div class="flex flex-wrap items-start justify-between gap-4 border-b border-[var(--border)] pb-4">
            <div>
              <div class="flex flex-wrap items-center gap-2">
                <span class="px-3 py-1 rounded-full text-xs font-extrabold bg-rose-500/20 text-rose-300 border border-rose-500/40">
                  ⚔️ ${b.date} • ${b.theatre}
                </span>
                <span class="px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                  📍 ${b.location} [${b.lat.toFixed(2)}°N, ${b.lon.toFixed(2)}°E]
                </span>
                <span class="px-3 py-1 rounded-full text-xs font-extrabold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                  🛡️ ${b.total_tanks}
                </span>
              </div>
              <h2 class="text-2xl sm:text-3xl font-extrabold text-[var(--foreground)] mt-2">${b.name}</h2>
              <p class="text-sm text-[var(--muted-foreground)] mt-1 max-w-4xl leading-relaxed">${b.summary}</p>
            </div>
            <button onclick="jumpToBattleOnMap('${b.id}')" class="px-3.5 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white text-xs font-extrabold shadow shrink-0">
              🌍 Locate on World Map →
            </button>
          </div>

          <!-- 4-Card Key Battle Facts: Winner, Defeated, Total Scale, Terrain & Range -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
            <div class="bg-emerald-500/10 border border-emerald-500/40 rounded-xl p-3.5">
              <div class="text-xs font-extrabold text-emerald-400 uppercase">🏆 Victorious Side (Who Won)</div>
              <div class="text-sm font-extrabold text-[var(--foreground)] mt-1">${b.winner}</div>
              <div class="text-xs text-[var(--muted-foreground)] mt-1">${b.outcome}</div>
            </div>
            <div class="bg-rose-500/10 border border-rose-500/40 rounded-xl p-3.5">
              <div class="text-xs font-extrabold text-rose-400 uppercase">💥 Defeated / Halted Side</div>
              <div class="text-sm font-extrabold text-[var(--foreground)] mt-1">${b.loser}</div>
              <div class="text-xs text-rose-300 mt-1">🟦 Lost: ${b.losses_a}<br/>🟥 Lost: ${b.losses_b}</div>
            </div>
            <div class="bg-amber-500/10 border border-amber-500/40 rounded-xl p-3.5">
              <div class="text-xs font-extrabold text-amber-400 uppercase">📊 Total Armor Involved</div>
              <div class="text-sm font-extrabold text-amber-300 mt-1">${b.total_tanks}</div>
              <div class="text-xs text-[var(--muted-foreground)] mt-1">🟦 ${b.side_a.count}<br/>🟥 ${b.side_b.count}</div>
            </div>
            <div class="bg-sky-500/10 border border-sky-500/40 rounded-xl p-3.5">
              <div class="text-xs font-extrabold text-sky-400 uppercase">🎯 Engagement Range &amp; Lesson</div>
              <div class="text-sm font-extrabold text-sky-300 mt-1">Range: ${b.tactical_zoom.range_m}</div>
              <div class="text-xs text-[var(--muted-foreground)] mt-1">${b.tactical_zoom.key_lesson}</div>
            </div>
          </div>

          <!-- ========================================================================= -->
          <!-- HOW THE TANKS GOT DESTROYED — FORENSIC LOSS BREAKDOWN (SIDE A & SIDE B)   -->
          <!-- ========================================================================= -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 pt-2">
            ${renderForensicCard(
              b.destruction_a,
              `💥 How ${b.side_a.name} Tanks Got Destroyed (${b.losses_a})`,
              'text-sky-400',
              'bg-sky-400'
            )}
            ${renderForensicCard(
              b.destruction_b,
              `💥 How ${b.side_b.name} Tanks Got Destroyed (${b.losses_b})`,
              'text-rose-400',
              'bg-rose-500'
            )}
          </div>

          <!-- Participating Tanks Roster with Real Photos & Direct Popup / Page Buttons -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 pt-2">
            <div class="bg-sky-500/5 border border-sky-500/30 rounded-xl p-4 flex flex-col gap-2.5">
              <div class="flex items-center justify-between">
                <span class="text-sm font-extrabold text-sky-400">🟦 ${b.side_a.flag || ''} ${b.side_a.name} — Participating Tank Models (${b.side_a.tanks.length})</span>
                <span class="text-xs font-bold text-slate-300">${b.side_a.count}</span>
              </div>
              <div class="text-xs text-rose-300 font-semibold">Recorded Losses: ${b.losses_a}</div>
              <div class="flex flex-col gap-2 mt-1">
                ${b.side_a.tanks.map(tid => renderParticipTankCard(tid, 'sky')).join('')}
              </div>
            </div>

            <div class="bg-rose-500/5 border border-rose-500/30 rounded-xl p-4 flex flex-col gap-2.5">
              <div class="flex items-center justify-between">
                <span class="text-sm font-extrabold text-rose-400">🟥 ${b.side_b.flag || ''} ${b.side_b.name} — Participating Tank Models (${b.side_b.tanks.length})</span>
                <span class="text-xs font-bold text-slate-300">${b.side_b.count}</span>
              </div>
              <div class="text-xs text-rose-300 font-semibold">Recorded Losses: ${b.losses_b}</div>
              <div class="flex flex-col gap-2 mt-1">
                ${b.side_b.tanks.map(tid => renderParticipTankCard(tid, 'rose')).join('')}
              </div>
            </div>
          </div>

          <!-- ========================================================================= -->
          <!-- 💥 HOW THE TANKS BLEW UP: INTERACTIVE BALLISTIC KILL-CAM + REAL WRECKAGE  -->
          <!-- ========================================================================= -->
          <div class="bg-slate-950 border-2 border-rose-500/70 rounded-2xl p-5 shadow-2xl flex flex-col gap-4">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
              <div>
                <div class="flex items-center gap-2">
                  <span class="px-2.5 py-1 rounded bg-rose-600 text-white text-xs font-extrabold">💥 BALLISTIC ARMOR PENETRATION &amp; COOK-OFF KILL-CAM</span>
                  <h3 class="text-lg font-extrabold text-white">How the Tanks Blew Up in ${b.name} — X-Ray Ballistics, Real Wreckage Photos &amp; Combat Footage</h3>
                </div>
                <p class="text-xs text-slate-300 mt-1">Select a historical engagement below to inspect the exact shell penetration vs. armor thickness, internal spall cone, ammunition cook-off, and turret blow-off physics.</p>
              </div>
            </div>

            <!-- Scenario Selector Buttons + Interactive X-Ray Kill-Cam Canvas -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 items-stretch">
              <div class="lg:col-span-5 flex flex-col gap-2">
                <div class="text-xs font-extrabold text-amber-400 uppercase">🎯 Select Historical Duel / Kill-Cam Scenario (${killScenarios.length}):</div>
                ${killScenarios.map((sc, idx) => `
                  <button id="killcam-btn-${idx}" onclick="selectKillCamScenario(${idx})" class="${idx === 0 ? 'p-2.5 rounded-xl border-2 border-rose-400 bg-rose-500/20 text-left transition shadow-lg flex flex-col gap-1' : 'p-2.5 rounded-xl border border-slate-700 bg-slate-900/90 hover:border-rose-400/60 text-left transition opacity-85 hover:opacity-100 flex flex-col gap-1'}">
                    <div class="flex items-center justify-between gap-2">
                      <span class="text-xs font-extrabold text-white">⚔️ ${sc.title}</span>
                      <span class="px-2 py-0.5 rounded text-xs font-mono font-extrabold ${sc.result === 'RICOCHET' ? 'bg-amber-500/20 text-amber-300 border border-amber-400/40' : 'bg-rose-500/30 text-rose-200 border border-rose-400/50'}">${sc.result.replace(/_/g, ' ')}</span>
                    </div>
                    <div class="text-xs font-mono text-sky-300">Projectile: ${sc.shell} (${sc.pen_mm}mm Pen vs ${sc.armor_mm}mm Armor)</div>
                  </button>
                `).join('')}
              </div>

              <div class="lg:col-span-7 bg-slate-900 border border-slate-700 rounded-xl overflow-hidden flex flex-col justify-between">
                <div class="relative h-[270px] w-full bg-[#050c16]">
                  <canvas id="killcam-canvas" class="w-full h-full block"></canvas>
                </div>
                <div id="killcam-scenario-desc" class="px-4 py-3 bg-slate-950 border-t border-slate-800 text-xs leading-relaxed">
                  ${killScenarios[0] ? `<strong class="text-rose-300">💥 ${killScenarios[0].title}:</strong> <span class="text-slate-200">${killScenarios[0].desc}</span>` : ''}
                </div>
              </div>
            </div>

            <!-- Real Historical Operational Maps + Real Knocked-Out Tank Wreckage Gallery + Playable Archival Video Footage -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 pt-2 border-t border-slate-800">
              <!-- Column 1 (4 cols): Real Historical Operational Battle Map(s) -->
              <div class="lg:col-span-4 bg-slate-900/90 border border-amber-500/40 rounded-xl p-3.5 flex flex-col gap-2.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-extrabold text-amber-400 uppercase">🗺️ Real Historical Battle Maps</span>
                  ${b.real_map_url ? `<a href="${b.real_map_url}" target="_blank" rel="noopener" class="text-xs font-bold text-sky-400 hover:underline">Open Full-Res Map ↗</a>` : ''}
                </div>
                ${b.real_map_url ? `
                  <a href="${b.real_map_url}" target="_blank" rel="noopener" class="block rounded-lg overflow-hidden border border-slate-700 hover:border-amber-400 transition">
                    <img src="${b.real_map_url}" alt="${b.name} Historical Map" class="w-full h-48 object-cover bg-slate-950" loading="lazy" />
                  </a>
                ` : ''}
                ${b.real_map_alt_url ? `
                  <a href="${b.real_map_alt_url}" target="_blank" rel="noopener" class="block rounded-lg overflow-hidden border border-slate-700 hover:border-amber-400 transition">
                    <img src="${b.real_map_alt_url}" alt="${b.name} Secondary Map" class="w-full h-40 object-cover bg-slate-950" loading="lazy" />
                  </a>
                ` : ''}
                <p class="text-xs text-slate-300 leading-relaxed">${b.real_map_caption || ''}</p>
              </div>

              <!-- Column 2 (5 cols): Real Archival Photographs of Knocked-Out Tanks & How They Blew Up -->
              <div class="lg:col-span-5 bg-slate-900/90 border border-rose-500/40 rounded-xl p-3.5 flex flex-col gap-2.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-extrabold text-rose-400 uppercase">🔥 Real Knocked-Out Tank Wreckage Photos (${wreckPhotos.length})</span>
                  <span class="text-xs font-mono text-slate-400">Archival Combat Forensics</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 overflow-y-auto max-h-[420px] custom-scroll pr-1">
                  ${wreckPhotos.map(w => `
                    <div class="bg-slate-950 border border-slate-800 rounded-lg overflow-hidden flex flex-col">
                      <a href="${w.url}" target="_blank" rel="noopener" class="block h-32 overflow-hidden bg-black">
                        <img src="${w.url}" alt="${w.title}" class="w-full h-full object-cover hover:scale-105 transition" loading="lazy" />
                      </a>
                      <div class="p-2.5 flex-1 flex flex-col justify-between gap-1">
                        <div class="text-xs font-extrabold text-rose-300 leading-snug">${w.title}</div>
                        <p class="text-xs text-slate-300 leading-relaxed">${w.how_destroyed}</p>
                      </div>
                    </div>
                  `).join('')}
                </div>
              </div>

              <!-- Column 3 (3 cols): Inline Playable Archival Combat & Anti-Tank Video Footage -->
              <div class="lg:col-span-3 bg-slate-900/90 border border-emerald-500/40 rounded-xl p-3.5 flex flex-col gap-2.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-extrabold text-emerald-400 uppercase">🎬 Playable Combat Footage</span>
                  <span class="text-xs font-mono text-emerald-300">HTML5 Video</span>
                </div>
                <div class="flex flex-col gap-2.5 overflow-y-auto max-h-[420px] custom-scroll pr-1">
                  ${combatVideos.map(v => `
                    <div class="bg-slate-950 border border-slate-800 rounded-lg p-2.5 flex flex-col gap-1.5">
                      <div class="text-xs font-extrabold text-white">${v.title}</div>
                      <div class="text-xs text-slate-400">${v.source}</div>
                      ${v.video_url ? `
                        <video controls preload="metadata" class="w-full rounded border border-slate-700 bg-black max-h-40">
                          <source src="${v.video_url}" />
                        </video>
                      ` : ''}
                      ${v.yt_url ? `
                        <a href="${v.yt_url}" target="_blank" rel="noopener" class="mt-1 px-2.5 py-1.5 rounded bg-red-600/20 hover:bg-red-600/30 border border-red-500/40 text-red-300 text-xs font-extrabold text-center transition">
                          ▶ Watch Full Historical Documentary on YouTube ↗
                        </a>
                      ` : ''}
                    </div>
                  `).join('')}
                </div>
              </div>
            </div>
          </div>

          <!-- Other major battles -->
          <div class="flex flex-wrap items-center gap-2 pt-3 border-t border-[var(--border)]">
            <span class="text-sm font-semibold text-[var(--foreground)] mr-1">Other major battles</span>
            ${['raseiniai_1941', 'kursk_1943', 'an_loc_dong_ha_1972', 'valley_of_tears_1973', 'easting_1991'].filter(id => id !== b.id && BATTLE_MAP[id]).map(id =>
              `<button onclick="openBattlePage('${id}')" class="cf-btn">${BATTLE_MAP[id].name.replace(/^Battles? of (the )?/, '')}, ${BATTLE_MAP[id].year}</button>`).join('')}
          </div>
        </section>
      `;

      const headerTitle = document.getElementById('battle-header-title');
      if (headerTitle) headerTitle.textContent = `${b.name}, ${b.year}`;
      syncPlayButton();
      syncSimOverlay();
      observeSimStage();

      setTimeout(() => {
        setSimMapBgMode(state.sim.mapBgMode || 'historical');
      }, 30);
    }

    let simBattleCache = { battleId: null, agents: [] };
    let simScreenAgents = [];
    let hoveredSimAgent = null;

    function shortTankLabel(t) {
      if (!t) return 'Tank';
      const n = t.name;
      if (n.includes('KV-2')) return 'KV-2 152mm';
      if (n.includes('KV-1')) return 'KV-1 90mm';
      if (n.includes('BT-7')) return 'BT-7';
      if (n.includes('T-26')) return 'T-26';
      if (n.includes('38(t)')) return 'Pz.38(t)';
      if (n.includes('Panzer IV')) return 'Pz.IV';
      if (n.includes('Panzer III')) return 'Pz.III';
      if (n.includes('Panzer II')) return 'Pz.II';
      if (n.includes('T-34/85')) return 'T-34/85';
      if (n.includes('T-34')) return 'T-34';
      if (n.includes('Tiger II')) return 'Tiger II';
      if (n.includes('Tiger I')) return 'Tiger I';
      if (n.includes('Panther')) return 'Panther';
      if (n.includes('Sherman Firefly')) return 'Firefly';
      if (n.includes('M4 Sherman')) return 'M4 Sherman';
      if (n.includes('M48')) return 'M48A3';
      if (n.includes('M41')) return 'M41';
      if (n.includes('T-54') || n.includes('T-55')) return 'T-54/55';
      if (n.includes('PT-76')) return 'PT-76';
      if (n.includes('Centurion')) return 'Centurion';
      if (n.includes('M1A1') || n.includes('Abrams')) return 'M1 Abrams';
      if (n.includes('T-72')) return 'T-72';
      return n.split(' ')[0].slice(0, 10);
    }

    function buildBattleAgents(b) {
      const agents = [];
      const isRaseiniai = b.id === 'raseiniai_1941';
      const winSide = b.winner_side || 'A';
      const lossRatioA = b.side_a_num ? Math.min(0.95, (b.loss_a_num || 100) / b.side_a_num) : (winSide === 'A' ? 0.28 : 0.78);
      const lossRatioB = b.side_b_num ? Math.min(0.95, (b.loss_b_num || 100) / b.side_b_num) : (winSide === 'B' ? 0.24 : 0.78);

      const tanksA = b.side_a.tanks.length ? b.side_a.tanks : ['t34_76'];
      const tanksB = b.side_b.tanks.length ? b.side_b.tanks : ['panzer_iv'];
      const causesA = (b.destruction_a || []).map(d => d.cause);
      const causesB = (b.destruction_b || []).map(d => d.cause);

      // Spawn 40 Side A Tank Platoon Agents across 4 Tactical Echelons
      // Never draw more counters than the side had tanks (small battles: one counter per tank)
      const countA = Math.max(1, Math.min(isRaseiniai ? 42 : 34, b.side_a_num || Infinity));
      for (let i = 0; i < countA; i++) {
        let tid = tanksA[i % tanksA.length];
        if (isRaseiniai) {
          // Historical mix: ~14% KV-1 & KV-2 heavy giants, ~46% BT-7, ~40% T-26 light tanks
          if (i === 0 || i === 3 || i === 5) tid = 'kv2';
          else if (i === 1 || i === 2 || i === 4) tid = 'kv1';
          else if (i % 2 === 0) tid = 'bt7';
          else tid = 't26';
        }
        const t = TANK_MAP[tid] || TANKS[0];
        const isHeavy = (t.armor_mm || 30) >= 75 || tid === 'kv1' || tid === 'kv2';
        const row = i % 7;
        const col = Math.floor(i / 7);

        let sx = isRaseiniai ? (74 + col * 3.8 + (row % 2) * 1.2) : (12 + col * 4.2);
        let sy = 14 + row * 11.5 + ((col % 2) * 3.5);
        let tx = isRaseiniai ? (42 + col * 2.6) : (48 + (col % 3) * 4);
        let ty = sy + (row - 3) * 1.8;

        let killAt = 9.9;
        let killCause = 'Survived Battle';
        let isLoneKV = false;

        if (isRaseiniai && i === 0) {
          // The Legendary Lone KV-2 (152mm) at the Northern Dubysa Crossroads!
          isLoneKV = true;
          sx = 62; sy = 23;
          tx = 33; ty = 22;
          killAt = 0.59;
          killCause = '🎯 88mm Flak 36 Battery (6 Rear Hits After 26h Stand)';
        } else {
          const willDie = (i / countA) < lossRatioA;
          if (willDie) {
            if (isRaseiniai) {
              if (isHeavy) {
                killAt = 0.52 + (i * 0.07) % 0.42;
                killCause = i % 2 === 0 ? '🎯 88mm Flak 36 / 105mm Direct Hit' : '⛽ Out of Fuel/Ammo in Pocket (Scuttled)';
              } else {
                // Light BT-7 / T-26 tanks hit in Phase 2-4 by 37mm/50mm flank crossfire or trapped in Phase 5 pocket
                killAt = 0.24 + ((i * 17) % 70) / 100;
                if (killAt > 0.80) killCause = '⛽ Out of Fuel in Raseiniai Pocket';
                else if (killAt > 0.58) killCause = '🔥 1st Pz.Div Flank Hook (50mm Ammo Cook-Off)';
                else killCause = i % 3 === 0 ? '✈️ Luftwaffe Stuka / 105mm Artillery' : '💥 37mm/50mm Pak & Pz.38(t) Crossfire';
              }
            } else {
              killAt = 0.20 + ((i * 19) % 74) / 100;
              killCause = causesA[i % Math.max(1, causesA.length)] || 'Direct AP/HEAT Penetration';
            }
          }
        }

        agents.push({
          id: 'A-' + i,
          side: 'A',
          tankId: tid,
          label: isLoneKV ? '⭐ LONE KV-2 (26h)' : shortTankLabel(t),
          isHeavy,
          isLoneKV,
          sx, sy, tx, ty,
          killAt,
          killCause
        });
      }

      // Spawn 30 Side B Tank Platoon Agents
      const countB = Math.max(1, Math.min(isRaseiniai ? 28 : 30, b.side_b_num || Infinity));
      for (let j = 0; j < countB; j++) {
        let tid = tanksB[j % tanksB.length];
        if (isRaseiniai) {
          if (j < 13) tid = 'pz_38t';
          else if (j < 19) tid = 'panzer_iv';
          else if (j < 24) tid = 'panzer_iii';
          else tid = 'panzer_ii';
        }
        const t = TANK_MAP[tid] || TANKS[1];
        const isHeavy = (t.armor_mm || 30) >= 80;
        const isFlankHook = isRaseiniai && j >= 14; // 1st Panzer Division Southern Flank Hook via Kelmė!
        const row = j % 7;
        const col = Math.floor(j / 7);

        let sx = isRaseiniai ? (12 + col * 4.5) : (88 - col * 4.2);
        let sy = isFlankHook ? (64 + (j % 4) * 7.5) : (15 + row * 11.2);
        let tx = isRaseiniai ? (isFlankHook ? 66 + (j % 4) * 5 : 40 + col * 3.5) : (52 - (col % 3) * 4);
        let ty = isRaseiniai ? (isFlankHook ? 52 - (j % 4) * 8 : sy + (row - 3) * 1.5) : sy;

        const willDie = (j / countB) < lossRatioB;
        let killAt = 9.9;
        let killCause = 'Survived Battle';
        if (willDie) {
          if (isRaseiniai) {
            killAt = 0.23 + ((j * 23) % 45) / 100;
            killCause = j % 2 === 0 ? '💥 Crushed / Overrun by KV-1 & KV-2' : '🎯 76.2mm / 152mm Direct Hit';
          } else {
            killAt = 0.22 + ((j * 17) % 72) / 100;
            killCause = causesB[j % Math.max(1, causesB.length)] || 'Direct AP/HEAT Penetration';
          }
        }

        agents.push({
          id: 'B-' + j,
          side: 'B',
          tankId: tid,
          label: shortTankLabel(t),
          isHeavy,
          isFlankHook,
          sx, sy, tx, ty,
          killAt,
          killCause
        });
      }

      return agents;
    }

    function drawArticulatedTankAgent(ctx, x, y, angle, color, agent, isWreck, isRicochet, isHovered, curProgress) {
      ctx.save();
      ctx.translate(x, y);

      const scale = agent.isLoneKV ? 1.42 : (agent.isHeavy ? 1.18 : 0.96);
      const tImg = getTankImg(agent.tankId);
      const isNoFuel = isWreck && (agent.killCause.includes('Fuel') || agent.killCause.includes('Scuttled') || agent.killCause.includes('Abandoned'));
      const dtKill = isWreck ? Math.max(0, (curProgress || 0) - agent.killAt) : 0;

      // 1. Rotated Armored Tracks + Main Gun Barrel + Muzzle Flash
      ctx.save();
      ctx.scale(scale, scale);
      ctx.rotate(angle);

      if (isWreck) {
        // Scorched / Shattered Chassis Hull
        ctx.fillStyle = isNoFuel ? '#0f172a' : '#18181b';
        ctx.strokeStyle = isNoFuel ? '#22d3ee' : '#ef4444';
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.roundRect(-14, -9, 28, 18, 3);
        ctx.fill();
        ctx.stroke();
      } else {
        // Armored Tracks
        ctx.fillStyle = '#020617';
        ctx.fillRect(-15, -11, 30, 3.5);
        ctx.fillRect(-15, 7.5, 30, 3.5);

        // Main Gun Barrel Extending Toward Target
        ctx.strokeStyle = agent.isLoneKV ? '#fde047' : '#ffffff';
        ctx.lineWidth = agent.isHeavy ? 3.0 : 2.2;
        ctx.beginPath();
        ctx.moveTo(6, 0);
        ctx.lineTo(agent.isHeavy ? 24 : 20, 0);
        ctx.stroke();

        // Periodic Muzzle Blast Flame when firing
        const firingNow = ((state.animTick + Math.floor(x * 3)) % 52) < 5 && (curProgress || 0) >= 0.12;
        if (firingNow) {
          ctx.fillStyle = '#fef08a';
          ctx.beginPath();
          ctx.arc(agent.isHeavy ? 26 : 22, 0, agent.isHeavy ? 5.5 : 4, 0, Math.PI * 2);
          ctx.fill();
        }
      }
      ctx.restore();

      // 2. Unrotated Real Tank Photo Badge on Every Unit!
      const pw = (agent.isLoneKV ? 38 : (agent.isHeavy || isHovered ? 31 : 25));
      const ph = (agent.isLoneKV ? 26 : (agent.isHeavy || isHovered ? 21 : 17));

      ctx.save();
      ctx.beginPath();
      ctx.roundRect(-pw / 2, -ph / 2, pw, ph, 4);
      ctx.fillStyle = '#0f172a';
      ctx.fill();
      if (tImg) {
        ctx.save();
        ctx.clip();
        if (isWreck && !isNoFuel) ctx.globalAlpha = 0.48;
        ctx.drawImage(tImg, -pw / 2, -ph / 2, pw, ph);
        ctx.restore();
      }
      ctx.strokeStyle = isWreck
        ? (isNoFuel ? '#22d3ee' : '#ef4444')
        : (isHovered || agent.isLoneKV ? '#fbbf24' : color);
      ctx.lineWidth = (agent.isLoneKV || isHovered) ? 2.4 : 1.7;
      ctx.stroke();

      // Heavy Frontal Armor Gold Shield Bar
      if (!isWreck && agent.isHeavy) {
        ctx.fillStyle = '#fde047';
        ctx.fillRect(-pw / 2, -ph / 2, pw, 2.5);
      }
      ctx.restore();

      // 3. CATASTROPHIC EXPLOSION, AMMO COOK-OFF & FLYING TURRET ANIMATION FOR WRECKS!
      if (isWreck) {
        if (!isNoFuel) {
          // Fresh Catastrophic Explosion & Flying Turret ("Jack-in-the-Box" Cook-Off) when just hit!
          if (dtKill < 0.14) {
            const ep = dtKill / 0.14; // 0 -> 1 explosion progress
            // Expanding Blast Shockwave Ring
            ctx.strokeStyle = `rgba(253, 224, 71, ${1 - ep})`;
            ctx.lineWidth = 2.6 * (1 - ep * 0.5);
            ctx.beginPath();
            ctx.arc(0, 0, 10 + ep * 42, 0, Math.PI * 2);
            ctx.stroke();

            // Multi-layered Propellant Cook-Off Fireball
            const fireR = Math.sin(ep * Math.PI) * 20;
            if (fireR > 1) {
              const grad = ctx.createRadialGradient(0, -4, 1, 0, -4, fireR);
              grad.addColorStop(0, '#ffffff');
              grad.addColorStop(0.35, '#fde047');
              grad.addColorStop(0.7, '#f97316');
              grad.addColorStop(1, 'rgba(220, 38, 38, 0)');
              ctx.fillStyle = grad;
              ctx.beginPath();
              ctx.arc(0, -4, fireR, 0, Math.PI * 2);
              ctx.fill();
            }

            // Flying Severed Turret spinning through the air!
            const turX = (agent.side === 'A' ? -1 : 1) * ep * 28;
            const turY = -Math.sin(ep * Math.PI) * 38 - ep * 8;
            ctx.save();
            ctx.translate(turX, turY);
            ctx.rotate(ep * 9.5);
            ctx.fillStyle = '#27272a';
            ctx.strokeStyle = '#fb923c';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.arc(0, 0, 5.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(4, 0);
            ctx.lineTo(13, 0);
            ctx.stroke();
            ctx.restore();

          }

          // Continuous Burning Wreckage Flames & Billowing Black Oil Smoke Plume
          const puff = (state.animTick * 0.035 + x * 0.13) % 1;
          ctx.fillStyle = `rgba(15, 23, 42, ${0.78 - puff * 0.65})`;
          ctx.beginPath();
          ctx.arc(puff * 6 - 3, -8 - puff * 20, 5 + puff * 6, 0, Math.PI * 2);
          ctx.fill();

          const flicker = 0.7 + Math.sin(state.animTick * 0.25 + y) * 0.3;
          ctx.fillStyle = `rgba(249, 115, 22, ${0.85 * flicker})`;
          ctx.beginPath();
          ctx.arc(0, -2, 4.5 * flicker, 0, Math.PI * 2);
          ctx.fill();

          // Red Knocked-Out Cross
          ctx.strokeStyle = '#ef4444';
          ctx.lineWidth = 2.0;
          ctx.beginPath();
          ctx.moveTo(-7, -5); ctx.lineTo(7, 5);
          ctx.moveTo(7, -5); ctx.lineTo(-7, 5);
          ctx.stroke();
        } else {
          // Out of Fuel / Scuttled badge
          ctx.fillStyle = 'rgba(8, 51, 68, 0.92)';
          ctx.strokeStyle = '#22d3ee';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.roundRect(-14, -7, 28, 14, 3);
          ctx.fill();
          ctx.stroke();
        }
      }

      ctx.restore();
    }

    function setupSimCanvas() {
      const canvas = document.getElementById('battle-sim-canvas');
      if (!canvas || canvas.dataset.bound === '1') return;
      canvas.dataset.bound = '1';

      canvas.addEventListener('mousemove', (e) => {
        const hit = hitTestSimAgent(canvas, e, 15);
        hoveredSimAgent = hit;
        canvas.style.cursor = hit ? 'pointer' : 'default';
      });

      // Touch gets a 22px radius (44px target); mouse keeps 15px
      canvas.addEventListener('click', (e) => {
        const touch = e.pointerType === 'touch' || matchMedia('(pointer: coarse)').matches;
        const hit = hitTestSimAgent(canvas, e, touch ? 22 : 15);
        if (hit && hit.tankId) selectSimUnit(hit.id);
      });
    }

    // Losses strip: knock-outs per time bin, Side A bars up from the middle, Side B down
    function renderLossStrip(agents, bins) {
      const a = new Array(bins).fill(0), b = new Array(bins).fill(0);
      agents.forEach(ag => {
        if (ag.killAt > 1) return; // survivors
        const i = Math.min(bins - 1, Math.floor(ag.killAt * bins));
        (ag.side === 'A' ? a : b)[i]++;
      });
      const max = Math.max(1, ...a, ...b);
      const bar = (v, i, up) => {
        const h = (v / max) * 7.5;
        return v ? `<rect x="${i + 0.15}" y="${up ? 8 - h : 8}" width="0.7" height="${h.toFixed(2)}" fill="${up ? 'var(--side-a)' : 'var(--side-b)'}"/>` : '';
      };
      return `<svg aria-hidden="true" viewBox="0 0 ${bins} 16" preserveAspectRatio="none" class="block w-full h-4">${a.map((v, i) => bar(v, i, true)).join('')}${b.map((v, i) => bar(v, i, false)).join('')}</svg>`;
    }

    function copySimMomentLink() {
      const url = `${location.origin}${location.pathname}${location.search}#/battles/${state.selectedBattleId}?t=${state.sim.progress.toFixed(3)}`;
      const btn = document.getElementById('sim-link-btn');
      const done = (label) => {
        btn.setAttribute('title', label);
        btn.setAttribute('aria-label', label);
        btn.classList.add('text-amber-400');
        setTimeout(() => {
          btn.setAttribute('title', 'Copy a link to this moment');
          btn.setAttribute('aria-label', 'Copy a link to this moment');
          btn.classList.remove('text-amber-400');
        }, 2000);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(url).then(() => done('Link copied'), () => prompt('Copy this link:', url));
      } else {
        prompt('Copy this link:', url);
      }
    }

    function formationPath(u, W, H) {
      return {
        x0: (u.x / 100) * W, y0: (u.y / 100) * H,
        x1: ((u.tx ?? (u.side === 'A' ? u.x + 14 : u.x - 14)) / 100) * W,
        y1: ((u.ty ?? u.y) / 100) * H
      };
    }

    function drawArrow(ctx, x0, y0, x1, y1, color, width, dashed, head) {
      const len = Math.hypot(x1 - x0, y1 - y0);
      if (len < 4) return;
      const ang = Math.atan2(y1 - y0, x1 - x0);
      ctx.save();
      ctx.lineCap = 'round';
      ctx.setLineDash(dashed ? [10, 8] : []);
      const ex = x1 - Math.cos(ang) * (head ? width * 1.6 : 0), ey = y1 - Math.sin(ang) * (head ? width * 1.6 : 0);
      // dark outline first so the arrow reads over busy historical maps
      ctx.strokeStyle = 'rgba(0, 0, 0, 0.45)';
      ctx.lineWidth = width + 4;
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(ex, ey);
      ctx.stroke();
      ctx.strokeStyle = color;
      ctx.fillStyle = color;
      ctx.lineWidth = width;
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(ex, ey);
      ctx.stroke();
      if (head) {
        const hs = width * 2.6;
        ctx.setLineDash([]);
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x1 - Math.cos(ang - 0.45) * hs, y1 - Math.sin(ang - 0.45) * hs);
        ctx.lineTo(x1 - Math.cos(ang + 0.45) * hs, y1 - Math.sin(ang + 0.45) * hs);
        ctx.closePath();
        ctx.fill();
      }
      ctx.restore();
    }

    function drawMovementArrows(ctx, b, p, W, H) {
      const units = (b.tactical_zoom && b.tactical_zoom.formations) || [];
      const moveT = Math.min(1, p * 1.15); // same pace as the formation banners
      units.forEach(u => {
        const { x0, y0, x1, y1 } = formationPath(u, W, H);
        const rgb = u.side === 'A' ? '79, 143, 232' : '229, 83, 75';
        drawArrow(ctx, x0, y0, x1, y1, `rgba(${rgb}, 0.5)`, 7, true, true);
        const cx = x0 + (x1 - x0) * moveT, cy = y0 + (y1 - y0) * moveT;
        drawArrow(ctx, x0, y0, cx, cy, `rgba(${rgb}, 0.9)`, 7, false, moveT > 0.04);
      });
    }

    function toggleSimKeys(open) {
      const box = document.getElementById('sim-keys');
      const btn = document.getElementById('sim-keys-btn');
      if (!box || !btn) return;
      const show = open === undefined ? box.classList.contains('hidden') : open;
      box.classList.toggle('hidden', !show);
      btn.setAttribute('aria-expanded', show ? 'true' : 'false');
    }

    function jumpToPhase(delta) {
      const b = BATTLE_MAP[state.selectedBattleId] || BATTLES[0];
      const phases = b.phases || [];
      if (!phases.length) return;
      const n = phases.length;
      const starts = phases.map((ph, i) => (ph.range && typeof ph.range[0] === 'number') ? ph.range[0] : i / n);
      let cur = 0;
      starts.forEach((r0, i) => { if (state.sim.progress >= r0) cur = i; });
      const target = Math.max(0, Math.min(n - 1, cur + delta));
      setBattleSimProgress(starts[target] * 100 + 0.1);
      if (state.sim.status === 'ready') setSimStatus('paused');
      announce(`Phase ${target + 1} of ${n}: ${phases[target].title || ''}`);
    }

    // Battle shortcuts. Space and arrows are left alone on buttons, links and form fields,
    // which have their own keyboard behaviour (and on the scrubber, which uses the arrows).
    document.addEventListener('keydown', (e) => {
      if (state.mainView !== 'battle-page' || e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target;
      const inField = t.closest && t.closest('input, select, textarea, [contenteditable="true"]');
      const onControl = t.closest && t.closest('button, a, [role="tab"]');
      if (e.key === 'Escape') { toggleSimKeys(false); return; }
      if (inField) return;
      if (e.key === '?') { e.preventDefault(); toggleSimKeys(); return; }
      if (onControl) return;
      if (e.key === ' ') {
        e.preventDefault();
        if (state.sim.status === 'ready' || (state.sim.status === 'paused' && state.sim.phaseCard != null)) setSimStatus('playing');
        else toggleSimPlay();
      } else if (e.key === 'ArrowRight') { e.preventDefault(); jumpToPhase(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); jumpToPhase(-1); }
    });
    document.addEventListener('click', (e) => {
      if (!e.target.closest('#sim-keys, #sim-keys-btn')) toggleSimKeys(false);
    });

    // Screen-reader announcer: at most one message every 3s; knock-outs in between are summarized
    const announcer = { phase: null, kills: [], last: 0, timer: null };
    function announce(text) {
      announcer.phase = text;
      scheduleAnnounce();
    }
    function announceKill(text) {
      announcer.kills.push(text);
      scheduleAnnounce();
    }
    function scheduleAnnounce() {
      if (announcer.timer) return;
      const wait = Math.max(0, 3000 - (performance.now() - announcer.last));
      announcer.timer = setTimeout(flushAnnounce, wait);
    }
    function flushAnnounce() {
      announcer.timer = null;
      const el = document.getElementById('sim-announcer');
      if (!el || state.mainView !== 'battle-page') { announcer.phase = null; announcer.kills = []; return; }
      const parts = [];
      if (announcer.phase) parts.push(announcer.phase);
      if (announcer.kills.length === 1) parts.push(announcer.kills[0]);
      else if (announcer.kills.length > 1) { const more = announcer.kills.length - 1; parts.push(`${announcer.kills[0]}, and ${more} more ${more === 1 ? 'tank' : 'tanks'} knocked out`); }
      announcer.phase = null;
      announcer.kills = [];
      if (!parts.length) return;
      el.textContent = parts.join('. ');
      announcer.last = performance.now();
    }

    function stripEmoji(text) {
      return String(text || '').replace(/[\u{1F000}-\u{1FFFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{FE0F}]/gu, '').replace(/\s+/g, ' ').trim();
    }

    // Knock-outs are announced once, when progress first passes killAt (reset on replay or rewind)
    const killCallouts = { seen: new Map(), lastP: 0, battleId: null };
    function drawKillCallouts(ctx, W, p) {
      const now = performance.now();
      if (killCallouts.battleId !== state.selectedBattleId || p < killCallouts.lastP - 0.01) {
        killCallouts.seen.clear();
        killCallouts.battleId = state.selectedBattleId;
        // units already knocked out at the starting point are not news
        simScreenAgents.forEach(a => { if (a.isWreck) killCallouts.seen.set(a.id, -Infinity); });
      }
      killCallouts.lastP = p;
      simScreenAgents.forEach(a => {
        if (a.isWreck && !killCallouts.seen.has(a.id)) {
          killCallouts.seen.set(a.id, now);
          if (state.sim.playing) {
            const cause = stripEmoji(a.killCause).replace(/\s*\(.*\)\s*$/, '');
            announceKill(`${stripEmoji(a.label)} knocked out${cause ? ': ' + cause : ''}`);
          }
        }
      });
      const live = simScreenAgents
        .filter(a => a.isWreck && now - killCallouts.seen.get(a.id) < 2000)
        .sort((a, b) => killCallouts.seen.get(b.id) - killCallouts.seen.get(a.id))
        .slice(0, 3);
      ctx.save();
      ctx.font = '600 13px "IBM Plex Sans", sans-serif';
      ctx.textAlign = 'left';
      live.forEach((a, i) => {
        const age = now - killCallouts.seen.get(a.id);
        const cause = stripEmoji(a.killCause).replace(/\s*\(.*\)\s*$/, '');
        const text = `${stripEmoji(a.label)} knocked out${cause ? ': ' + cause : ''}`.slice(0, 60);
        const tw = ctx.measureText(text).width;
        const x = 12, y = 12 + i * 30;
        ctx.globalAlpha = age > 1500 ? (2000 - age) / 500 : 1;
        ctx.fillStyle = 'rgba(17, 22, 17, 0.9)';
        ctx.beginPath();
        ctx.roundRect(x, y, tw + 20, 24, 6);
        ctx.fill();
        ctx.fillStyle = a.side === 'A' ? '#4f8fe8' : '#e5534b';
        ctx.fillRect(x, y + 4, 3, 16);
        ctx.fillStyle = '#ecefe6';
        ctx.fillText(text, x + 12, y + 16.5);
      });
      ctx.restore();
      killCallouts.live = live.map(a => a.id);
    }

    function hitTestSimAgent(canvas, e, radius) {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;
      for (let i = simScreenAgents.length - 1; i >= 0; i--) {
        const a = simScreenAgents[i];
        if (Math.hypot(mx - a.x, my - a.y) <= radius) return a;
      }
      return null;
    }

    // Clicking a unit pauses the battle, rings the unit and shows its tank card in the story panel.
    // Back to story, Play or Esc restores the panel and resumes only if the battle was playing.
    function selectSimUnit(agentId) {
      const agent = simScreenAgents.find(a => a.id === agentId);
      if (!agent) return;
      if (state.sim.selectedAgentId == null) state.sim.statusBeforeSelect = state.sim.status;
      state.sim.selectedAgentId = agentId;
      if (state.sim.status === 'playing') setSimStatus('paused');
      renderSimUnitCard(agent);
    }

    function clearSimUnit(resume = true) {
      if (state.sim.selectedAgentId == null) return;
      state.sim.selectedAgentId = null;
      document.getElementById('sim-unit-card')?.classList.add('hidden');
      document.getElementById('sim-story')?.classList.remove('hidden');
      if (resume && state.sim.statusBeforeSelect === 'playing') setSimStatus('playing');
      state.sim.statusBeforeSelect = null;
    }

    function renderSimUnitCard(agent) {
      const card = document.getElementById('sim-unit-card');
      const t = TANK_MAP[agent.tankId];
      if (!card || !t) return;
      const status = agent.isWreck
        ? `Knocked out at ${Math.round(agent.killAt * 100)}% of the battle${agent.killCause ? ': ' + stripEmoji(agent.killCause) : ''}`
        : 'In action';
      card.innerHTML = `
        <button onclick="clearSimUnit()" class="self-start h-10 px-2 -ml-2 rounded-md text-sm font-semibold text-[var(--muted-foreground)] hover:text-[var(--foreground)] flex items-center gap-1">
          <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
          Back to story
        </button>
        <div class="aspect-[4/3] w-full rounded-md overflow-hidden bg-[var(--surface-raised)] border border-[var(--border)]">
          <img src="${t.photo_url || t.image_url || ''}" alt="${t.name}" class="w-full h-full object-cover" />
        </div>
        <div>
          <div class="text-xs font-semibold uppercase tracking-wide ${agent.side === 'A' ? 'text-sky-400' : 'text-rose-400'}">${agent.side === 'A' ? 'Side A' : 'Side B'}</div>
          <h3 class="text-lg font-semibold text-[var(--foreground)] leading-snug">${t.name} (${t.year})</h3>
          <div class="text-sm text-[var(--muted-foreground)]">${t.role || ''}</div>
        </div>
        <dl class="grid grid-cols-2 gap-x-3 gap-y-1 text-sm">
          <dt class="text-[var(--muted-foreground)]">Gun</dt><dd class="text-[var(--foreground)]">${t.gun}</dd>
          <dt class="text-[var(--muted-foreground)]">Armor</dt><dd class="text-[var(--foreground)] tabular-nums">${t.armor_mm} mm</dd>
          <dt class="text-[var(--muted-foreground)]">Weight</dt><dd class="text-[var(--foreground)] tabular-nums">${t.weight_t} t</dd>
          <dt class="text-[var(--muted-foreground)]">Status</dt><dd class="${agent.isWreck ? 'text-rose-400' : 'text-[var(--foreground)]'}">${status}</dd>
        </dl>
        <button onclick="openTankPage('${t.id}')" class="h-11 px-4 rounded-md bg-amber-500 hover:bg-amber-400 text-slate-950 text-sm font-semibold">Open tank page</button>`;
      document.getElementById('sim-story')?.classList.add('hidden');
      card.classList.remove('hidden');
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && state.mainView === 'battle-page') clearSimUnit();
    });

    function drawBattleSimCanvas() {
      const canvas = document.getElementById('battle-sim-canvas');
      if (!canvas || state.mainView !== 'battle-page') return;
      setupSimCanvas();

      const b = BATTLE_MAP[state.selectedBattleId] || BATTLES[0];
      if (simBattleCache.battleId !== b.id) {
        simBattleCache.battleId = b.id;
        simBattleCache.agents = buildBattleAgents(b);
      }

      // Advance simulation progress if playing
      if (state.sim.playing) {
        const prevP = state.sim.progress;
        state.sim.progress += 0.0010 * state.sim.speed;
        const stop = state.sim.stopAtPhases !== false ? phaseStartCrossed(b, prevP, state.sim.progress) : null;
        if (stop) {
          state.sim.progress = stop.r0 + 0.001; // just inside the new phase, so the panel and notch agree with the card
          state.sim.phaseCard = stop.idx;
          setSimStatus('paused');
        } else if (state.sim.progress >= 1.0) {
          state.sim.progress = 1.0;
          setSimStatus('ended');
        }
        const scrub = document.getElementById('sim-scrubber');
        if (scrub) scrub.value = state.sim.progress.toFixed(3);
      }

      const p = state.sim.progress;

      // Determine Active Historical Phase from b.phases (5 Phases!)
      const phases = b.phases || [];
      const nPh = Math.max(1, phases.length);
      // Current phase = the last phase that has started (a boundary belongs to the phase it opens)
      let phaseIdx = 0;
      for (let i = 0; i < phases.length; i++) {
        const r0 = (phases[i].range && typeof phases[i].range[0] === 'number') ? phases[i].range[0] : (i / nPh);
        if (p >= r0) phaseIdx = i;
      }
      const rawPhase = phases[phaseIdx] || {};
      const curPhase = {
        phase: typeof rawPhase.phase === 'number' ? `Phase ${rawPhase.phase}` : (rawPhase.phase || `Phase ${phaseIdx + 1}`),
        time: rawPhase.time || b.date,
        title: rawPhase.title || b.name,
        desc: rawPhase.desc || b.summary,
        losses_note: rawPhase.losses_note || rawPhase.focus_event || `${b.losses_a} vs ${b.losses_b}`
      };

      const timeEl = document.getElementById('sim-time-readout');
      if (timeEl) timeEl.textContent = curPhase.time;
      const phaseEl = document.getElementById('sim-phase-label');
      if (phaseEl) phaseEl.textContent = `${curPhase.phase} of ${nPh}${rawPhase.night ? ' · Night' : ''}`;

      const bTitle = document.getElementById('sim-banner-title');
      const bDesc = document.getElementById('sim-banner-desc');
      const bLoss = document.getElementById('sim-banner-losses');
      if (bTitle) bTitle.textContent = curPhase.title;
      if (bDesc) bDesc.textContent = curPhase.desc;
      if (bLoss) bLoss.textContent = curPhase.losses_note;

      // Highlight the active phase notch on the scrubber
      for (let i = 0; i < phases.length; i++) {
        const notch = document.getElementById('sim-notch-' + i);
        if (notch) notch.setAttribute('aria-current', i === phaseIdx ? 'step' : 'false');
      }

      // Compute Live Tank Counts & Destroyed Counts scaled to b.side_a_num / b.side_b_num
      const agents = simBattleCache.agents;
      const agentsA = agents.filter(a => a.side === 'A');
      const agentsB = agents.filter(a => a.side === 'B');
      const deadAgentsA = agentsA.filter(a => p >= a.killAt).length;
      const deadAgentsB = agentsB.filter(a => p >= a.killAt).length;

      const totalNumA = b.side_a_num || 749;
      const totalNumB = b.side_b_num || 245;
      const maxLossNumA = b.loss_a_num || Math.round(totalNumA * 0.7);
      const maxLossNumB = b.loss_b_num || Math.round(totalNumB * 0.3);

      const curLostA = Math.min(maxLossNumA, Math.round((deadAgentsA / Math.max(1, agentsA.length)) * totalNumA));
      const curLostB = Math.min(maxLossNumB, Math.round((deadAgentsB / Math.max(1, agentsB.length)) * totalNumB));
      const curActiveA = Math.max(0, totalNumA - curLostA);
      const curActiveB = Math.max(0, totalNumB - curLostB);

      const curIntA = Math.max(4, Math.round((curActiveA / Math.max(1, totalNumA)) * 100));
      const curIntB = Math.max(4, Math.round((curActiveB / Math.max(1, totalNumB)) * 100));

      const barA = document.getElementById('sim-bar-a');
      const pctA = document.getElementById('sim-pct-a');
      const barB = document.getElementById('sim-bar-b');
      const pctB = document.getElementById('sim-pct-b');
      const cntA = document.getElementById('sim-count-a');
      const lstA = document.getElementById('sim-lost-a');
      const cntB = document.getElementById('sim-count-b');
      const lstB = document.getElementById('sim-lost-b');
      if (barA) barA.style.width = curIntA + '%';
      if (pctA) pctA.textContent = curIntA + '%';
      if (barB) barB.style.width = curIntB + '%';
      if (pctB) pctB.textContent = curIntB + '%';
      if (cntA) cntA.textContent = curActiveA.toLocaleString();
      if (lstA) lstA.textContent = curLostA.toLocaleString();
      if (cntB) cntB.textContent = curActiveB.toLocaleString();
      if (lstB) lstB.textContent = curLostB.toLocaleString();

      // Update Chronological Kill Feed & Phase Log
      if (state.sim.lastPhaseLogged !== phaseIdx) {
        const firstLog = state.sim.lastPhaseLogged === -1;
        state.sim.lastPhaseLogged = phaseIdx;
        canvas.setAttribute('aria-label', `${b.name}: battlefield, ${curPhase.phase} of ${nPh}${rawPhase.night ? ', at night' : ''}. ${curPhase.title}`);
        if (!firstLog && state.sim.playing) announce(`${curPhase.phase} of ${nPh}: ${curPhase.title}`);
        const logEl = document.getElementById('sim-telemetry-log');
        if (logEl && phases.length) {
          logEl.innerHTML = phases.slice(0, phaseIdx + 1).reverse().map((ph, idx) => `
            <div class="p-2.5 rounded-lg bg-slate-950 border ${idx === 0 ? 'border-amber-400 text-amber-100 shadow' : 'border-slate-800 text-slate-300'} flex flex-col gap-1">
              <div class="flex items-center justify-between text-xs font-bold ${idx === 0 ? 'text-amber-300' : 'text-slate-400'}">
                <span>${ph.phase} • ${ph.time}</span>
              </div>
              <div class="text-xs font-extrabold text-white">${ph.title}</div>
              <div class="text-xs leading-snug text-slate-300">${ph.desc}</div>
              <div class="text-xs font-bold text-rose-300 pt-1 border-t border-slate-800/80">${ph.losses_note}</div>
            </div>
          `).join('');
        }
      }

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

      const isRaseiniai = b.id === 'raseiniai_1941';
      const terr = (b.tactical_zoom.terrain || '').toLowerCase();
      ctx.clearRect(0, 0, W, H);
      if (state.sim.mapBgMode === 'tactical') {
        if (terr.includes('desert') || terr.includes('sand') || terr.includes('wadi') || terr.includes('sinai')) {
          ctx.fillStyle = '#1c160d';
        } else if (terr.includes('jungle') || terr.includes('vietnam') || terr.includes('rubber') || terr.includes('rice')) {
          ctx.fillStyle = '#071c15';
        } else if (terr.includes('snow') || terr.includes('ardennes') || terr.includes('winter')) {
          ctx.fillStyle = '#0f1b2d';
        } else {
          ctx.fillStyle = '#081520';
        }
        ctx.fillRect(0, 0, W, H);
      } else {
        // Subtle contrast vignette over Real Historical Operational Map / Real Leaflet Topographic Map
        ctx.fillStyle = 'rgba(2, 6, 23, 0.22)';
        ctx.fillRect(0, 0, W, H);
      }

      // Tactical 1km Grid
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.10)';
      ctx.lineWidth = 1;
      for (let x = 0; x < W; x += 55) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
      }
      for (let y = 0; y < H; y += 55) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
      }

      // Authentic Geographic Landmarks (Especially Dubysa River, Crossroads, Raseiniai Town & Kelmė Flank for Raseiniai 1941)
      if (isRaseiniai) {
        // Dubysa River meandering north-to-south at ~28% width
        ctx.save();
        ctx.strokeStyle = 'rgba(14, 165, 233, 0.45)';
        ctx.lineWidth = 14;
        ctx.beginPath();
        ctx.moveTo(W * 0.27, 0);
        ctx.bezierCurveTo(W * 0.31, H * 0.33, W * 0.24, H * 0.66, W * 0.29, H);
        ctx.stroke();
        ctx.fillStyle = '#38bdf8';
        ctx.font = 'bold 10px monospace';
        ctx.fillText('Dubysa River bridgeheads', W * 0.14, H * 0.10);

        // Raseiniai Forest & Pocket Zone
        ctx.fillStyle = 'rgba(16, 185, 129, 0.08)';
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.35)';
        ctx.setLineDash([5, 4]);
        ctx.beginPath();
        ctx.ellipse(W * 0.54, H * 0.46, W * 0.20, H * 0.30, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#6ee7b7';
        ctx.font = 'bold 10.5px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('Raseiniai town and forest pocket', W * 0.54, H * 0.14);

        // Northern Crossroads (Lone KV-1/KV-2 26-Hour Stand)
        ctx.fillStyle = 'rgba(251, 191, 36, 0.16)';
        ctx.strokeStyle = '#fbbf24';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(W * 0.35, H * 0.22, 26, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = '#fde68a';
        ctx.font = 'bold 10px Inter, sans-serif';
        ctx.fillText('Lone KV crossroads', W * 0.35, H * 0.22 - 32);

        // Southern Kelmė Flank Hook Arrow (1st Panzer Division encirclement)
        if (p >= 0.45) {
          ctx.strokeStyle = 'rgba(244, 63, 94, 0.55)';
          ctx.lineWidth = 3;
          ctx.setLineDash([7, 4]);
          ctx.beginPath();
          ctx.moveTo(W * 0.25, H * 0.84);
          ctx.quadraticCurveTo(W * 0.55, H * 0.92, W * 0.74, H * 0.56);
          ctx.stroke();
          ctx.setLineDash([]);
          ctx.fillStyle = '#fda4af';
          ctx.font = 'bold 10px Inter, sans-serif';
          ctx.fillText('1st Panzer flank hook from Kelmė', W * 0.52, H * 0.91);
        }
        ctx.restore();
      } else {
        // Topographic Contours for other battles
        ctx.strokeStyle = 'rgba(251, 191, 36, 0.14)';
        ctx.lineWidth = 1.4;
        [0.26, 0.52, 0.76].forEach((cxRatio, idx) => {
          ctx.beginPath();
          ctx.ellipse(W * cxRatio, H * (0.32 + (idx % 2) * 0.34), 115, 55, 0.25 * idx, 0, Math.PI * 2);
          ctx.stroke();
        });
      }

      // Movement arrows: each formation's planned route (faint, dashed) and the part covered so far (solid)
      drawMovementArrows(ctx, b, p, W, H);

      // Night phases: darken the battlefield under the units
      if (rawPhase.night) {
        ctx.fillStyle = 'rgba(4, 8, 24, 0.5)';
        ctx.fillRect(0, 0, W, H);
      }

      // Compute Current Agent Screen Coordinates & Status
      simScreenAgents = [];
      const activeA = [];
      const activeB = [];

      agents.forEach(a => {
        const isWreck = p >= a.killAt;
        const effectiveP = isWreck ? a.killAt : p;
        const moveT = Math.min(1, effectiveP * 1.25);

        const startX = (a.sx / 100) * W;
        const startY = (a.sy / 100) * H;
        const endX = (a.tx / 100) * W;
        const endY = (a.ty / 100) * H;

        // Slight tactical weave for living tanks
        const wobble = isWreck ? 0 : Math.sin(state.animTick * 0.05 + a.sx) * 2.2;
        const x = startX + (endX - startX) * moveT;
        const y = startY + (endY - startY) * moveT + wobble;
        const angle = Math.atan2(endY - startY, endX - startX);

        // Heavy tanks (KV-1/KV-2, Tiger, etc.) show ricochet sparks during Phase 2 & 3!
        const isRicochet = !isWreck && a.isHeavy && p >= 0.18 && p <= 0.62 && ((state.animTick + Math.floor(a.sx * 7)) % 45 < 18);

        const entry = { ...a, x, y, angle, isWreck, isRicochet };
        simScreenAgents.push(entry);
        if (!isWreck) {
          if (a.side === 'A') activeA.push(entry);
          else activeB.push(entry);
        }
      });

      // Draw Ballistic AP/HEAT/88mm Salvos & Ricochet Deflections between Active Platoons
      if (p >= 0.10 && activeA.length && activeB.length) {
        const pairs = Math.min(18, Math.max(activeA.length, activeB.length));
        for (let i = 0; i < pairs; i++) {
          const ua = activeA[i % activeA.length];
          const ub = activeB[(i * 3) % activeB.length];

          // Shell B -> A (e.g., German 37mm/50mm/88mm firing at Soviet KV-1/BT-7/T-26)
          const tShotB = ((state.animTick * 0.032 + i * 0.29) % 1);
          const sxB = ub.x + (ua.x - ub.x) * tShotB;
          const syB = ub.y + (ua.y - ub.y) * tShotB;
          ctx.fillStyle = ua.isLoneKV && p > 0.45 ? '#fde047' : '#fb7185';
          ctx.beginPath();
          ctx.arc(sxB, syB, ua.isLoneKV ? 3.6 : 2.6, 0, Math.PI * 2);
          ctx.fill();

          // If hitting a Heavy KV tank, draw deflecting ricochet vector!
          if (ua.isHeavy && tShotB > 0.85) {
            ctx.strokeStyle = '#fde047';
            ctx.lineWidth = 1.8;
            ctx.beginPath();
            ctx.moveTo(ua.x, ua.y);
            ctx.lineTo(ua.x - 18, ua.y - 16 * (i % 2 === 0 ? 1 : -1));
            ctx.stroke();
          }

          // Shell A -> B (e.g., Soviet 76.2mm / 45mm firing at German Pz.38(t) / Pz.IV)
          if (i % 2 === 0) {
            const tShotA = ((state.animTick * 0.028 + i * 0.41 + 0.4) % 1);
            const sxA = ua.x + (ub.x - ua.x) * tShotA;
            const syA = ua.y + (ub.y - ua.y) * tShotA;
            ctx.fillStyle = '#38bdf8';
            ctx.beginPath();
            ctx.arc(sxA, syA, 2.8, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }

      // Draw All 70+ Articulated Tank Platoon Agents (Wrecks first so live tanks maneuver over/around them)
      const sortedAgents = [...simScreenAgents].sort((a, b) => (a.isWreck === b.isWreck ? 0 : (a.isWreck ? -1 : 1)));
      sortedAgents.forEach((ag, idx) => {
        const color = ag.side === 'A' ? '#38bdf8' : '#f43f5e';
        const isSel = state.sim.selectedAgentId === ag.id;
        const isHov = (hoveredSimAgent && hoveredSimAgent.id === ag.id) || isSel;

        if (state.sim.showHulls || ag.isLoneKV || isHov) {
          drawArticulatedTankAgent(ctx, ag.x, ag.y, ag.angle, color, ag, ag.isWreck, ag.isRicochet, isHov, p);
        }
        if (isSel) {
          ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#f2a93b';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.arc(ag.x, ag.y, 22, 0, Math.PI * 2);
          ctx.stroke();
        }

        // Units are unlabeled counters; only the hovered or selected unit gets its name
        if (isHov) {
          ctx.font = '600 12px "IBM Plex Sans", sans-serif';
          ctx.textAlign = 'center';
          ctx.fillStyle = ag.isWreck ? '#fca5a5' : '#ffffff';
          ctx.fillText(stripEmoji(ag.label), ag.x, ag.y + 30);
        }
      });

      // Draw Command Echelon Formation Banners from b.tactical_zoom.formations
      const units = b.tactical_zoom.formations || [];
      units.forEach(u => {
        const startX = (u.x / 100) * W;
        const startY = (u.y / 100) * H;
        const endX = ((u.tx ?? (u.side === 'A' ? u.x + 14 : u.x - 14)) / 100) * W;
        const endY = ((u.ty ?? u.y) / 100) * H;
        const moveT = Math.min(1, p * 1.15);
        const cx = startX + (endX - startX) * moveT;
        const cy = startY + (endY - startY) * moveT;
        const isA = u.side === 'A';
        const color = isA ? '#38bdf8' : '#f43f5e';

        ctx.font = '600 12px "IBM Plex Sans", sans-serif';
        const label = u.label.length > 28 ? u.label.slice(0, 27) + '…' : u.label;
        const tw = ctx.measureText(label).width;
        ctx.fillStyle = 'rgba(2, 6, 23, 0.88)';
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.3;
        ctx.beginPath();
        ctx.roundRect(cx - tw / 2 - 7, cy - 28, tw + 14, 18, 4);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.fillText(label, cx, cy - 15.5);
      });

      // Kill callouts: one short line per knock-out, fades after 2s, at most 3 on screen
      drawKillCallouts(ctx, W, p);

      // Hovered Tank Agent Tooltip on Battlefield Canvas
      if (hoveredSimAgent && hoveredSimAgent.id !== state.sim.selectedAgentId) {
        const t = TANK_MAP[hoveredSimAgent.tankId];
        const statusTxt = hoveredSimAgent.isWreck
          ? `Knocked out: ${stripEmoji(hoveredSimAgent.killCause)}`
          : `In action${t ? ', ' + t.gun : ''}`;
        const tipW = 290;
        const tipH = 52;
        const tx = Math.min(W - tipW - 10, Math.max(10, hoveredSimAgent.x - tipW / 2));
        const ty = Math.max(10, hoveredSimAgent.y - 66);
        ctx.fillStyle = 'rgba(15, 23, 42, 0.96)';
        ctx.strokeStyle = '#fbbf24';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.roundRect(tx, ty, tipW, tipH, 6);
        ctx.fill();
        ctx.stroke();

        ctx.textAlign = 'left';
        ctx.font = '600 13px "IBM Plex Sans", sans-serif';
        ctx.fillStyle = '#ffffff';
        ctx.fillText(t ? t.name : stripEmoji(hoveredSimAgent.label), tx + 8, ty + 19);
        ctx.font = '12px "IBM Plex Sans", sans-serif';
        ctx.fillStyle = hoveredSimAgent.isWreck ? '#fca5a5' : '#c4cbbb';
        ctx.fillText(statusTxt.slice(0, 46), tx + 8, ty + 35);
        ctx.fillStyle = '#a9b2a0';
        ctx.fillText('Click for details', tx + 8, ty + 48);
      }

      ctx.restore();
    }

    // INTERACTIVE BALLISTIC X-RAY PENETRATION & AMMO COOK-OFF / TURRET BLOW-OFF KILL-CAM
    function drawKillCamCanvas() {
      const canvas = document.getElementById('killcam-canvas');
      if (!canvas || state.mainView !== 'battle-page') return;
      const b = BATTLE_MAP[state.selectedBattleId] || BATTLES[0];
      const scenarios = b.killcam_scenarios || [];
      if (!scenarios.length) return;
      const sc = scenarios[state.sim.killcamIdx || 0] || scenarios[0];

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

      // Dark X-Ray Ballistics Lab Background
      ctx.fillStyle = '#050b14';
      ctx.fillRect(0, 0, W, H);
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.08)';
      for (let x = 0; x < W; x += 32) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
      for (let y = 0; y < H; y += 32) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }

      state.sim.killcamTick = (state.sim.killcamTick || 0) + 1;
      const cycle = (state.sim.killcamTick % 190) / 190; // 0.0 to 1.0 repeating cycle
      const impactT = 0.42;
      const isRicochet = (sc.result || '').includes('RICOCHET');

      const atkTank = TANK_MAP[sc.attacker_id] || TANK_MAP[sc.attacker] || TANK_MAP[(b.side_b.tanks && b.side_b.tanks[0])] || TANKS[0];
      const defTank = TANK_MAP[sc.defender_id] || TANK_MAP[sc.defender] || TANK_MAP[(b.side_a.tanks && b.side_a.tanks[0])] || TANKS[1];
      const atkImg = getTankImg(atkTank.id);
      const defImg = getTankImg(defTank.id);

      // Ground Line
      const groundY = H - 36;
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(15, groundY);
      ctx.lineTo(W - 15, groundY);
      ctx.stroke();

      // 1. LEFT SIDE: ATTACKER TANK & REAL PHOTOGRAPH
      const atkX = 88;
      const atkY = groundY - 40;
      if (atkImg) {
        ctx.save();
        ctx.beginPath();
        ctx.roundRect(atkX - 58, atkY - 38, 116, 70, 6);
        ctx.clip();
        ctx.drawImage(atkImg, atkX - 58, atkY - 38, 116, 70);
        ctx.restore();
      }
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2;
      ctx.strokeRect(atkX - 58, atkY - 38, 116, 70);

      // Gun Barrel extending right from Attacker
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(atkX + 58, atkY - 6);
      ctx.lineTo(atkX + 95, atkY - 6);
      ctx.stroke();

      // Muzzle Flash at start of shot
      if (cycle < 0.12) {
        ctx.fillStyle = '#fde047';
        ctx.beginPath();
        ctx.arc(atkX + 98, atkY - 6, 12 * (1 - cycle * 6), 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.fillStyle = '#bae6fd';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`🎯 ${atkTank.name.slice(0, 22)}`, atkX, groundY + 16);
      ctx.fillStyle = '#94a3b8';
      ctx.font = '10px monospace';
      ctx.fillText(`${sc.shell} (${sc.pen_mm}mm Pen)`, atkX + 12, groundY + 29);

      // 2. RIGHT SIDE: DEFENDER TANK X-RAY CROSS-SECTION (ARMOR PLATE + AMMO RACK + FUEL + TURRET)
      const defX = W - 155;
      const hullY = groundY - 68;
      const hullW = 138;
      const hullH = 62;

      const postImpact = Math.max(0, (cycle - impactT) / (1 - impactT)); // 0 -> 1 after impact

      // Defender Hull Cross-Section Box
      ctx.fillStyle = 'rgba(15, 23, 42, 0.92)';
      ctx.strokeStyle = isRicochet ? '#38bdf8' : (postImpact > 0 ? '#ef4444' : '#94a3b8');
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.roundRect(defX, hullY, hullW, hullH, 5);
      ctx.fill();
      ctx.stroke();

      // Defender Real Photo Watermark inside Hull
      if (defImg) {
        ctx.save();
        ctx.globalAlpha = 0.25;
        ctx.drawImage(defImg, defX + 4, hullY + 4, hullW - 8, hullH - 8);
        ctx.restore();
      }

      // Sloped / Thick Frontal Armor Plate (Left wall of Defender)
      const plateThick = Math.max(6, Math.min(20, (sc.armor_mm || 50) / 7));
      ctx.fillStyle = isRicochet ? '#fde047' : '#cbd5e1';
      ctx.fillRect(defX - plateThick / 2, hullY - 2, plateThick, hullH + 4);
      ctx.fillStyle = '#fde047';
      ctx.font = 'bold 10px monospace';
      ctx.textAlign = 'right';
      ctx.fillText(`${sc.armor_mm}mm ARMOR`, defX - 10, hullY + 14);

      // Internal Modules: Ammo Rack & Fuel Tank
      const ammoBlown = !isRicochet && postImpact > 0.08;
      ctx.fillStyle = ammoBlown ? '#dc2626' : '#f59e0b';
      ctx.fillRect(defX + 26, hullY + 26, 42, 26);
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 8.5px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('AMMO RACK', defX + 47, hullY + 42);

      ctx.fillStyle = ammoBlown ? '#ea580c' : '#0284c7';
      ctx.fillRect(defX + 78, hullY + 26, 46, 26);
      ctx.fillStyle = '#ffffff';
      ctx.fillText('FUEL/ENG', defX + 101, hullY + 42);

      // Defender Turret (Flies into the air if sc.turret_blow && postImpact > 0.1!)
      let turOffsetX = 0;
      let turOffsetY = 0;
      let turRot = 0;
      if (!isRicochet && sc.turret_blow && postImpact > 0.08) {
        const tp = Math.min(1, (postImpact - 0.08) * 1.3);
        turOffsetX = tp * 28;
        turOffsetY = -Math.sin(tp * Math.PI * 0.85) * 72 - tp * 18;
        turRot = tp * 4.2;
      }

      ctx.save();
      ctx.translate(defX + 62 + turOffsetX, hullY - 18 + turOffsetY);
      ctx.rotate(turRot);
      ctx.fillStyle = '#1e293b';
      ctx.strokeStyle = ammoBlown ? '#f97316' : '#cbd5e1';
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      ctx.roundRect(-38, -16, 76, 32, 6);
      ctx.fill();
      ctx.stroke();
      // Defender gun pointing left
      ctx.beginPath();
      ctx.moveTo(-38, -2);
      ctx.lineTo(-76, -2);
      ctx.stroke();
      ctx.fillStyle = '#e2e8f0';
      ctx.font = 'bold 9px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(defTank.name.slice(0, 14), 0, 4);
      ctx.restore();

      ctx.fillStyle = '#fecdd3';
      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`🛡️ ${defTank.name.slice(0, 24)}`, defX + hullW / 2, groundY + 16);
      ctx.fillStyle = '#94a3b8';
      ctx.font = '10px monospace';
      ctx.fillText(`Armor: ${sc.armor_mm}mm RHAe`, defX + hullW / 2, groundY + 29);

      // 3. ANIMATED PROJECTILE FLIGHT + PENETRATION SPALL CONE / RICOCHET + COOK-OFF FIREBALL
      const startShotX = atkX + 98;
      const startShotY = atkY - 6;
      const hitX = defX;
      const hitY = hullY + 34;

      if (cycle <= impactT) {
        const st = cycle / impactT;
        const sx = startShotX + (hitX - startShotX) * st;
        const sy = startShotY + (hitY - startShotY) * st;

        // Tracer Trail
        ctx.strokeStyle = '#fde047';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(Math.max(startShotX, sx - 45), startShotY + (hitY - startShotY) * Math.max(0, st - 0.18));
        ctx.lineTo(sx, sy);
        ctx.stroke();

        // Glowing AP/HEAT Projectile Nose
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(sx, sy, 5, 0, Math.PI * 2);
        ctx.fill();
      } else {
        // Post-Impact Effect!
        if (isRicochet) {
          // RICOCHET: Shell deflects skyward off the thick armor!
          const rt = postImpact;
          const rx = hitX - rt * 70;
          const ry = hitY - rt * 115;
          ctx.strokeStyle = '#fde047';
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.moveTo(hitX, hitY);
          ctx.lineTo(rx, ry);
          ctx.stroke();

          ctx.fillStyle = '#fde047';
          ctx.beginPath();
          ctx.arc(hitX, hitY, 12 * (1 - rt * 0.6), 0, Math.PI * 2);
          ctx.fill();

          ctx.fillStyle = '#fde047';
          ctx.font = 'bold 13px Inter, sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText(`⚡ SHELL RICOCHET! (${sc.pen_mm}mm Pen < ${sc.armor_mm}mm Armor)`, W / 2, 26);
        } else {
          // ARMOR PENETRATION + INTERNAL SPALL CONE + CATASTROPHIC AMMO COOK-OFF!
          // 1. Spall Cone spraying inside crew & ammo compartment
          ctx.save();
          ctx.fillStyle = `rgba(249, 115, 22, ${0.75 - postImpact * 0.45})`;
          ctx.beginPath();
          ctx.moveTo(hitX, hitY);
          ctx.lineTo(hitX + 95, hitY - 26);
          ctx.lineTo(hitX + 95, hitY + 24);
          ctx.closePath();
          ctx.fill();
          ctx.restore();

          // 2. Internal Ammo Rack & Fuel Cook-Off Fireball erupting through turret ring
          const fireRadius = 18 + Math.sin(postImpact * Math.PI) * 52;
          const grad = ctx.createRadialGradient(defX + 55, hullY + 12, 2, defX + 55, hullY + 12, fireRadius);
          grad.addColorStop(0, '#ffffff');
          grad.addColorStop(0.3, '#fde047');
          grad.addColorStop(0.65, '#f97316');
          grad.addColorStop(1, 'rgba(220, 38, 38, 0)');
          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.arc(defX + 55, hullY + 12, fireRadius, 0, Math.PI * 2);
          ctx.fill();

          // 3. Top Forensic Status Callout
          ctx.fillStyle = '#fda4af';
          ctx.font = 'bold 13px Inter, sans-serif';
          ctx.textAlign = 'center';
          const bannerMsg = sc.turret_blow
            ? `💥 PENETRATION (${sc.pen_mm}mm > ${sc.armor_mm}mm) → AMMO COOK-OFF & TURRET BLOW-OFF!`
            : `💥 PENETRATION (${sc.pen_mm}mm > ${sc.armor_mm}mm) → INTERNAL CREW & ENGINE KNOCKOUT!`;
          ctx.fillText(bannerMsg, W / 2, 26);
        }
      }

      ctx.restore();
    }

    function drawTacticalSchematic() {
      const canvas = document.getElementById('tactical-schematic-canvas');
      if (!canvas || !state.tacticalZoomOpen) return;
      const b = BATTLE_MAP[state.selectedBattleId] || BATTLES[0];

      if (simBattleCache.battleId !== b.id) {
        simBattleCache.battleId = b.id;
        simBattleCache.agents = buildBattleAgents(b);
      }

      // Advance simulation progress smoothly while modal is open
      state.sim.progress = ((state.sim.progress || 0) + 0.0012) % 1.0;
      const p = state.sim.progress;

      const titleEl = document.getElementById('tac-overlay-title');
      if (titleEl) titleEl.textContent = `🎬 Live Tactical Battle Simulation: ${b.name} (${b.date}) — ${Math.round(p * 100)}% Timeline`;

      const footerEl = document.getElementById('tac-overlay-footer');
      if (footerEl) {
        footerEl.innerHTML = `
          <div><strong class="text-amber-400">Combat Scale:</strong> ${b.total_tanks} (Range: ${b.tactical_zoom.range_m})</div>
          <div><strong class="text-emerald-400">Winner:</strong> ${b.winner}</div>
          <div class="flex items-center justify-between gap-2">
            <span><strong class="text-sky-400">Key Lesson:</strong> ${b.tactical_zoom.key_lesson}</span>
            <button onclick="toggleTacticalZoomModal(false); openBattlePage('${b.id}')" class="px-2.5 py-1 rounded bg-rose-600 hover:bg-rose-500 text-white text-xs font-extrabold shrink-0">
              🎬 Open Full 5-Phase Sim + X-Ray Kill-Cam →
            </button>
          </div>
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

      ctx.fillStyle = '#071320';
      ctx.fillRect(0, 0, W, H);

      ctx.strokeStyle = 'rgba(45, 212, 191, 0.11)';
      ctx.lineWidth = 1;
      for (let x = 0; x < W; x += 55) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
      }
      for (let y = 0; y < H; y += 55) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
      }

      const agents = simBattleCache.agents || [];
      const activeA = [];
      const activeB = [];
      const rendered = [];

      agents.forEach(a => {
        const isWreck = p >= a.killAt;
        const effectiveP = isWreck ? a.killAt : p;
        const moveT = Math.min(1, effectiveP * 1.25);
        const startX = (a.sx / 100) * W;
        const startY = (a.sy / 100) * H;
        const endX = (a.tx / 100) * W;
        const endY = (a.ty / 100) * H;
        const wobble = isWreck ? 0 : Math.sin(state.animTick * 0.05 + a.sx) * 2.0;
        const x = startX + (endX - startX) * moveT;
        const y = startY + (endY - startY) * moveT + wobble;
        const angle = Math.atan2(endY - startY, endX - startX);
        const isRicochet = !isWreck && a.isHeavy && p >= 0.18 && p <= 0.62 && ((state.animTick + Math.floor(a.sx * 7)) % 45 < 18);
        const entry = { ...a, x, y, angle, isWreck, isRicochet };
        rendered.push(entry);
        if (!isWreck) {
          if (a.side === 'A') activeA.push(entry);
          else activeB.push(entry);
        }
      });

      // Draw Live AP/HEAT Tracer Salvos
      if (p >= 0.08 && activeA.length && activeB.length) {
        const pairs = Math.min(14, Math.max(activeA.length, activeB.length));
        for (let i = 0; i < pairs; i++) {
          const ua = activeA[i % activeA.length];
          const ub = activeB[(i * 3) % activeB.length];
          const tShotB = ((state.animTick * 0.032 + i * 0.29) % 1);
          ctx.fillStyle = '#fb7185';
          ctx.beginPath();
          ctx.arc(ub.x + (ua.x - ub.x) * tShotB, ub.y + (ua.y - ub.y) * tShotB, 2.8, 0, Math.PI * 2);
          ctx.fill();

          if (i % 2 === 0) {
            const tShotA = ((state.animTick * 0.028 + i * 0.41 + 0.4) % 1);
            ctx.fillStyle = '#38bdf8';
            ctx.beginPath();
            ctx.arc(ua.x + (ub.x - ua.x) * tShotA, ua.y + (ub.y - ua.y) * tShotA, 2.8, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }

      // Draw All Articulated Photo-Tank Agents & Explosions
      rendered.forEach((ag, idx) => {
        const color = ag.side === 'A' ? '#38bdf8' : '#f43f5e';
        drawArticulatedTankAgent(ctx, ag.x, ag.y, ag.angle, color, ag, ag.isWreck, ag.isRicochet, false, p);
        if (ag.isLoneKV || idx % 4 === 0) {
          ctx.font = 'bold 8.5px Inter, sans-serif';
          ctx.textAlign = 'center';
          ctx.fillStyle = ag.isLoneKV ? '#fde047' : (ag.isWreck ? '#fca5a5' : '#e2e8f0');
          ctx.fillText(ag.isWreck ? `💥 ${ag.label}` : ag.label, ag.x, ag.y + 15);
        }
      });

      const units = b.tactical_zoom.formations || [];
      units.forEach(u => {
        const ux = ((u.x + ((u.tx ?? u.x) - u.x) * Math.min(1, p * 1.15)) / 100) * W;
        const uy = ((u.y + ((u.ty ?? u.y) - u.y) * Math.min(1, p * 1.15)) / 100) * H;
        const isA = u.side === 'A';
        const color = isA ? '#38bdf8' : '#f43f5e';
        ctx.font = 'bold 10.5px Inter, sans-serif';
        const tw = ctx.measureText(u.label).width;
        ctx.fillStyle = 'rgba(2, 6, 23, 0.88)';
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.roundRect(ux - tw / 2 - 7, uy - 26, tw + 14, 18, 4); ctx.fill(); ctx.stroke();
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.fillText(u.label, ux, uy - 13.5);
      });

      ctx.restore();
    }

    // =========================================================================
    // 5. HEAD-TO-HEAD TANK DUEL COMPARATOR (VIEW 5)
    // =========================================================================
    function initSelectDropdowns() {
      const opts = TANKS.map(t => `<option value="${t.id}">${NATION_MAP[t.nation].flag} ${t.name} (${t.year}) — ${t.gun}</option>`).join('');
      const selA = document.getElementById('duel-select-a');
      const selB = document.getElementById('duel-select-b');
      const selTP = document.getElementById('tank-page-select');
      if (selA) { selA.innerHTML = opts; selA.value = state.duelA; }
      if (selB) { selB.innerHTML = opts; selB.value = state.duelB; }
      if (selTP) { selTP.innerHTML = opts; selTP.value = state.selectedTankId; }

      const bOpts = BATTLES.map(b => `<option value="${b.id}">${b.year} — ${b.name} (${b.theatre})</option>`).join('');
      const selBP = document.getElementById('battle-page-select');
      if (selBP) { selBP.innerHTML = bOpts; selBP.value = state.selectedBattleId; }
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

      const directCombatEdge = EDGES.find(e => e.type === 'combat' && ((e.source === tA.id && e.target === tB.id) || (e.source === tB.id && e.target === tA.id)));
      const sharedBattles = BATTLES.filter(b =>
        (b.side_a.tanks.includes(tA.id) && b.side_b.tanks.includes(tB.id)) ||
        (b.side_b.tanks.includes(tA.id) && b.side_a.tanks.includes(tB.id))
      );

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
        return `${(cx + Math.cos(angle) * R * val).toFixed(1)},${(cy + Math.sin(angle) * R * val).toFixed(1)}`;
      }).join(' ');

      const axisLabelsSvg = axes.map((ax, i) => {
        const angle = -Math.PI / 2 + (i * 2 * Math.PI) / axes.length;
        return `<text x="${(cx + Math.cos(angle) * (R + 24)).toFixed(1)}" y="${(cy + Math.sin(angle) * (R + 18)).toFixed(1)}" fill="#cbd5e1" font-size="10" font-weight="bold" text-anchor="middle">${ax.label}</text>`;
      }).join('');

      const cardHtml = (t, badgeColor, tag) => {
        const nat = NATION_MAP[t.nation];
        return `
          <div class="lg:col-span-4 bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 flex flex-col gap-3">
            <div class="flex items-center justify-between">
              <span class="px-2 py-0.5 rounded text-xs font-bold ${badgeColor}">${tag} • ${nat.flag} ${nat.short || nat.id}</span>
              <button onclick="openTankPage('${t.id}')" class="px-2.5 py-1 rounded bg-amber-500 text-slate-950 text-xs font-extrabold">📄 Full Tank Page →</button>
            </div>
            <h3 class="text-lg font-extrabold text-[var(--foreground)]">${t.name} (${t.year})</h3>
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
          <div class="text-xs font-extrabold uppercase tracking-wider text-amber-400">5-Axis Telemetry Overlay</div>
          <svg viewBox="0 0 260 250" class="w-full max-w-[260px] h-auto">
            <circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="rgba(148,163,184,0.25)" stroke-dasharray="3,3"/>
            <circle cx="${cx}" cy="${cy}" r="${R*0.66}" fill="none" stroke="rgba(148,163,184,0.2)"/>
            <circle cx="${cx}" cy="${cy}" r="${R*0.33}" fill="none" stroke="rgba(148,163,184,0.2)"/>
            <polygon points="${polyPoints(tA)}" fill="rgba(56, 189, 248, 0.30)" stroke="#38bdf8" stroke-width="2.4"/>
            <polygon points="${polyPoints(tB)}" fill="rgba(244, 63, 94, 0.30)" stroke="#f43f5e" stroke-width="2.4"/>
            ${axisLabelsSvg}
          </svg>
          <div class="w-full p-3 rounded-lg border ${directCombatEdge || sharedBattles.length ? 'bg-rose-500/15 border-rose-500/40' : 'bg-[var(--card)] border-[var(--border)]'} text-xs">
            <div class="font-extrabold ${directCombatEdge || sharedBattles.length ? 'text-rose-300' : 'text-[var(--muted-foreground)]'}">
              ${directCombatEdge || sharedBattles.length ? '⚔️ VERIFIED HISTORICAL COMBAT OPPONENTS' : '📐 Cross-Era / Technical Comparison'}
            </div>
            <div class="text-xs text-[var(--foreground)] mt-1">
              ${directCombatEdge ? directCombatEdge.label : (sharedBattles.length ? 'Fought on opposing sides in recorded armored battles.' : 'No direct historical duel recorded between these two specific models.')}
            </div>
            ${sharedBattles.length ? `
              <div class="flex flex-wrap gap-1.5 mt-2">
                ${sharedBattles.map(b => `
                  <button onclick="openBattlePage('${b.id}')" class="px-2 py-1 rounded bg-rose-600 text-white text-xs font-bold hover:bg-rose-500">
                    🎬 Battle Page &amp; Sim: ${b.name} (${b.year})
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
    // 6. 2D PANNING TECH-TREE MATRIX & ENCYCLOPEDIA GRID (VIEW 6)
    // =========================================================================
    function renderCatalogAndMatrix() {
      const surface = document.getElementById('blueprint-pan-surface');
      const grid = document.getElementById('catalog-grid');
      if (!surface || !grid) return;

      surface.innerHTML = `
        <div class="grid grid-cols-8 gap-2 text-xs">
          <div class="p-2.5 rounded-lg bg-[var(--card)] border border-[var(--border)] font-extrabold text-amber-400">
            Nation \\ Era
          </div>
          ${ERAS.map(e => `
            <div class="p-2.5 rounded-lg bg-[var(--card)] border border-[var(--border)]">
              <div class="font-extrabold text-[var(--foreground)]">${e.short}</div>
              <div class="text-xs font-mono text-[var(--muted-foreground)]">${e.years}</div>
            </div>
          `).join('')}

          ${NATIONS.map(nat => `
            <div class="p-2.5 rounded-lg bg-[var(--card)] border border-[var(--border)] flex flex-col justify-center" style="border-left: 4px solid ${nat.color}">
              <div class="font-extrabold text-[var(--foreground)]">${nat.flag} ${nat.short || nat.id}</div>
              <div class="text-xs text-[var(--muted-foreground)]">${nat.name}</div>
            </div>
            ${ERAS.map(era => {
              const cellTanks = TANKS.filter(t => t.nation === nat.id && t.era === era.id);
              return `
                <div class="p-2 rounded-lg bg-[var(--card)]/70 border border-[var(--border)] flex flex-col gap-1.5 min-h-[92px]">
                  ${cellTanks.map(t => {
                    const rivals = EDGES.filter(e => e.type === 'combat' && (e.source === t.id || e.target === t.id)).length;
                    return `
                      <button onclick="openTankPage('${t.id}')" class="p-1.5 rounded bg-[var(--background)] border border-[var(--border)] hover:border-amber-400 text-left transition">
                        <div class="font-bold text-xs text-[var(--foreground)]">${t.name}</div>
                        <div class="flex items-center justify-between text-xs text-[var(--muted-foreground)] mt-0.5">
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

      const visibleTanks = TANKS.filter(isTankVisible);
      grid.innerHTML = visibleTanks.map(t => {
        const nat = NATION_MAP[t.nation];
        const rivals = EDGES.filter(e => e.type === 'combat' && (e.source === t.id || e.target === t.id));
        return `
          <div class="bg-[var(--background)] border border-[var(--border)] hover:border-amber-500 rounded-xl overflow-hidden flex flex-col justify-between transition shadow">
            <div>
              <div onclick="openTankPopup('${t.id}')" class="h-36 w-full bg-slate-950 border-b border-slate-800 relative overflow-hidden flex items-center justify-center cursor-pointer group">
                <img src="${t.photo_url || t.image_url}" alt="${t.name}" class="w-full h-full object-cover group-hover:scale-105 transition" onerror="this.src='${t.image_url}'" />
                <span class="absolute top-2 left-2 px-2 py-0.5 rounded bg-slate-900/90 text-xs font-extrabold border" style="color:${nat.color}; border-color:${nat.color}66">${nat.flag} ${t.year}</span>
                <span class="absolute top-2 right-2 px-2 py-0.5 rounded bg-slate-900/90 text-xs font-mono text-amber-300 border border-slate-700">${t.weight_t}t • ${t.armor_mm}mm</span>
              </div>
              <div class="p-3.5">
                <h4 class="text-sm font-extrabold text-[var(--foreground)]">${t.name}</h4>
                <div class="text-xs text-amber-400 font-bold mt-0.5">${t.gun}</div>
                <p class="text-xs text-[var(--muted-foreground)] mt-1.5 line-clamp-3">${t.summary}</p>
              </div>
            </div>
            <div class="px-3.5 py-2.5 bg-[var(--card)] border-t border-[var(--border)] flex items-center justify-between gap-2">
              <span class="text-xs text-rose-400 font-bold">⚔️ ${rivals.length} Rivals</span>
              <div class="flex items-center gap-1.5">
                <button onclick="openTankPopup('${t.id}')" class="px-2 py-1 rounded bg-[var(--background)] border border-emerald-500/40 hover:border-emerald-400 text-emerald-300 text-xs font-bold">🔍 Popup</button>
                <button onclick="openTankPage('${t.id}')" class="px-2.5 py-1 rounded bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-extrabold">
                  📄 Tank Page →
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

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

    function tick() {
      state.animTick++;
      if (state.mainView === 'graph') {
        drawGraphCanvas();
      } else if (state.mainView === 'map') {
        drawWorldMap();
        if (state.tacticalZoomOpen) drawTacticalSchematic();
      } else if (state.mainView === 'battle-page') {
        drawBattleSimCanvas();
        drawKillCamCanvas();
      }
      requestAnimationFrame(tick);
    }

    window.addEventListener('DOMContentLoaded', () => {
      initSelectDropdowns();
      renderEraStepper();
      renderTankInspector();
      renderMapBattleStrip();
      renderMapTankPhotoStrip();
      renderBattleInspector();
      renderAll85TanksPhotoGrid();
      renderTankPage();
      renderBattlePage();
      setupGraphCanvas();
      setupMapCanvas();
      setup2DPanningFallback();
      applyRoute();
      requestAnimationFrame(tick);
    });
  </script>
</body>
</html>
"""

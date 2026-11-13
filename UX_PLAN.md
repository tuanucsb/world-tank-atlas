# World Tank Atlas: Ease-of-Use Redesign Plan

Source of truth for the UX changes approved in the 2026-11-05 `/plan-design-review`.
All changes land in the generators under `tank_atlas_src/`, never by hand-editing
`world_tanks_atlas.html` (it is a build output).

Target: `world-tank-atlas/world_tanks_atlas.html`
(moved from the parent `Scifi/` folder on 2026-11-05).

## Goal

Make the atlas easy to use: the map and the battle simulator get the screen,
navigation fits in one glance, every state is designed, and it works on a phone,
by keyboard and with a screen reader.

## What the audit measured (before)

| Problem | Evidence (live page, 2026-11-05) |
|---|---|
| Sticky header eats the screen | 26 controls above the map; ~290 of 900px desktop, 748 of 812px phone |
| Battle popup + side panel open on load | Raseiniai pre-selected, popup covers the map |
| Counts disagree | `<title>` 86 tanks, h1 85, notes file 67 |
| Simulator below the fold, autoplays unseen | Battlefield 3 scrolls down; already playing when reached |
| Sim controls split in 3 places | Play/speed above map, scrubber inside, feed beside |
| Unit labels pile up | 20+ overlapping callouts at the Raseiniai crossroads |
| Tiny text | 266x 12px, 64x 10px, 54x 11px, 13x 9-9.5px |
| No design tokens | 7 CSS vars vs 78 inline hex colors; Tailwind via CDN |
| No routing | Browser Back leaves the app; nothing shareable |
| A11y | 1 `aria-label` on 376 buttons, no tab roles, no focus style, canvas-only sim, no reduced-motion |
| No empty state | Searching "zzqq" shows nothing |
| Build drift | Live strings "CHRONOLOGICAL TIMELINE", "VICTORIOUS SIDE" exist in no local source file |

## Approved design decisions

### Navigation and layout (Pass 1)

**D3 / 1A: one app bar.** A 56px sticky bar (desktop) holds:
- Wordmark "World Tank Atlas" with a site-switcher caret (see D21).
- Tabs: `Map · Battles · Tanks · Lineage · Compare · Tech tree`.
- Search field "Search tanks or battles".
- Theme toggle icon.

Era chips and the Nation select move into a 40px filter row, shown only on views
that use them (Map, Tanks, Lineage). The featured battles (Raseiniai 1941,
Kursk 1943, Vietnam 1972) move into the Battles view index. The subtitle,
region chips and the "Launch sim" pill leave the header.

**D4 / 1B: map-first home.**
- The map loads with nothing selected and no popup.
- Only the 3-4 largest battles are labeled.
- A hint chip at bottom-left says "Click a battle to explore".
- Clicking a battle opens one right side panel (no floating popup) with its
  date, place, sides, result and a primary **Watch battle** button.
- Region filters become a "Theatre" select inside the map's filter row.

**D5 / 1C: battle theater.** Top to bottom:
1. App bar.
2. A 48px battle header: `← All battles`, the battle title, a battle-switcher
   dropdown, and `Details ↓`.
3. A thin force-strength bar showing Side A and Side B active/lost counts as
   opposing bars.
4. The battlefield, which fills the remaining height (75% width on desktop).
5. One docked control bar: Play/Pause, current date-time, a scrubber with
   5 phase notches, and speed 0.5x / 1x / 2x.

The right panel (25%) shows the current phase title, 2-3 lines of narrative and
the event feed. "Battle details" (D20) and the knock-out scenarios sit below the
fold. The separate row of 5 phase cards is removed; phases live on the scrubber.

```
DESKTOP MAP (1440x900)
┌ [◆ World Tank Atlas ▾]  Map Battles Tanks Lineage Compare Tech tree  [Search…] [◐] ┐ 56
├ Era: All WWI WWII Cold War Vietnam Arab-Israeli Gulf Ukraine  Nation ▾  Theatre ▾ ┤ 40
│                                                                                    │
│                         world map, edge to edge                                     │
│                ● Kursk 1943        ● Raseiniai 1941                                │
│                                         ● 73 Easting 1991                          │
│ [Click a battle to explore]                                    [+][-] legend       │
└────────────────────────────────────────────────────────────────────────────────────┘

DESKTOP BATTLE THEATER
┌ app bar ─────────────────────────────────────────────────────────────────────────── ┐ 56
├ ← All battles   Battle of Raseiniai, 1941  [switch ▾]                  Details ↓   ┤ 48
├ ■■■■■■■■■■■ Soviet 678 / -71           German 219 / -26 ■■■■■■■ ─────────────────── ┤ 24
│                                                   │ Phase 2: Soviet counterattack │
│          battlefield (counters, no labels)        │ 2-3 lines of narrative        │
│                 [ ▶ Play ]  (ready state)         │ ───────────────────────────── │
│                                                   │ 06:10 KV-1 knocks out Pz.38(t)│
│                                                   │ 06:02 Phase 2 begins          │
├ ▶  Jun 24 1941 06:00  ──|──●──|────|────|──  0.5x 1x 2x ──────────────────────────── ┤ 56
└ Battle details (comparison table), knock-out scenarios: below the fold ──────────── ┘

PHONE BATTLE THEATER (375x812)
┌ [◆] World Tank Atlas        [⌕] [☰] ┐ 48
├ ■■■■ 678/-71      219/-26 ■■■■     ┤ 24
│                                     │
│     battlefield, full width          │
│                                     │
├ ═══ bottom sheet (peek 30%) ═══════ ┤  drag up to 90%
│ Phase 2: Soviet counterattack        │
├ ▶  06:00  ──|──●──|──|──|──  1x    ┤ 56  fixed, thumb reach
└─────────────────────────────────────┘
```

### States (Pass 2)

**D6 / 2A: no-results state.** One shared component:
- Message: `No tanks or battles match "<query>"`.
- A **Clear search** button (or **Reset filters**, for filter combos).
- Three suggestions: Tiger I, Kursk 1943, T-34-85.

On the map it shows as a centered chip over the map.

**D7 / 2B: simulator playback states.**

| State | What the user sees |
|---|---|
| Ready | First frame drawn, large Play button centered on the battlefield, scrubber at Phase 1 |
| Playing | Units move, control bar shows Pause, phase notch highlights in amber |
| Paused | Control bar shows Play. Auto-pause when the battlefield leaves the viewport (IntersectionObserver), the tab is hidden (`visibilitychange`), or a unit is selected (D10) |
| Ended | Overlay: winner, losses per side, **Replay** and **Next battle** buttons |

**D8 / 2C: photo states.**
- Every photo slot is a fixed 4:3 box with the `surface-raised` placeholder
  while loading.
- On `error`, render that tank's existing SVG blueprint in the slot with the
  caption "Photo unavailable".

| Feature | Loading | Empty | Error | Success | Partial |
|---|---|---|---|---|---|
| Search / filters | n/a (instant) | No-results message + Clear/Reset + 3 suggestions | n/a | Results list / filtered pins | Pins dimmed outside filter |
| Map battle panel | n/a | Hint chip "Click a battle to explore" | n/a | Side panel with Watch battle | n/a |
| Simulator | Ready state with Play | n/a | n/a | Ended overlay with result | Paused mid-battle |
| Tank photos | 4:3 tinted placeholder | n/a | SVG blueprint + "Photo unavailable" | Photo | n/a |

### Journey (Pass 3)

**D9 / 3A: hash routing.** Routes:
- `#/map`
- `#/battles`
- `#/battles/<battle-id>` (for example `#/battles/raseiniai-1941`)
- `#/tanks`
- `#/tanks/<tank-id>`
- `#/lineage`
- `#/compare`
- `#/tech-tree`

Every `open*()` call goes through one router that updates `location.hash`.
`hashchange` renders the view. Back and Forward work, and a pasted link opens
that exact view.

**D10 / 3B: clicking a unit during playback.**
- The sim pauses and the unit gets an amber selection ring.
- The right panel (bottom sheet on phone/tablet) swaps to that tank's card:
  photo, name, gun, armor and an **Open tank page** link.
- A "← Back to story" link, Play, or Esc resumes and restores the phase story.

```
STEP | USER DOES                     | USER FEELS     | PLAN SPECIFIES
-----|-------------------------------|----------------|-----------------------------------
1    | Lands on atlas                | Curious        | Clean map, one hint chip (D3, D4)
2    | Clicks a battle dot           | Oriented       | Side panel + Watch battle (D4)
3    | Watch battle                  | Anticipation   | Theater in Ready state (D5, D7)
4    | Clicks a tank mid-battle      | Curious        | Pause + tank card in panel (D10)
5    | Presses browser Back          | In control     | Returns to previous view (D9)
6    | Battle ends                   | Satisfied      | Result overlay, Replay/Next (D7)
7    | Shares the battle             | Proud          | #/battles/<id> link (D9)
```
5-second: the map and the wordmark. 5-minute: the battle plays with clear
controls. Return visits: shareable links and keyboard shortcuts.

### Visual clarity and copy (Pass 4)

**D11 / 4A: no emoji.**
- Labels are plain text.
- Single-color line icons appear only on controls (play, pause, zoom, search,
  theme, menu).
- Country flags appear only where a nation is being chosen or identified.

**D12 / 4B: plain copy, counts from data.**
- `<title>` and h1 read "World Tank Atlas".
- The map view has one subtitle line: "{N_TANKS} tanks and {N_BATTLES} battles,
  1916–2026".
- `N_TANKS = len(TANKS)` and `N_BATTLES = len(BATTLES)` are computed at build
  time, and every count on the page uses these values.
- Section renames:

| Old | New |
|---|---|
| Kill-Cam / X-Ray Ballistics | How tanks were knocked out |
| Victorious side, Defeated, etc. | Battle details |
| Lineage & Combat Graph | Lineage |

**D13 / 4C: battlefield labels.**
- Units draw as unlabeled counters, `side-a` blue or `side-b` red.
- A label appears only on hover or selection.
- Kill events show as one short callout ("KV-1 knocks out Pz.38(t)") that fades
  after 2s, with at most 3 on screen.
- The full detail stays in the event feed.

### Design tokens (Pass 5)

**D14 / 5A: minimal token set.** Write `DESIGN.md` in this folder. The CSS
variables below are the only color sources: replace all 78 inline hex values
and arbitrary Tailwind sizes. The light/dark toggle swaps the token values.

| Token | Dark | Light | Use |
|---|---|---|---|
| `--surface` | `#111611` | `#eef0ea` | page / map ground |
| `--surface-raised` | `#1a211a` | `#ffffff` | panels, sheet, bars, photo placeholder |
| `--text` | `#ecefe6` | `#1b2118` | body |
| `--text-muted` | `#a9b2a0` | `#4f5a4a` | secondary (both ≥ 4.5:1 on surface) |
| `--border` | `#2e3a2e` | `#c9cfc2` | dividers |
| `--accent` | `#f2a93b` | `#b86e00` | selection, active phase, active tab |
| `--focus` | `#f2a93b` | `#b86e00` | 2px focus ring, 2px offset |
| `--side-a` | `#4f8fe8` | `#1f5fbf` | Side A units, force bar, table column |
| `--side-b` | `#e5534b` | `#c0342b` | Side B units, force bar, table column |
| `--tint-east` | `#8a3b3b33` | `#c0342b1f` | E. Front theatre polygon |
| `--tint-desert` | `#8a733b33` | `#b86e001f` | N. Africa / Middle East polygons |
| `--tint-asia` | `#3b7a5a33` | `#2f7a521f` | Asia polygons |

- **Type:** IBM Plex Sans for the UI and Barlow Condensed 600 for the wordmark
  only (Google Fonts). Numbers use `font-variant-numeric: tabular-nums`.
- **Type scale:** 14 / 16 / 20 / 28px; line-height 1.5 for body, 1.25 for
  headings.
- **Spacing:** 4, 8, 12, 16, 24, 32, 48px.
- **Radius:** 6px controls, 10px panels and sheet.
- **UI motion:** 150ms ease-out. Sim effects keep their own timing (see D18).
- Browser surfaces are themed from tokens: `::selection` background
  `--accent` at 30%, `caret-color: var(--accent)`, `scrollbar-color`, and
  focus rings.

### Responsive and accessibility (Pass 6)

**D15 / 6A and D19 / 7.1: viewports.**

| Width | App bar | Map / battlefield | Panel | Sim controls |
|---|---|---|---|---|
| < 768px | 48px: wordmark, search icon, menu with the 6 views | full screen | bottom sheet, peek 30% / full 90%, drag handle + tap to toggle | fixed bottom bar |
| 768-1024px | 56px, tabs may scroll horizontally | full width | bottom sheet (same component) | docked under battlefield |
| > 1024px | 56px full | 75% width | right side panel 25% (min 320px) | docked under battlefield |

**D16 / 6B: sizes.**
- Body 16px; nothing renders below 14px.
- Every tappable element is at least 44x44px on touch (padding may extend the
  hit area beyond the visual).
- Dense tables such as the duel comparator are re-laid out to fit.

**D17 / 6C: keyboard and screen reader.**
- The view tabs get `role="tablist"` / `role="tab"` with `aria-selected`, and
  arrow keys move between them.
- Landmarks: `<header>`, `<nav>`, `<main>`.
- Every interactive element shows a visible `--focus` ring.
- Map battle markers are `<button>`s with `aria-label="Battle of Kursk, 1943"`.
- Sim shortcuts (also shown in a `?` tooltip):

| Key | Action |
|---|---|
| Space | play / pause |
| ← / → | previous / next phase |
| Esc | close panel / deselect |

- The event feed is `aria-live="polite"`. It announces phase changes and kills,
  throttled to one announcement every 3s; kills in between are summarized
  ("4 more tanks knocked out").
- The canvas gets `role="img"` with an `aria-label` describing the battle and
  the current phase.

**D18 / 6D: reduced motion.** Under `prefers-reduced-motion: reduce`:
- Units still move.
- Tracers, explosion flashes and flying turrets become a static "knocked out"
  mark.
- Map zooms jump instead of animating.
- Default speed is 0.5x.

### Battle details and site switcher (Pass 7)

**D20 / 7.2: battle details.**
- One summary paragraph.
- Then a two-column comparison table, Side A (`--side-a` header) vs Side B
  (`--side-b` header). Rows: Forces, Tanks committed, Tank types (linked),
  Losses, Result.
- Loss breakdowns are edited down to fit their cells.
- The knock-out scenarios become a list ("88mm Flak vs KV-1 at the
  crossroads"); each expands its X-ray animation inline.

**D21 / 7.3: site switcher.**
- Clicking the wordmark opens a 2-item menu: World Tank Atlas (current) and
  Sci-Fi AI Atlas.
- The link target is `../scifi-ai-atlas/index.html`.

Today the link is broken. `href="index.html"` (`build_v2_part1.py:82`) used to
point at the root `index.html`, a byte-identical copy of the tank atlas, and
since the move it points at nothing.

## NOT in scope

- Layout redesign of the Tanks, Lineage, Compare and Tech-tree views: they get
  the app bar, tokens, sizes and routing, but their layouts weren't reviewed
  (TODOS.md).
- First-paint loading screen for the 750 KB file (TODOS.md).
- Exploring alternative visual directions: tokens were chosen in this plan, not
  explored. `/design-consultation` remains an option.
- Saving favorites or other return-visit features.
- Visual mockups: the designer had no OpenAI API key, so 0 images were
  generated.

## What already exists (reuse)

- The 6-view switch in `build_v2_part1.py` / `build_v2_part2a.py`
  (`openBattlePage`, `openTankPage`, `openTankPopup`). Route these through the
  router; don't rewrite them.
- The scrub slider, play/pause and speed controls, and the 5-phase timeline
  data in `build_v2_part2b.py`. Re-dock them; the phase data drives the
  scrubber notches.
- The per-tank SVG blueprint renderer. Reuse it as the photo fallback (D8).
- The light/dark toggle. Keep it and point it at the token values.
- The era chips and Nation select. Move them into the filter row.
- The event and kill feed data. It drives the panel feed, the aria-live
  announcements and the fading callouts.

## Implementation Tasks

Synthesized from this review's findings. Each task derives from a specific
finding above. Effort assumes features ~30x, architecture ~5x human:CC.

- [x] **TB (P1, human: ~10min / CC: ~2min): repo: git baseline before any change.**
  - Surfaced by: eng review S5 / R1 (D3).
  - Files: `world-tank-atlas/.gitignore` (new, `.gstack/`), repo root `world-tank-atlas/`.
  - Verify: `git log --oneline` shows the baseline commit, and `git status` is clean.
- [x] **T0 (P1, human: ~1 day / CC: ~45min): build: make the generator self-contained and single-writer. Blocks all other tasks.**
  - Surfaced by: D24, corrected by eng review E1/E2. The scripts `sys.path.insert(0, ~/.gemini/.../scratch)` (`assemble_v2.py:3` and 5 others), so Python loads the scratch copies before local siblings. Local edits would be silently ignored; today they're byte-identical (`cmp`). `assemble_v2.py:13` reads `WORLD_POLYGONS` from its own previous output, and that is the only place the polygon data exists. `render_html.py:1929` is a legacy v1 writer to the same output. `assemble_v2.py:52` also writes a copy into `~/.gemini`.
  - Files: `tank_atlas_src/assemble_v2.py`, `tank_atlas_src/*.py` (remove the `sys.path.insert` lines), `tank_atlas_src/world_polygons.json` (new, extracted from `render_html.py:13` `WORLD_POLYGONS` **before** deleting that file; it equals the 12 polygons in the current output, see E5), delete `render_html.py` and `build_tank_atlas.py` (not in the `assemble_v2` import chain).
  - Verify: `python3 assemble_v2.py` with no `~/.gemini` folder on disk and no prior HTML present reproduces `world_tanks_atlas.html` byte-for-byte (a probe on a copy already matched 754,548/754,548 bytes with the self-read in place).
- [x] **T1 (P1, human: ~1 day / CC: ~45min): tokens: write DESIGN.md and migrate colors and type to tokens.**
  - Surfaced by: Pass 5 (D14), Pass 6 (D16).
  - Files: `DESIGN.md` (new), `tank_atlas_src/build_v2_part1.py` (head CSS / Tailwind config), `build_v2_part2a.py`, `build_v2_part2b.py`.
  - Also (eng D4): delete the gstatic dev Tailwind script (`build_v2_part1.py:8`); map tokens through an inline `tailwind.config` for `cdn.tailwindcss.com`.
  - Verify: `grep -c 'gstatic.com/antigravity' world_tanks_atlas.html` is 0; `grep -oiE '#[0-9a-f]{6}'` on the output only finds token definitions; no `text-[9|9.5|10|10.5|11px]` or `text-xs` on content; contrast spot-check in both themes.
- [x] **T2 (P1, human: ~1 day / CC: ~30min): app bar: 56px bar, filter row, site switcher, plain copy.**
  - Surfaced by: Pass 1 (D3), Pass 4 (D11, D12), Pass 7 (D21).
  - Files: `tank_atlas_src/build_v2_part1.py`.
  - Verify: in the browser at 1440x900, header height is 56px plus a 40px filter row on Map only; title/h1 read "World Tank Atlas"; counts equal `len(TANKS)`/`len(BATTLES)`; switcher opens `../scifi-ai-atlas/index.html`.
- [x] **T3 (P1, human: ~1 day / CC: ~40min): router: hash routes for all views, battles and tanks.**
  - Surfaced by: Pass 3 (D9).
  - Files: `tank_atlas_src/build_v2_part2a.py`.
  - Verify: open battle → tank → Back → Back returns to battle, then the map; pasting `#/battles/raseiniai-1941` in a new tab opens it.
- [x] **T4 (P1, human: ~3h / CC: ~10min): map: clean first load, single side panel, Watch battle.**
  - Surfaced by: Pass 1 (D4).
  - Files: `tank_atlas_src/build_v2_part1.py`, `build_v2_part2a.py`.
  - Verify: fresh load shows no popup and no selection; one panel opens on click.
- [x] **T5 (P1, human: ~2 days / CC: ~1h): simulator: theater layout and docked control bar.**
  - Surfaced by: Pass 1 (D5).
  - Files: `tank_atlas_src/build_v2_part2b.py`.
  - Verify: at 1440x900 the battlefield and control bar are fully visible without scrolling below the app bar.
- [x] **T6 (P1, human: ~4h / CC: ~20min): simulator: Ready/Playing/Paused/Ended states and auto-pause.**
  - Surfaced by: Pass 2 (D7).
  - Files: `tank_atlas_src/build_v2_part2b.py`.
  - Verify: the sim is in Ready on open; scrolling away pauses it; reaching the end shows the result overlay.
- [x] **T7 (P1, human: ~4h / CC: ~20min): simulator: unit select pauses and shows the tank card in the panel.**
  - Surfaced by: Pass 3 (D10).
  - Files: `tank_atlas_src/build_v2_part2b.py`, `build_v2_part2a.py`.
  - Verify: clicking a unit pauses, shows the ring and the card; Esc resumes.
- [x] **T8 (P1, human: ~4h / CC: ~20min): simulator: counters, on-demand labels, ≤3 fading callouts.**
  - Surfaced by: Pass 4 (D13).
  - Files: `tank_atlas_src/build_v2_part2b.py`.
  - Verify: screenshot of the Raseiniai crossroads mid-Phase 2 has no overlapping text.
- [x] **T9 (P1, human: ~2 days / CC: ~1h): responsive: phone/tablet bottom sheet, phone app bar, bottom controls.**
  - Surfaced by: Pass 6 (D15, D19).
  - Files: `tank_atlas_src/build_v2_part1.py`, `build_v2_part2b.py`.
  - Verify: at 375x812 the header is 48px and the battlefield plus control bar are visible; at 768 and 1024 the sheet is used; no horizontal scroll.
- [x] **T10 (P1, human: ~1 day / CC: ~40min): a11y: tablist, focus rings, focusable pins, sim shortcuts, aria-live feed.**
  - Surfaced by: Pass 6 (D17).
  - Files: `tank_atlas_src/build_v2_part1.py`, `build_v2_part2a.py`, `build_v2_part2b.py`.
  - Verify: the full journey works with keyboard only; VoiceOver announces the phase change; feed announcements are throttled.
- [x] **T11 (P2, human: ~3h / CC: ~15min): reduced-motion mode.**
  - Surfaced by: Pass 6 (D18).
  - Files: `tank_atlas_src/build_v2_part2b.py`.
  - Verify: with emulated `prefers-reduced-motion: reduce`, no tracers or explosions draw, and the speed defaults to 0.5x.
- [x] **T12 (P2, human: ~2h / CC: ~10min): search and filter no-results state.**
  - Surfaced by: Pass 2 (D6).
  - Files: `tank_atlas_src/build_v2_part1.py`, `build_v2_part2a.py`.
  - Verify: "zzqq" shows the message, Clear and 3 suggestions; Ukraine + Japan on the map shows Reset filters.
- [x] **T13 (P2, human: ~3h / CC: ~15min): photo 4:3 placeholders and blueprint fallback.**
  - Surfaced by: Pass 2 (D8).
  - Files: `tank_atlas_src/build_v2_part2a.py`.
  - Verify: block `upload.wikimedia.org` in devtools; every card shows a blueprint and "Photo unavailable", with no layout shift.
- [x] **T14 (P2, human: ~4h / CC: ~20min + copy edits): battle details comparison table and knock-out list.**
  - Surfaced by: Pass 7 (D20).
  - Files: `tank_atlas_src/build_v2_part2b.py`, `battle_timelines_and_destruction.py`.
  - Verify: each of the 27 battles renders the table with no cell overflowing at 1440 and 375.
- [x] **T15 (P2, human: ~2h / CC: ~10min): sim: map-tile fallback (other provider once, then schematic + chip).**
  - Surfaced by: eng review A2 (D5).
  - Files: `tank_atlas_src/build_v2_part2b.py` (`L.tileLayer` at `:441`).
  - Verify: Playwright blocks `*.tile.opentopomap.org` → ArcGIS tiles load; blocking both → schematic + "Map tiles unavailable", no provider flip-flop.
- [x] **T16 (P1, human: ~2 days / CC: ~1h): tests: pytest build/data checks + Playwright E2E harness.**
  - Surfaced by: eng review TG1 (D7).
  - Files: `tests/test_build.py`, `tests/e2e/*.spec.ts`, `package.json`, `playwright.config.ts` (all in `world-tank-atlas/`).
  - Verify: `python3 -m pytest tests/` and `npx playwright test` pass; each UI task T3-T15 and T18 adds its spec when it lands.
- [x] **T17 (P1, human: ~4h / CC: ~15min): tests: regression suite over all 27 battles and 86 tanks.**
  - Surfaced by: eng review RG1 (D8).
  - Files: `tests/e2e/regression.spec.ts`.
  - Verify: written and green against the baseline page right after T0, and still green after every later task.
- [x] **T18 (P2, human: ~3h / CC: ~15min): perf: draw only while playing or when dirty; kill-cam only in viewport.**
  - Surfaced by: eng review P1 (D9), measured 7.83 ms/frame paused.
  - Files: `tank_atlas_src/build_v2_part2b.py` (`tick` at `:2272`).
  - Verify: rerun the 3 s draw-count probe; paused battle and idle map show ~0 draw calls; a hover after pause still redraws.

### Battle improvements: quick wins (added 2026-11-07 at the user's request)

- [x] **B1+B2 (P2, CC: ~15min): battlefield: say what a counter stands for and that positions are illustrative.**
  - Why: most battles draw a fixed 34 vs 30 counters whatever their size (Brody: ~103 tanks per counter; Villers-Bretonneux: 64 counters for 20 real tanks), so "one counter ≈ N tanks" would be false. The note states both numbers ("42 counters for 749 tanks · 28 for 245") and that positions are illustrative, while phases, counts and losses come from the sources.
  - Files: `tank_atlas_src/build_v2_part2b.py` (`renderBattlePage`).
- [x] **B3 (P2, CC: ~20min): losses strip above the scrubber.** Knock-outs over time per side (blue above, red below), from the same deterministic `buildBattleAgents` the simulator draws. Hidden below 768px.
- [x] **B4 (P2, CC: ~20min): link to a moment.** `#/battles/<id>?t=0.42` opens the battle at that point (Ready state). A link button in the control bar copies the current moment.
- [x] **B5 (P2, CC: ~15min): night phases.** Phases whose text describes night fighting get `night: true` in the data (Lang Vei/Ben Het 2 and 4, Chinese Farm 2 and 5, Valley of Tears 2, Balaton 3, Sinai 5); the battlefield darkens and the phase label adds "Night".
- [x] **B7 (P2, CC: ~30min): movement arrows.** Each formation's route from the data (`x,y` → `tx,ty`, all 62 formations) is drawn under the units: dashed and faint for the full route, solid for the stretch covered so far, with a dark outline so it reads over historical maps.
- [x] **B8 (P2, CC: ~40min): stop at each phase.** On by default ("Stop at each phase" in the story panel). While playing, crossing into a new phase pauses just inside it with a card (phase n of N, time, title, narrative, losses, Continue, Play without stopping). Scrubbing never stops. The phase lookup now picks the last phase that has started, so a boundary belongs to the phase it opens.
- Later candidates (not scheduled): link knock-outs to the kill-cam, camera follows the action, see it from one side, end-of-battle quiz.
- [x] **B6 (P2, CC: ~10min): cap counters at the real tank count.** A side never shows more counters than it had tanks; changes Cambrai (Side B 30 → 7), Villers-Bretonneux (34/30 → 7/13) and Chawinda (Side A 34 → 20). The note reads "7 tanks, one counter each" when they match.

Task notes from the eng review:
- **T3:** routes use data ids verbatim (`#/battles/raseiniai_1941`, E4). The hash is the single owner of navigation, with `hashchange` → `applyRoute()`. Unknown ids go to the section index plus the no-results message via `replaceState` (D6).
- **T7:** raise the canvas hit radius from 15px (`build_v2_part2b.py:1247`) to 22px on touch, for the 44px target in D16 (C1).

Order: TB → T0 → T16 (pytest part) + T17 (baseline regression) → T1 → T2/T3 → T4-T8, T15, T18 → T9-T14. Run `/design-review` on the built
page after T9.

## Design Review Completion Summary

```
  +====================================================================+
  |         DESIGN PLAN REVIEW — COMPLETION SUMMARY                    |
  +====================================================================+
  | System Audit         | no DESIGN.md; 6 views, 376 buttons, UI scope |
  | Step 0               | 3/10 initial; focus: all 7 passes            |
  | Pass 1  (Info Arch)  | 2/10 → 8/10 after fixes                      |
  | Pass 2  (States)     | 2/10 → 9/10 after fixes                      |
  | Pass 3  (Journey)    | 3/10 → 9/10 after fixes                      |
  | Pass 4  (AI Slop)    | 3/10 → 8/10 after fixes                      |
  | Pass 5  (Design Sys) | 2/10 → 8/10 after fixes                      |
  | Pass 6  (Responsive) | 1/10 → 9/10 after fixes                      |
  | Pass 7  (Decisions)  | 3 resolved, 0 deferred                       |
  +--------------------------------------------------------------------+
  | NOT in scope         | written (5 items)                            |
  | What already exists  | written                                      |
  | TODOS.md updates     | 2 items added                                |
  | Approved Mockups     | 0 generated (no OpenAI key), 0 approved      |
  | Decisions made       | 20 added to plan (19 design + T0 scope)      |
  | Decisions deferred   | 2 (listed below)                             |
  | Overall design score | 1/10 → 8/10                                  |
  +====================================================================+
```

Remaining below 10:
- Pass 1 (8): the other four views keep their current layouts.
- Pass 4 (8): the palette and type were chosen here, not explored.
- Pass 5 (8): same reason.
- Passes 2, 3 and 6 (9): the other views' states, return-visit features and
  responsive behavior were not examined.

### Unresolved Decisions

- Layout review of the Tanks, Lineage, Compare and Tech-tree views: deferred to TODOS.md (D22).
- First-load loading screen: deferred to TODOS.md (D23).

## Eng Review (2026-11-05)

Target: `world-tank-atlas/UX_PLAN.md` (this file). No git
repo, no design doc; `/office-hours` skipped (eng D1).

### Scope record

feature answers: no cuts proposed (all 19 UX decisions individually approved in the design review); structure: A, Original arrangement (eng D2); accepted scope: 9 files: edit `build_v2_part1.py`, `build_v2_part2a.py`, `build_v2_part2b.py`, `battle_timelines_and_destruction.py`; fix `assemble_v2.py`; delete `render_html.py`, `build_tank_atlas.py`; add `DESIGN.md`, `world_polygons.json`; router, bottom sheet, playback states and announcer as functions on the existing `state` + `tick` in the part files; pending remedies: R1 (version control), A1 (Tailwind delivery), test approach.

### Factual corrections (no behavior change)

- **E1:** The design review said "CHRONOLOGICAL TIMELINE" / "VICTORIOUS SIDE" exist in no local source. Wrong: both are in `build_v2_part2b.py` in mixed case and uppercased by CSS. Local `tank_atlas_src/` equals the Gemini scratch copies (`cmp`), except the two path edits.
- **E2:** The design review said `openBattlePage` is defined twice. Wrong: `build_v2_part2a.py:480` defines it once; the grep also matched `openBattlePageAtPhase` (`:1568`).
- **E3:** Rebuild probe: `assemble_v2.py` on a scratchpad copy reproduced the current page byte-for-byte (754,548 bytes). The data has 86 tanks / 27 battles / 194 edges; the h1's "85" is hand-typed (supports D12).

- **E5:** The polygon data is not only in the previous output. `render_html.py:13` holds `WORLD_POLYGONS` as Python source, equal to the 12 polygons in the current page (`ast` vs `json` compare: equal). T0 must extract it to `world_polygons.json` before deleting `render_html.py`.

## Decision ledger

### R1: Put the atlas under version control before T0
Finding: S5, CRITICAL, confidence 9/10, the `Scifi/` folder (`git rev-parse` fails; `gstack-review-read` prints `HEAD unknown`), reviewer: Claude (plan-eng-review)
Plan baseline: no version control; the plan's 15 tasks rewrite ~4,600 lines of generators with no rollback.
Runtime evidence: not a git repository (`git rev-parse --show-toplevel` fails in `Scifi/` and `world-tank-atlas/`); `scifi-ai-atlas/` has its own `.git`.
Comparison grid:
| Choice | Current | A | B |
|---|---|---|---|
| R1 version control | none | `git init` in `world-tank-atlas/`, `.gitignore` for `.gstack/`, baseline commit of the current page + src before T0 | none; rely on the rebuild probe and manual copies |
| A1 Tailwind delivery | pending | pending | pending |
| Test approach | pending | pending | pending |
Question D3:
D3 — Put the tank atlas under git before any task starts?
Project: World Tank Atlas, world-tank-atlas/ (no git repo; the sister scifi-ai-atlas/ has one).
ELI10: The plan rewrites about 4,600 lines of generator code across 15 tasks, and none of it is under version control. If a change breaks the simulator or the build produces a worse page, there's no way back except hand-made copies, and no way to see what changed. Running `git init` in world-tank-atlas/ and committing today's page and sources as a baseline takes a minute, and every task after that gets its own commit.
Stakes if we pick wrong: one bad edit to a 2,300-line generator file with no history can cost hours to undo or lose working simulator code.
Recommendation: A because a baseline commit makes every later task reversible, at almost no cost.
Note: options differ in kind, not coverage — no completeness score.
Pros / cons:
A) git init + baseline commit (recommended)
  ✅ Every task becomes one reversible commit, and diffs show exactly what changed in the page
  ✅ Lets the rebuild check compare against the committed page, not a loose copy
  ❌ Adds a repo to maintain; nothing is pushed anywhere unless you add a remote later
  (human: ~10 min / CC: ~2 min)
B) No version control
  ✅ Nothing new to manage in the folder
  ✅ The rebuild probe still proves the build reproduces today's page
  ❌ No rollback or history across 15 tasks of generator edits
Net: a one-minute setup that makes every later change undoable.
Header: Git
Options:
A) Git baseline (recommended)
git init in world-tank-atlas/, ignore .gstack/, commit current page + sources before T0.
B) No version control
Keep the folder as plain files; rely on the rebuild probe and manual copies.

State: approved
Actual answer: A) Git baseline (recommended), eng D3
Accepted scope: task TB (before T0): `git init` in `world-tank-atlas/`, `.gitignore` with `.gstack/`, baseline commit of the current page + `tank_atlas_src/` + docs; one commit per task afterwards. Nothing is pushed.
History: none

### A1: How Tailwind is delivered once tokens land (T1)
Finding: A1, INFORMATIONAL, confidence 9/10, `build_v2_part1.py:8-9` (`<script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js">` and `<script src="https://cdn.tailwindcss.com">`), reviewer: Claude (plan-eng-review)
Plan baseline: T1 says "Tailwind config"; delivery unspecified.
Runtime evidence: two runtime JIT Tailwind scripts load on every visit, one from a Gemini dev URL; no node/package.json in the folder.
Comparison grid:
| Choice | Current | A | B | C |
|---|---|---|---|---|
| A1 Tailwind delivery | two runtime CDNs incl. Gemini dev URL | drop the gstatic dev script; keep `cdn.tailwindcss.com` with an inline `tailwind.config` mapping the D14 tokens | precompile CSS at build time with the Tailwind CLI and inline it; no runtime Tailwind | leave both scripts |
| R1 version control | approved (D3) | unchanged | unchanged | unchanged |
| A2 tile failure | pending | pending | pending | pending |
| Test approach | pending | pending | pending | pending |
Question D4:
D4 — How should Tailwind load once the design tokens land?
Project: World Tank Atlas, build_v2_part1.py:8-9 (no git yet; TB approved).
ELI10: The page loads Tailwind, the CSS tool behind all its class names, twice at runtime: once from a Google/Gemini developer URL and once from Tailwind's own 'Play' CDN. Both compile styles in the browser on every visit. The developer URL can disappear at any time, and the Play CDN is meant for prototyping. Option A drops the developer copy and keeps one CDN with our tokens in an inline config. Option B compiles the CSS once at build time, which is fastest for visitors but adds Node and the Tailwind CLI to a Python-only build.
Stakes if we pick wrong: if the dev URL vanishes the page still works through the second copy, but loading both wastes ~100 KB and slows first paint on every visit.
Recommendation: A because it removes the fragile dependency with a one-line change and no new toolchain.
Completeness: A=8/10, B=10/10, C=3/10
Pros / cons:
A) One Play CDN + inline token config (recommended)
  ✅ Removes the Gemini developer URL dependency and the duplicate download in one line
  ✅ Tokens from D14 plug in through an inline tailwind.config, no new build tools
  ❌ Styles still compile in the browser, so the unstyled flash in TODOS.md stays
  (human: ~30 min / CC: ~5 min)
B) Precompile Tailwind at build time
  ✅ No runtime CSS compiler: faster first paint, which also closes the loading-screen TODO
  ✅ Ships only the classes actually used, a smaller page
  ❌ Adds Node + Tailwind CLI to the Python build and a second step every rebuild
  (human: ~1 day / CC: ~30 min)
C) Leave both scripts
  ✅ Zero work, nothing to test
  ✅ Two copies mean one outage doesn't unstyle the page
  ❌ Keeps a dependency on a Gemini developer URL and loads Tailwind twice on every visit
Net: a one-line fix now, or a build-time compile that also fixes first paint.
Header: Tailwind
Options:
A) One CDN + config (recommended)
Drop the gstatic dev script; keep cdn.tailwindcss.com with an inline tailwind.config of the D14 tokens.
B) Precompile at build
Add the Tailwind CLI to the build, inline compiled CSS, remove runtime Tailwind.
C) Leave both
Keep both runtime scripts as they are.

State: approved
Actual answer: A) One CDN + config (recommended), eng D4
Accepted scope: in T1, delete the `gstatic.com/antigravity/.../tailwindcss.min.js` script (`build_v2_part1.py:8`); keep `cdn.tailwindcss.com` with an inline `tailwind.config` whose `theme.extend.colors` / `fontSize` / `spacing` map to the D14 CSS variables. No build-time CSS compile.
History: none

### A2: Battlefield map tiles fail to load
Finding: A2, INFORMATIONAL, confidence 8/10, `build_v2_part2b.py:439-441` (`'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png'` ... `L.tileLayer(tileUrl, { maxZoom: 17 }).addTo(battleSimLeaflet);`, no `tileerror` handler), reviewer: Claude (plan-eng-review)
Plan baseline: D7/D8 define sim and photo states; map-tile failure is unspecified.
Runtime evidence: tiles come from OpenTopoMap (topographic) or ArcGIS (satellite); no error handler in source. Visible result offline or when OpenTopoMap rate-limits: a grey battlefield behind the counters, with no message (inferred from Leaflet's default behavior, not observed).
Comparison grid:
| Choice | Current | A | B |
|---|---|---|---|
| A2 tile failure | silent grey background | on the first `tileerror`, switch the layer to the other provider once; if that also fails, hide tiles and show the existing tactical schematic background + chip "Map tiles unavailable" | no change; grey background |
| R1, A1 | approved | unchanged | unchanged |
| Test approach | pending | pending | pending |
Question D5:
D5 — What should the battlefield show when map tiles fail to load?
Project: World Tank Atlas, build_v2_part2b.py:439-441 (Leaflet battlefield background).
ELI10: The battlefield background is live map tiles from OpenTopoMap (terrain) or ArcGIS (satellite). Offline, behind a strict network, or when OpenTopoMap throttles traffic (it's a free volunteer server), tiles fail quietly and the battle plays over a blank grey box with no explanation. The fix: if tiles fail, try the other provider once; if that fails too, fall back to the app's own drawn tactical schematic background and a small 'Map tiles unavailable' chip.
Stakes if we pick wrong: on a bad network the star feature looks broken, with tanks moving over grey nothing.
Recommendation: A because it reuses the schematic the app already draws, so failures look intentional.
Completeness: A=10/10, B=4/10
Pros / cons:
A) Fallback provider, then schematic + chip (recommended)
  ✅ Battle stays readable with real terrain or the drawn schematic, never a blank box
  ✅ The chip tells the viewer why it looks different instead of looking broken
  ❌ Needs a once-only retry guard so a flaky network doesn't flip providers back and forth
  (human: ~2h / CC: ~10 min)
B) Leave as is
  ✅ No work, and most broadband visitors never see a failure
  ✅ Nothing extra to test in the sim
  ❌ Offline or throttled viewers get a grey battlefield with no explanation
Net: a small guard so the battle never plays over an empty box.
Header: Tiles
Options:
A) Fallback + schematic (recommended)
On tileerror switch provider once; if that fails, show the tactical schematic background and a "Map tiles unavailable" chip.
B) Leave as is
No tile error handling; grey background on failure.

State: approved
Actual answer: A) Fallback + schematic (recommended), eng D5
Accepted scope: task T15: on the first Leaflet `tileerror` for a battle, switch to the other provider once (OpenTopoMap ↔ ArcGIS, guarded by a per-battle flag); if that layer also errors, remove tiles, draw the existing tactical schematic background, and show the chip "Map tiles unavailable".
History: none

### C2: Route points at a battle or tank that doesn't exist
Finding: C2, INFORMATIONAL, confidence 8/10, proposed `applyRoute()` (D9) calling `openBattlePage(battleId)` (`build_v2_part2a.py:480`) / `openTankPage` with an id from the URL; no lookup guard is specified, reviewer: Claude (plan-eng-review)
Plan baseline: D9 approves hash routes; the unknown-id behavior is unspecified.
Runtime evidence: ids are data keys like `raseiniai_1941` (`build_tank_atlas_app.py`); there's no routing today, so no current behavior to preserve.
Comparison grid:
| Choice | Current | A | B |
|---|---|---|---|
| C2 unknown route id | unspecified | open that section's index (`#/battles` or `#/tanks`), `replaceState` the hash, and show the D6 no-results component: `No battle matches "tigr"` + 3 suggestions | open the home map `#/map` silently |
| R1, A1, A2 | approved | unchanged | unchanged |
| Test approach | pending | pending | pending |
Question D6:
D6 — What happens when a link points at a battle or tank that doesn't exist?
Project: World Tank Atlas, the hash router approved in D9 (proposed applyRoute in build_v2_part2a.py).
ELI10: Once every battle and tank has a link, people will share them and sometimes mistype them, and an ID may get renamed later. Today nothing defines what the router does with '#/tanks/tigr'. It could hand an unknown ID to the page renderer and show a broken or empty page. Option A sends you to the tank (or battle) list, fixes the URL, and shows the same 'no results' message approved in D6 with suggestions. Option B quietly sends you to the home map.
Stakes if we pick wrong: a shared or old link shows a broken page, and the person who clicked it assumes the atlas is broken.
Recommendation: A because it reuses the approved no-results component and tells people what happened.
Completeness: A=10/10, B=6/10
Pros / cons:
A) Section index + no-results message (recommended)
  ✅ A bad link lands somewhere useful, with an explanation and suggestions to try next
  ✅ Reuses the D6 no-results component, so there's no new UI to design
  ❌ Needs one guard per route type (battle, tank) and a test for each
  (human: ~1h / CC: ~5 min)
B) Silently open the home map
  ✅ One fallback for every bad route, simplest to write
  ✅ Never shows an error state to anyone
  ❌ People who clicked a specific link land somewhere unrelated with no idea why
Net: a little guard code so bad links explain themselves.
Header: Bad link
Options:
A) Index + message (recommended)
Open the section index, replaceState the hash, show the no-results message with suggestions.
B) Silent home map
Redirect any unknown id to #/map without a message.

State: approved
Actual answer: A) Index + message (recommended), eng D6
Accepted scope: in T3, `applyRoute()` looks the id up in `BATTLES` / `TANKS`; if it's missing, open `#/battles` or `#/tanks`, `history.replaceState` the corrected hash (no extra Back entry), and render the D6 no-results component: `No battle matches "<id>"` / `No tank matches "<id>"`, with its 3 suggestions. Unknown top-level routes go to `#/map`.
History: none

### TA: Test tooling for the plan
Finding: TG1, CRITICAL, confidence 9/10, no tests or test config anywhere in `world-tank-atlas/` (0 test files; `pytest` 8.4.2 and Node v22.16.0 installed, Playwright not installed), reviewer: Claude (plan-eng-review)
Plan baseline: each task has a manual "Verify:" line; no automated tests.
Runtime evidence: 26 proposed code paths/flows, 0 covered; the build is deterministic (byte-identical rebuild probe), so a golden check is feasible.
Comparison grid:
| Choice | Current | A | B | C |
|---|---|---|---|---|
| TA test tooling | manual Verify lines | pytest (build reproducibility, data invariants, injected counts) + Playwright E2E suite in `world-tank-atlas/tests/` for the 14 [→E2E] flows | pytest build/data checks only; E2E flows stay manual Verify lines, run with `/qa` | manual Verify lines only |
| Regression contract | pending | pending | pending | pending |
| R1, A1, A2, C2 | approved | unchanged | unchanged | unchanged |
Question D7:
D7 — How should the plan's changes be tested?
Project: World Tank Atlas, world-tank-atlas/ (no tests; pytest and Node installed, Playwright not).
ELI10: The plan changes the build, adds a router, rewrites the simulator's playback and labels, and adds fallbacks for broken photos and map tiles. None of that has tests today. There are 26 behaviors to protect, and 14 only show up in a real browser (deep links, Back, play-to-end, blocked images). Option A adds two layers: fast Python checks (does the build reproduce, are tank/battle IDs unique, do counts match the data) and a Playwright browser suite that clicks through those 14 flows, including with Wikimedia and tile servers blocked. Option B keeps the Python checks and leaves the browser flows as a manual checklist.
Stakes if we pick wrong: without browser tests, a router or sim change can quietly break Back, deep links or the Ended state, and nobody notices until a visitor does.
Recommendation: A because the browser flows are exactly where this plan's risk is, and Playwright can block network hosts to test the fallbacks.
Completeness: A=10/10, B=7/10, C=3/10
Pros / cons:
A) pytest + Playwright E2E (recommended)
  ✅ Every approved behavior, including offline fallbacks and keyboard control, is checked on each rebuild
  ✅ Network blocking in Playwright makes the photo and tile fallbacks testable without being offline
  ❌ Adds package.json, Playwright and ~150 MB of browser binaries to the folder's toolchain
  (human: ~2 days / CC: ~1h)
B) pytest build/data checks + manual browser checklist
  ✅ No Node toolchain; the Python checks run in about a second
  ✅ Still catches build breakage, duplicate IDs and wrong counts automatically
  ❌ Router, playback and fallback regressions are only caught when someone runs the checklist
  (human: ~3h / CC: ~15 min)
C) Manual Verify lines only
  ✅ Nothing to set up or maintain
  ✅ The plan's Verify lines already describe each check
  ❌ Every one of the 26 behaviors depends on someone remembering to recheck it
Net: a real browser suite for the risky flows, or lighter checks with manual browser QA.
Header: Tests
Options:
A) pytest + Playwright (recommended)
Python checks for build/data/counts plus a Playwright suite covering the 14 browser flows, with network blocking for fallbacks.
B) pytest + manual QA
Python build/data/count checks; browser flows stay a manual checklist run via /qa.
C) Manual only
Keep only the plan's manual Verify lines.

State: approved
Actual answer: A) pytest + Playwright (recommended), eng D7
Accepted scope: task T16: `world-tank-atlas/tests/test_build.py` (pytest: byte-reproducible rebuild into a temp dir with `~/.gemini` absent; unique tank/battle ids; every edge and battle side references an existing tank; injected counts equal `len(TANKS)` / `len(BATTLES)`), plus `world-tank-atlas/tests/e2e/*.spec.ts` (Playwright, `package.json` in `world-tank-atlas/`) covering the 14 [→E2E] flows, with `page.route` blocking `upload.wikimedia.org` and the tile hosts for the fallback tests. Each UI task (T3-T15) lands with its E2E spec.
History: none

### RG: Regression contract for existing behavior
Finding: RG1, CRITICAL, confidence 9/10, rewrites of the existing sim (`build_v2_part2b.py:346-381` play/scrub, `:1258` canvas click → `openTankPopup`), map popup and header (`build_v2_part1.py`), and view switching (`build_v2_part2a.py:445` `switchMainView`), reviewer: Claude (plan-eng-review)
Plan baseline: tooling approved (D7 A); what must keep working is unspecified.
Runtime evidence: 27 battles and 86 tanks in data (rebuild probe); each battle has `winner`, `side_a`, `side_b`; the views are map, battle-page, tank-page, graph, duel, matrix (`view-*` ids on the live page).
Comparison grid:
| Choice | Current | A | B |
|---|---|---|---|
| RG regression contract | none | all 27 battles + all 86 tanks parametrized; plus filters, other views, theme, console | 3 featured battles + 10 sampled tanks; same other assertions |
| TA tooling | approved (D7 A) | unchanged | unchanged |
Question D8:
D8 — How much existing behavior should the regression suite lock down?
Project: World Tank Atlas, Playwright + pytest approved in D7.
ELI10: Besides testing the new features, we need tests proving the redesign doesn't break what works today. Behavior to keep:
• Every battle opens and plays to its end.
• Every tank page opens.
• The era and nation filters show the same tanks and battles.
• The Lineage, Compare and Tech-tree views still render.
• The theme toggle still works.
• No view throws a console error.
Intentional changes that are NOT regressions: no popup on load, no autoplay, unit labels hidden until hover, emoji removed, counts from data, slim header. Option A checks all 27 battles and 86 tanks; option B checks a sample.
Stakes if we pick wrong: a sample can miss the one battle whose data shape breaks the new Ended overlay or router, which visitors then hit.
Recommendation: A because a parametrized test covers all 113 pages for little extra code, and the sim can jump to its end so the run stays short.
Completeness: A=10/10, B=6/10
Pros / cons:
A) All 27 battles + 86 tanks (recommended)
  ✅ Any battle or tank whose data breaks the new router, overlay or fallback fails the suite
  ✅ Same test code as the sample, just parametrized over the data ids
  ❌ Suite takes roughly 1-2 minutes instead of ~20 seconds
  (human: ~4h / CC: ~15 min)
B) 3 featured battles + 10 sampled tanks
  ✅ Fast run, about 20 seconds
  ✅ Covers the flagship battles most visitors open
  ❌ 24 battles and 76 tanks are never checked after the rewrite
Net: a slightly slower suite that checks every page against the rewrite.
Header: Regression
Options:
A) All pages (recommended)
Assert all 27 battles (route renders, play-to-end shows Ended with data winner) and all 86 tanks (route renders name + photo or blueprint); era/nation filter counts match data; Lineage/Compare/Tech-tree render; theme toggle swaps tokens; zero console errors on every route.
B) Sample pages
Same assertions over 3 featured battles and 10 sampled tanks only.

State: approved
Actual answer: A) All pages (recommended), eng D8
Accepted scope: task T17: `tests/e2e/regression.spec.ts` parametrized over every battle id (27) and tank id (86) read from the built page's `BATTLES` / `TANKS`.
- Each battle route renders the sim, and `setBattleSimProgress(100)` shows Ended naming the data `winner`.
- Each tank route renders its name plus a photo or blueprint.
- Era/nation filter pin counts equal the data counts.
- Lineage/Compare/Tech-tree render.
- The theme toggle swaps the `--surface` value.
- Zero console errors on every route.

The parts that exist today (filters, views, theme, console, tank/battle render) are written against the baseline page right after T0, before T2. Intentional changes (no popup on load, no autoplay, hidden unit labels, no emoji, data counts, slim header) are asserted as their new behavior in the owning task's spec, not as regressions.
History: none

### P1: Redraw only when something changed
Finding: P1, INFORMATIONAL, confidence 9/10, `build_v2_part2b.py:2272-2283` (`function tick() { ... } else if (state.mainView === 'battle-page') { drawBattleSimCanvas(); drawKillCamCanvas(); } requestAnimationFrame(tick); }`), reviewer: Claude (plan-eng-review)
Plan baseline: D7 pauses sim *progress* when hidden or paused; the draw loop is unspecified and keeps redrawing.
Runtime evidence: [measured: live page, pane hidden, ~30 fps] over 3 s: paused `drawBattleSimCanvas` 7.83 ms/frame (98 calls, 767 ms); idle `drawWorldMap` 1.46 ms/frame (90 calls); `drawKillCamCanvas` 0.41 ms/frame. Phone cost is [estimated] several times higher, not measured.
Comparison grid:
| Choice | Current | A | B |
|---|---|---|---|
| P1 draw scheduling | every frame for the active view, playing or not | draw only while playing or when a `state.dirty` flag is set (hover/selection change, scrub, resize, route, theme); kill-cam canvas draws only while in the viewport (IntersectionObserver) | unchanged |
| D7 playback states | approved (design) | unchanged | unchanged |
Question D9:
D9 — Stop redrawing the battlefield when nothing is moving?
Project: World Tank Atlas, the tick() loop in build_v2_part2b.py:2272-2283.
ELI10: The app redraws the whole battlefield about 30-60 times a second, even when the battle is paused and nothing moves. I measured 7.8 ms per redraw for a paused Raseiniai on this Mac, roughly a quarter of the browser's main thread spent repainting a still picture. Phones are slower, so a paused battle likely makes scrolling and the new bottom sheet stutter and drains battery. The fix: redraw only while playing, or once when something changes (hover, selection, scrubbing, resize, theme). The below-the-fold kill-cam canvas only draws while visible.
Stakes if we pick wrong: on phones the new bottom sheet and scrolling may stutter, because a paused battle keeps the main thread busy.
Recommendation: A because the D7 playback states already define when the picture changes, so a dirty flag is a small addition.
Completeness: A=10/10, B=4/10
Pros / cons:
A) Redraw only while playing or when marked dirty (recommended)
  ✅ A paused battle or idle map costs nearly nothing, keeping scroll and the sheet smooth on phones
  ✅ Reuses D7's playing flag; kill-cam stops drawing when it's scrolled away
  ❌ Every input that changes the picture must set the dirty flag, or the screen goes stale
  (human: ~3h / CC: ~15 min)
B) Leave the loop as is
  ✅ No risk of a stale frame from a missed dirty flag
  ✅ No change to the draw code at all
  ❌ Paused battles keep burning about 8 ms per frame on desktop and more on phones
Net: a dirty flag to stop repainting a still battlefield.
Header: Redraw
Options:
A) Draw when dirty (recommended)
Draw while playing or when state.dirty is set; kill-cam only draws in the viewport.
B) Leave as is
Keep redrawing every frame.

State: approved
Actual answer: A) Draw when dirty (recommended), eng D9
Accepted scope: task T18: `tick()` draws the battle canvas only while `state.sim.playing` or when `state.dirty` is set. `state.dirty` is set by hover/selection change, scrub, resize, route change, theme toggle and tile fallback, and cleared after a draw. The map canvas draws only when dirty. The kill-cam canvas draws only while an IntersectionObserver reports it in the viewport. Verify: rerun the 3 s probe; paused battle and idle map show ~0 draw calls.
History: none

### Correction E4 (no behavior change)
D9's example route `#/battles/raseiniai-1941` becomes `#/battles/raseiniai_1941`: routes use the data `id` values verbatim (`build_tank_atlas_app.py`: `"id": "raseiniai_1941"`), so no kebab/snake mapping list exists to drift. Router shape: the hash is the single owner of navigation. `switchMainView` (`build_v2_part2a.py:445`) and the `open*()` functions only set `location.hash`; one `hashchange` → `applyRoute()` calls the existing render functions (design-twice pick A over pushState mirroring, which would split ownership).

Approval readiness: PASS. R1 (eng D3), A1 (eng D4), A2 (eng D5), C2 (eng D6), TA (eng D7), RG (eng D8), P1 (eng D9). T0 S1-S4 are carried under design D24 (option C). C1 is carried under design D16.

### Eng review findings and dispositions

| # | Section | Finding | Disposition |
|---|---|---|---|
| S5 | Scope | `[CRITICAL] (9/10)` no version control (`git rev-parse` fails) | accepted, eng D3 → TB |
| S1-S4 | Scope | `[CRITICAL] (9/10)` `assemble_v2.py:3` scratch import wins over local files; `:13` polygon self-read; `render_html.py:1929` legacy writer; `:52` second output into `~/.gemini` | carried, design D24 → T0 |
| A1 | Architecture | `[INFORMATIONAL] (9/10)` `build_v2_part1.py:8-9` Tailwind loaded twice, one from a Gemini dev URL | accepted, eng D4 → T1 |
| A2 | Architecture | `[INFORMATIONAL] (8/10)` `build_v2_part2b.py:439-441` no `tileerror` handling | accepted, eng D5 → T15 |
| C1 | Code quality | `[INFORMATIONAL] (8/10)` `build_v2_part2b.py:1247` 15px hit radius vs 44px touch target | carried, design D16 → T7 note |
| C2 | Code quality | `[INFORMATIONAL] (8/10)` router has no unknown-id behavior | accepted, eng D6 → T3 note |
| TG1 | Tests | `[CRITICAL] (9/10)` 0/26 planned paths tested; no framework | accepted, eng D7 → T16 |
| RG1 | Tests | `[CRITICAL] (9/10)` rewrite of sim/header/views with no regression contract | accepted, eng D8 → T17 |
| P1 | Performance | `[INFORMATIONAL] (9/10)` `build_v2_part2b.py:2272` paused sim redraws at 7.83 ms/frame [measured] | accepted, eng D9 → T18 |

Suppressed (confidence ≤ 4): none.

### NOT in scope (eng)

- Hosting/deploy: the atlas is a local static file; no CI, publish target or remote. Add with a separate change if it gets published.
- Build-time Tailwind compile: rejected in favor of one CDN plus config (D4); revisit with the loading-screen TODO.
- Splitting `build_v2_part2b.py` (2,305 lines) into modules: the arrangement stays as it is (eng D2).
- Pinning `cdn.tailwindcss.com` to a version: Leaflet is pinned (`leaflet@1.9.4`), Tailwind's Play CDN isn't. Low risk, not raised.

### What already exists (eng)

- **Build:** `assemble_v2.py` is the only live entry point (import chain `enrich_v3_80tanks` → `enrich_vietnam_and_media` → `build_tank_atlas_app` / `generate_data` / `expand_tanks`, plus `battle_timelines_and_destruction`, `build_v2_part1/2a/2b`). It rebuilds the current page byte-for-byte (E3).
- **Navigation:** one `switchMainView(view)` (`build_v2_part2a.py:445`), the router's single hook.
- **Sim:** a global `state.sim` (`playing`, `progress`, `speed`, `logs`), `toggleSimPlay` / `restartBattleSim` / `setBattleSimProgress` (`build_v2_part2b.py:346-381`), canvas hit-testing via `simScreenAgents` (`:1242-1262`), one `tick()` loop (`:2272`). D7, D10 and D18 extend these; nothing is rebuilt.
- **Data checks:** an early-stage validation prints "0 broken IDs" for the 53-tank set only. T16 covers the final 86/27 set.

### Diagrams

```
BUILD (after T0)
world_polygons.json ─┐
generate_data ─► build_tank_atlas_app ─► enrich_vietnam ─► enrich_v3 ─┐
battle_timelines_and_destruction ─────────────────────────────────────┤
build_v2_part1 / 2a / 2b (HTML+JS strings) ──────────────────────────┼─► assemble_v2.py ─► world_tanks_atlas.html (only output)
                                                                       └── counts = len(TANKS), len(BATTLES)

ROUTING (T3)
click / open*() ──► location.hash = '#/battles/<id>'
                         │ hashchange (also on load)
                         ▼
                   applyRoute() ── id in BATTLES/TANKS? ──no──► replaceState('#/battles') + no-results msg
                         │ yes
                         ▼
                   switchMainView(view) + openBattlePage(id) / openTankPage(id) ──► state.dirty = true

SIM STATES (T6/T7/T18)
 Ready ──Play/Space──► Playing ──progress ≥ 0.999──► Ended ──Replay──► Ready
   ▲                    │  ▲
   │       Pause/hidden/off-screen/unit click   Play/Esc
   │                    ▼  │
   └────Replay──────── Paused        tick(): draw if playing || state.dirty
```

Inline-comment candidates when implementing: `applyRoute()` (route table + fallback), the sim state transitions in `build_v2_part2b.py`, and the tile-fallback guard.

### Failure modes

| New path | Realistic failure | Test | Handling | User sees |
|---|---|---|---|---|
| Build | scratch folder gone or polygons missing | T16 build test | T0 vendoring + JSON file | build error, not a broken page |
| Router | mistyped or renamed id | T16 E2E | D6 index + message | clear message |
| Sim playback | `progress` never reaches end for a battle | T17 per battle | Ended at ≥ 0.999 | regression caught in tests |
| Map tiles | OpenTopoMap throttled / offline | T15 E2E (blocked hosts) | provider switch → schematic | chip "Map tiles unavailable" |
| Photos | Wikimedia blocked | T13 E2E | blueprint fallback | "Photo unavailable" |
| Dirty-flag draw | an input forgets to set `dirty` | T18 hover-after-pause check | n/a | stale frame (caught by test) |

Critical gaps (no test, no handling, silent): 0.

### Worktree parallelization strategy

| Step | Modules touched | Depends on |
|------|----------------|------------|
| TB, T0 | repo root, `tank_atlas_src/` build | — |
| T16 pytest, T17 baseline | `tests/` | T0 |
| T1, T2, T4, T12 | `tank_atlas_src/` part1 (+ part2a) | T0 |
| T3, T13 | `tank_atlas_src/` part2a | T0 |
| T5-T8, T11, T14, T15, T18, T9 | `tank_atlas_src/` part2b (+ part1 for T9) | T1, T3 |
| E2E specs per task | `tests/e2e/` | owning task |

- **Lane A:** TB → T0 → T1 → T2/T3 → sim tasks → T9-T14 (all touch the same three generator files, so sequential).
- **Lane B:** T16 + T17 (the `tests/` module) in parallel with T1-T3 once T0 is merged.
- **Execution order:** TB, T0. Then launch Lane A (T1) and Lane B together. Merge B before T5 so the sim tasks run against the regression suite.
- **Conflict flags:** every UI task shares `build_v2_part2b.py` / `build_v2_part1.py`; never run two UI tasks in parallel worktrees.

### Reality rows

```
REALITY: premise-table pass 10 premises checked; unverified=1 (phone draw cost estimated) assemble_v2.py:3, assemble_v2.py:13, render_html.py:13, build_v2_part1.py:8, build_v2_part2a.py:480, build_v2_part2b.py:441, build_v2_part2b.py:2272
REALITY: already-done pass no git history exists; no hashchange/pushState in build_v2_part1/2a/2b (grep 0), nothing in the plan is built build_v2_part2a.py:445
REALITY: surface-check pass python3 -m http.server --bind/--directory (--help), pytest 8.4.2, node v22.16.0 verified; Playwright not installed, T16 adds it .claude/launch.json:5
REALITY: binding-decisions pass gstack-decision-search returned none; plan has no Binding decisions section; design D3-D21/D24 honored UX_PLAN.md:33
REALITY: numbers pass draw costs [measured: live page], 754,548-byte rebuild [measured], 86/27/194 [measured: get_v3_data]; effort figures [estimated] UX_PLAN.md:322
REALITY: deferred-asks pass no linked issue UX_PLAN.md:1
REALITY: pr-count pass no ship-policy, no remote; one commit per task in a single local repo (TB) UX_PLAN.md:327
```

### Eng Review Completion Summary

- Step 0: Scope Challenge: scope accepted as-is
- Reality rows: 7/7 applicable rows emitted, 1 unverified premise
- Architecture Review: 2 issues found (A1, A2)
- Code Quality Review: 2 issues found (C1, C2)
- Test Review: diagram produced, 26 gaps identified (TG1, RG1)
- Performance Review: 1 issue found (P1)
- NOT in scope: written
- What already exists: written
- TODOS.md updates: 0 items proposed (every finding got an approved fix)
- Failure modes: 0 critical gaps flagged
- Unresolved decisions: 0 in this review
- Outside voice: codex not installed; native Plan-agent fallback stopped at the user's request, so outside_status: skipped
- Parallelization: 2 lanes, 1 parallel (tests) / 1 sequential (UI)
- Lake Score: 5/6 (D5, D6, D7, D8, D9 picked the 10/10 option; D4 picked 8/10)
- Corrections to the design review: E1, E2, E5 (premises in T0 were overstated; behavior unchanged)

Test plan: kept locally in gstack's project folder for world-tank-atlas (eng review test plan, 2026-11-05); not in this repo.

## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO Review | `/plan-ceo-review` | Scope & strategy | 0 | — | — |
| Outside Review | codex (`/plan-eng-review` outside voice; native fallback) | Independent 2nd opinion | 1 | skipped | codex not installed; native fallback stopped at user request |
| Eng Review | `/plan-eng-review` | Architecture & tests (required) | 1 | issues_open | 7 issues, 0 critical gaps (all 7 have approved fixes) |
| Design Review | `/plan-design-review` | UI/UX gaps | 1 | issues_open | score: 1/10 → 8/10, 20 decisions |
| DX Review | `/plan-devex-review` | Developer experience gaps | 0 | — | — |

- **OUTSIDE COVERAGE:**
  - Design phase: outside voices skipped (design D2).
  - Plan-review phase: Codex not installed, and the native Plan-agent fallback was stopped at the user's request (skipped).
  - No external provider completed.
- **VERDICT:** no reviews CLEAR. The eng review is complete, with every finding mapped to an approved task (status issues_open counts mapped work, not failures). The plan is ready to implement starting at TB → T0.

**UNRESOLVED DECISIONS:**
- + 2 unresolved from prior reviews (design review: 2 items deferred to TODOS.md)

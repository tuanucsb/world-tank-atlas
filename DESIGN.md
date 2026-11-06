# World Tank Atlas: Design System

Source: design review D14 (2026-11-05). Tokens live in the `<style>` and
`tailwind.config` blocks at the top of `tank_atlas_src/build_v2_part1.py`.
Use tokens only; no new raw hex values in markup.

## Use scene

History readers and wargamers at a desk or on a phone, often in the evening.
Dark is the default; light is one toggle away (`html.light-theme`).

## Color tokens

| Token | Dark | Light | Use |
|---|---|---|---|
| `--surface` | `#111611` | `#eef0ea` | page / map ground |
| `--surface-raised` | `#1a211a` | `#ffffff` | panels, sheet, bars, photo placeholder |
| `--text` | `#ecefe6` | `#1b2118` | body |
| `--text-muted` | `#a9b2a0` | `#4f5a4a` | secondary (≥ 4.5:1 on surface) |
| `--border-token` | `#2e3a2e` | `#c9cfc2` | dividers |
| `--accent` | `#f2a93b` | `#935a00` | selection, active phase, active tab (light value darkened from D14 `#b86e00`, which measured 3.99:1 on white) |
| `--focus` | `#f2a93b` | `#935a00` | 2px focus ring, 2px offset |
| `--side-a` | `#4f8fe8` | `#1f5fbf` | Side A units, force bar, table column |
| `--side-b` | `#e5534b` | `#c0342b` | Side B units, force bar, table column |
| `--tint-east` | `#8a3b3b33` | `#c0342b1f` | E. Front theatre polygon |
| `--tint-desert` | `#8a733b33` | `#b86e001f` | N. Africa / Middle East polygons |
| `--tint-asia` | `#3b7a5a33` | `#2f7a521f` | Asia polygons |

### Tailwind palettes

Tailwind's palette names resolve to token ramps (`rgb(var(--x-NNN) / <alpha-value>)`),
so existing classes follow the theme:

| Tailwind names | Ramp | Meaning |
|---|---|---|
| `white`, `slate`, `gray`, `zinc` | `--n-*` (`white` = `--n-50`) | neutrals (inverted in light theme: 950 = ground, 100 = text) |
| `amber`, `yellow`, `orange` | `--acc-*` | accent |
| `sky`, `cyan`, `blue`, `indigo`, `violet`, `purple`, `fuchsia`, `pink` | `--sa-*` | Side A / cool highlight |
| `rose`, `red` | `--sb-*` | Side B |
| `emerald`, `green`, `teal`, `lime` | `--ok-*` | winner / success (dark 400 `#4cc38a`, light 400 `#2f7a52`) |

Canvas drawing (map, battlefield, kill-cam) still uses literal hex colors on a
fixed dark canvas (`--canvas-bg`); move those to tokens when the simulator
tasks (T5-T8) touch that code.

## Type

- UI: IBM Plex Sans 400/500/600/700. Wordmark only: Barlow Condensed 600.
- Scale: 14 / 16 / 20 / 28px; body 16px, line-height 1.5; headings 1.25.
- Floor: nothing renders below 14px (`text-xs` is 14px).
- Counts and stats: `font-variant-numeric: tabular-nums`.

## Space, shape, motion

- Spacing: 4, 8, 12, 16, 24, 32, 48px.
- Radius: 6px controls, 10px panels and sheet.
- UI motion: 150ms ease-out. Simulator effects keep their own timing and
  respect `prefers-reduced-motion`.
- Touch targets: at least 44×44px.

## Browser surfaces

`::selection` uses the accent at 30%, the caret is the accent,
`scrollbar-color` comes from the neutral ramp, and every focusable element
shows the `--focus` ring.

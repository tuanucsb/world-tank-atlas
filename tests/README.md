# Tests

Run from `world-tank-atlas/`:

```bash
npm install          # once: installs @playwright/test
npm test             # pytest build/data checks, then the Playwright suite
```

- `python3 -m pytest tests/` checks the build (the committed page matches a fresh build, builds are
  deterministic, inline scripts parse) and the data (86 tanks, 27 battles, ids, fields, references).
- `npx playwright test` runs the browser suite on the installed Google Chrome. Set `PW_CHANNEL=chromium`
  to use Playwright's own build instead (after `npx playwright install chromium`).
- The browser suite is offline: Tailwind and Leaflet are cached in `tests/.cdn-cache/` on the first run
  (git-ignored); photos, map tiles, fonts and videos are blocked, which also exercises the fallbacks.
  Any console error fails a test.
- On a busy machine, run with fewer workers (`npx playwright test --workers=2`); timeouts under heavy
  load are not page failures, so re-run them with `--last-failed` before digging in.

| Spec | Covers |
|---|---|
| `e2e/navigation.spec.ts` | app bar (T2), first load (T4), router and moment links (T3, B4), keyboard tabs (T10), search and filters (T12), theme |
| `e2e/simulator.spec.ts` | theater fit and playback states (T5, T6), phase stops (B8), unit select (T7), reduced motion (T11), tile fallback (T15), drawing only when needed (T18) |
| `e2e/layout.spec.ts` | phone and tablet layouts (T9, T14), photo fallback (T13) |
| `e2e/loading.spec.ts` | first-load screen: shown before styles, slow and failed loads, removed once styled |
| `e2e/regression.spec.ts` | all 27 battles open and play to the end, all 86 tanks open, the other views and the conflict filters (T17) |

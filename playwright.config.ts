import { defineConfig } from '@playwright/test';

// Runs on the installed Google Chrome by default, so no browser download is needed.
// PW_CHANNEL=chromium uses Playwright's own build (after `npx playwright install chromium`).
const channel = process.env.PW_CHANNEL || 'chrome';
const PORT = 8798;

export default defineConfig({
  testDir: 'tests/e2e',
  timeout: 60_000,
  expect: { timeout: 10_000 },
  fullyParallel: true,
  retries: process.env.CI ? 1 : 0,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: `http://127.0.0.1:${PORT}/`,
    channel: channel === 'chromium' ? undefined : channel,
    viewport: { width: 1440, height: 900 },
    trace: 'retain-on-failure',
  },
  webServer: {
    command: `python3 -m http.server ${PORT} --bind 127.0.0.1`,
    url: `http://127.0.0.1:${PORT}/world_tanks_atlas.html`,
    reuseExistingServer: !process.env.CI,
    stdout: 'ignore',
    stderr: 'ignore',
  },
});

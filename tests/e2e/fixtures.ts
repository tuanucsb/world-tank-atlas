import { test as base, expect, Page } from '@playwright/test';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

// Tests run offline. Tailwind and Leaflet come from a local cache filled on the first run
// (tests/.cdn-cache, git-ignored); every other outside request (photos, map tiles, fonts,
// video embeds) is aborted, which also exercises the photo and tile fallbacks.
const CACHE_DIR = path.join(__dirname, '..', '.cdn-cache');
const CACHED_HOSTS = new Set(['cdn.tailwindcss.com', 'unpkg.com']);

async function serveCdn(route: import('@playwright/test').Route) {
  const url = route.request().url();
  const file = path.join(CACHE_DIR, createHash('sha1').update(url).digest('hex'));
  if (fs.existsSync(file + '.json')) {
    const { contentType } = JSON.parse(fs.readFileSync(file + '.json', 'utf8'));
    return route.fulfill({ status: 200, contentType, body: fs.readFileSync(file) });
  }
  const res = await route.fetch({ timeout: 120_000 });
  const body = await res.body();
  if (res.ok()) {
    // Write-then-rename, body before its .json marker, so parallel workers never read half a file
    fs.mkdirSync(CACHE_DIR, { recursive: true });
    const tmp = `${file}.${process.pid}.tmp`;
    fs.writeFileSync(tmp, body);
    fs.renameSync(tmp, file);
    fs.writeFileSync(tmp, JSON.stringify({ url, contentType: res.headers()['content-type'] || '' }));
    fs.renameSync(tmp, file + '.json');
  }
  return route.fulfill({ response: res, body });
}

type Fixtures = { errors: string[] };

export const test = base.extend<Fixtures>({
  page: async ({ page }, use) => {
    await page.route(url => url.hostname !== '127.0.0.1' && url.hostname !== 'localhost', route => {
      const host = new URL(route.request().url()).hostname;
      return CACHED_HOSTS.has(host) ? serveCdn(route) : route.abort('internetdisconnected');
    });
    await use(page);
  },
  // Fails the test on any script error or console error, except the aborted outside requests
  errors: [async ({ page }, use) => {
    const errors: string[] = [];
    page.on('pageerror', e => errors.push(`pageerror: ${e.message}`));
    page.on('console', m => {
      if (m.type() === 'error' && !/Failed to load resource|net::ERR_/.test(m.text())) errors.push(m.text());
    });
    await use(errors);
    expect(errors, 'console errors').toEqual([]);
  }, { auto: true }],
});

export { expect };

// Opens the page at a route and waits until Tailwind is loaded and the app has started
// (DOMContentLoaded handler done: it requests the first frames)
export async function openAtlas(page: Page, hash = '#/map') {
  await page.goto('world_tanks_atlas.html' + hash, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() =>
    typeof (window as any).tailwind !== 'undefined' &&
    // @ts-ignore page globals
    typeof drawUntil === 'number' && drawUntil > 0, null, { timeout: 30_000 });
}

// Battle and tank data straight from the built page, so tests follow the data
export function atlasData(): { battles: any[]; tanks: any[] } {
  const html = fs.readFileSync(path.join(__dirname, '..', '..', 'world_tanks_atlas.html'), 'utf8');
  const grab = (name: string) => JSON.parse(html.match(new RegExp(`^\\s*const ${name} = (.*);$`, 'm'))![1]);
  return { battles: grab('BATTLES'), tanks: grab('TANKS') };
}

// Frames the page actually draws over ms (T18 counter)
export async function framesDrawn(page: Page, ms: number) {
  // @ts-ignore page globals
  return page.evaluate(async (ms) => { const f0 = drawFrames; await new Promise(r => setTimeout(r, ms)); return drawFrames - f0; }, ms);
}

// The battle page's simulator state
export async function simState(page: Page) {
  // @ts-ignore page globals
  return page.evaluate(() => ({ status: state.sim.status, progress: state.sim.progress, speed: state.sim.speed, selected: state.sim.selectedAgentId }));
}

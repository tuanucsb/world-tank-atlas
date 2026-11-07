import { test, expect, openAtlas, simState, framesDrawn } from './fixtures';

// T5 theater, T6 states, T7 unit select, B8 phase stops, T11 reduced motion, T15 tiles, T18 drawing

const BATTLE = '#/battles/kursk_1943';

async function play(page: import('@playwright/test').Page, { stops = false } = {}) {
  // @ts-ignore page globals
  await page.evaluate((stops) => setStopAtPhases(stops), stops);
  await page.getByRole('button', { name: 'Play the battle' }).click();
  // Left Ready; a start just before a phase or the end may already have stopped again
  await expect.poll(async () => (await simState(page)).status).not.toBe('ready');
}

test.describe('theater and states (T5, T6)', () => {
  test('battlefield and control bar fit under the app bar at 1440x900', async ({ page }) => {
    await openAtlas(page, BATTLE);
    for (const sel of ['.sim-stage', '#sim-controls']) {
      const box = (await page.locator(sel).boundingBox())!;
      expect(box.y).toBeGreaterThanOrEqual(56);
      expect(box.y + box.height).toBeLessThanOrEqual(900);
    }
  });

  test('opens Ready, plays, pauses on Space, resumes', async ({ page }) => {
    await openAtlas(page, BATTLE);
    expect((await simState(page)).status).toBe('ready');
    await expect(page.locator('#sim-overlay-ready')).toBeVisible();
    await play(page);
    const p0 = (await simState(page)).progress;
    await expect.poll(async () => (await simState(page)).progress).toBeGreaterThan(p0);
    await page.locator('body').press(' ');
    expect((await simState(page)).status).toBe('paused');
    await page.locator('body').press(' ');
    expect((await simState(page)).status).toBe('playing');
  });

  test('scrolling the battlefield away pauses it', async ({ page }) => {
    await openAtlas(page, BATTLE);
    await play(page);
    await page.locator('#battle-details').scrollIntoViewIfNeeded();
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await expect.poll(async () => (await simState(page)).status).toBe('paused');
  });

  test('reaching the end shows the result overlay', async ({ page }) => {
    await openAtlas(page, BATTLE);
    // @ts-ignore page globals
    await page.evaluate(() => { scrubBattleSim(0.985); setSimSpeed(2); });
    await play(page);
    await expect(page.locator('#sim-overlay-ended')).toBeVisible({ timeout: 20_000 });
    expect((await simState(page)).status).toBe('ended');
  });

  test('stops at the start of the next phase with a card (B8)', async ({ page }) => {
    await openAtlas(page, BATTLE);
    const r0 = await page.evaluate(() => {
      // @ts-ignore page globals
      const b = BATTLE_MAP[state.selectedBattleId], ph = b.phases[1];
      return ph.range && typeof ph.range[0] === 'number' ? ph.range[0] : 1 / b.phases.length;
    });
    // @ts-ignore page globals
    await page.evaluate((r0) => { scrubBattleSim(r0 - 0.01); setSimSpeed(2); }, r0);
    await play(page, { stops: true });
    await expect(page.locator('#sim-overlay-phase')).toBeVisible({ timeout: 20_000 });
    expect((await simState(page)).status).toBe('paused');
    await expect(page.locator('#sim-overlay-phase')).toContainText('Phase 2');
  });

  test('arrow keys jump between phases', async ({ page }) => {
    await openAtlas(page, BATTLE);
    const label = page.locator('#sim-phase-label');
    const before = await label.innerText();
    await page.locator('body').press('ArrowRight');
    await expect(label).not.toHaveText(before);
  });
});

test.describe('unit select (T7)', () => {
  test('clicking a unit pauses, shows its card; Esc resumes', async ({ page }) => {
    await openAtlas(page, BATTLE);
    await play(page);
    // @ts-ignore page globals
    const pt = await page.evaluate(() => { const a = simScreenAgents.find((x: any) => !x.isWreck) || simScreenAgents[0]; const r = document.getElementById('battle-sim-canvas')!.getBoundingClientRect(); return { x: r.left + a.x, y: r.top + a.y }; });
    await page.mouse.click(pt.x, pt.y);
    await expect.poll(async () => (await simState(page)).selected).not.toBeNull();
    await expect(page.locator('#sim-unit-card')).toBeVisible();
    expect((await simState(page)).status).toBe('paused');
    await page.keyboard.press('Escape');
    await expect(page.locator('#sim-unit-card')).toBeHidden();
    expect(await simState(page)).toMatchObject({ selected: null, status: 'playing' });
  });
});

test.describe('reduced motion (T11)', () => {
  test.use({ reducedMotion: 'reduce' });
  test('speed defaults to 0.5x and the kill-cam holds one frame', async ({ page }) => {
    await openAtlas(page, BATTLE);
    expect((await simState(page)).speed).toBe(0.5);
    await page.locator('#killcam-canvas').scrollIntoViewIfNeeded();
    await page.waitForTimeout(1200);
    expect(await framesDrawn(page, 800)).toBe(0);
  });
});

test.describe('map tiles (T15)', () => {
  test('both providers down: grid plus "Map tiles unavailable", no retry', async ({ page }) => {
    await openAtlas(page, BATTLE);
    await page.locator('#sim-bg-topo').click();
    await expect(page.locator('#sim-tile-chip')).toBeVisible();
    await expect(page.locator('#sim-tile-chip')).toContainText('Map tiles unavailable');
    await expect(page.locator('#battle-sim-leaflet-map')).toBeHidden();
    await page.locator('#sim-bg-historical').click();
    await expect(page.locator('#sim-tile-chip')).toBeHidden();
    await page.locator('#sim-bg-topo').click();
    await expect(page.locator('#sim-tile-chip')).toBeVisible();
    // @ts-ignore page globals
    expect(await page.evaluate(() => tileProviderIdx.topo)).toBe(2);
  });

  test('first provider down: the second one is used', async ({ page }) => {
    const png = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=', 'base64');
    await page.route('https://server.arcgisonline.com/**', route => route.fulfill({ status: 200, contentType: 'image/png', body: png }));
    await openAtlas(page, BATTLE);
    await page.locator('#sim-bg-topo').click();
    await expect(page.locator('#sim-tile-credit')).toContainText('Esri World Topo Map');
    await expect(page.locator('#battle-sim-leaflet-map .leaflet-tile-loaded').first()).toBeAttached();
    await expect(page.locator('#sim-tile-chip')).toBeHidden();
    // @ts-ignore page globals
    expect(await page.evaluate(() => tileProviderIdx.topo)).toBe(1);
  });
});

test.describe('drawing only when needed (T18)', () => {
  test('idle map draws nothing; a hover redraws', async ({ page }) => {
    await openAtlas(page);
    await expect.poll(() => framesDrawn(page, 500), { timeout: 15_000 }).toBe(0);
    await page.mouse.move(600, 500);
    await page.mouse.move(640, 520);
    expect(await framesDrawn(page, 300)).toBeGreaterThan(0);
  });

  test('ready and paused battles draw nothing; playing draws', async ({ page }) => {
    await openAtlas(page, BATTLE);
    await expect.poll(() => framesDrawn(page, 500), { timeout: 15_000 }).toBe(0);
    await play(page);
    expect(await framesDrawn(page, 500)).toBeGreaterThan(5);
    await page.locator('body').press(' ');
    await expect.poll(() => framesDrawn(page, 500), { timeout: 15_000 }).toBe(0);
    const box = (await page.locator('#battle-sim-canvas').boundingBox())!;
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    expect(await framesDrawn(page, 300)).toBeGreaterThan(0);
  });

  test('the kill-cam animates only while on screen', async ({ page }) => {
    await openAtlas(page, BATTLE);
    // @ts-ignore page globals
    const tick = () => page.evaluate(() => state.sim.killcamTick || 0);
    await page.locator('#killcam-canvas').scrollIntoViewIfNeeded();
    await expect.poll(async () => { const t = await tick(); await page.waitForTimeout(400); return (await tick()) - t; }).toBeGreaterThan(5);
    await page.evaluate(() => window.scrollTo(0, 0));
    await expect.poll(async () => { const t = await tick(); await page.waitForTimeout(400); return (await tick()) - t; }, { timeout: 15_000 }).toBe(0);
  });
});

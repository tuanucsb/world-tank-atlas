import { test, expect, openAtlas } from './fixtures';

// T9 responsive, T13 photo fallback, T14 details table on phones

const noSideScroll = (page: import('@playwright/test').Page) =>
  page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);

test.describe('phone (T9, T14)', () => {
  test.use({ viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true });

  for (const hash of ['#/map', '#/battles/kursk_1943', '#/tanks/tiger_i', '#/lineage', '#/compare', '#/tech-tree']) {
    test(`no sideways scroll on ${hash}`, async ({ page }) => {
      await openAtlas(page, hash);
      await expect.poll(() => noSideScroll(page)).toBeLessThanOrEqual(0);
    });
  }

  test('48px app bar; battlefield and controls on screen', async ({ page }) => {
    await openAtlas(page, '#/battles/kursk_1943');
    await expect.poll(async () => (await page.locator('#app-bar > div').first().boundingBox())?.height).toBe(48);
    for (const sel of ['.sim-stage', '#sim-controls']) {
      const box = (await page.locator(sel).boundingBox())!;
      expect(box.y).toBeGreaterThanOrEqual(0);
      expect(box.y + box.height).toBeLessThanOrEqual(812);
    }
  });

  test('details table stacks: label on top, two sides below', async ({ page }) => {
    await openAtlas(page, '#/battles/kursk_1943');
    const table = page.locator('.battle-compare');
    await table.scrollIntoViewIfNeeded();
    expect(await table.evaluate(t => t.scrollWidth <= t.clientWidth + 1)).toBe(true);
    const a = (await table.locator('th.side-a').boundingBox())!;
    const b = (await table.locator('th.side-b').boundingBox())!;
    expect(b.x).toBeGreaterThan(a.x + a.width - 1);
  });
});

test.describe('tablet sheet (T9)', () => {
  for (const width of [768, 1023]) {
    test(`story panel is a bottom sheet at ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 1024 });
      await openAtlas(page, '#/battles/kursk_1943');
      const sheet = page.locator('.sim-panel.sheet');
      await expect(sheet).toBeVisible();
      expect(await sheet.evaluate(el => getComputedStyle(el).position)).toBe('fixed');
      await expect(sheet.locator('.sheet-handle')).toBeVisible();
      await expect.poll(() => noSideScroll(page)).toBeLessThanOrEqual(0);
    });
  }
});

test.describe('photo fallback (T13)', () => {
  test('failed tank photos become blueprints marked "Photo unavailable"', async ({ page }) => {
    // Every outside request is aborted by the fixture, so every photo fails
    await openAtlas(page, '#/tanks');
    const fallbacks = page.locator('#view-tank-page .photo-fallback');
    await expect.poll(() => fallbacks.count()).toBeGreaterThan(5);
    const first = fallbacks.first();
    await expect(first.locator('svg')).toBeAttached();
    await expect(first).toHaveAttribute('aria-label', /photo unavailable/);
  });

  test('a fallback keeps the photo slot size', async ({ page }) => {
    await page.route(/upload\.wikimedia\.org/, route => route.abort());
    await openAtlas(page, '#/tanks/tiger_i');
    const box = page.locator('#view-tank-page .photo-fallback').first();
    await expect(box).toBeVisible();
    const size = (await box.boundingBox())!;
    expect(size.width).toBeGreaterThan(40);
    expect(size.height).toBeGreaterThan(30);
  });
});

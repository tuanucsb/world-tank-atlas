import { test, expect, openAtlas, atlasData, simState } from './fixtures';

// T17: every battle and every tank page still works. Console errors fail any test (fixture).

const { battles, tanks } = atlasData();

test.describe('every battle', () => {
  for (const b of battles) {
    test(`${b.id} opens, shows its details and plays to the end`, async ({ page }) => {
      await openAtlas(page, `#/battles/${b.id}`);
      await expect(page.locator('#view-battle-page')).toBeVisible();
      await expect(page.locator('#battle-header-title')).toContainText(String(b.year));
      expect((await simState(page)).status).toBe('ready');

      const details = page.locator('#battle-details');
      await expect(details.locator('.battle-compare tbody tr')).toHaveCount(7);
      await expect(details.locator('.killcam-item')).toHaveCount(b.killcam_scenarios.length);
      expect(await details.innerText()).not.toMatch(/[\u{1F300}-\u{1FAFF}]/u);

      // Ended overlay from near the end, without phase stops
      // @ts-ignore page globals
      await page.evaluate(() => { setStopAtPhases(false); scrubBattleSim(0.985); setSimSpeed(2); });
      await page.getByRole('button', { name: 'Play the battle' }).click();
      await expect(page.locator('#sim-overlay-ended')).toBeVisible({ timeout: 20_000 });
      const lost = await page.evaluate(() => [document.getElementById('sim-lost-a')!.textContent, document.getElementById('sim-lost-b')!.textContent]);
      expect(lost.every(t => /\d/.test(t || ''))).toBe(true);
    });
  }
});

test.describe('every tank', () => {
  for (const t of tanks) {
    test(`${t.id} page opens`, async ({ page }) => {
      await openAtlas(page, `#/tanks/${t.id}`);
      await expect(page.locator('#view-tank-page')).toBeVisible();
      await expect(page.locator('#tank-page-content')).toContainText(t.name);
      await expect(page.locator('#route-notice')).toBeHidden();
    });
  }
});

test.describe('other views', () => {
  for (const [hash, view] of [['#/lineage', '#view-graph'], ['#/compare', '#view-duel'], ['#/tech-tree', '#view-matrix'], ['#/tanks', '#view-tank-page'], ['#/battles', '#view-battle-page']]) {
    test(`${hash} renders`, async ({ page }) => {
      await openAtlas(page, hash);
      await expect(page.locator(view)).toBeVisible();
      expect(await page.locator(view).evaluate(el => el.innerText.trim().length)).toBeGreaterThan(20);
    });
  }

  test('conflict filters keep matching tanks and battles', async ({ page }) => {
    await openAtlas(page);
    for (const cf of ['ww2', 'vietnam', 'gulf', 'ukraine', 'all']) {
      await page.locator(`#cf-${cf}`).click();
      // @ts-ignore page globals
      const n = await page.evaluate(() => ({ tanks: TANKS.filter((t: any) => isTankVisible(t)).length, battles: BATTLES.filter((b: any) => isBattleVisible(b)).length }));
      expect(n.tanks, cf).toBeGreaterThan(0);
      if (cf !== 'gulf' && cf !== 'ukraine') expect(n.battles, cf).toBeGreaterThan(0);
    }
  });
});

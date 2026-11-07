import { test, expect, openAtlas } from './fixtures';

// T2 app bar, T3 router, T4 first load, T10 tabs, T12 search, theme

test.describe('app bar (T2)', () => {
  test('56px bar, 40px filter row on the map, plain title, counts from data', async ({ page }) => {
    await openAtlas(page);
    await expect(page).toHaveTitle(/World Tank Atlas/);
    await expect.poll(async () => (await page.locator('#app-bar > div').first().boundingBox())?.height).toBe(56);
    await expect.poll(() => page.locator('#filter-row').evaluate(el => el.clientHeight)).toBe(40); // inside its top border
    // @ts-ignore page globals
    const counts = await page.evaluate(() => [TANKS.length, BATTLES.length]);
    await expect(page.locator('#atlas-summary')).toContainText(`${counts[0]} tanks`);
    await expect(page.locator('#atlas-summary')).toContainText(`${counts[1]} battles`);
  });

  test('theme toggle switches light and dark', async ({ page }) => {
    await openAtlas(page);
    const html = page.locator('html');
    const startsLight = await html.evaluate(el => el.classList.contains('light-theme'));
    await page.locator('#theme-toggle-btn').click();
    await expect(html).toHaveClass(startsLight ? /^(?!.*light-theme)/ : /light-theme/);
    await page.locator('#theme-toggle-btn').click();
    expect(await html.evaluate(el => el.classList.contains('light-theme'))).toBe(startsLight);
  });
});

test.describe('first load (T4)', () => {
  test('no popup, no selection, nothing playing', async ({ page }) => {
    await openAtlas(page);
    await expect(page.locator('#tank-popup-modal')).toBeHidden();
    // @ts-ignore page globals
    expect(await page.evaluate(() => state.sim.status)).not.toBe('playing');
    await expect(page).toHaveURL(/#\/map$|world_tanks_atlas\.html$/);
  });
});

test.describe('router (T3, B4)', () => {
  test('tabs change the hash and the view', async ({ page }) => {
    await openAtlas(page);
    const views: [string, string][] = [
      ['#tab-battle-page', '#/battles'], ['#tab-tank-page', '#/tanks'], ['#tab-graph', '#/lineage'],
      ['#tab-duel', '#/compare'], ['#tab-matrix', '#/tech-tree'], ['#tab-map', '#/map'],
    ];
    for (const [tab, hash] of views) {
      await page.locator(tab).click();
      await expect(page).toHaveURL(new RegExp(hash.replace('/', '\\/') + '$'));
      await expect(page.locator(tab)).toHaveAttribute('aria-selected', 'true');
      await expect(page.locator('#' + (await page.locator(tab).getAttribute('aria-controls')))).toBeVisible();
    }
  });

  test('battle → tank → Back → Back returns to the battle, then the map', async ({ page }) => {
    await openAtlas(page);
    await page.evaluate(() => (window as any).openBattlePage('kursk_1943'));
    await expect(page).toHaveURL(/#\/battles\/kursk_1943/);
    await page.locator('#battle-details .cf-btn').first().click();
    await expect(page).toHaveURL(/#\/tanks\//);
    await expect(page.locator('#view-tank-page')).toBeVisible();
    await page.goBack();
    await expect(page).toHaveURL(/#\/battles\/kursk_1943/);
    await expect(page.locator('#view-battle-page')).toBeVisible();
    await page.goBack();
    await expect(page.locator('#view-map')).toBeVisible();
  });

  test('a pasted battle link opens that battle', async ({ page }) => {
    await openAtlas(page, '#/battles/raseiniai_1941');
    await expect(page.locator('#view-battle-page')).toBeVisible();
    await expect(page.locator('#battle-header-title')).toContainText('Raseiniai');
  });

  test('a link to a moment opens the battle there, ready to play (B4)', async ({ page }) => {
    await openAtlas(page, '#/battles/kursk_1943?t=0.42');
    // @ts-ignore page globals
    const s = await page.evaluate(() => ({ p: state.sim.progress, status: state.sim.status }));
    expect(s.p).toBeCloseTo(0.42, 2);
    expect(s.status).toBe('ready');
  });

  test('unknown ids show a notice and fall back to the list', async ({ page }) => {
    await openAtlas(page, '#/battles/not_a_battle');
    await expect(page.locator('#route-notice')).toContainText('No battle matches "not_a_battle"');
    await expect(page).toHaveURL(/#\/battles$/);
    await openAtlas(page, '#/tanks/not_a_tank');
    await expect(page.locator('#route-notice')).toContainText('No tank matches "not_a_tank"');
    await expect(page).toHaveURL(/#\/tanks$/);
  });
});

test.describe('keyboard tabs (T10)', () => {
  test('arrow keys move between tabs and open the view', async ({ page }) => {
    await openAtlas(page);
    await page.locator('#tab-map').focus();
    await page.keyboard.press('ArrowRight');
    await expect(page.locator('#tab-battle-page')).toBeFocused();
    await expect(page.locator('#tab-battle-page')).toHaveAttribute('aria-selected', 'true');
    await expect(page.locator('#tab-battle-page')).toHaveAttribute('tabindex', '0');
    await page.keyboard.press('End');
    await expect(page.locator('#tab-matrix')).toBeFocused();
    await page.keyboard.press('Home');
    await expect(page.locator('#tab-map')).toBeFocused();
  });
});

test.describe('search and filters (T12)', () => {
  test('a search with no matches says so and offers a way back', async ({ page }) => {
    await openAtlas(page);
    await page.locator('#search-input').fill('zzqq');
    const msg = page.locator('#map-no-results');
    await expect(msg).toBeVisible();
    await expect(msg).toContainText('No tanks or battles match "zzqq"');
    await msg.getByRole('button', { name: 'Clear search' }).click();
    await expect(msg).toBeHidden();
    await expect(page.locator('#search-input')).toHaveValue('');
  });

  test('a search narrows the gallery', async ({ page }) => {
    await openAtlas(page, '#/tanks');
    // @ts-ignore page globals
    const all = await page.evaluate(() => TANKS.filter((t: any) => isTankVisible(t)).length);
    await page.locator('#search-input').fill('tiger');
    // @ts-ignore page globals
    const some = await page.evaluate(() => TANKS.filter((t: any) => isTankVisible(t)).length);
    expect(some).toBeGreaterThan(0);
    expect(some).toBeLessThan(all);
  });

  test('conflicting filters offer Reset filters', async ({ page }) => {
    await openAtlas(page);
    await page.locator('#cf-ukraine').click();
    await page.locator('#nation-select').selectOption({ label: await page.locator('#nation-select option').filter({ hasText: /japan/i }).first().innerText() });
    const msg = page.locator('#map-no-results');
    await expect(msg).toBeVisible();
    await msg.getByRole('button', { name: 'Reset filters' }).click();
    await expect(msg).toBeHidden();
    await expect(page.locator('#cf-all')).toHaveAttribute('aria-pressed', 'true');
  });
});

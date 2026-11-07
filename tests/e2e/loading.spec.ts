import { test, expect, openAtlas } from './fixtures';

// First-load screen: shows before Tailwind arrives, explains a slow or failed load, then gets out of the way

test('shows the loading screen first, then removes it once styled', async ({ page }) => {
  let release!: () => void;
  const held = new Promise<void>(r => (release = r));
  await page.route(/cdn\.tailwindcss\.com/, async route => { await held; await route.fallback(); });
  await page.goto('world_tanks_atlas.html', { waitUntil: 'commit' });
  const loader = page.locator('#atlas-loader');
  await expect(loader).toBeVisible();
  await expect(loader).toContainText('World Tank Atlas');
  await expect(loader).toContainText(/Loading \d+ tanks and \d+ battles/);
  await expect(loader.getByRole('button', { name: 'Reload' })).toBeHidden();
  release();
  await expect(loader).not.toBeAttached({ timeout: 30_000 });
  expect(await page.locator('#app-bar').evaluate(el => getComputedStyle(el).position)).toBe('sticky');
});

test('says so when the styles cannot load, and can show the page anyway', async ({ page }) => {
  await page.route(/cdn\.tailwindcss\.com/, route => route.abort());
  await page.goto('world_tanks_atlas.html', { waitUntil: 'domcontentloaded' });
  const loader = page.locator('#atlas-loader');
  await expect(loader).toContainText("The page styles couldn't load");
  await expect(loader.getByRole('button', { name: 'Reload' })).toBeVisible();
  await expect(loader.locator('.atlas-loader-bar')).toBeHidden();
  await loader.getByRole('button', { name: 'Show the page anyway' }).click();
  await expect(loader).not.toBeAttached();
});

test('says it is still loading on a slow connection', async ({ page }) => {
  await page.clock.install();
  await page.route(/cdn\.tailwindcss\.com/, () => { /* never answers */ });
  await page.goto('world_tanks_atlas.html', { waitUntil: 'commit' });
  await expect(page.locator('#atlas-loader')).toBeVisible();
  await page.clock.runFor(10_500);
  await expect(page.locator('#atlas-loader')).toContainText('Still loading');
  await expect(page.locator('#atlas-loader').getByRole('button', { name: 'Reload' })).toBeVisible();
});

test('a normal load leaves no loading screen behind', async ({ page }) => {
  await openAtlas(page);
  await expect(page.locator('#atlas-loader')).toHaveCount(0);
  await expect(page.locator('#tab-map')).toBeVisible();
});

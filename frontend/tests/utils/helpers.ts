/**
 * Shared utility helpers for Playwright functional tests.
 */
import { type Page } from '@playwright/test';

/**
 * Wait for the application to fully load (sidebar + main content visible).
 */
export async function waitForAppLoad(page: Page): Promise<void> {
  await page.waitForSelector('nav', { state: 'visible', timeout: 15_000 });
}

/**
 * Navigate to a specific tab via the sidebar.
 */
export async function navigateToTab(page: Page, tabLabel: string): Promise<void> {
  await page.getByRole('button', { name: tabLabel }).click();
  await page.waitForTimeout(300);
}

/**
 * Take a screenshot with a descriptive name.
 */
export async function captureScreenshot(page: Page, name: string): Promise<void> {
  await page.screenshot({
    path: `test-results/screenshots/${name}.png`,
    fullPage: true,
  });
}

/**
 * Collect all 404 response URLs during test execution.
 * Returns a Set of URLs that returned 404.
 */
export function collect404Responses(page: Page): Set<string> {
  const notFoundUrls = new Set<string>();
  page.on('response', (response) => {
    if (response.status() === 404) {
      notFoundUrls.add(response.url());
    }
  });
  return notFoundUrls;
}

/**
 * Inject mock data into localStorage before navigating.
 * Useful for setting up state for report pages.
 */
export async function setLocalStorageData(
  page: Page,
  key: string,
  value: unknown,
): Promise<void> {
  await page.addInitScript(({ k, v }) => {
    localStorage.setItem(k, JSON.stringify(v));
  }, { k: key, v: value });
}

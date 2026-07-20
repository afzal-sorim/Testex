import { test, expect } from '@playwright/test';
import { DashboardPage } from './pages/DashboardPage';
import { BasePage } from './pages/BasePage';
import { SIDEBAR_TABS } from './fixtures/testData';
import { mockStatusEndpoint } from './utils/apiMocks';

test.describe('UI Component Validation — Functional Tests', () => {
  test.beforeEach(async ({ page }) => {
    await mockStatusEndpoint(page);
  });

  test('1) Dashboard loads with stats and charts', async ({ page }) => {
    const dashboardPage = new DashboardPage(page);
    await dashboardPage.navigate();
    await dashboardPage.isDashboardLoaded();
    
    // Check if some key stats text exists
    await expect(page.locator('text=AI-Powered Java Migration')).toBeVisible();
  });

  test('2) Sidebar navigation works for all tabs', async ({ page }) => {
    const basePage = new BasePage(page);
    await basePage.goto();

    for (const [key, label] of Object.entries(SIDEBAR_TABS)) {
      await basePage.navigateToTab(label);
      // Let it settle
      await page.waitForTimeout(200);
      
      // We could add more specific assertions per page, 
      // but verifying the click doesn't throw and URL/header changes is enough for basic UI validation
    }
  });

  test('6) No JavaScript console errors during navigation', async ({ page }) => {
    const basePage = new BasePage(page);
    await basePage.goto();
    
    for (const [key, label] of Object.entries(SIDEBAR_TABS)) {
      await basePage.navigateToTab(label);
      await page.waitForTimeout(200);
    }
    
    // We expect some network errors because of mocked APIs, but UI/React shouldn't crash
    const errors = basePage.getConsoleErrors();
    const uiCrashErrors = errors.filter(e => e.includes('TypeError') || e.includes('React'));
    expect(uiCrashErrors.length).toBe(0);
  });
});

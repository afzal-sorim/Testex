import { type Page, type Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * Page Object Model for the Dashboard page.
 */
export class DashboardPage extends BasePage {
  readonly pageContainer: Locator;

  constructor(page: Page) {
    super(page);
    // The dashboard renders multiple Card components; detect by the overall container
    this.pageContainer = page.locator('main');
  }

  /** Navigate to the Dashboard tab */
  async navigate(): Promise<void> {
    await this.goto();
    await this.navigateToTab('Dashboard');
  }

  /** Verify the dashboard has rendered content */
  async isDashboardLoaded(): Promise<void> {
    await expect(this.pageContainer).toBeVisible();
  }
}

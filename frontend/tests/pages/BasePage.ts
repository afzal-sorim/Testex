import { type Page, type Locator, expect } from '@playwright/test';

/**
 * Base Page Object shared by all page objects.
 * Provides common sidebar navigation, wait utilities, and error collection.
 */
export class BasePage {
  readonly page: Page;
  readonly sidebar: Locator;
  readonly consoleErrors: string[] = [];

  constructor(page: Page) {
    this.page = page;

    // Desktop sidebar nav container
    this.sidebar = page.locator('nav');

    // Collect console errors during test
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        this.consoleErrors.push(msg.text());
      }
    });
  }

  /** Navigate to the app root */
  async goto(): Promise<void> {
    await this.page.goto('/');
    await this.page.waitForLoadState('domcontentloaded');
  }

  /** Click a sidebar tab by its visible label text */
  async navigateToTab(tabLabel: string): Promise<void> {
    await this.page.getByRole('button', { name: tabLabel }).click();
    // Brief settle for animation
    await this.page.waitForTimeout(300);
  }

  /** Wait until network is idle (no pending requests for 500ms) */
  async waitForNetworkIdle(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
  }

  /** Capture a full-page screenshot */
  async captureScreenshot(name: string): Promise<void> {
    await this.page.screenshot({
      path: `test-results/screenshots/${name}.png`,
      fullPage: true,
    });
  }

  /** Return accumulated console errors */
  getConsoleErrors(): string[] {
    return [...this.consoleErrors];
  }
}

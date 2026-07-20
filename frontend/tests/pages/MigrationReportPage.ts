import { type Page, type Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * Page Object Model for the Migration Report page.
 */
export class MigrationReportPage extends BasePage {
  readonly pageHeader: Locator;
  readonly downloadPdfLink: Locator;

  // Metadata table
  readonly metadataSection: Locator;
  readonly targetUpgradeCell: Locator;
  readonly buildSystemCell: Locator;
  readonly buildStatusCell: Locator;

  // Modified files
  readonly modifiedFilesSection: Locator;

  // Refactoring logs
  readonly refactoringLogsSection: Locator;
  readonly refactoringLogsContent: Locator;

  // Compilation failures
  readonly compilationFailuresSection: Locator;

  // Empty state
  readonly emptyState: Locator;

  constructor(page: Page) {
    super(page);

    this.pageHeader = page.locator('h2', { hasText: 'Java Migration Summary Report' });
    this.downloadPdfLink = page.locator('a', { hasText: 'Download PDF' });

    // Metadata
    this.metadataSection = page.locator('h3', { hasText: 'Metadata' });
    this.targetUpgradeCell = page.locator('td:has-text("Target Upgrade")').first();
    this.buildSystemCell = page.locator('td:has-text("Build System")').first();
    this.buildStatusCell = page.locator('td:has-text("Build Status")').first();

    // Modified files
    this.modifiedFilesSection = page.locator('h3', { hasText: /Updated File Inventory/i });

    // Refactoring logs
    this.refactoringLogsSection = page.locator('h3', { hasText: 'Refactoring Logs' });
    this.refactoringLogsContent = page.locator('pre').first();

    // Compilation failures
    this.compilationFailuresSection = page.locator('h3', { hasText: 'Compilation Failures' });

    // Empty state
    this.emptyState = page.locator('h3', { hasText: 'No Migration Report Available' });
  }

  /** Navigate to the Migration Report tab */
  async navigate(): Promise<void> {
    await this.goto();
    await this.navigateToTab('Migration Report');
  }
}

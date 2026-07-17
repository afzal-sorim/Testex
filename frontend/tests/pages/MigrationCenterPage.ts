import { type Page, type Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * Page Object Model for the Migration Center page.
 * Matches locators against MigrationCenter.jsx UI elements.
 */
export class MigrationCenterPage extends BasePage {
  // Page header
  readonly pageHeader: Locator;

  // Target project info
  readonly targetProjectUrl: Locator;
  readonly noAnalysisWarning: Locator;

  // Form & version selectors
  readonly migrationForm: Locator;
  readonly java11Radio: Locator;
  readonly java17Radio: Locator;
  readonly java21Radio: Locator;
  readonly java25Radio: Locator;
  readonly runMigrationButton: Locator;

  // Loading state
  readonly progressBar: Locator;
  readonly statusIndicator: Locator;

  // Success banner
  readonly successBanner: Locator;

  // Error state
  readonly errorBanner: Locator;
  readonly errorTitle: Locator;

  // Build Check
  readonly buildCheckSection: Locator;
  readonly buildStatusIndicator: Locator;

  // Modified files
  readonly modifiedFilesSection: Locator;

  // LLM Execution Log
  readonly llmLogSection: Locator;
  readonly llmLogContent: Locator;

  // Compiler errors
  readonly compilerErrorSection: Locator;

  // Reports & actions
  readonly downloadPdfLink: Locator;
  readonly viewMigrationReportButton: Locator;

  // Project Runner Dashboard
  readonly projectRunnerDashboard: Locator;
  readonly runProjectButton: Locator;
  readonly stopProjectButton: Locator;
  readonly restartProjectButton: Locator;
  readonly runnerStatusBadge: Locator;
  readonly logConsole: Locator;
  readonly livePreviewPane: Locator;

  // Migration History
  readonly migrationHistorySection: Locator;
  readonly migrationHistoryTable: Locator;

  constructor(page: Page) {
    super(page);

    this.pageHeader = page.locator('h2', { hasText: 'Universal Polyglot Migration Center' });

    // Target project
    this.targetProjectUrl = page.locator('text=Target Project:');
    this.noAnalysisWarning = page.locator('text=No project analysis loaded');

    // Form — scoped to avoid ChatbotWidget
    this.migrationForm = page.locator('form').filter({ has: page.locator('input[name="targetVersion"]') });
    this.java11Radio = page.locator('input[name="targetVersion"][value="11"]');
    this.java17Radio = page.locator('input[name="targetVersion"][value="17"]');
    this.java21Radio = page.locator('input[name="targetVersion"][value="21"]');
    this.java25Radio = page.locator('input[name="targetVersion"][value="25"]');
    this.runMigrationButton = this.migrationForm.locator('button[type="submit"]');

    // Loading
    this.progressBar = page.locator('.rocket-progress-container');
    this.statusIndicator = page.locator('text=Status:').first();

    // Success
    this.successBanner = page.locator('text=Migration & compiler verification completed in');

    // Error
    this.errorBanner = page.locator('h4', { hasText: 'Migration Failed' });
    this.errorTitle = page.locator('h4', { hasText: 'Migration Failed' });

    // Build Check
    this.buildCheckSection = page.locator('h3', { hasText: 'Build Check' });
    this.buildStatusIndicator = page.locator('text=Build Success').first();

    // Modified files
    this.modifiedFilesSection = page.locator('h4', { hasText: 'Modified Files' });

    // LLM Log
    this.llmLogSection = page.locator('h3', { hasText: 'LLM Execution Log' });
    this.llmLogContent = page.locator('pre').first();

    // Compiler errors
    this.compilerErrorSection = page.locator('h3', { hasText: 'Compiler Error Log' });

    // Reports
    this.downloadPdfLink = page.locator('a', { hasText: 'Download PDF Report' });
    this.viewMigrationReportButton = page.getByRole('button', { name: 'View Migration Report' });

    // Project Runner
    this.projectRunnerDashboard = page.locator('h3', { hasText: 'Project Runner Dashboard' });
    this.runProjectButton = page.getByRole('button', { name: 'Run Project' });
    this.stopProjectButton = page.getByRole('button', { name: 'Stop' });
    this.restartProjectButton = page.getByRole('button', { name: 'Restart' });
    this.runnerStatusBadge = page.locator('text=Status:').last();
    this.logConsole = page.locator('#runner-console');
    this.livePreviewPane = page.locator('text=Live Application Preview');

    // Migration History
    this.migrationHistorySection = page.locator('h3', { hasText: 'Migration History' });
    this.migrationHistoryTable = page.locator('table').last();
  }

  /** Navigate to the Migration Center tab */
  async navigate(): Promise<void> {
    await this.goto();
    await this.navigateToTab('Migration Center');
    await expect(this.pageHeader).toBeVisible();
  }

  /** Select a target Java version */
  async selectTargetVersion(version: '11' | '17' | '21' | '25'): Promise<void> {
    const label = this.page.locator(`label`).filter({ has: this.page.locator(`input[value="${version}"]`) });
    await label.click();
  }

  /** Click Run Migration button */
  async clickRunMigration(): Promise<void> {
    await this.runMigrationButton.click();
  }

  /** Check if migration is loading */
  async isMigrationLoading(): Promise<void> {
    await expect(this.runMigrationButton).toContainText('Processing Migration...');
    await expect(this.runMigrationButton).toBeDisabled();
  }

  /** Check if run migration button is ready */
  async isRunMigrationButtonReady(): Promise<void> {
    await expect(this.runMigrationButton).toContainText('Run Migration');
    await expect(this.runMigrationButton).toBeEnabled();
  }
}

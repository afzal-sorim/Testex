import { type Page, type Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * Page Object Model for the Repository Analysis page.
 * Matches locators against RepositoryAnalysis.jsx UI elements.
 */
export class RepositoryAnalysisPage extends BasePage {
  // Form elements — scoped to the analysis form to avoid ChatbotWidget conflicts
  readonly form: Locator;
  readonly urlInput: Locator;
  readonly analyzeButton: Locator;
  readonly pageHeader: Locator;

  // Loading state
  readonly progressBar: Locator;
  readonly statusText: Locator;

  // Success state
  readonly successBanner: Locator;

  // Error state
  readonly errorBanner: Locator;
  readonly errorTitle: Locator;

  // Result — Project Parameters table
  readonly projectParametersSection: Locator;
  readonly javaVersionCell: Locator;
  readonly buildToolCell: Locator;
  readonly frameworkCell: Locator;
  readonly riskLevelBadge: Locator;

  // Result — Dependencies
  readonly dependenciesSection: Locator;

  // Result — Deprecated APIs
  readonly deprecatedApisSection: Locator;

  // Result — AI Recommendation
  readonly aiRecommendationSection: Locator;
  readonly recommendationText: Locator;
  readonly reasoningText: Locator;

  // Result — Proceed to Migration
  readonly proceedToMigrationButton: Locator;

  // Non-Java warning
  readonly migrationNotApplicableWarning: Locator;

  // View mode tabs
  readonly overviewTab: Locator;
  readonly graphicalTab: Locator;

  constructor(page: Page) {
    super(page);

    // Scoped form to avoid matching ChatbotWidget submit button
    this.form = page.locator('form').filter({ has: page.locator('input[type="url"]') });
    this.urlInput = this.form.locator('input[type="url"]');
    this.analyzeButton = this.form.locator('button[type="submit"]');
    this.pageHeader = page.locator('h2', { hasText: 'GitHub Repository Analysis' });

    // Loading
    this.progressBar = page.locator('.rocket-progress-container');
    this.statusText = page.locator('text=Status:').first();

    // Success banner
    this.successBanner = page.locator('text=Repository analysis completed in');

    // Error
    this.errorBanner = page.locator('h4', { hasText: 'Analysis Failed' });
    this.errorTitle = page.locator('h4', { hasText: 'Analysis Failed' });

    // Project Parameters
    this.projectParametersSection = page.locator('h3', { hasText: 'Project Parameters' });
    this.javaVersionCell = page.locator('td', { hasText: 'Java Version' }).locator('~ td').first();
    this.buildToolCell = page.locator('td:has-text("Build Tool / PM")').first();
    this.frameworkCell = page.locator('td:has-text("Framework")').first();
    this.riskLevelBadge = page.locator('td:has-text("Risk Level")').first();

    // Dependencies
    this.dependenciesSection = page.locator('h3', { hasText: 'Core Dependencies' });

    // Deprecated APIs
    this.deprecatedApisSection = page.locator('h3', { hasText: 'Deprecated APIs Found' });

    // AI Recommendation
    this.aiRecommendationSection = page.locator('h3', { hasText: 'AI Recommendation' });
    this.recommendationText = page.locator('.text-indigo-600, .dark\\:text-indigo-400').first();
    this.reasoningText = page.locator('.whitespace-pre-wrap').first();

    // Proceed button
    this.proceedToMigrationButton = page.getByRole('button', { name: /Proceed to Migration Center/i });

    // Non-Java warning
    this.migrationNotApplicableWarning = page.locator('h4', { hasText: 'Migration Not Applicable' });

    // View mode tabs
    this.overviewTab = page.getByRole('button', { name: 'Overview' });
    this.graphicalTab = page.getByRole('button', { name: 'Graphical View' });
  }

  /** Navigate to the Repository Analysis tab */
  async navigate(): Promise<void> {
    await this.goto();
    await this.navigateToTab('Repository Analysis');
    await expect(this.pageHeader).toBeVisible();
  }

  /** Enter a URL in the input field */
  async enterRepositoryUrl(url: string): Promise<void> {
    await this.urlInput.fill(url);
  }

  /** Clear the URL input */
  async clearUrlInput(): Promise<void> {
    await this.urlInput.clear();
  }

  /** Click the Analyze / Run Audit button */
  async clickAnalyze(): Promise<void> {
    await this.analyzeButton.click();
  }

  /** Assert the button is in loading state */
  async isAnalysisLoading(): Promise<void> {
    await expect(this.analyzeButton).toContainText('Analyzing...');
    await expect(this.analyzeButton).toBeDisabled();
  }

  /** Assert the button is ready (idle) */
  async isAnalyzeButtonReady(): Promise<void> {
    await expect(this.analyzeButton).toContainText('Run Audit');
    await expect(this.analyzeButton).toBeEnabled();
  }

  /** Assert the input is disabled during loading */
  async isInputDisabledDuringLoading(): Promise<void> {
    await expect(this.urlInput).toBeDisabled();
  }

  /** Assert the progress bar is visible */
  async isProgressVisible(): Promise<void> {
    await expect(this.progressBar).toBeVisible();
  }

  /** Get HTML5 validation message from the URL input */
  async getValidationMessage(): Promise<string> {
    return await this.urlInput.evaluate((el: HTMLInputElement) => el.validationMessage);
  }

  /** Switch to Graphical View tab */
  async switchToGraphicalView(): Promise<void> {
    await this.graphicalTab.click();
  }

  /** Switch to Overview tab */
  async switchToOverview(): Promise<void> {
    await this.overviewTab.click();
  }
}

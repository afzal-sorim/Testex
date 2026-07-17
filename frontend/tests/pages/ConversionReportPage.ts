import { type Page, type Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

/**
 * Page Object Model for the Conversion Report page.
 */
export class ConversionReportPage extends BasePage {
  readonly pageHeader: Locator;
  readonly downloadZipLink: Locator;
  readonly downloadPdfLink: Locator;

  // Files Processed
  readonly filesProcessedSection: Locator;

  // Converted Files Mapping
  readonly convertedFilesMappingSection: Locator;

  // Explanation
  readonly explanationSection: Locator;

  // Warnings
  readonly warningsSection: Locator;

  // Empty state
  readonly emptyState: Locator;

  constructor(page: Page) {
    super(page);

    this.pageHeader = page.locator('h2', { hasText: 'Java to Python Conversion Report' });
    this.downloadZipLink = page.locator('a', { hasText: 'Download ZIP' });
    this.downloadPdfLink = page.locator('a', { hasText: 'Download PDF' });

    this.filesProcessedSection = page.locator('h3', { hasText: 'Files Processed' });
    this.convertedFilesMappingSection = page.locator('h3', { hasText: 'Converted Files Mapping' });
    this.explanationSection = page.locator('h3', { hasText: 'Structure Conversion Explanation' });
    this.warningsSection = page.locator('h3', { hasText: 'Unsupported Features' });

    this.emptyState = page.locator('h3', { hasText: 'No Conversion Report Available' });
  }

  /** Navigate to the Conversion Report tab */
  async navigate(): Promise<void> {
    await this.goto();
    await this.navigateToTab('Conversion Report');
  }
}

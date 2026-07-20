/**
 * API Mock utilities using Playwright route interception.
 * These intercept fetch/XHR requests and return deterministic mock data
 * so tests run without a live backend.
 */
import { type Page } from '@playwright/test';
import {
  MOCK_ANALYSIS_SUCCESS,
  MOCK_ANALYSIS_NON_JAVA,
  MOCK_MIGRATION_TASK_RESPONSE,
  MOCK_MIGRATION_STATUS_PENDING,
  MOCK_MIGRATION_STATUS_SUCCESS,
  MOCK_MIGRATION_STATUS_BUILD_FAILURE,
  MOCK_MIGRATION_STATUS_FAILURE,
  MOCK_RUN_START_RESPONSE,
  MOCK_RUN_STATUS_STOPPED,
  MOCK_RUN_STATUS_RUNNING,
  MOCK_ERROR_RESPONSES,
} from '../fixtures/mockResponses';

/** Mock successful analysis */
export async function mockAnalysisSuccess(page: Page): Promise<void> {
  await page.route('**/api/analyze', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(MOCK_ANALYSIS_SUCCESS),
    });
  });
}

/** Mock analysis returning a non-Java project */
export async function mockAnalysisNonJava(page: Page): Promise<void> {
  await page.route('**/api/analyze', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(MOCK_ANALYSIS_NON_JAVA),
    });
  });
}

/** Mock analysis with a specific error response */
export async function mockAnalysisError(
  page: Page,
  errorType: 'privateRepo' | 'notFound' | 'serverError',
): Promise<void> {
  await page.route('**/api/analyze', (route) => {
    if (errorType === 'serverError') {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_ERROR_RESPONSES.serverError),
      });
    } else {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_ERROR_RESPONSES[errorType]),
      });
    }
  });
}

/** Mock successful migration (task + polling success) */
export async function mockMigrationSuccess(page: Page): Promise<void> {
  let pollCount = 0;

  await page.route('**/api/migrate', (route) => {
    if (route.request().method() === 'POST') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_MIGRATION_TASK_RESPONSE),
      });
    } else {
      route.continue();
    }
  });

  await page.route('**/api/migrate/status/**', (route) => {
    pollCount++;
    // Return PENDING on first poll, then SUCCESS
    const response = pollCount <= 1 ? MOCK_MIGRATION_STATUS_PENDING : MOCK_MIGRATION_STATUS_SUCCESS;
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(response),
    });
  });
}

/** Mock migration with build failure */
export async function mockMigrationBuildFailure(page: Page): Promise<void> {
  await page.route('**/api/migrate', (route) => {
    if (route.request().method() === 'POST') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_MIGRATION_TASK_RESPONSE),
      });
    } else {
      route.continue();
    }
  });

  await page.route('**/api/migrate/status/**', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(MOCK_MIGRATION_STATUS_BUILD_FAILURE),
    });
  });
}

/** Mock migration task failure */
export async function mockMigrationFailure(page: Page): Promise<void> {
  await page.route('**/api/migrate', (route) => {
    if (route.request().method() === 'POST') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_MIGRATION_TASK_RESPONSE),
      });
    } else {
      route.continue();
    }
  });

  await page.route('**/api/migrate/status/**', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(MOCK_MIGRATION_STATUS_FAILURE),
    });
  });
}

/** Mock backend completely unavailable (abort all API requests) */
export async function mockBackendUnavailable(page: Page): Promise<void> {
  await page.route('**/api/**', (route) => {
    route.abort('connectionrefused');
  });
}

/** Mock project runner start + status */
export async function mockRunProjectSuccess(page: Page): Promise<void> {
  let pollCount = 0;

  await page.route('**/api/run/start', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(MOCK_RUN_START_RESPONSE),
    });
  });

  await page.route('**/api/run/status/**', (route) => {
    pollCount++;
    const response = pollCount <= 1 ? MOCK_RUN_STATUS_STOPPED : MOCK_RUN_STATUS_RUNNING;
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(response),
    });
  });
}

/** Mock the report download endpoints */
export async function mockReportDownloads(page: Page): Promise<void> {
  await page.route('**/api/report/migration', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/pdf',
      body: Buffer.from('mock-pdf-content'),
    });
  });

  await page.route('**/api/report/conversion', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/pdf',
      body: Buffer.from('mock-pdf-content'),
    });
  });

  await page.route('**/api/download/python', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/zip',
      body: Buffer.from('mock-zip-content'),
    });
  });
}

/** Mock the status endpoint (used by Dashboard) */
export async function mockStatusEndpoint(page: Page): Promise<void> {
  await page.route('**/api/status', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'ok', version: '1.0.0' }),
    });
  });
}

/** Mock API keys endpoints */
export async function mockApiKeysEndpoints(page: Page): Promise<void> {
  await page.route('**/api/keys/**', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ keys: [], activeProvider: 'gemini' }),
    });
  });
}

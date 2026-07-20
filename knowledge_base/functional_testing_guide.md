# Functional Testing Guide (Playwright & Selenium)

## Playwright Setup
The project uses Playwright for end-to-end UI testing. Tests are located in the `tests/` directory.
### playwright.config.ts
```typescript
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests/e2e',
  reporter: [['html'], ['json', { outputFile: 'playwright-report/test-results.json' }]],
  use: { 
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:8081',
    video: 'on',
    trace: 'on',
    screenshot: 'on'
  },
});
```

### Running Playwright Tests
To run Playwright tests, you can use the command:
```bash
npx playwright test --headed
```
The backend API provides an endpoint `/api/system/run-ui-tests/{repo_name}` to trigger these tests dynamically.

## Selenium Setup
Selenium can also be used for cross-browser functional testing. The backend provides Selenium integration via `selenium_service.py`. Selenium tests run WebDriver scripts to interact with the UI elements. Make sure to configure the correct WebDriver (e.g., ChromeDriver) before running.

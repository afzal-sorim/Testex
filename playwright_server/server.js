const express = require('express');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { exec } = require('child_process');
const AdmZip = require('adm-zip');

const app = express();
app.use(express.json({ limit: '50mb' }));

const PORT = process.env.PORT || 3000;

// Simple healthcheck endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'playwright-execution-service' });
});

// Run endpoint
app.post('/run', async (req, res) => {
  const { baseURL, testFiles } = req.body;

  if (!baseURL) {
    return res.status(400).json({ error: 'baseURL is required' });
  }
  if (!testFiles || !Array.isArray(testFiles)) {
    return res.status(400).json({ error: 'testFiles array is required' });
  }

  let tempDir = null;

  try {
    // 1. Create a unique temporary directory
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'playwright-run-'));
    
    // Create subdirectories
    const testsDir = path.join(tempDir, 'tests');
    fs.mkdirSync(testsDir);

    // 2. Write the Playwright config file
    const configContent = `
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  reporter: [
    ['html', { open: 'never', outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'playwright-report/test-results.json' }]
  ],
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL,
    screenshot: 'on',
    video: 'on',
    trace: 'on'
  }
});
`;
    fs.writeFileSync(path.join(tempDir, 'playwright.config.ts'), configContent);

    // 3. Write all the test files
    for (const file of testFiles) {
      if (file.name && file.content) {
        // Sanitize filename to prevent path traversal
        const safeName = path.basename(file.name);
        fs.writeFileSync(path.join(testsDir, safeName), file.content);
      }
    }

    // 4. Execute the Playwright tests
    const env = { ...process.env, PLAYWRIGHT_BASE_URL: baseURL };
    
    console.log(`[Playwright Server] Executing tests for target: ${baseURL} inside: ${tempDir}`);
    
    // We run "npx playwright test"
    exec('npx playwright test', { cwd: tempDir, env, maxBuffer: 10 * 1024 * 1024 }, (error, stdout, stderr) => {
      const exitCode = error ? error.code : 0;
      console.log(`[Playwright Server] Tests finished with exit code: ${exitCode}`);

      let testResultsJson = null;
      let htmlReportZipBase64 = null;

      // 5. Read json results if available
      const jsonReportPath = path.join(tempDir, 'playwright-report', 'test-results.json');
      if (fs.existsSync(jsonReportPath)) {
        try {
          testResultsJson = JSON.parse(fs.readFileSync(jsonReportPath, 'utf8'));
        } catch (e) {
          console.error('[Playwright Server] Error parsing test-results.json:', e);
        }
      }

      // 6. Zip the playwright-report directory if it exists
      const reportDir = path.join(tempDir, 'playwright-report');
      if (fs.existsSync(reportDir)) {
        try {
          const zip = new AdmZip();
          zip.addLocalFolder(reportDir);
          const zipBuffer = zip.toBuffer();
          htmlReportZipBase64 = zipBuffer.toString('base64');
        } catch (e) {
          console.error('[Playwright Server] Error zipping report directory:', e);
        }
      }

      // 7. Return the response
      res.json({
        success: true,
        exitCode,
        stdout,
        stderr,
        testResultsJson,
        htmlReportZipBase64
      });

      // 8. Clean up temp directory asynchronously to not block response
      setTimeout(() => {
        try {
          if (tempDir && fs.existsSync(tempDir)) {
            fs.rmSync(tempDir, { recursive: true, force: true });
            console.log(`[Playwright Server] Cleaned up temporary directory: ${tempDir}`);
          }
        } catch (cleanupError) {
          console.error(`[Playwright Server] Error during cleanup of ${tempDir}:`, cleanupError);
        }
      }, 1000);
    });

  } catch (err) {
    console.error('[Playwright Server] Exception in /run handler:', err);
    res.status(500).json({ error: err.message });
    
    // Clean up if we failed before starting the process
    if (tempDir && fs.existsSync(tempDir)) {
      try {
        fs.rmSync(tempDir, { recursive: true, force: true });
      } catch (cleanupError) {
        console.error('[Playwright Server] Error cleaning up directory after exception:', cleanupError);
      }
    }
  }
});

app.listen(PORT, () => {
  console.log(`Playwright Execution Server listening on port ${PORT}`);
});

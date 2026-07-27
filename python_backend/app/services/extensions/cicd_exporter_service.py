from pathlib import Path
from typing import Dict

class CICDExporterService:
    """
    Non-invasive CI/CD Pipeline Exporter Service.
    Exports automated workflow templates (GitHub Actions, Jenkinsfile, GitLab CI, Azure DevOps)
    for seamless CI/CD test automation integration.
    """

    def export_github_actions(self, repo_name: str, output_dir: Path) -> Path:
        """Exports GitHub Actions workflow file .github/workflows/playwright_e2e.yml."""
        target_dir = output_dir / ".github" / "workflows"
        target_dir.mkdir(parents=True, exist_ok=True)
        yml_path = target_dir / "playwright_e2e.yml"

        content = (
            f"name: PROVA Playwright E2E Tests - {repo_name}\n\n"
            "on:\n"
            "  push:\n"
            "    branches: [ main, master, v1 ]\n"
            "  pull_request:\n"
            "    branches: [ main, master ]\n\n"
            "jobs:\n"
            "  test:\n"
            "    timeout-minutes: 60\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - uses: actions/checkout@v4\n"
            "      - uses: actions/setup-node@v4\n"
            "        with:\n"
            "          node-version: lts/*\n"
            "      - name: Install dependencies\n"
            "        run: npm ci || npm install\n"
            "      - name: Install Playwright Browsers\n"
            "        run: npx playwright install --with-deps chromium\n"
            "      - name: Run Playwright tests\n"
            "        run: npx playwright test\n"
            "      - uses: actions/upload-artifact@v4\n"
            "        if: ${{ !cancelled() }}\n"
            "        with:\n"
            "          name: playwright-report\n"
            "          path: playwright-report/\n"
            "          retention-days: 30\n"
        )

        yml_path.write_text(content, encoding="utf-8")
        print(f"[CICDExporterService] Exported GitHub Actions workflow to {yml_path}")
        return yml_path

    def export_jenkinsfile(self, repo_name: str, output_dir: Path) -> Path:
        """Exports Jenkinsfile for Jenkins automation pipeline."""
        output_dir.mkdir(parents=True, exist_ok=True)
        jenkins_path = output_dir / "Jenkinsfile"

        content = (
            f"// Jenkins Pipeline for {repo_name}\n"
            "pipeline {\n"
            "    agent {\n"
            "        docker {\n"
            "            image 'mcr.microsoft.com/playwright:v1.41.0-jammy'\n"
            "        }\n"
            "    }\n"
            "    stages {\n"
            "        stage('Install') {\n"
            "            steps {\n"
            "                sh 'npm ci || npm install'\n"
            "            }\n"
            "        }\n"
            "        stage('Run E2E Tests') {\n"
            "            steps {\n"
            "                sh 'npx playwright test'\n"
            "            }\n"
            "        }\n"
            "    }\n"
            "    post {\n"
            "        always {\n"
            "            junit '**/junit_results_*.xml'\n"
            "            archiveArtifacts artifacts: 'playwright-report/**'\n"
            "        }\n"
            "    }\n"
            "}\n"
        )

        jenkins_path.write_text(content, encoding="utf-8")
        print(f"[CICDExporterService] Exported Jenkinsfile to {jenkins_path}")
        return jenkins_path

cicd_exporter_service = CICDExporterService()

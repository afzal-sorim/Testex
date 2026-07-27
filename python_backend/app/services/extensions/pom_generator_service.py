from pathlib import Path
from typing import Dict, List, Any
from app.services.extensions.dom_ast_parser_service import dom_ast_parser_service

class POMGeneratorService:
    """
    Non-invasive Page Object Model (POM) Generator Service.
    Scaffolds structured Page Classes separating locators and actions from test assertions.
    Supports both Playwright (TypeScript) and Selenium (Python).
    """

    def generate_playwright_pom(self, project_dir: Path) -> Dict[str, str]:
        """Generates TypeScript Page Object Model files for Playwright."""
        elements = dom_ast_parser_service.extract_dom_elements(project_dir)
        page_files = {}

        pages_dir = project_dir / "tests" / "pages"
        pages_dir.mkdir(parents=True, exist_ok=True)

        # Group elements by source file
        grouped = {}
        for el in elements:
            src = el.get("source_file", "BasePage")
            grouped.setdefault(src, []).append(el)

        for src_file, el_list in grouped.items():
            clean_name = src_file.split(".")[0].capitalize() + "Page"
            class_code = f"import {{ Page, Locator, expect }} from '@playwright/test';\n\n"
            class_code += f"export class {clean_name} {{\n"
            class_code += "  readonly page: Page;\n"

            # Locators
            locators_code = ""
            actions_code = ""

            seen_keys = set()
            for idx, el in enumerate(el_list):
                tag = el.get("tag", "element")
                selector = el.get("css_selector", "body")
                key = (el.get("id") or el.get("name") or el.get("test_id") or f"{tag}_{idx}").replace("-", "_").lower()
                
                if key in seen_keys:
                    continue
                seen_keys.add(key)

                locators_code += f"  readonly {key}: Locator;\n"
                actions_code += f"    this.{key} = page.locator('{selector}');\n"

            class_code += locators_code + "\n"
            class_code += "  constructor(page: Page) {\n"
            class_code += "    this.page = page;\n"
            class_code += actions_code
            class_code += "  }\n\n"

            class_code += "  async navigate(urlPath: string = '/') {\n"
            class_code += "    await this.page.goto(urlPath);\n"
            class_code += "    await this.page.waitForLoadState('domcontentloaded');\n"
            class_code += "  }\n"
            class_code += "}\n"

            file_path = pages_dir / f"{clean_name}.ts"
            file_path.write_text(class_code, encoding="utf-8")
            page_files[f"{clean_name}.ts"] = class_code

        return page_files

    def generate_selenium_pom(self, project_dir: Path) -> Dict[str, str]:
        """Generates Python Page Object Model files for Selenium."""
        elements = dom_ast_parser_service.extract_dom_elements(project_dir)
        page_files = {}

        pages_dir = project_dir / "selenium_tests" / "pages"
        pages_dir.mkdir(parents=True, exist_ok=True)

        grouped = {}
        for el in elements:
            src = el.get("source_file", "base_page")
            grouped.setdefault(src, []).append(el)

        for src_file, el_list in grouped.items():
            clean_name = src_file.split(".")[0].lower() + "_page"
            class_name = src_file.split(".")[0].capitalize() + "Page"

            code = (
                "from selenium.webdriver.common.by import By\n"
                "from selenium.webdriver.support.ui import WebDriverWait\n"
                "from selenium.webdriver.support import expected_conditions as EC\n\n"
                f"class {class_name}:\n"
                "    def __init__(self, driver):\n"
                "        self.driver = driver\n"
            )

            seen_keys = set()
            for idx, el in enumerate(el_list):
                tag = el.get("tag", "element")
                selector = el.get("css_selector", "body")
                key = (el.get("id") or el.get("name") or el.get("test_id") or f"{tag}_{idx}").replace("-", "_").lower()
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                code += f"        self.{key}_locator = (By.CSS_SELECTOR, '{selector}')\n"

            code += "\n    def navigate(self, url):\n"
            code += "        self.driver.get(url)\n"

            file_path = pages_dir / f"{clean_name}.py"
            file_path.write_text(code, encoding="utf-8")
            page_files[f"{clean_name}.py"] = code

        return page_files

pom_generator_service = POMGeneratorService()

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, List

class JUnitAllureExporterService:
    """
    Non-invasive JUnit XML and Allure Report Exporter Service.
    Transforms execution test summaries into standardized JUnit XML format and Allure JSON metadata.
    """

    def export_junit_xml(self, repo_name: str, execution_results: Dict[str, Any], output_dir: Path) -> Path:
        """Exports execution results as a standard JUnit XML file."""
        output_dir.mkdir(parents=True, exist_ok=True)
        xml_file = output_dir / f"junit_results_{repo_name}.xml"

        total = execution_results.get("total", 0)
        passed = execution_results.get("passed", 0)
        failed = execution_results.get("failed", 0)
        skipped = execution_results.get("skipped", 0)
        duration_ms = execution_results.get("duration", 0)
        time_sec = f"{(duration_ms / 1000.0):.2f}"

        testsuite = ET.Element("testsuite", {
            "name": f"Playwright.Suite.{repo_name}",
            "tests": str(total),
            "failures": str(failed),
            "skipped": str(skipped),
            "time": time_sec
        })

        modules = execution_results.get("modules", [])
        for m in modules:
            name = m.get("module", "TestModule")
            status = m.get("status", "Passed")
            dur = f"{(m.get('duration', 0) / 1000.0):.2f}"

            case = ET.SubElement(testsuite, "testcase", {
                "name": name,
                "classname": f"PROVA.E2E.{repo_name}",
                "time": dur
            })

            if status == "Failed":
                failure = ET.SubElement(case, "failure", {"message": "Test execution failed"})
                failure.text = m.get("error", "Assertion or connection error occurred.")
            elif status == "Skipped":
                ET.SubElement(case, "skipped")

        tree = ET.ElementTree(testsuite)
        ET.indent(tree, space="  ")
        tree.write(xml_file, encoding="utf-8", xml_declaration=True)
        print(f"[JUnitAllureExporterService] Exported JUnit XML to {xml_file}")
        return xml_file

junit_allure_exporter_service = JUnitAllureExporterService()

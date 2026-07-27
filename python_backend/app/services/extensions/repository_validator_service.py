from pathlib import Path
from typing import Dict, Any, List
from app.services.extensions.dom_ast_parser_service import dom_ast_parser_service

class RepositoryValidatorService:
    """
    Non-invasive Repository Pre-Execution Validator Service.
    Validates repository clone integrity, build configs, controllers, routes,
    templates, and DOM selectors before generating Playwright or Selenium tests.
    """

    def validate_repository(self, project_dir: Path) -> Dict[str, Any]:
        """Runs pre-generation validation checks on target repository directory."""
        diagnostics = {
            "cloned_successfully": False,
            "build_config_found": False,
            "build_tool": None,
            "controllers_count": 0,
            "routes_count": 0,
            "elements_count": 0,
            "is_testable": False,
            "errors": [],
            "warnings": []
        }

        if not project_dir.exists():
            diagnostics["errors"].append(f"Project directory {project_dir} does not exist.")
            return diagnostics

        diagnostics["cloned_successfully"] = True

        # Check build config
        if (project_dir / "pom.xml").exists():
            diagnostics["build_config_found"] = True
            diagnostics["build_tool"] = "Maven (pom.xml)"
        elif (project_dir / "build.gradle").exists() or (project_dir / "build.gradle.kts").exists():
            diagnostics["build_config_found"] = True
            diagnostics["build_tool"] = "Gradle"
        elif (project_dir / "package.json").exists():
            diagnostics["build_config_found"] = True
            diagnostics["build_tool"] = "Node.js (package.json)"
        else:
            diagnostics["warnings"].append("No standard build configuration (pom.xml, build.gradle, package.json) detected.")

        # Discover routes & DOM elements
        routes = dom_ast_parser_service.extract_controller_annotations(project_dir)
        elements = dom_ast_parser_service.extract_dom_elements(project_dir)

        diagnostics["routes_count"] = len(routes)
        diagnostics["elements_count"] = len(elements)
        
        unique_controllers = {r["controller"] for r in routes}
        diagnostics["controllers_count"] = len(unique_controllers)

        if len(routes) == 0 and len(elements) == 0:
            diagnostics["warnings"].append("No controller routes or UI template elements discovered in repository.")
        
        # Repository is testable if cloned and contains either routes, UI templates, or build config
        diagnostics["is_testable"] = diagnostics["cloned_successfully"] and (diagnostics["build_config_found"] or len(routes) > 0 or len(elements) > 0)

        return diagnostics

repository_validator_service = RepositoryValidatorService()

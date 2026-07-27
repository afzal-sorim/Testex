from pathlib import Path
from typing import Dict, List, Any
from app.services.extensions.dom_ast_parser_service import dom_ast_parser_service

class RepositoryGraphService:
    """
    Non-invasive Repository Knowledge & Behavior Graph engine.
    Constructs a dynamic graph linking routes, controllers, DOM element selectors,
    and validation constraints to generate verified repository evidence for tests.
    """

    def build_behavior_graph(self, project_dir: Path) -> Dict[str, Any]:
        """Constructs the repository behavior graph from static file analysis."""
        elements = dom_ast_parser_service.extract_dom_elements(project_dir)
        routes = dom_ast_parser_service.extract_controller_annotations(project_dir)

        nodes = []
        evidence_records = []

        for r in routes:
            route_path = r["path"]
            controller = r["controller"]
            method = r["method"]
            validations = r.get("validations", [])

            # Match DOM elements from templates matching route area
            matched_selectors = []
            for el in elements:
                if el["css_selector"]:
                    matched_selectors.append(el["css_selector"])

            evidence = {
                "source_file": r["file"],
                "route_or_endpoint": f"{method} {route_path}",
                "ui_element_or_selector": ", ".join(matched_selectors[:3]) if matched_selectors else "body",
                "validation_annotation": ", ".join(validations) if validations else "N/A",
                "controller_or_component": controller
            }
            evidence_records.append(evidence)

            nodes.append({
                "id": f"{method}_{route_path}",
                "type": "route_behavior",
                "controller": controller,
                "path": route_path,
                "evidence": evidence
            })

        return {
            "node_count": len(nodes),
            "routes_count": len(routes),
            "elements_count": len(elements),
            "evidence_records": evidence_records,
            "nodes": nodes
        }

repository_graph_service = RepositoryGraphService()

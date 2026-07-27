import re
from pathlib import Path
from typing import Dict, List, Any, Optional

class DOMASTParserService:
    """
    Non-invasive AST & HTML/JSX/TSX/JSP/Vue parser service.
    Extracts DOM element attributes (id, name, data-testid, aria-label, placeholder, CSS classes)
    and route annotations (@GetMapping, @PostMapping, etc.) without altering any existing codebase files.
    """

    def extract_dom_elements(self, project_dir: Path) -> List[Dict[str, Any]]:
        """Scans templates and UI source files for interactive DOM elements."""
        elements = []
        if not project_dir.exists():
            return elements

        ui_extensions = {".html", ".jsp", ".jsx", ".tsx", ".vue", ".htm"}
        for file_path in project_dir.rglob("*"):
            if file_path.suffix.lower() not in ui_extensions:
                continue
            if any(part in {"target", "build", ".git", "node_modules"} for part in file_path.parts):
                continue
            
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                parsed = self._parse_file_content(content, file_path.name)
                elements.extend(parsed)
            except Exception as e:
                print(f"[DOMASTParserService] Error parsing {file_path.name}: {e}")

        return elements

    def _parse_file_content(self, content: str, filename: str) -> List[Dict[str, Any]]:
        results = []
        # Match input, button, select, textarea, form tags with attributes
        tag_pattern = re.compile(r'<(input|button|select|textarea|form|a|table)\b([^>]*)>', re.IGNORECASE)
        
        for match in tag_pattern.finditer(content):
            tag_name = match.group(1).lower()
            attrs_raw = match.group(2)
            
            attr_dict = self._extract_attributes(attrs_raw)
            element_id = attr_dict.get("id")
            element_name = attr_dict.get("name")
            test_id = attr_dict.get("data-testid") or attr_dict.get("data-test") or attr_dict.get("data-cy")
            aria_label = attr_dict.get("aria-label")
            placeholder = attr_dict.get("placeholder")
            element_type = attr_dict.get("type", "text" if tag_name == "input" else tag_name)
            css_class = attr_dict.get("class")

            # Determine best CSS selector
            css_selector = None
            if test_id:
                css_selector = f"[data-testid='{test_id}']"
            elif element_id:
                css_selector = f"#{element_id}"
            elif element_name:
                css_selector = f"{tag_name}[name='{element_name}']"
            elif placeholder:
                css_selector = f"{tag_name}[placeholder='{placeholder}']"
            elif css_class:
                first_class = css_class.split()[0]
                css_selector = f"{tag_name}.{first_class}"
            else:
                css_selector = tag_name

            results.append({
                "tag": tag_name,
                "type": element_type,
                "id": element_id,
                "name": element_name,
                "test_id": test_id,
                "aria_label": aria_label,
                "placeholder": placeholder,
                "css_selector": css_selector,
                "source_file": filename
            })

        return results

    def _extract_attributes(self, attrs_raw: str) -> Dict[str, str]:
        attrs = {}
        pattern = re.compile(r'([a-zA-Z0-9_-]+)\s*=\s*["\']([^"\']*)["\']')
        for match in pattern.finditer(attrs_raw):
            key = match.group(1).lower()
            val = match.group(2)
            attrs[key] = val
        return attrs

    def extract_controller_annotations(self, project_dir: Path) -> List[Dict[str, Any]]:
        """Parses Java/Spring controllers for routes and validation annotations."""
        routes = []
        if not project_dir.exists():
            return routes

        for file_path in project_dir.rglob("*.java"):
            if any(part in {"target", "build", ".git", "node_modules"} for part in file_path.parts):
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if "@Controller" in content or "@RestController" in content:
                    class_match = re.search(r'public\s+class\s+(\w+)', content)
                    class_name = class_match.group(1) if class_match else file_path.name
                    
                    mapping_matches = re.finditer(
                        r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)\s*\(\s*(?:value\s*=\s*)?["\']([^"\']+)["\']',
                        content
                    )
                    for m in mapping_matches:
                        method = m.group(1).upper()
                        if method == "REQUESTMAPPING":
                            method = "GET"
                        path = m.group(2)
                        
                        # Check validations near method
                        has_valid = "@Valid" in content
                        has_not_blank = "@NotBlank" in content or "@NotEmpty" in content
                        validations = []
                        if has_not_blank:
                            validations.append("@NotBlank")
                        if has_valid:
                            validations.append("@Valid")
                            
                        routes.append({
                            "controller": class_name,
                            "method": method,
                            "path": path,
                            "validations": validations,
                            "file": file_path.name
                        })
            except Exception as e:
                print(f"[DOMASTParserService] Error parsing controller {file_path.name}: {e}")

        return routes

dom_ast_parser_service = DOMASTParserService()

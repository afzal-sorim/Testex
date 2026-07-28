import os
import re
from pathlib import Path
from typing import List, Dict
from app.services.module_analysis.parser.base_parser import BaseParserAdapter
from app.services.module_analysis.metadata.project_metadata import (
    ProjectMetadata, EntityItem, ControllerItem, ServiceItem, RepositoryItem, ApiEndpoint
)


class PythonParserAdapter(BaseParserAdapter):
    """
    Python FastAPI / Django / Flask Parser Adapter.
    """

    def parse(self) -> ProjectMetadata:
        metadata = ProjectMetadata(language="PYTHON", build_tool="pip/poetry")

        py_files = []
        for root, dirs, files in os.walk(self.repo_dir):
            dirs[:] = [d for d in dirs if d not in {'.git', 'venv', '__pycache__', 'build', 'dist', '.pytest_cache'}]
            for f in files:
                if f.endswith('.py'):
                    p = Path(root) / f
                    rel = p.relative_to(self.repo_dir).as_posix()
                    py_files.append((p, rel, f[:-3]))

        metadata.all_source_files = [rel for _, rel, _ in py_files]

        for p, rel_path, module_name in py_files:
            if 'test' in rel_path.lower() or module_name.startswith('__'):
                continue

            try:
                content = p.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            # Extract class names
            class_matches = re.findall(r'class\s+([A-Z][a-zA-Z0-9_]+)', content)

            for class_name in class_matches:
                if class_name in {'Config', 'Settings', 'Base', 'BaseModel', 'Meta'}:
                    continue

                stem = self._extract_stem(class_name)
                if not stem or stem.lower() in {'core', 'app', 'data', 'base', 'config', 'util'}:
                    continue

                if 'Controller' in class_name or 'View' in class_name or 'router' in rel_path.lower() or 'api' in rel_path.lower():
                    apis = self._extract_python_apis(content, rel_path)
                    metadata.controllers.append(ControllerItem(name=class_name, stem=stem, apis=apis, source_file=rel_path))
                    metadata.apis.extend(apis)

                elif 'Service' in class_name or 'service' in rel_path.lower():
                    metadata.services.append(ServiceItem(name=class_name, stem=stem, source_file=rel_path))

                elif 'Repository' in class_name or 'repo' in rel_path.lower():
                    metadata.repositories.append(RepositoryItem(name=class_name, stem=stem, source_file=rel_path))

                elif 'Model' in class_name or '(Base)' in content or '(models.Model)' in content or '(BaseModel)' in content or '/models/' in rel_path.lower() or '/schemas/' in rel_path.lower():
                    attrs = self._extract_fields(content)
                    metadata.entities.append(EntityItem(name=class_name, stem=stem, attributes=attrs, source_file=rel_path))

        return metadata

    def _extract_python_apis(self, content: str, source_file: str) -> List[ApiEndpoint]:
        endpoints = []
        routes = re.findall(r'@(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
        for method, path in routes:
            endpoints.append(ApiEndpoint(path=path, method=method.upper(), source_file=source_file))
        return endpoints

    def _extract_fields(self, content: str) -> List[Dict[str, str]]:
        attrs = []
        py_fields = re.findall(r'([a-zA-Z0-9_]+)\s*:\s*([a-zA-Z0-9_\[\]\.\,]+)', content)
        for fname, ftype in py_fields[:10]:
            if fname not in {'self', 'cls', 'Config'}:
                attrs.append({"name": fname, "type": ftype.strip()})
        return attrs or [{"name": "id", "type": "int"}, {"name": "name", "type": "str"}]

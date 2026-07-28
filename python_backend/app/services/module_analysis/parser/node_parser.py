import os
import re
from pathlib import Path
from typing import List, Dict
from app.services.module_analysis.parser.base_parser import BaseParserAdapter
from app.services.module_analysis.metadata.project_metadata import (
    ProjectMetadata, EntityItem, ControllerItem, ServiceItem, RepositoryItem, ApiEndpoint
)


class NodeParserAdapter(BaseParserAdapter):
    """
    Node.js Express / NestJS / TypeScript / Mongoose / TypeORM Parser Adapter.
    """

    def parse(self) -> ProjectMetadata:
        metadata = ProjectMetadata(language="NODE", build_tool="npm/yarn")

        js_files = []
        for root, dirs, files in os.walk(self.repo_dir):
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.next'}]
            for f in files:
                if f.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    p = Path(root) / f
                    rel = p.relative_to(self.repo_dir).as_posix()
                    js_files.append((p, rel, f.split('.')[0]))

        metadata.all_source_files = [rel for _, rel, _ in js_files]

        for p, rel_path, file_stem in js_files:
            if 'test' in rel_path.lower() or 'spec' in rel_path.lower():
                continue

            try:
                content = p.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            # Class/interface or mongoose schema matches
            classes = re.findall(r'(?:export\s+)?(?:class|interface)\s+([A-Z][a-zA-Z0-9_]+)', content)
            mongoose_models = re.findall(r'mongoose\.model\s*\(\s*["\']([A-Za-z0-9_]+)["\']', content)
            classes.extend(mongoose_models)

            for class_name in classes:
                if class_name in {'Props', 'State', 'Config', 'App', 'Component'}:
                    continue

                stem = self._extract_stem(class_name)
                if not stem or stem.lower() in {'core', 'app', 'data', 'base', 'config', 'util'}:
                    continue

                if 'Controller' in class_name or '@Controller' in content or '/controllers/' in rel_path.lower() or '/routes/' in rel_path.lower():
                    apis = self._extract_node_apis(content, rel_path)
                    metadata.controllers.append(ControllerItem(name=class_name, stem=stem, apis=apis, source_file=rel_path))
                    metadata.apis.extend(apis)

                elif 'Service' in class_name or '@Injectable' in content or '/services/' in rel_path.lower():
                    metadata.services.append(ServiceItem(name=class_name, stem=stem, source_file=rel_path))

                elif 'Repository' in class_name or '/repository/' in rel_path.lower():
                    metadata.repositories.append(RepositoryItem(name=class_name, stem=stem, source_file=rel_path))

                elif '@Entity' in content or 'Schema' in class_name or '/models/' in rel_path.lower() or '/entities/' in rel_path.lower():
                    attrs = self._extract_fields(content)
                    metadata.entities.append(EntityItem(name=class_name, stem=stem, attributes=attrs, source_file=rel_path))

        return metadata

    def _extract_node_apis(self, content: str, source_file: str) -> List[ApiEndpoint]:
        endpoints = []
        routes = re.findall(r'router\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
        nest_routes = re.findall(r'@(Get|Post|Put|Delete|Patch)\s*\(\s*["\']?([^"\'\)]*)["\']?\s*\)', content)
        
        for method, path in routes:
            endpoints.append(ApiEndpoint(path=path, method=method.upper(), source_file=source_file))
        for method, path in nest_routes:
            endpoints.append(ApiEndpoint(path=path or "/", method=method.upper(), source_file=source_file))
            
        return endpoints

    def _extract_fields(self, content: str) -> List[Dict[str, str]]:
        attrs = []
        ts_fields = re.findall(r'([a-zA-Z0-9_]+)\s*\??\s*:\s*([a-zA-Z0-9_\[\]\.\,\s]+)', content)
        for fname, ftype in ts_fields[:10]:
            if fname not in {'export', 'import', 'const', 'let', 'var'}:
                attrs.append({"name": fname, "type": ftype.strip()})
        return attrs or [{"name": "id", "type": "string"}, {"name": "name", "type": "string"}]

import os
import re
from pathlib import Path
from typing import List, Dict, Set
from app.services.module_analysis.parser.base_parser import BaseParserAdapter
from app.services.module_analysis.metadata.project_metadata import (
    ProjectMetadata, EntityItem, ControllerItem, ServiceItem, RepositoryItem, ApiEndpoint
)


class JavaParserAdapter(BaseParserAdapter):
    """
    Java Spring / Jakarta Parser Adapter.
    Extracts Controllers, Services, Repositories, Entities, and APIs into ProjectMetadata.
    """

    _IGNORE_CLASSES = {
        'Main', 'App', 'Application', 'SpringBootApplication', 'BaseEntity', 'NamedEntity',
        'Config', 'Configuration', 'Utils', 'Helper', 'Common', 'Data', 'Core', 'SwaggerConfig',
        'Packageinfo', 'PackageInfo', 'package-info'
    }

    def parse(self) -> ProjectMetadata:
        metadata = ProjectMetadata(language="JAVA", build_tool="Maven/Gradle")

        java_files = []
        for root, dirs, files in os.walk(self.repo_dir):
            dirs[:] = [d for d in dirs if d not in {'.git', 'target', 'build', '.idea', '.vscode'}]
            for f in files:
                if f.endswith('.java'):
                    p = Path(root) / f
                    rel = p.relative_to(self.repo_dir).as_posix()
                    java_files.append((p, rel, f[:-5]))

        metadata.all_source_files = [rel for _, rel, _ in java_files]

        for p, rel_path, class_name in java_files:
            if 'test' in rel_path.lower() or class_name in self._IGNORE_CLASSES:
                continue

            try:
                content = p.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue

            stem = self._extract_stem(class_name)
            if not stem or stem.lower() in {'core', 'app', 'data', 'base', 'config', 'util', 'common'}:
                continue

            # 1. Controller detection
            if '@Controller' in content or '@RestController' in content or 'Controller' in class_name:
                apis = self._extract_java_apis(content, rel_path)
                metadata.controllers.append(ControllerItem(
                    name=class_name,
                    stem=stem,
                    apis=apis,
                    source_file=rel_path
                ))
                metadata.apis.extend(apis)

            # 2. Service detection
            elif '@Service' in content or 'Service' in class_name:
                metadata.services.append(ServiceItem(
                    name=class_name,
                    stem=stem,
                    source_file=rel_path
                ))

            # 3. Repository / DAO detection
            elif '@Repository' in content or 'Repository' in class_name or 'Dao' in class_name or 'extends JpaRepository' in content or 'extends CrudRepository' in content:
                metadata.repositories.append(RepositoryItem(
                    name=class_name,
                    stem=stem,
                    source_file=rel_path
                ))

            # 4. Entity / Domain Model detection
            elif (
                '@Entity' in content or '@Table' in content or '@Document' in content or
                'extends BaseEntity' in content or 'extends NamedEntity' in content or
                '/model/' in rel_path.lower() or '/domain/' in rel_path.lower() or '/entity/' in rel_path.lower() or '/entities/' in rel_path.lower()
            ):
                attrs = self._extract_fields(content)
                metadata.entities.append(EntityItem(
                    name=class_name,
                    stem=stem,
                    attributes=attrs,
                    source_file=rel_path
                ))

        return metadata

    def _extract_java_apis(self, content: str, source_file: str) -> List[ApiEndpoint]:
        endpoints = []
        base_path = ""
        req_match = re.search(r'@RequestMapping\s*\(\s*(?:value\s*=\s*)?["\']([^"\']+)["\']', content)
        if req_match:
            base_path = req_match.group(1).rstrip('/')

        mapping_pats = [
            (r'@GetMapping\s*\(\s*(?:value\s*=\s*)?["\']([^"\']+)["\']', 'GET'),
            (r'@PostMapping\s*\(\s*(?:value\s*=\s*)?["\']([^"\']+)["\']', 'POST'),
            (r'@PutMapping\s*\(\s*(?:value\s*=\s*)?["\']([^"\']+)["\']', 'PUT'),
            (r'@DeleteMapping\s*\(\s*(?:value\s*=\s*)?["\']([^"\']+)["\']', 'DELETE'),
            (r'@RequestMapping\s*\(\s*(?:value\s*=\s*)?["\']([^"\']+)["\']', 'GET')
        ]

        for pat, method in mapping_pats:
            for sub in re.findall(pat, content):
                full_path = f"{base_path}/{sub.lstrip('/')}".rstrip('/')
                if full_path:
                    endpoints.append(ApiEndpoint(path=full_path, method=method, source_file=source_file))

        if not endpoints and base_path:
            endpoints.append(ApiEndpoint(path=base_path, method="GET", source_file=source_file))

        return endpoints

    def _extract_fields(self, content: str) -> List[Dict[str, str]]:
        attrs = []
        fields_raw = re.findall(r'(?:private|protected|public)\s+([A-Z][a-zA-Z0-9_<>,\s]*)\s+([a-zA-Z0-9_]+)\s*(?:=|[;,\n])', content)
        for ftype, fname in fields_raw[:10]:
            clean_type = ftype.strip()
            if fname not in {'serialVersionUID', 'class', 'id'} and clean_type not in {'class', 'public'}:
                attrs.append({"name": fname, "type": clean_type})
        if not attrs:
            attrs = [{"name": "id", "type": "Long"}, {"name": "name", "type": "String"}]
        return attrs

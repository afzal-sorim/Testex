import re
from typing import List, Dict, Any, Set
from app.services.module_analysis.metadata.project_metadata import ProjectMetadata


class ModuleGroup:
    def __init__(self, stem: str, display_name: str):
        self.stem = stem
        self.display_name = display_name
        self.controllers: Set[str] = set()
        self.services: Set[str] = set()
        self.repositories: Set[str] = set()
        self.entities: Set[str] = set()
        self.apis: Set[str] = set()
        self.files: Set[str] = set()
        self.attributes: List[Dict[str, str]] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stem": self.stem,
            "name": self.display_name,
            "controllers": sorted(list(self.controllers)),
            "services": sorted(list(self.services)),
            "repositories": sorted(list(self.repositories)),
            "entities": sorted(list(self.entities)),
            "apis": sorted(list(self.apis)),
            "files": sorted(list(self.files)),
            "attributes": self.attributes[:10]
        }


class ModuleDetector:
    """
    Step 4: Language-independent Business Module Grouping.
    Groups controllers, services, repositories, entities, and APIs by business stem.
    Filters out technical architecture noise (Core, App, Data, Config, Base).
    """

    _GENERIC_TECHNICAL_STEMS = {
        'core', 'app', 'application', 'data', 'base', 'config', 'configuration',
        'util', 'utils', 'utility', 'common', 'shared', 'internal', 'main',
        'web', 'rest', 'api', 'system', 'test', 'sample', 'example', 'demo'
    }

    def detect_modules(self, metadata: ProjectMetadata) -> List[Dict[str, Any]]:
        modules: Dict[str, ModuleGroup] = {}

        def get_or_create_group(raw_stem: str) -> ModuleGroup:
            clean_stem = re.sub(r'[^a-zA-Z0-9]', '', raw_stem).strip()
            key = clean_stem.lower()

            # 100% Dynamic Business Title Generation from Code Stems
            formatted = re.sub(r'([a-z])([A-Z])', r'\1 \2', clean_stem).title()
            if not any(formatted.endswith(w) for w in ['Management', 'Processing', 'Services', 'System', 'Control', 'Tracking', 'Operations']):
                title = f"{formatted} Management"
            else:
                title = formatted

            if key not in modules:
                modules[key] = ModuleGroup(stem=clean_stem, display_name=title)
            return modules[key]

        # 1. Group Entities (highest domain model signal)
        for entity in metadata.entities:
            if entity.stem.lower() in self._GENERIC_TECHNICAL_STEMS:
                continue
            group = get_or_create_group(entity.stem)
            group.entities.add(entity.name)
            if entity.source_file: group.files.add(entity.source_file)
            if entity.attributes and not group.attributes:
                group.attributes = entity.attributes

        # 2. Group Controllers & APIs
        for ctrl in metadata.controllers:
            if ctrl.stem.lower() in self._GENERIC_TECHNICAL_STEMS:
                continue
            group = get_or_create_group(ctrl.stem)
            group.controllers.add(ctrl.name)
            if ctrl.source_file: group.files.add(ctrl.source_file)
            for api in ctrl.apis:
                group.apis.add(f"{api.method} {api.path}")

        # 3. Group Services
        for srv in metadata.services:
            if srv.stem.lower() in self._GENERIC_TECHNICAL_STEMS:
                continue
            group = get_or_create_group(srv.stem)
            group.services.add(srv.name)
            if srv.source_file: group.files.add(srv.source_file)

        # 4. Group Repositories
        for repo in metadata.repositories:
            if repo.stem.lower() in self._GENERIC_TECHNICAL_STEMS:
                continue
            group = get_or_create_group(repo.stem)
            group.repositories.add(repo.name)
            if repo.source_file: group.files.add(repo.source_file)

        # Filter out empty or purely technical noise modules
        result = [
            g.to_dict() for g in modules.values()
            if g.entities or g.controllers or g.services or len(g.files) >= 2
        ]

        # Sort by component weight (most prominent modules first)
        result.sort(key=lambda m: len(m["entities"])*3 + len(m["controllers"])*2 + len(m["services"])*2 + len(m["apis"]), reverse=True)
        return result

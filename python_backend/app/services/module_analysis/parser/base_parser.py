from abc import ABC, abstractmethod
from pathlib import Path
from app.services.module_analysis.metadata.project_metadata import ProjectMetadata


class BaseParserAdapter(ABC):
    """
    Step 2 Interface: Language-specific parser adapter.
    All adapters return the same ProjectMetadata model.
    """

    def __init__(self, repo_dir: Path):
        self.repo_dir = Path(repo_dir)

    @abstractmethod
    def parse(self) -> ProjectMetadata:
        pass

    def _extract_stem(self, name: str) -> str:
        """Extract business stem by stripping architectural role suffixes."""
        import re
        suffixes = (
            'Controller', 'RestController', 'Service', 'ServiceImpl', 'Repository', 'Dao',
            'Entity', 'Dto', 'DTO', 'Model', 'View', 'Component', 'Handler', 'Filter',
            'Manager', 'Resource', 'Endpoint', 'Router', 'Api', 'API'
        )
        stem = name
        for s in suffixes:
            if stem.endswith(s) and len(stem) > len(s):
                stem = stem[:-len(s)]
                break
        stem = re.sub(r'([a-z])([A-Z])', r'\1 \2', stem).strip()
        return stem or name

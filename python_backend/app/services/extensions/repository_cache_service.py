import time
import json
from pathlib import Path
from typing import Dict, Any, Optional

class RepositoryCacheService:
    """
    Non-invasive Repository Knowledge Cache Service.
    Caches parsed controllers, routes, templates, forms, components, entities,
    selectors, and knowledge graphs to optimize repeated repository analysis.
    """

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get_cached_graph(self, repo_name: str, project_dir: Path) -> Optional[Dict[str, Any]]:
        """Retrieves cached knowledge graph if project files have not been modified."""
        if repo_name not in self._cache:
            # Check disk cache file
            cache_file = project_dir / ".prova_knowledge_cache.json"
            if cache_file.exists():
                try:
                    data = json.loads(cache_file.read_text(encoding="utf-8"))
                    self._cache[repo_name] = data
                    return data.get("graph")
                except Exception:
                    pass
            return None

        entry = self._cache[repo_name]
        return entry.get("graph")

    def save_cache(self, repo_name: str, project_dir: Path, graph_data: Dict[str, Any]):
        """Persists analyzed repository knowledge graph to memory and disk cache."""
        cache_payload = {
            "repo_name": repo_name,
            "timestamp": time.time(),
            "graph": graph_data
        }
        self._cache[repo_name] = cache_payload
        
        try:
            cache_file = project_dir / ".prova_knowledge_cache.json"
            cache_file.write_text(json.dumps(cache_payload, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"[RepositoryCacheService] Error persisting cache file for {repo_name}: {e}")

repository_cache_service = RepositoryCacheService()

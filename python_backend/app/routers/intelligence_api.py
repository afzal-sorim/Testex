from fastapi import APIRouter
from app.config import app_config
from app.services.extensions.repository_graph_service import repository_graph_service
from app.services.extensions.repository_validator_service import repository_validator_service
from app.services.extensions.repository_cache_service import repository_cache_service

router = APIRouter(prefix="/api/v2/intelligence", tags=["Repository Intelligence Extensions"])

@router.get("/graph/{repo_name}")
async def get_repository_evidence_graph(repo_name: str):
    """Returns Repository Behavior Knowledge Graph and Evidence records."""
    project_dir = app_config.get_project_dir(repo_name)
    cached = repository_cache_service.get_cached_graph(repo_name, project_dir)
    if cached:
        return {"status": "SUCCESS", "cached": True, "repo_name": repo_name, "graph": cached}

    graph = repository_graph_service.build_behavior_graph(project_dir)
    repository_cache_service.save_cache(repo_name, project_dir, graph)
    return {"status": "SUCCESS", "cached": False, "repo_name": repo_name, "graph": graph}

@router.get("/validate/{repo_name}")
async def validate_repository_readiness(repo_name: str):
    """Runs pre-generation validation and returns health diagnostics."""
    project_dir = app_config.get_project_dir(repo_name)
    diagnostics = repository_validator_service.validate_repository(project_dir)
    return {"status": "SUCCESS", "repo_name": repo_name, "diagnostics": diagnostics}

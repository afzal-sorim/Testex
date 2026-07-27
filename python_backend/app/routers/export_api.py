from fastapi import APIRouter
from app.config import app_config
from app.services.extensions.pom_generator_service import pom_generator_service
from app.services.extensions.cicd_exporter_service import cicd_exporter_service

router = APIRouter(prefix="/api/v2/export", tags=["Export Extensions"])

@router.get("/pom/{repo_name}")
async def export_page_object_models(repo_name: str, framework: str = "playwright"):
    """Generates Page Object Model classes for Playwright or Selenium."""
    project_dir = app_config.get_project_dir(repo_name)
    if framework.lower() == "selenium":
        poms = pom_generator_service.generate_selenium_pom(project_dir)
    else:
        poms = pom_generator_service.generate_playwright_pom(project_dir)
    return {
        "status": "SUCCESS",
        "repo_name": repo_name,
        "framework": framework,
        "pom_files": list(poms.keys())
    }

@router.post("/cicd/{repo_name}")
async def export_cicd_pipelines(repo_name: str):
    """Exports automated GitHub Actions & Jenkins workflow pipelines."""
    project_dir = app_config.get_project_dir(repo_name)
    gh_path = cicd_exporter_service.export_github_actions(repo_name, project_dir)
    jk_path = cicd_exporter_service.export_jenkinsfile(repo_name, project_dir)
    return {
        "status": "SUCCESS",
        "repo_name": repo_name,
        "github_actions": str(gh_path),
        "jenkinsfile": str(jk_path)
    }

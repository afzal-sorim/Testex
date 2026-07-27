from fastapi import APIRouter
from app.config import app_config
from app.services.extensions.junit_allure_exporter_service import junit_allure_exporter_service
from app.services.playwright_service import playwright_service

router = APIRouter(prefix="/api/v2/reports", tags=["Enterprise Reporting Extensions"])

@router.post("/junit/{repo_name}")
async def export_junit_report(repo_name: str):
    """Exports test execution results as standard JUnit XML report format."""
    project_dir = app_config.get_project_dir(repo_name)
    status_dict = playwright_service.get_status(repo_name, project_dir)
    reports_dir = project_dir / "reports"
    xml_file = junit_allure_exporter_service.export_junit_xml(repo_name, status_dict, reports_dir)
    return {
        "status": "SUCCESS",
        "repo_name": repo_name,
        "junit_file": str(xml_file)
    }

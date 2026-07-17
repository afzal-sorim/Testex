import asyncio
from pathlib import Path
import json
import sys

# Add backend to path
sys.path.insert(0, r"c:\Users\ST-Balakumaran\Downloads\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\Testex-92bbf37d232ecd081fe67ba27facad4e4494d74b\python_backend")

from app.services.playwright_service import PlaywrightService
from app.config import app_config

async def test_status():
    repo_name = "Student_Mangement_System"
    project_dir = app_config.get_project_dir(repo_name)
    service = PlaywrightService()
    
    # Check what get_status returns
    status = service.get_status(repo_name, project_dir)
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    asyncio.run(test_status())

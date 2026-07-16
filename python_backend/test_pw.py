import asyncio
from pathlib import Path
from app.services.playwright_service import PlaywrightService
import sys
import shutil

async def main():
    service = PlaywrightService()
    # Let's find any project in the workspace
    from app.config import app_config
    workspace_dir = app_config.workspace_directory
    print(f"Workspace: {workspace_dir}")
    
    # Just grab the first project dir or java_convertion 4
    project_dir = Path(r"C:\Users\ST-Sivaranjini\Downloads\java_convertion 4")
    if not project_dir.exists():
        projects = list(workspace_dir.glob("*"))
        if projects:
            project_dir = projects[0]
            
    print(f"Testing on project dir: {project_dir}")
    
    res = await service.run_playwright_tests("test_repo", project_dir)
    print("Result:")
    print(res)

if __name__ == "__main__":
    asyncio.run(main())

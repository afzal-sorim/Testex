import os
import zipfile
from pathlib import Path

source_dir = Path(r"c:\Users\ST-Sivaranjini\OneDrive - SORIM TECHNOLOGIES\Desktop\Testex working code")
output_zip = source_dir / "frontend" / "public" / "project.zip"

# Ensure target directory exists
output_zip.parent.mkdir(parents=True, exist_ok=True)

exclude_dirs = {
    "node_modules",
    "venv",
    ".git",
    "target",
    ".idea",
    "playwright-report",
    "test-results",
    ".metadata",
    "__pycache__",
    ".pytest_cache",
    ".ipynb_checkpoints",
    "apache-maven-3.9.6"
}

exclude_files = {
    "project.zip"
}

print("Zipping files...")
count = 0
with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(source_dir):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file in exclude_files:
                continue
            file_path = Path(root) / file
            # Relative path to keep the zip file clean
            rel_path = file_path.relative_to(source_dir)
            # Skip if it is the output zip file itself
            if file_path == output_zip:
                continue
            try:
                zipf.write(file_path, rel_path)
                count += 1
            except Exception as e:
                print(f"Skipping file {file_path} due to error: {e}")

print(f"Successfully zipped {count} files to: {output_zip}")

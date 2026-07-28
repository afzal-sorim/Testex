import os
from pathlib import Path
from typing import Dict, Any


class LanguageDetector:
    """
    Step 1: Inspect repository build files to identify project language and build tool.
    Takes milliseconds.
    """

    def __init__(self, repo_dir: Path):
        self.repo_dir = Path(repo_dir)

    def detect(self) -> Dict[str, str]:
        if (self.repo_dir / "pom.xml").exists():
            return {"language": "JAVA", "build_tool": "Maven"}
        if (self.repo_dir / "build.gradle").exists() or (self.repo_dir / "build.gradle.kts").exists():
            return {"language": "JAVA", "build_tool": "Gradle"}
        if (self.repo_dir / "package.json").exists():
            return {"language": "NODE", "build_tool": "npm/yarn"}
        if (self.repo_dir / "requirements.txt").exists() or (self.repo_dir / "pyproject.toml").exists() or (self.repo_dir / "Pipfile").exists():
            return {"language": "PYTHON", "build_tool": "pip/poetry"}
        if (self.repo_dir / "go.mod").exists():
            return {"language": "GO", "build_tool": "go mod"}
        if (self.repo_dir / "Cargo.toml").exists():
            return {"language": "RUST", "build_tool": "cargo"}

        for p in self.repo_dir.glob("*.csproj"):
            return {"language": "CSHARP", "build_tool": "dotnet"}

        # File extension fallback
        ext_counts = {"JAVA": 0, "NODE": 0, "PYTHON": 0, "GO": 0, "CSHARP": 0}
        for root, dirs, files in os.walk(self.repo_dir):
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", "target", "build", "venv", "dist", ".next"}]
            for f in files:
                l = f.lower()
                if l.endswith(".java"): ext_counts["JAVA"] += 1
                elif l.endswith((".js", ".jsx", ".ts", ".tsx")): ext_counts["NODE"] += 1
                elif l.endswith(".py"): ext_counts["PYTHON"] += 1
                elif l.endswith(".go"): ext_counts["GO"] += 1
                elif l.endswith(".cs"): ext_counts["CSHARP"] += 1

        top_lang = max(ext_counts, key=ext_counts.get)
        if ext_counts[top_lang] > 0:
            return {"language": top_lang, "build_tool": "Standard"}

        return {"language": "JAVA", "build_tool": "Maven"}

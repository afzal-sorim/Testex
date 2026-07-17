import os
import json
import uuid
from pathlib import Path
from app.config import app_config

class SessionService:
    def __init__(self):
        self.sessions_dir = app_config.workspace_directory / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def _get_session_path(self, session_id: str) -> Path:
        return self.sessions_dir / f"{session_id}.json"

    def create_session(self, repo_url: str = "", local_path: str = "") -> str:
        session_id = str(uuid.uuid4())
        session_data = {
            "sessionId": session_id,
            "repoUrl": repo_url,
            "localPath": local_path,
            "analysisResult": None,
            "workflowState": {
                "analysisCompleted": False,
                "runnerCompleted": False
            },
            "migrationResult": None,
            "stats": {
                "reposAnalyzed": 0,
                "migrationsRun": 0,
                "filesConverted": 0
            },
            "migrations": []
        }
        self.save_session(session_id, session_data)
        return session_id

    def get_session(self, session_id: str) -> dict:
        path = self._get_session_path(session_id)
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_session(self, session_id: str, data: dict):
        path = self._get_session_path(session_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def update_session(self, session_id: str, updates: dict) -> dict:
        session_data = self.get_session(session_id)
        if not session_data:
            raise ValueError("Session not found")
        
        # Merge updates
        for key, value in updates.items():
            if isinstance(value, dict) and isinstance(session_data.get(key), dict):
                session_data[key].update(value)
            else:
                session_data[key] = value
                
        self.save_session(session_id, session_data)
        return session_data

session_service = SessionService()

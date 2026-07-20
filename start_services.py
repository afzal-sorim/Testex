import os
import subprocess
import time
import sys
import json
from pathlib import Path

# Paths setup
WORKSPACE_ROOT = Path(__file__).parent.absolute()
REDIS_DIR = WORKSPACE_ROOT / "redis"
REDIS_SERVER = REDIS_DIR / "redis-server.exe"
BACKEND_DIR = WORKSPACE_ROOT / "python_backend"
VENV_PYTHON = BACKEND_DIR / "venv" / "Scripts" / "python.exe"
VENV_CELERY = BACKEND_DIR / "venv" / "Scripts" / "celery.exe"
LOGS_DIR = WORKSPACE_ROOT / "service_logs"

# Ensure logs directory exists
LOGS_DIR.mkdir(exist_ok=True)

print(f"Workspace Root: {WORKSPACE_ROOT}")

# 1. Start Redis Server
print("\n[1/4] Starting Redis Server...")
redis_log = open(LOGS_DIR / "redis.log", "w", encoding="utf-8")
try:
    redis_proc = subprocess.Popen(
        [str(REDIS_SERVER)],
        cwd=str(REDIS_DIR),
        stdout=redis_log,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    print("Redis Server process launched.")
except Exception as e:
    print(f"Error starting Redis: {e}")
    sys.exit(1)

# Wait a second for Redis to initialize
time.sleep(2)

# Set up environment variables for child processes to avoid charmap encode errors with emojis
env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"

# Run database migrations
print("\n[*] Running Database Migrations (Alembic)...")
try:
    subprocess.run(
        [str(VENV_PYTHON), "-m", "alembic", "upgrade", "head"],
        cwd=str(BACKEND_DIR),
        check=True,
        env=env
    )
    print("Database migrations applied successfully.")
except Exception as e:
    print(f"Warning: Database migration failed: {e}")

# 2. Start FastAPI Backend
print("\n[2/4] Starting FastAPI Backend...")
backend_log = open(LOGS_DIR / "backend.log", "w", encoding="utf-8")
try:
    # Run main.py using virtual environment python
    backend_proc = subprocess.Popen(
        [str(VENV_PYTHON), "main.py"],
        cwd=str(BACKEND_DIR),
        stdout=backend_log,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
        env=env
    )
    print("FastAPI Backend process launched (listening on port 8000).")
except Exception as e:
    print(f"Error starting FastAPI: {e}")
    sys.exit(1)

# 3. Start Celery Worker
print("\n[3/4] Starting Celery Worker...")
celery_log = open(LOGS_DIR / "celery.log", "w", encoding="utf-8")
try:
    celery_proc = subprocess.Popen(
        [str(VENV_CELERY), "-A", "app.celery_app.celery_app", "worker", "--loglevel=info", "-P", "solo"],
        cwd=str(BACKEND_DIR),
        stdout=celery_log,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
        env=env
    )
    print("Celery Worker process launched.")
except Exception as e:
    print(f"Error starting Celery: {e}")
    sys.exit(1)

# 4. Set up Local URL Info
print("\n[4/4] Setting up Local URL Info...")
(WORKSPACE_ROOT / "tunnel_url.txt").write_text("http://localhost:8000", encoding="utf-8")
print("\n" + "="*50)
print(f" SUCCESS: Services running locally!")
print(f" Backend API URL: http://localhost:8000")
print("="*50)

print("\nAll background services are running! Logs are stored in 'service_logs/' folder.")
print("To stop all services, terminate this script (Ctrl+C).")

try:
    # Keep the script running to monitor processes
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTerminating background services...")
    # Clean up subprocesses
    try:
        redis_proc.terminate()
        backend_proc.terminate()
        celery_proc.terminate()
    except Exception:
        pass
    print("Services stopped.")

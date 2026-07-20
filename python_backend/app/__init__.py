"""Backend app package."""
from __future__ import annotations
import os
from pathlib import Path

# Monkey patch redis.ConnectionPool to force protocol=2 (RESP2) for compatibility with older Redis servers
try:
    import redis
    original_pool_init = redis.ConnectionPool.__init__
    def patched_pool_init(self, *args, **connection_kwargs):
        connection_kwargs['protocol'] = 2
        original_pool_init(self, *args, **connection_kwargs)
    redis.ConnectionPool.__init__ = patched_pool_init
except Exception:
    pass





def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


_load_env_file(Path(__file__).resolve().parent.parent / ".env")
#!/bin/bash

# If REDIS_URL points to localhost or is empty, we spin up local redis-server
if [[ "$REDIS_URL" == *"localhost"* ]] || [[ "$REDIS_URL" == *"127.0.0.1"* ]] || [ -z "$REDIS_URL" ]; then
    echo "Starting local Redis server..."
    redis-server --daemonize yes
    export REDIS_URL="redis://127.0.0.1:6379/0"
else
    echo "Using external Redis server: $REDIS_URL"
fi

# Start the Celery worker process in the background.
# Restrict to solo pool and 1 concurrency to minimize RAM footprint.
echo "Starting Celery worker..."
celery -A app.celery_app.celery_app worker --loglevel=info -P solo --concurrency=1 &

# Start the FastAPI app in the foreground.
# Bind to the Render-provided PORT, default to 8000.
echo "Starting FastAPI server on port ${PORT:-8000}..."
exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"

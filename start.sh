#!/bin/bash
set -e

echo "🚀 Starting S1NGULARITY..."

# Initialize database if needed
echo "🗄️  Initializing database..."
python init_db.py || echo "⚠️  Database initialization failed (may already be initialized)"

# Start the application
echo "✅ Starting FastAPI server..."
exec uvicorn main:app --host "${HOST:-0.0.0.0}" --port "${PORT:-8000}" --workers "${WORKERS:-4}"

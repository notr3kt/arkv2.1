#!/bin/bash
# Railway initialization script

echo "🚀 Starting S1NGULARITY deployment on Railway..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Initialize database
echo "🗄️  Initializing PostgreSQL database..."
python init_db.py

# Start the application
echo "✅ Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}

#!/bin/bash
# S1NGULARITY Quick Start Script

set -e

echo "🚀 S1NGULARITY Quick Start"
echo "================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Copying .env.example to .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys before proceeding!"
    echo ""
    echo "Required API keys:"
    echo "  - JOBDIVA_CLIENT_ID"
    echo "  - JOBDIVA_USERNAME"
    echo "  - JOBDIVA_PASSWORD"
    echo "  - ANTHROPIC_API_KEY (or OPENAI_API_KEY)"
    echo "  - TAVILY_API_KEY"
    echo ""
    echo "Run this script again after updating .env"
    exit 1
fi

# Check for required API keys
echo "🔍 Checking environment configuration..."

MISSING_KEYS=()

if ! grep -q "JOBDIVA_CLIENT_ID=.*[^[:space:]]" .env; then
    MISSING_KEYS+=("JOBDIVA_CLIENT_ID")
fi

if ! grep -q "TAVILY_API_KEY=.*[^[:space:]]" .env; then
    MISSING_KEYS+=("TAVILY_API_KEY")
fi

if ! grep -q "ANTHROPIC_API_KEY=.*[^[:space:]]" .env && ! grep -q "OPENAI_API_KEY=.*[^[:space:]]" .env; then
    MISSING_KEYS+=("ANTHROPIC_API_KEY or OPENAI_API_KEY")
fi

if [ ${#MISSING_KEYS[@]} -gt 0 ]; then
    echo "❌ Missing required API keys in .env:"
    for key in "${MISSING_KEYS[@]}"; do
        echo "  - $key"
    done
    echo ""
    echo "Please update .env and run this script again."
    exit 1
fi

echo "✅ Environment configuration looks good!"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🐳 Docker is running"
echo ""

# Ask user for deployment type
echo "Choose deployment method:"
echo "  1) Docker Compose (Recommended - Full stack with DB)"
echo "  2) Local Development (Python virtual environment)"
read -p "Enter choice (1 or 2): " choice

if [ "$choice" == "1" ]; then
    echo ""
    echo "🐳 Starting S1NGULARITY with Docker Compose..."
    echo ""

    # Build and start services
    docker-compose up -d --build

    echo ""
    echo "⏳ Waiting for services to be ready..."
    sleep 10

    # Health check
    echo "🏥 Running health check..."
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo ""
        echo "✅ S1NGULARITY is running!"
        echo ""
        echo "🌐 API Endpoints:"
        echo "   • API: http://localhost:8000"
        echo "   • Docs: http://localhost:8000/docs"
        echo "   • Health: http://localhost:8000/health"
        echo ""
        echo "📊 Services:"
        echo "   • PostgreSQL: localhost:5432"
        echo "   • Redis: localhost:6379"
        echo ""
        echo "📝 View logs:"
        echo "   docker-compose logs -f api"
        echo ""
        echo "🛑 Stop services:"
        echo "   docker-compose down"
    else
        echo ""
        echo "⚠️  Health check failed. Checking logs..."
        docker-compose logs api | tail -n 20
        echo ""
        echo "Run 'docker-compose logs -f api' for full logs"
    fi

elif [ "$choice" == "2" ]; then
    echo ""
    echo "🐍 Setting up local development environment..."
    echo ""

    # Check Python version
    if ! command -v python3.11 &> /dev/null; then
        echo "❌ Python 3.11 not found. Please install Python 3.11+"
        exit 1
    fi

    # Create virtual environment
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3.11 -m venv venv
    fi

    # Activate virtual environment
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate

    # Install dependencies
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt

    # Start PostgreSQL and Redis via Docker
    echo "🐳 Starting PostgreSQL and Redis..."
    docker-compose up -d postgres redis

    echo "⏳ Waiting for database..."
    sleep 5

    # Initialize database
    echo "🗄️  Initializing database..."
    python -c "import asyncio; from database import init_db; asyncio.run(init_db())"

    # Start server
    echo ""
    echo "🚀 Starting S1NGULARITY development server..."
    echo ""
    echo "✅ Server will start at http://localhost:8000"
    echo "📚 Docs available at http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop"
    echo ""

    uvicorn main:app --reload --host 0.0.0.0 --port 8000

else
    echo "Invalid choice. Please run again and select 1 or 2."
    exit 1
fi

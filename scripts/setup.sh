#!/bin/bash

# SecureWatch Setup Script
echo "🚀 SecureWatch SOC Platform Setup"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

echo "✓ Docker and Docker Compose found"
echo "✓ Python found"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created. Please review and update if needed."
else
    echo "✓ .env file already exists"
fi

# Train ML model
echo ""
echo "🤖 Training ML model..."
cd ml-engine
if [ -f "train_model.py" ]; then
    python3 train_model.py
    echo "✓ ML model trained"
else
    echo "⚠️  ML model training script not found. Skipping..."
fi
cd ..

# Start Docker services
echo ""
echo "🐳 Starting Docker services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "🔍 Checking service health..."

# Check PostgreSQL
if docker-compose exec -T postgres pg_isready -U admin &> /dev/null; then
    echo "✓ PostgreSQL is ready"
else
    echo "⚠️  PostgreSQL is not ready yet"
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping &> /dev/null; then
    echo "✓ Redis is ready"
else
    echo "⚠️  Redis is not ready yet"
fi

# Check Elasticsearch
if curl -s http://localhost:9200/_cluster/health &> /dev/null; then
    echo "✓ Elasticsearch is ready"
else
    echo "⚠️  Elasticsearch is not ready yet"
fi

# Check Backend
if curl -s http://localhost:8000/health &> /dev/null; then
    echo "✓ Backend API is ready"
else
    echo "⚠️  Backend API is not ready yet"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 Access the application:"
echo "   Frontend: http://localhost:8080"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Next steps:"
echo "   1. Install frontend dependencies: npm install"
echo "   2. Start frontend dev server: npm run dev"
echo "   3. (Optional) Run log simulator: python scripts/log_simulator.py"
echo ""


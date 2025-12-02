#!/bin/bash
# Development environment startup script

echo "🚀 Starting PDF to CSV Microservices..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Build and start all services
echo "📦 Building Docker images..."
docker-compose build

echo ""
echo "🎯 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Health checks
echo ""
echo "🏥 Checking service health..."

check_service() {
    local name=$1
    local url=$2
    if curl -s "$url" > /dev/null 2>&1; then
        echo "✅ $name is healthy"
    else
        echo "❌ $name is not responding"
    fi
}

check_service "Upload Service" "http://localhost:5001/api/health"
check_service "Conversion Service" "http://localhost:5002/api/health"
check_service "Download Service" "http://localhost:5003/api/health"
check_service "Frontend" "http://localhost:3000"

echo ""
echo "🎉 All services are running!"
echo ""
echo "📋 Service URLs:"
echo "   Frontend:    http://localhost:3000"
echo "   Upload:      http://localhost:5001"
echo "   Conversion:  http://localhost:5002"
echo "   Download:    http://localhost:5003"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop services: docker-compose down"
echo ""

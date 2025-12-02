# Development environment startup script for Windows

Write-Host "🚀 Starting PDF to CSV Microservices..." -ForegroundColor Green
Write-Host ""

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Build and start all services
Write-Host "📦 Building Docker images..." -ForegroundColor Yellow
docker-compose build

Write-Host ""
Write-Host "🎯 Starting services..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Health checks
Write-Host ""
Write-Host "🏥 Checking service health..." -ForegroundColor Yellow

function Test-Service {
    param($name, $url)
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2
        Write-Host "✅ $name is healthy" -ForegroundColor Green
    } catch {
        Write-Host "❌ $name is not responding" -ForegroundColor Red
    }
}

Test-Service "Upload Service" "http://localhost:5001/api/health"
Test-Service "Conversion Service" "http://localhost:5002/api/health"
Test-Service "Download Service" "http://localhost:5003/api/health"
Test-Service "Frontend" "http://localhost:3000"

Write-Host ""
Write-Host "🎉 All services are running!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Service URLs:" -ForegroundColor Cyan
Write-Host "   Frontend:    http://localhost:3000"
Write-Host "   Upload:      http://localhost:5001"
Write-Host "   Conversion:  http://localhost:5002"
Write-Host "   Download:    http://localhost:5003"
Write-Host ""
Write-Host "📊 View logs: docker-compose logs -f" -ForegroundColor Yellow
Write-Host "🛑 Stop services: docker-compose down" -ForegroundColor Yellow
Write-Host ""

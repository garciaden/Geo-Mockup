#!/bin/bash
# Quick start script for development
# Run from HOST terminal: ./start-dev.sh

set -e  # Exit on error

echo "🚀 Starting CULS Development Environment"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found!"
    echo "Please run this script from the CULS-Mockup directory"
    exit 1
fi

# Start PostgreSQL
echo "📦 Starting PostgreSQL database..."
docker compose up postgres -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for database to be ready..."
sleep 5

# Check if database is healthy
if docker ps | grep -q culs_postgres; then
    echo "✅ PostgreSQL is running!"
    echo ""
    echo "📊 Database Status:"
    docker exec culs_postgres pg_isready -U culs_user -d culs_db
    echo ""
    echo "🎯 Next Steps:"
    echo "1. Open VS Code: code ."
    echo "2. Click 'Reopen in Container' when prompted"
    echo "3. In VS Code terminal, run: python3 myapp.py"
    echo "4. Access app at: http://localhost:5000"
    echo ""
    echo "📝 Useful Commands:"
    echo "  - Stop database: docker compose stop postgres"
    echo "  - View logs: docker logs culs_postgres"
    echo "  - Database shell: docker exec -it culs_postgres psql -U culs_user -d culs_db"
else
    echo "❌ Error: PostgreSQL failed to start"
    echo "Check logs: docker logs culs_postgres"
    exit 1
fi

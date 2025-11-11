#!/bin/bash
# Stop development environment
# Run from HOST terminal: ./stop-dev.sh

echo "🛑 Stopping CULS Development Environment"
echo "=========================================="
echo ""

# Stop PostgreSQL
if docker ps | grep -q culs_postgres; then
    echo "📦 Stopping PostgreSQL..."
    docker compose stop postgres
    echo "✅ PostgreSQL stopped"
else
    echo "ℹ️  PostgreSQL is not running"
fi

echo ""
echo "✨ Done! All services stopped."
echo ""
echo "To restart: ./start-dev.sh"

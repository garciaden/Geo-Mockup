#!/bin/bash
set -e

echo ">>> Pulling latest changes from main..."
git fetch origin
git reset --hard origin/main

echo ">>> Building and deploying Docker container..."
docker compose down
docker compose up -d --build

echo ">>> Cleaning up old images..."
docker image prune -f

echo ">>> Deployment complete!"
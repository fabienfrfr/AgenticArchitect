#!/bin/bash
set -e

docker-compose -f ../infra/docker-compose.yml up --build -d
echo "✅ Services deployed! Access dashboard at http://localhost:3000"

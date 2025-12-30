#!/bin/bash

ENV=${1:-local}  # Default: local

case $ENV in
  local)
    echo "🚀 Deploying locally..."
    cd infra/local
    ./setup.sh
    ;;
  cloud)
    echo "☁️ Deploying to cloud..."
    cd infra/cloud/terraform
    terraform init
    terraform apply -auto-approve
    cd ../helm
    helm install ollama ./ollama
    helm install chromadb ./chromadb
    helm install architect ./architect    ;;
  *)
    echo "❌ Unrecognized environment. Use 'local' or 'cloud'."
    exit 1
    ;;
esac

#!/usr/bin/env bash
# Primera descarga de la base de datos de la NVD (10 a 30 minutos con key).
set -euo pipefail
cd "$(dirname "$0")/.."
./scripts/verify-nvd-key.sh
./mvnw -B org.owasp:dependency-check-maven:13.0.0:update-only \
  -DnvdApiKeyEnvironmentVariable=NVD_API_KEY \
  -DdataDirectory="$HOME/.dependency-check-data"

#!/usr/bin/env bash
# Ejecuta el análisis SCA. Reportes en target/dependency-check-report.{html,sarif}
set -euo pipefail
cd "$(dirname "$0")/.."
./scripts/verify-nvd-key.sh
./mvnw -B dependency-check:check

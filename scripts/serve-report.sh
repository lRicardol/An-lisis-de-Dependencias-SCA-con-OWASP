#!/usr/bin/env bash
# Sirve target/ en el puerto 8000 para abrir el HTML desde Codespaces (Ctrl+C para detener).
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f target/dependency-check-report.html ] || { echo "Primero ejecuta ./scripts/run-sca.sh"; exit 1; }
echo "Abre el puerto 8000 en la pestaña Ports y entra a dependency-check-report.html"
jwebserver -d "$PWD/target" -b 0.0.0.0 -p 8000

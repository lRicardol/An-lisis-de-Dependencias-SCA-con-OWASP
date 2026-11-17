#!/usr/bin/env bash
# Verifica que NVD_API_KEY exista, sin imprimir su valor.
if [ -n "$NVD_API_KEY" ]; then
  echo "NVD_API_KEY disponible"
else
  echo "NVD_API_KEY NO disponible"
  echo "Crea el secreto en GitHub > Settings > Codespaces y reconstruye el contenedor (Codespaces: Rebuild Container)."
  exit 1
fi

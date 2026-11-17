#!/usr/bin/env bash
# Lanza un hook escrito en Python con el primer intérprete de Python 3 que funcione.
#
# Uso: bash ejecutar.sh <hook.py> [bloquear|avisar]
#
# Por qué existe: en Windows, Claude Code ejecuta los hooks con Git Bash, y allí
# "python3" suele ser el alias de Microsoft Store, que no ejecuta nada. Si el hook
# llamara a "python3" directamente, fallaría sin bloquear y las protecciones
# quedarían desactivadas sin aviso.
#
# Si no hay Python 3:
#   bloquear (por defecto) -> sale con 2: la acción se bloquea y Claude ve el motivo.
#   avisar                 -> sale con 1: se informa al usuario sin bloquear.

hook="$(dirname "$0")/$1"
modo="${2:-bloquear}"

for py in python3 python py; do
  if command -v "$py" >/dev/null 2>&1 \
     && "$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1; then
    exec "$py" "$hook"
  fi
done

echo "No se encuentra Python 3.8 o superior: el hook $1 no puede ejecutarse." \
     "Instala Python (python.org) y reinicia Claude Code." >&2
if [ "$modo" = "avisar" ]; then exit 1; else exit 2; fi

#!/usr/bin/env bash
# Verificación completa del proyecto. La usan el agente, el subagente
# `verificador` y el hook Stop. Debe terminar con código 0 solo si todo pasa.
#
# RELLENAR con los comandos reales del proyecto (descomenta y adapta).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== Build ==";  # npm run build      | cargo build      | python -m compileall -q src
echo "== Lint ==";   # npm run lint       | ruff check .     | cargo clippy -- -D warnings
echo "== Tipos ==";  # npx tsc --noEmit   | mypy src
echo "== Tests ==";  # npm test           | pytest -q        | cargo test

echo "AVISO: scripts/verificar.sh aún no está configurado; no se ha comprobado nada." >&2
exit 0

#!/usr/bin/env python3
"""Hook PreToolUse (Edit/Write): impide modificar archivos protegidos.

Protege secretos y la propia configuración de seguridad del agente: un agente
no debe poder desactivar sus hooks ni sus permisos. Para cambiarlos, hazlo tú.
"""
import json
import os
import sys
from fnmatch import fnmatch

# Patrones relativos a la raíz del proyecto. Añade los propios del proyecto.
PROTEGIDOS = [
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "secrets/*",
    ".git/*",
    ".claude/settings.json",
    ".claude/hooks/*",
]


def ruta_relativa(ruta: str) -> str:
    raiz = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    absoluta = os.path.realpath(os.path.join(raiz, ruta))
    return os.path.relpath(absoluta, os.path.realpath(raiz)).replace(os.sep, "/")


def main() -> int:
    try:
        datos = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Hook proteger-archivos: entrada no válida; se bloquea por seguridad.", file=sys.stderr)
        return 2

    entrada = datos.get("tool_input") or {}
    ruta = entrada.get("file_path") or entrada.get("notebook_path") or ""
    if not ruta:
        return 0

    relativa = ruta_relativa(ruta)
    nombre = os.path.basename(relativa)
    for patron in PROTEGIDOS:
        if fnmatch(relativa, patron) or fnmatch(nombre, patron):
            print(
                f"Bloqueado por .claude/hooks/proteger-archivos.py: '{relativa}' está protegido "
                f"(patrón '{patron}').\n"
                "Si el cambio es necesario, explícaselo al usuario para que lo haga él.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

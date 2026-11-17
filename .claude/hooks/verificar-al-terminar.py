#!/usr/bin/env python3
"""Hook Stop: no deja terminar si hay cambios y scripts/verificar.sh falla.

- Si no hay cambios sin confirmar en git, no hace nada (turnos de conversación).
- Si Claude ya está continuando por este hook (stop_hook_active), no vuelve a
  bloquear, para evitar bucles infinitos.
- Si scripts/verificar.sh no existe o no está configurado, avisa pero no bloquea.
"""
import json
import os
import subprocess
import sys

MAX_SALIDA = 3000  # caracteres de la salida del verificador que se envían a Claude


def hay_cambios(raiz: str) -> bool:
    try:
        r = subprocess.run(["git", "status", "--porcelain"], cwd=raiz,
                           capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return True  # si no se puede saber, verifica
    return r.returncode != 0 or bool(r.stdout.strip())


def main() -> int:
    try:
        datos = json.load(sys.stdin)
    except json.JSONDecodeError:
        datos = {}
    if datos.get("stop_hook_active"):
        return 0

    raiz = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    script = os.path.join(raiz, "scripts", "verificar.sh")

    if not hay_cambios(raiz):
        return 0
    if not os.path.isfile(script):
        print("Aviso: no existe scripts/verificar.sh; no se ha verificado el cambio.", file=sys.stderr)
        return 1  # no bloquea: solo informa al usuario

    try:
        r = subprocess.run(["bash", script], cwd=raiz, capture_output=True, text=True, timeout=570)
    except subprocess.TimeoutExpired:
        print("scripts/verificar.sh superó el tiempo límite. Revisa por qué tarda tanto "
              "antes de dar la tarea por terminada.", file=sys.stderr)
        return 2

    if r.returncode == 0:
        return 0

    salida = (r.stdout + r.stderr)[-MAX_SALIDA:]
    print(
        "scripts/verificar.sh ha fallado, así que la tarea no está terminada.\n"
        "Corrige el problema, o explica al usuario por qué no puede corregirse ahora.\n"
        f"--- Últimas líneas de la salida ---\n{salida}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())

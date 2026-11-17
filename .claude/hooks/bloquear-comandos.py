#!/usr/bin/env python3
"""Hook PreToolUse (Bash): bloquea comandos destructivos o irreversibles.

Claude Code envía por stdin un JSON con tool_input.command.
Salida con código 2: el comando no se ejecuta y el mensaje de stderr llega a
Claude, que debe pedir autorización al usuario.
"""
import json
import re
import sys

# (patrón, motivo). Los patrones se aplican al comando completo.
REGLAS = [
    (r"\brm\s+(-[a-zA-Z]*[rR][a-zA-Z]*\s+)+(/|~|\$HOME|\.|\.\.|\*)(\s|/?$|/\*)",
     "borrado recursivo de la raíz, del home, del directorio actual o con comodín"),
    (r"\bgit\s+push\b.*\s(--force(?!-with-lease)|-f)\b",
     "git push forzado (usa --force-with-lease y pide autorización)"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard descarta cambios sin posibilidad de recuperarlos"),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "git clean -f borra archivos no versionados"),
    (r"\bgit\s+(filter-branch|filter-repo)\b", "reescritura del historial de git"),
    (r"\b(DROP\s+(DATABASE|SCHEMA|TABLE)|TRUNCATE\s+TABLE)\b", "operación destructiva en base de datos"),
    (r"\bDELETE\s+FROM\s+[\w.`\"]+\s*(;|'|\"|$)", "DELETE sin WHERE"),
    (r"\bmkfs(\.\w+)?\b", "formateo de un sistema de archivos"),
    (r"\bdd\b.*\bof=/dev/", "escritura directa sobre un dispositivo"),
    (r"\bchmod\s+-R\s+0?777\b", "permisos 777 recursivos"),
    (r"(curl|wget)\b[^|]*\|\s*(sudo\s+)?(ba|z)?sh\b", "ejecutar un script descargado sin revisarlo"),
    (r"(^|[\s;&|])(cat|less|more|head|tail)\s+[^|;&]*\.env(\.\w+)?\b", "leer un archivo de secretos"),
]


def main() -> int:
    try:
        datos = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Hook bloquear-comandos: entrada no válida; se bloquea por seguridad.", file=sys.stderr)
        return 2

    comando = (datos.get("tool_input") or {}).get("command", "")
    for patron, motivo in REGLAS:
        if re.search(patron, comando, flags=re.IGNORECASE):
            print(
                f"Bloqueado por .claude/hooks/bloquear-comandos.py: {motivo}.\n"
                f"Comando: {comando}\n"
                "Esta acción requiere autorización explícita del usuario. "
                "Explícale qué quieres hacer y por qué, y espera su respuesta.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

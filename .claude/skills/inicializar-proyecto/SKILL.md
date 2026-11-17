---
name: inicializar-proyecto
description: Prepara un repositorio nuevo o recién adoptado para trabajar con esta configuración - rellena CLAUDE.md, configura scripts/verificar.sh, comprueba los hooks y ajusta los skills. Usar una sola vez al empezar en un proyecto.
---

# Inicializar un proyecto

## Pasos

1. Inspecciona el repositorio con búsquedas acotadas (usa `Explore` si es
   grande): lenguajes, gestor de paquetes, framework, tests y CI.
2. Si el proyecto ya existe, respeta su arquitectura y convenciones. No
   reorganices carpetas.
3. Localiza y ejecuta los comandos reales de construcción, lint, tipos y tests.
   Anota solo los que funcionen.
4. Rellena `scripts/verificar.sh` con esos comandos y comprueba que termina con
   código 0 en el estado actual. Si hoy falla, informa antes de seguir.
5. Rellena en `CLAUDE.md` las secciones "Comandos", "Convenciones no estándar" y
   "Trampas conocidas".
   - No añadas un resumen del repositorio ni de su estructura: el agente lo
     descubre leyendo el código y los estudios muestran que no ayuda.
   - Escribe solo lo que el agente no deduciría por sí mismo.
6. Comprueba los hooks ejecutando
   `echo '{"tool_input":{"command":"git push --force"}}' | bash .claude/hooks/ejecutar.sh bloquear-comandos.py`:
   debe terminar con código 2. Si responde que no encuentra Python, avisa al
   usuario de que los hooks bloquearán todas las acciones hasta que lo instale.
   Comprueba también que el proyecto es un repositorio git.
   No puedes editar `.claude/hooks/` ni `.claude/settings.json` (están
   protegidos): si hay que añadir archivos sensibles propios del proyecto a
   `PROTEGIDOS` en `proteger-archivos.py`, indica al usuario qué añadir.
7. Ajusta los skills: borra `diseno-interfaz` si no hay interfaz; concreta y
   renombra `dominio`, o bórralo si no hay reglas de dominio propias.
8. Si `docs/especificacion.md` está vacía, pregunta al usuario qué quiere
   construir y redáctala con el skill `especificar`. En un proyecto existente,
   puede bastar con el objetivo, los usuarios y lo que queda fuera de alcance.
9. Si el repositorio está vacío, propón una arquitectura mínima con el skill
   `arquitectura`, a partir de la especificación aprobada, y espera
   confirmación antes de crear la estructura.
10. Propón al usuario un conjunto de tareas de evaluación con el skill
   `evaluar-configuracion`.

## Qué no hacer

- No crees directorios vacíos ni documentación de relleno.
- No montes CI, contenedores ni infraestructura que todavía no hagan falta.
- No añadas subagentes que escriban archivos: el único que escribe es el agente
  principal. Un subagente nuevo solo se justifica si separa contexto o aporta
  una evaluación independiente (ver README, sección 2.3).

## Resultado

Resumen breve: stack detectado, comandos verificados, estado de
`scripts/verificar.sh`, skills que quedan y dudas abiertas.

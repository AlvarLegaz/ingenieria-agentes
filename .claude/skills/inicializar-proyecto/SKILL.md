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
6. Comprueba los hooks: deben ser ejecutables y `python3` debe estar disponible.
   Añade a `PROTEGIDOS` en `.claude/hooks/proteger-archivos.py` los archivos
   sensibles propios del proyecto.
7. Ajusta los skills: borra `diseno-interfaz` si no hay interfaz; concreta y
   renombra `dominio`, o bórralo si no hay reglas de dominio propias.
8. Si el repositorio está vacío, propón una arquitectura mínima con el skill
   `arquitectura` y espera confirmación antes de crear la estructura.
9. Propón al usuario un conjunto de tareas de evaluación con el skill
   `evaluar-configuracion`.

## Qué no hacer

- No crees directorios vacíos ni documentación de relleno.
- No montes CI, contenedores ni infraestructura que todavía no hagan falta.
- No añadas subagentes por rol. Uno nuevo solo se justifica si separa contexto
  (ver README, sección 3).

## Resultado

Resumen breve: stack detectado, comandos verificados, estado de
`scripts/verificar.sh`, skills que quedan y dudas abiertas.

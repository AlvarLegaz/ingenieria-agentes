---
name: inicializar-proyecto
description: Prepara un repositorio nuevo o recién adoptado para trabajar con este sistema, rellenando CLAUDE.md, ajustando los subagentes y fijando los comandos de verificación. Usar una sola vez al empezar en un proyecto.
---

# Inicializar un proyecto

## Pasos

1. Inspecciona el repositorio: lenguajes, gestor de paquetes, framework, tests,
   CI y estructura de carpetas. Usa búsquedas acotadas, no leas todo.
2. Si el proyecto ya existe, respeta su arquitectura y convenciones. No
   reorganices carpetas.
3. Localiza y ejecuta los comandos reales de construcción, tests, lint y tipos.
   Anota solo los que funcionen.
4. Rellena las secciones "Proyecto" y "Comandos" de `CLAUDE.md` con lo
   encontrado, incluidas las trampas conocidas.
5. Revisa `.claude/agents/`:
   - Elimina los subagentes que el proyecto no necesite (por ejemplo `ux` y
     `gui` si no hay interfaz).
   - Concreta `especialista-dominio` con el dominio real y renómbralo.
6. Identifica los contratos esenciales entre módulos y defínelos con el skill
   `contrato`.
7. Si se toma una decisión arquitectónica de fondo, regístrala con el skill
   `adr`.
8. Si el repositorio está vacío, propón la arquitectura mínima mantenible y
   espera confirmación antes de crear la estructura.

## Qué no hacer

- No crees directorios vacíos ni documentación de relleno.
- No montes CI, contenedores ni infraestructura que todavía no hagan falta.
- No añadas subagentes "por si acaso".

## Resultado

Resumen breve: stack detectado, comandos verificados, subagentes que quedan
activos, contratos definidos y dudas abiertas para el usuario.

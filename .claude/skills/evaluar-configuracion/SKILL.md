---
name: evaluar-configuracion
description: Medir si un cambio en la configuración de Claude Code (CLAUDE.md, un skill, un subagente o un hook) mejora los resultados, comparando tareas reales con y sin el cambio. Usar antes de añadir o quitar un subagente y cuando se modifique CLAUDE.md de forma relevante.
---

# Evaluar la configuración

Un cambio en la configuración es una hipótesis hasta que se mide. Los estudios
sobre archivos de contexto y subagentes dan resultados distintos según el
proyecto, así que la decisión se toma con datos propios.

## 1. Prepara el conjunto de tareas

- Elige entre 5 y 10 tareas reales y ya resueltas del proyecto (issues o PR
  cerrados) que tengan tests capaces de decir si la solución es correcta.
- Para cada tarea guarda: commit de partida, enunciado tal como lo recibiría el
  agente y comando que la valida.
- Mezcla tipos: corrección de error, funcionalidad pequeña, cambio en varios
  componentes.

## 2. Define las variantes

- **A:** configuración actual.
- **B:** configuración con el cambio que se quiere probar (y nada más).

## 3. Ejecuta

- Cada tarea en cada variante, partiendo del mismo commit y en sesión nueva.
- Repite cada combinación al menos 3 veces: los resultados de un agente varían
  entre ejecuciones.
- Mismo modelo y misma versión de Claude Code en todas las ejecuciones.

## 4. Mide

| Métrica | Cómo |
|---|---|
| Éxito | El comando de validación de la tarea termina con código 0 |
| Coste | Tokens totales de la sesión, incluidos los subagentes |
| Tiempo | Duración de la sesión hasta que el agente da la tarea por cerrada |
| Falsos "terminado" | Veces que el agente dice que funciona y la validación falla |
| Cumplimiento | Reglas de CLAUDE.md que se espera ver aplicadas, comprobadas en el diff |

## 5. Decide

- Mantén el cambio solo si mejora el éxito o reduce coste o tiempo sin empeorar
  el éxito.
- Con 5–10 tareas y 3 repeticiones, una diferencia pequeña es un indicio, no una
  prueba. Si el resultado es ambiguo, quédate con la opción más simple.
- Registra el resultado con el skill `adr`, incluyendo las cifras.

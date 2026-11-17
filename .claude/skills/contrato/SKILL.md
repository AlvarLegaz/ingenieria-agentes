---
name: contrato
description: Define o modifica un contrato compartido entre módulos o agentes (API, esquema, interfaz pública). Usar antes de repartir trabajo en tareas MEDIAS o COMPLEJAS y siempre que haya que cambiar un contrato existente.
---

# Contratos entre módulos y agentes

## Definir un contrato

1. Exprésalo primero en forma ejecutable, eligiendo lo que el proyecto ya use:
   tipos, JSON Schema, OpenAPI, interfaz formal, validador, test de contrato o
   restricción de base de datos.
2. Documenta en `docs/contracts/<id>.md` solo lo que la forma ejecutable no
   pueda expresar. Si lo expresa todo, no hace falta documento.

## Plantilla

```markdown
# <id>: propósito en una línea

- Responsable: <módulo o agente>
- Definición ejecutable: <ruta al tipo, esquema o test>
- Consumidores: <módulos que dependen de él>

## Entradas y precondiciones
## Salidas y formato
## Restricciones e invariantes
## Errores y recuperación
## Criterios de aceptación
## Verificación
Comando o test que demuestra que se cumple.
```

## Modificar un contrato existente

1. Explica el motivo del cambio.
2. Localiza todos los consumidores con una búsqueda en el repositorio.
3. Si el cambio es estructural, pásalo a revisión de `arquitecto`.
4. Actualiza primero la definición ejecutable y sus tests.
5. Adapta los consumidores, manteniendo la compatibilidad cuando sea posible.
6. Ejecuta los tests de integración y de contrato.

Ningún agente cambia un contrato compartido sin completar estos pasos.

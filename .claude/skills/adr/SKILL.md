---
name: adr
description: Registra una decisión arquitectónica significativa como ADR en docs/adr/. Usar al elegir o cambiar arquitectura, una dependencia importante, un patrón transversal o un contrato estructural. No usar para cambios menores.
---

# Registrar un ADR

Un ADR recoge una decisión real que condiciona el proyecto. No se crea uno por
función, archivo o cambio menor, y no sustituye al código ni a sus contratos.

## Pasos

1. Mira en `docs/adr/` si ya hay un ADR sobre el tema. Si la decisión cambia, no
   edites el antiguo: crea uno nuevo y marca el anterior como "Sustituido por
   NNNN".
2. Numera de forma correlativa: `docs/adr/NNNN-titulo-en-kebab-case.md`.
3. Usa la plantilla y mantenlo en una página.

## Plantilla

```markdown
# NNNN. Título de la decisión

- Estado: Propuesto | Aceptado | Sustituido por NNNN | Descartado
- Fecha: AAAA-MM-DD

## Contexto
Situación y restricciones que obligan a decidir.

## Problema
Qué hay que resolver, en una o dos frases.

## Decisión
Qué se ha decidido.

## Alternativas consideradas
- Alternativa A: por qué no.
- Alternativa B: por qué no.

## Consecuencias
Qué se gana, qué se pierde y qué queda condicionado a partir de ahora.
```

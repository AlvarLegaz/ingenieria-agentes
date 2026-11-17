---
name: arquitectura
description: Decisiones estructurales - fronteras entre módulos, interfaces, dependencias y cambios que afectan a varios componentes. Usar antes de implementar un subsistema nuevo, una integración importante o una reorganización, y al evaluar un cambio en un contrato compartido.
---

# Decisiones de arquitectura

Úsalo para decidir antes de implementar. No para tareas localizadas.

## Pasos

1. **Delimita el problema.** Qué hay que resolver y qué restricciones lo
   condicionan, en dos o tres frases.
2. **Respeta lo existente.** Revisa `docs/adr/` y la estructura actual. Propón
   cambios solo con una necesidad concreta, nunca por preferencia.
3. **Divide por decisiones ocultas.** Cada módulo debe esconder una decisión que
   pueda cambiar (formato de datos, proveedor, algoritmo), de modo que se pueda
   sustituir sin tocar a los demás.
4. **Define las interfaces de forma ejecutable.** Tipos, esquemas o tests de
   contrato, con el skill `contrato`.
5. **Justifica cada dependencia nueva**: qué resuelve, alternativas, coste de
   mantenerla.
6. **Busca acoplamientos y riesgos**: qué se rompe si cambia cada pieza.
7. **Diseña restricciones contra errores previsibles**: tipos que impidan
   estados inválidos, validación en las fronteras, hooks o checks de CI.
8. Si la decisión es significativa, regístrala con el skill `adr`.

## Resultado

Antes de implementar, deja escrito (en la conversación o en el ADR):

1. Decisión, en una o dos frases.
2. Módulos e interfaces afectados, con rutas.
3. Contratos nuevos o modificados y sus consumidores.
4. Alternativas descartadas y por qué.
5. Riesgos y cómo se verificará que el diseño se cumple.

## Evitar

- Capas, abstracciones o dependencias sin un problema real que las justifique.
- Diseñar para requisitos hipotéticos.

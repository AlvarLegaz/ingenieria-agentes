---
name: especificar
description: Convierte la idea del usuario sobre qué quiere construir en docs/especificacion.md, con funcionalidades y criterios de aceptación comprobables. Usar al empezar un proyecto, al añadir una funcionalidad importante o cuando el usuario describa lo que quiere que haga el proyecto.
---

# Redactar o ampliar la especificación

La especificación dice QUÉ debe hacer el proyecto. No incluye decisiones de
implementación: esas van en el skill `arquitectura` y en los ADR.

## Pasos

1. **Lee lo que ya existe.** Si `docs/especificacion.md` tiene contenido, amplíalo;
   no lo reescribas.
2. **Escucha la idea completa** antes de escribir. No completes huecos con
   suposiciones: anótalos en "Preguntas abiertas".
3. **Pregunta lo imprescindible**, como mucho tres o cuatro preguntas a la vez:
   quién lo usa, qué es lo mínimo que debe funcionar y qué queda fuera.
4. **Redacta** siguiendo la plantilla de `docs/especificacion.md`:
   - Objetivo y usuarios en pocas frases.
   - Una sección por funcionalidad, cada una con criterios de aceptación que un
     test o una prueba manual puedan responder con sí o no.
   - Incluye los casos de error y de ausencia de datos en los criterios.
   - "Fuera de alcance" explícito.
5. **Revisa los criterios.** Reescribe los vagos: "que sea rápido" pasa a
   "la portada carga en menos de 2 s en móvil con 4G".
6. **Devuelve el borrador al usuario para que lo revise.** No empieces a
   implementar hasta que lo apruebe.

## Al implementar después

- Cada tarea de funcionalidad remite a su sección (por ejemplo, F2).
- `planificador-evaluador` parte de esa sección para el plan (modo PLAN) y
  comprueba sus criterios de aceptación al terminar (modo EVALUAR).
- Si durante la implementación aparece algo no previsto, se añade a
  "Preguntas abiertas" y se consulta; no se decide en silencio.

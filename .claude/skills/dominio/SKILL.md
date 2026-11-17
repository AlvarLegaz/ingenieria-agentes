---
name: dominio
description: PLANTILLA - renombrar y concretar para el dominio del proyecto (física, instrumentación, inferencia de modelos, reglas de negocio, tiempo real...). Reglas, invariantes, unidades y rangos válidos del dominio. Usar cuando la corrección dependa del dominio y no solo del código.
---

<!-- RELLENAR: cambia `name` y `description` para que el skill se cargue en los
     casos correctos, y sustituye cada sección por el contenido real. Si el
     proyecto no tiene un dominio con reglas propias, borra este skill. -->

# Reglas del dominio

## Conceptos y unidades

<!-- Magnitudes, unidades, sistemas de referencia, convenciones de signo. -->

## Invariantes

Cada invariante con su forma de comprobarla:

| Invariante | Cómo se verifica |
|---|---|
| <ej.: la energía total no aumenta sin aporte externo> | <test o aserción> |

## Rangos válidos

<!-- Valores físicos o de negocio posibles; qué hacer fuera de rango. -->

## Modelos y algoritmos

<!-- Modelo elegido, supuestos, casos en que deja de ser válido, referencias. -->

## Errores conceptuales frecuentes

<!-- Lo que compila y pasa los tests pero es incorrecto en el dominio. -->

## Al aplicarlo

- Distingue lo exacto de lo aproximado y declara los supuestos.
- Convierte cada invariante en una aserción o un test siempre que sea posible.

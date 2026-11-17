---
name: diseno-interfaz
description: Diseñar e implementar interfaces de usuario - flujos, estados de cada pantalla, componentes, accesibilidad y verificación visual. Usar al crear o cambiar pantallas, formularios o flujos de usuario.
---

# Diseño e implementación de interfaz

## 1. Especifica antes de implementar

- **Flujo:** pasos numerados desde el punto de vista del usuario.
- **Estados de cada pantalla:** carga, vacío, error, éxito y sin permisos. Cada
  uno debe tener un comportamiento definido.
- **Validaciones y mensajes:** qué se valida, cuándo y qué ve el usuario.
- **Coherencia:** parte de los patrones que el proyecto ya usa antes de crear
  uno nuevo.

## 2. Implementa

- Reutiliza componentes, estilos y tokens de diseño existentes.
- Implementa todos los estados de la tabla, no solo el de éxito.
- La lógica de negocio no va en la interfaz: se consume de la API o del módulo
  correspondiente. Si falta un dato, cámbialo en el contrato, no en la vista.
- Accesibilidad: navegación por teclado, etiquetas, contraste y foco visible.
- No introduzcas una librería de componentes o estilos nueva sin justificarlo.

## 3. Verifica

- Ejecuta la interfaz o sus tests de extremo a extremo y comprueba cada estado.
- Si hay herramienta de capturas, compara con lo esperado.
- Los criterios de aceptación que evalúe `planificador-evaluador` deben incluir
  los estados de error y vacío.

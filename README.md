# Ingeniería de agentes para programación

Configuración base de Claude Code para trabajar con un sistema multiagente
proporcionado: un `CLAUDE.md` corto con las reglas comunes, subagentes
especializados y skills con los procedimientos reutilizables.

## Contenido

| Ruta | Qué es |
|---|---|
| `CLAUDE.md` | Reglas comunes: delegación, contratos, verificación y acciones que requieren autorización |
| `.claude/agents/` | Subagentes: `arquitecto`, `programador`, `tester`, `ux`, `gui`, `especialista-dominio` |
| `.claude/skills/` | Procedimientos: `adr`, `contrato`, `inicializar-proyecto` |

## Uso

1. Copia `CLAUDE.md` y la carpeta `.claude/` a la raíz de tu proyecto.
2. Rellena las secciones "Proyecto" y "Comandos" de `CLAUDE.md`, o lanza el
   skill `inicializar-proyecto` para que lo haga Claude Code.
3. Concreta `especialista-dominio` con el dominio real y elimina los subagentes
   que no apliquen.
4. Comprueba con `/agents` que los subagentes aparecen.

## Criterios de diseño

- `CLAUDE.md` se carga en cada sesión, así que se mantiene por debajo de 200
  líneas y solo contiene lo que aplica siempre.
- Los roles viven en `.claude/agents/` y los procedimientos en
  `.claude/skills/`: se cargan únicamente cuando se usan.
- Se delega solo cuando aporta especialización, paralelismo real o una
  verificación independiente.
- Lo que pueda imponerse con tipos, tests, hooks o CI no se deja como texto.

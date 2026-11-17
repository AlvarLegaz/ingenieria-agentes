# Ingeniería de agentes para programación

Configuración base de Claude Code para un sistema multiagente **proporcionado**:
pocas reglas siempre cargadas, especialistas que solo se activan cuando aportan
algo y verificaciones que no dependen de que el modelo las recuerde.

Este documento explica el *porqué* de cada decisión, con referencias a las
fuentes. Las instrucciones de instalación están al final, en [Uso](#uso).

Cada afirmación lleva un número entre corchetes que remite a la sección
[Referencias](#referencias), con enlace o DOI para comprobarla. Cuando algo es
una interpretación propia y no una conclusión de la fuente, se indica.

---

## 1. El contexto es un recurso finito

Un modelo de lenguaje no usa igual de bien toda la información que recibe.

- **La posición importa.** Liu et al. midieron que el rendimiento es mayor
  cuando la información relevante está al principio o al final de la entrada, y
  cae de forma notable cuando está en medio, incluso en modelos diseñados para
  contextos largos [1].
- **El tamaño importa.** Anthropic llama *context rot* a la pérdida de precisión
  a medida que crece el contexto, y concluye que este debe tratarse como un
  recurso finito con rendimientos decrecientes [2].
- **El número de instrucciones importa.** El benchmark IFScale evaluó 20 modelos
  con hasta 500 instrucciones simultáneas: incluso los mejores se quedaron en un
  68 % de cumplimiento, con sesgo a favor de las primeras instrucciones [3].

La documentación de Claude Code aplica esto al `CLAUDE.md`: recomienda mantener
cada archivo por debajo de 200 líneas, porque los archivos largos consumen más
contexto y reducen la adherencia [4]. Recuerda además que su contenido es
contexto y no configuración impuesta: el modelo lo sigue con mayor o menor
fiabilidad según cómo esté escrito [4].

**Cómo se aplica aquí**

- `CLAUDE.md` tiene menos de 100 líneas y solo contiene lo que vale para
  cualquier tarea.
- Los roles van en `.claude/agents/` y los procedimientos en `.claude/skills/`,
  que se cargan solo cuando se usan.
- Se eliminaron las reglas que repiten el comportamiento por defecto del modelo
  ("código limpio", "no sobreingenierizar"): ocupan contexto sin cambiar la
  conducta.

---

## 2. Más agentes no es mejor por defecto

### La regla de la solución más simple

En su guía sobre agentes, Anthropic recomienda buscar la solución más simple
posible y añadir complejidad solo cuando haga falta, lo que a veces significa no
construir un sistema agéntico [5]. Distingue entre *flujos de trabajo*, con
caminos predefinidos y comportamiento predecible, y *agentes*, que deciden su
propio proceso y convienen cuando se necesita flexibilidad [5].

### La evidencia a favor

En su sistema de investigación, un agente principal con subagentes superó en un
90,2 % a un único agente en una evaluación interna [6]. La propia Anthropic
acota el resultado:

- Funciona mejor en tareas muy paralelizables, con información que no cabe en un
  solo contexto y con muchas herramientas complejas [6].
- Consume unas 15 veces más tokens que una conversación normal, por lo que solo
  compensa cuando el valor del resultado lo justifica [6].
- La mayoría de tareas de programación tienen menos partes realmente paralelas
  que la investigación, y los agentes aún coordinan mal en tiempo real [6].

### La evidencia en contra

- Cognition (creadores de Devin) sostiene que, con varios agentes, las
  decisiones quedan demasiado dispersas y el contexto no se comparte lo
  suficiente [7]. En un artículo posterior matizan que funciona una clase más
  estrecha de sistemas: varios agentes aportan análisis, pero las escrituras
  siguen en un solo hilo [8].
- Cemri et al. analizaron sistemas multiagente populares y encontraron que su
  mejora sobre un único agente suele ser mínima. Identificaron 14 modos de fallo
  agrupados en 3 categorías [9].

**Cómo se aplica aquí**

- Cada tarea se clasifica (TRIVIAL, SIMPLE, MEDIA, COMPLEJA) y solo se delega si
  aporta especialización, paralelismo real o verificación independiente.
- Nunca se activan todos los agentes por defecto.
- Solo se paraleliza cuando las tareas no comparten archivos y los contratos ya
  están definidos. *Interpretación propia:* es la versión práctica de la
  advertencia de Cognition sobre escrituras concurrentes [7][8].
- Varios agentes son de solo lectura o escriben en un ámbito acotado
  (`arquitecto`, `ux`, `tester`). La implementación queda concentrada en
  `programador` y `gui`.

---

## 3. Subagentes: aislar contexto y limitar permisos

En Claude Code, cada subagente trabaja en su propia ventana de contexto, con su
propio prompt de sistema, sus herramientas y sus permisos [10]. Anthropic
describe esto como una forma de compresión: los subagentes exploran en paralelo
y devuelven al agente principal solo lo más importante [6].

**Cómo se aplica aquí**

- Cada subagente declara en `tools` solo las herramientas que necesita: `ux` no
  puede editar archivos y `arquitecto` no ejecuta comandos.
- Cada uno usa el modelo adecuado a su tarea: `opus` para arquitectura y dominio,
  `sonnet` para implementación y pruebas.
- Al delegar se pasa solo el objetivo, los archivos relevantes, el contrato y el
  resultado esperado, no el historial completo, para no repetir el problema de
  la sección 1.

---

## 4. Verificación independiente

### Un agente no debe aprobarse a sí mismo

- Huang et al. muestran que, sin realimentación externa, los modelos tienen
  dificultades para corregir su propio razonamiento, y a veces empeoran al
  intentarlo [11].
- Panickssery et al. documentan el *sesgo de autopreferencia*: un modelo que
  evalúa tiende a puntuar mejor sus propios textos que otros de calidad
  equivalente según evaluadores humanos [12].

### La verificación tiene que ser ejecutable

La guía de buenas prácticas de Claude Code considera que dar al modelo una forma
de comprobar su trabajo (tests, capturas, salidas esperadas) es lo que más
mejora los resultados. Sin criterios de éxito claros, puede producir algo que
parece correcto pero no funciona [13].

**Cómo se aplica aquí**

- `tester` es un agente separado del que implementa, y no puede modificar código
  de producción.
- Una tarea solo está terminada si pasan build, lint, tipos y tests. Lo que no se
  haya podido ejecutar debe declararse, junto con su riesgo.
- Está prohibido afirmar que algo funciona o que se han ejecutado pruebas sin
  haberlo hecho.

---

## 5. Contratos entre agentes

El *diseño por contrato* de Bertrand Meyer trata cada componente como una
implementación que satisface una especificación con obligaciones y beneficios
explícitos para ambas partes, en lugar de como texto ejecutable arbitrario [14].
Parnas propuso dividir un sistema en módulos según qué decisiones de diseño
oculta cada uno, de modo que una implementación pueda cambiar sin afectar a las
demás [15].

*Interpretación propia:* entre agentes, un contrato cumple la función de contexto
compartido que Cognition echa en falta [7]. En vez de que cada agente deduzca
las decisiones de los demás, estas quedan escritas y comprobables.

**Cómo se aplica aquí**

- El skill `contrato` exige expresar el contrato primero en forma ejecutable:
  tipos, JSON Schema, OpenAPI o un test de contrato.
- Ningún agente cambia un contrato compartido por su cuenta: se identifican los
  consumidores y, si el cambio es estructural, lo revisa `arquitecto`.

---

## 6. Hacer el error imposible

La jerarquía rediseñar → restringir → automatizar → documentar viene de tres
ideas:

- **Poka-yoke.** Shigeo Shingo desarrolló dispositivos que impiden cometer un
  error o lo hacen evidente al instante, e inspecciones que comprueban las
  condiciones *antes* de producir, no los defectos después [16][17].
- **Estados ilegales irrepresentables.** El principio de Yaron Minsky propone
  modelar los datos de forma que los estados inválidos no se puedan ni escribir,
  y que sea el compilador quien lo impida [18].
- **Hooks frente a instrucciones.** La documentación de Claude Code explica que
  los hooks dan control determinista: ciertas acciones ocurren siempre, en lugar
  de depender de que el modelo decida ejecutarlas [19].

Las tres apuntan a lo mismo: una regla en lenguaje natural es la protección más
débil, porque depende de que alguien (o el modelo) la recuerde y la aplique.

**Cómo se aplica aquí**

- Ante un error relevante se intenta, en orden: rediseñar, restringir con tipos o
  validadores, añadir un test de regresión y, solo como último recurso,
  documentar.
- La protección debe ser proporcional al riesgo, sin grandes refactorizaciones
  para errores hipotéticos.
- Lo que deba cumplirse siempre (formatear, bloquear comandos peligrosos, impedir
  terminar con tests en rojo) debería implementarse como hook, no como línea en
  `CLAUDE.md`.

---

## 7. Memoria de decisiones: ADR

Michael Nygard propuso en 2011 los *Architecture Decision Records*: documentos
breves, guardados en el repositorio junto al código, con el contexto, la
decisión, el estado y las consecuencias de cada decisión arquitectónica
relevante [20].

Para un agente esto tiene un valor añadido. *Interpretación propia:* cada sesión
empieza sin memoria, así que un ADR evita que el agente reabra decisiones ya
tomadas o las deshaga sin saber por qué se tomaron.

**Cómo se aplica aquí**

- El skill `adr` usa la plantilla de Nygard con una sección añadida de
  alternativas consideradas.
- Solo se registran decisiones significativas, no una por cada cambio.

---

## 8. Limitaciones

- La mayor parte de la evidencia cuantitativa sobre sistemas multiagente procede
  de tareas de investigación, no de programación [6], o de benchmarks concretos
  [9]. Su extrapolación a este repositorio no está medida.
- El límite de 200 líneas es una recomendación de Anthropic [4], no un umbral
  experimental. La degradación con el número de instrucciones sí está medida
  [3], pero en una tarea distinta.
- Las cifras del sistema de investigación de Anthropic proceden de evaluaciones
  internas [6].
- Esta configuración no ha sido evaluada de forma sistemática. Para validarla
  haría falta comparar tareas reales con y sin subagentes, midiendo tests
  superados, tokens consumidos y tiempo.

---

## Uso

| Ruta | Qué es |
|---|---|
| `CLAUDE.md` | Reglas comunes: delegación, contratos, verificación y acciones que requieren autorización |
| `.claude/agents/` | Subagentes: `arquitecto`, `programador`, `tester`, `ux`, `gui`, `especialista-dominio` |
| `.claude/skills/` | Procedimientos: `adr`, `contrato`, `inicializar-proyecto` |

1. Copia `CLAUDE.md` y la carpeta `.claude/` a la raíz de tu proyecto.
2. Rellena las secciones "Proyecto" y "Comandos" de `CLAUDE.md`, o lanza el
   skill `inicializar-proyecto` para que lo haga Claude Code.
3. Concreta `especialista-dominio` con el dominio real y elimina los subagentes
   que no apliquen.
4. Comprueba con `/agents` que los subagentes aparecen.

---

## Referencias

1. Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F. y
   Liang, P. (2023). *Lost in the Middle: How Language Models Use Long
   Contexts*. arXiv:2307.03172.
   <https://arxiv.org/abs/2307.03172>
2. Anthropic (2025). *Effective context engineering for AI agents*.
   <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
3. Jaroslawicz, D., Whiting, B., Shah, P. y Maamari, K. (2025). *How Many
   Instructions Can LLMs Follow at Once?* NeurIPS 2025. arXiv:2507.11538.
   <https://arxiv.org/abs/2507.11538>
4. Anthropic. *How Claude remembers your project* (documentación de Claude Code,
   memoria y `CLAUDE.md`). <https://code.claude.com/docs/en/memory>
5. Anthropic (2024, 19 de diciembre). *Building effective agents*.
   <https://www.anthropic.com/engineering/building-effective-agents>
6. Anthropic (2025, junio). *How we built our multi-agent research
   system*. <https://www.anthropic.com/engineering/multi-agent-research-system>
7. Yan, W. (2025, 12 de junio). *Don't Build Multi-Agents*. Cognition.
   <https://cognition.ai/blog/dont-build-multi-agents>
8. Yan, W. *Multi-Agents: What's Actually Working*. Cognition.
   <https://cognition.ai/blog/multi-agents-working>
9. Cemri, M., Pan, M. Z., Yang, S. et al. (2025). *Why Do Multi-Agent LLM
   Systems Fail?* arXiv:2503.13657. <https://arxiv.org/abs/2503.13657>
10. Anthropic. *Create custom subagents* (documentación de Claude Code).
    <https://code.claude.com/docs/en/sub-agents>
11. Huang, J., Chen, X., Mishra, S., Zheng, H. S., Yu, A. W., Song, X. y Zhou, D.
    (2024). *Large Language Models Cannot Self-Correct Reasoning Yet*. ICLR 2024.
    arXiv:2310.01798. <https://arxiv.org/abs/2310.01798>
12. Panickssery, A., Bowman, S. R. y Feng, S. (2024). *LLM Evaluators Recognize
    and Favor Their Own Generations*. NeurIPS 2024. arXiv:2404.13076.
    <https://arxiv.org/abs/2404.13076>
13. Anthropic. *Best practices for Claude Code* (documentación de Claude Code).
    <https://code.claude.com/docs/en/best-practices>
14. Meyer, B. (1992). Applying "Design by Contract". *IEEE Computer*, 25(10),
    40–51. <https://doi.org/10.1109/2.161279>
15. Parnas, D. L. (1972). On the Criteria To Be Used in Decomposing Systems into
    Modules. *Communications of the ACM*, 15(12), 1053–1058.
    <https://doi.org/10.1145/361598.361623>
16. Shingo, S. (1986). *Zero Quality Control: Source Inspection and the
    Poka-Yoke System*. Routledge. ISBN 9780915299072.
17. Grout, J. R. y Downs, B. T. *A Brief Tutorial on Mistake-proofing,
    Poka-Yoke, and ZQC*.
    <https://mistakeproofing.com/a-brief-tutorial-on-mistake-proofing-poka-yoke-and-zqc/>
18. Minsky, Y. (2010). *Effective ML*. Conferencia en Harvard (origen del
    principio "make illegal states unrepresentable"). Desarrollo del principio:
    Wlaschin, S. *Designing with types: Making illegal states unrepresentable*.
    <https://fsharpforfunandprofit.com/posts/designing-with-types-making-illegal-states-unrepresentable/>
19. Anthropic. *Automate workflows with hooks* (documentación de Claude Code).
    <https://code.claude.com/docs/en/hooks-guide>
20. Nygard, M. (2011, 15 de noviembre). *Documenting Architecture Decisions*.
    Cognitect.
    <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>

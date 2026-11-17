# Ingeniería de agentes para programación

Configuración de Claude Code basada en la evidencia disponible a finales de
2026: **un solo agente por defecto**, conocimiento especializado en skills que
se cargan cuando hacen falta, **un único subagente para verificar** y **hooks**
para lo que debe cumplirse siempre.

Este documento explica el porqué de cada decisión, con referencias. La
instalación está al final, en [Uso](#uso).

**Sobre las fuentes.** Se priorizan estudios y guías de 2026. Los trabajos de
2023–2025 se mantienen cuando siguen siendo la referencia de un fenómeno y la
evidencia nueva no los contradice. Los clásicos de ingeniería del software
(Parnas, Meyer, Shingo, Nygard) se citan como fundamentos, no como evidencia
sobre LLM. Cada afirmación remite a [Referencias](#referencias); lo que es
interpretación propia se indica.

---

## Resumen: de la evidencia al diseño

| Evidencia | Decisión |
|---|---|
| Los archivos de contexto no mejoran el éxito de las tareas y encarecen la inferencia; los resúmenes del repositorio no ayudan [6] | `CLAUDE.md` corto, sin resumen del repo: comandos, convenciones no estándar y trampas |
| Dividir el trabajo por roles degrada la información en cada traspaso [11]; un solo agente con skills suele rendir igual o mejor [18] | Sin subagentes por rol. Arquitectura, interfaz y dominio son skills |
| Dos agentes escribiendo en paralelo rinden de media un 30 % peor que uno solo [13] | Las escrituras las hace un solo agente |
| Los modelos juzgan mal su propio trabajo [19][20][21]; la verificación necesita poco contexto compartido [11] | Un subagente `verificador` independiente y sin permisos de escritura |
| Las instrucciones se cumplen peor a medida que avanza la sesión [8]; los hooks se ejecutan siempre [23] | Hooks para lo obligatorio: comandos peligrosos, archivos protegidos, verificación al terminar |
| Los resultados varían según el proyecto [6][7][8] | Un skill para medir cada cambio de configuración antes de adoptarlo |

---

## 1. Contexto y archivos de instrucciones

### El contexto es un recurso finito

- El rendimiento cae cuando la información relevante está en medio de un
  contexto largo, y empeora a medida que el contexto crece [1].
- Anthropic llama *context rot* a esa pérdida y propone tratar el contexto como
  un recurso finito con rendimientos decrecientes [2].
- Con cientos de instrucciones simultáneas, incluso los mejores modelos dejan de
  cumplir una parte importante, y cumplen mejor las primeras [3].

### Qué dicen los estudios de 2026 sobre CLAUDE.md y AGENTS.md

- **Son el mecanismo de configuración dominante.** Un estudio de 2.303 archivos
  de 1.925 repositorios los caracteriza como un artefacto nuevo que se mantiene y
  modifica con frecuencia [4]. Otro, sobre 2.926 repositorios, encuentra que son
  el mecanismo más usado y a menudo el único [5].
- **No mejoran el éxito de las tareas.** Gloaguen et al. evaluaron cuatro agentes
  de programación: los archivos de contexto no mejoran en general la tasa de
  tareas resueltas y aumentan el coste de inferencia en más de un 20 % [6]. Los
  agentes siguen bien sus instrucciones, pero los resúmenes del repositorio no
  ayudan. Su conclusión: sirven para indicar prácticas no estándar, y cualquier
  mejora debe evaluarse antes de adoptarla [6].
- **Pueden mejorar la eficiencia.** En 124 pull requests reales, la presencia de
  un AGENTS.md se asoció con un 28,64 % menos de tiempo mediano y un 16,58 %
  menos de tokens de salida, con tasas de finalización similares [7].
- **La longitud pesa menos de lo esperado; la sesión, más.** Variar el archivo
  entre 25 y 500 líneas, la posición de la instrucción y el número de archivos
  no tuvo efectos detectables sobre el cumplimiento de una instrucción concreta
  [8]. El efecto mayor fue otro: cada función generada en la sesión reducía un
  5,6 % la probabilidad de cumplirla [8].

La documentación de Claude Code recomienda no pasar de 200 líneas por archivo y
recuerda que su contenido es contexto, no configuración impuesta [9].

**Cómo se aplica**

- `CLAUDE.md` tiene 85 líneas: comandos, convenciones no estándar, trampas
  conocidas, forma de trabajar y reglas de cierre.
- No incluye resumen del repositorio ni de su estructura [6].
- *Interpretación propia:* que la longitud no tenga efecto medible en [8] no
  justifica alargarlo. Ese estudio mide una sola instrucción, y [6] sí mide un
  coste mayor.

---

## 2. Un solo agente por defecto

- **Empezar por lo simple.** Anthropic recomienda la solución más simple posible
  y añadir complejidad solo cuando haga falta [10].
- **Los sistemas multiagente se usan de más.** En enero de 2026 Anthropic
  advierte que a menudo se aplican donde un solo agente funcionaría mejor, y que
  ha visto equipos dedicar meses a arquitecturas complejas para descubrir que un
  único agente con mejor prompt lograba lo mismo [11]. Consumen entre 3 y 10
  veces más tokens para la misma tarea [11].
- **Cuándo compensan.** Cuando la contaminación del contexto degrada el
  rendimiento, cuando las tareas pueden ir en paralelo y cuando la
  especialización mejora la elección de herramientas [11].
- **Investigación frente a programación.** En investigación, con lectura en
  paralelo, el sistema multiagente de Anthropic superó en un 90,2 % a un único
  agente, a costa de unas 15 veces más tokens que una conversación [12]. En
  programación, CooperBench asignó a dos agentes funcionalidades distintas de un
  mismo repositorio: juntos lograron de media un 30 % menos de éxito que uno
  solo haciendo ambas [13]. Los fallos venían de mensajes vagos o inexactos,
  compromisos incumplidos y expectativas erróneas sobre el plan del otro [13].
- **La posición de Cognition.** En 2025 desaconsejó los sistemas multiagente
  porque las decisiones quedan dispersas [14]. En abril de 2026 matizó que
  funciona una clase más estrecha: varios agentes aportan análisis, pero las
  escrituras siguen en un solo hilo [15].
- **Fallos recurrentes.** La taxonomía MAST recoge 14 modos de fallo de sistemas
  multiagente, cuyas mejoras sobre un solo agente suelen ser mínimas [16].

**Cómo se aplica**

- Un solo agente hace el trabajo de principio a fin y es el único que escribe.
- No hay clasificación de tareas por complejidad para decidir cuántos agentes
  activar: la pregunta es si hace falta separar contexto (sección 3).

---

## 3. Subagentes solo para separar contexto

### Qué es un subagente

En Claude Code, cada subagente trabaja en su propia ventana de contexto, con su
prompt de sistema, sus herramientas y sus permisos [17]. Claude Code incluye ya
un subagente `Explore`, de solo lectura, para búsquedas en el código [17].

### Dividir por contexto, no por rol

- **El problema de los roles.** Repartir el trabajo por roles (planificador,
  implementador, tester, revisor) produce un "teléfono roto": la información se
  degrada en cada traspaso [11]. Las fases sucesivas de un mismo trabajo deben
  quedarse en un solo agente [11].
- **Las buenas fronteras.** Líneas de investigación independientes, componentes
  con interfaces limpias y verificación de caja negra [11].
- **Integrar en el bucle principal.** En octubre de 2026, el equipo de Applied AI
  de Anthropic informa de despliegues que mejoraron al integrar planificadores y
  subagentes de dominio en un solo agente con skills [18]. Los skills cargan
  primero una descripción corta y el contenido completo solo cuando hace falta,
  lo que elimina el motivo principal para repartir el trabajo [18]. Un cliente
  midió una ejecución unas 2 veces más rápida [18].
- **Cuándo mantener un subagente.** Cuando hay degradación medible por exceso de
  contexto, cuando varias tareas necesitan contextos nuevos en paralelo que se
  descartan al terminar, o cuando un solo agente no acierta con las herramientas
  [18].

**Cómo se aplica**

| Antes (por rol) | Ahora |
|---|---|
| `arquitecto` | Skill `arquitectura` |
| `ux` + `gui` | Skill `diseno-interfaz` |
| `especialista-dominio` | Skill `dominio` (plantilla) |
| `programador` | El agente principal |
| `tester` | Subagente `verificador` (verificación de caja negra) |
| — | `Explore` (incluido en Claude Code) para búsquedas amplias |

---

## 4. Verificación independiente

- **Un modelo no debe aprobarse a sí mismo.** Sin realimentación externa, los
  modelos tienen dificultades para corregir su razonamiento y a veces empeoran
  [19]. Al evaluar, tienden a puntuar mejor sus propios textos [20].
- **Confirmado en programación (2026).** Anthropic observó que los agentes que
  desarrollan aplicaciones durante horas elogian con seguridad su propio trabajo
  aunque sea mediocre. Separar un evaluador fue mucho más tratable que hacer
  autocrítico al generador [21].
- **La separación no basta.** El evaluador sigue siendo un modelo y tiende a ser
  indulgente; necesita criterios concretos [21].
- **Cómo debe trabajar un verificador.** Criterios concretos en lugar de
  objetivos vagos, casos límite y pruebas negativas, y la batería completa,
  porque los verificadores suelen parar tras unos pocos tests superados [11].
- **Comprobaciones ejecutables.** Dar al modelo una forma de verificar su
  trabajo (tests, capturas, salidas esperadas) es lo que más mejora los
  resultados [22].

**Cómo se aplica**

- `scripts/verificar.sh` reúne build, lint, tipos y tests en un solo comando.
- El subagente `verificador` es escéptico por instrucción, ejecuta la batería
  completa, prueba casos negativos y devuelve evidencia. No tiene herramientas
  de edición: no puede "arreglar" lo que verifica.
- El hook `Stop` ejecuta `scripts/verificar.sh` cuando hay cambios y, si falla,
  impide dar la tarea por terminada.

---

## 5. Hooks: lo obligatorio no se deja en texto

- Los hooks de Claude Code dan control determinista: la acción ocurre siempre,
  sin depender de que el modelo decida hacerla [23].
- Es la versión en software de dos ideas clásicas: el poka-yoke de Shingo,
  dispositivos que impiden un error o lo hacen evidente al instante [26][27], y
  el principio de Minsky de hacer irrepresentables los estados inválidos [28].
- *Interpretación propia:* la caída del cumplimiento a lo largo de la sesión [8]
  hace que una regla en `CLAUDE.md` pierda fuerza con el tiempo. Un hook no.

**Cómo se aplica**

| Hook | Qué hace |
|---|---|
| `bloquear-comandos.py` | Bloquea borrados recursivos peligrosos, `git push --force`, `reset --hard`, `clean -f`, `DROP`/`TRUNCATE`/`DELETE` sin `WHERE`, `curl \| sh` y lecturas de `.env` |
| `proteger-archivos.py` | Impide editar secretos y la propia configuración de seguridad (`.claude/settings.json`, `.claude/hooks/`), para que el agente no pueda desactivarla |
| `verificar-al-terminar.py` | Si hay cambios sin confirmar y `scripts/verificar.sh` falla, obliga al agente a seguir. Si el agente ya está continuando por este hook, no vuelve a bloquear, para evitar bucles infinitos |

Además, `.claude/settings.json` deniega la lectura de `.env`, `secrets/` y
claves privadas.

Ante un error relevante, el orden es: rediseñar, restringir con tipos o
validadores, automatizar con un test o un hook y, solo al final, documentar.

---

## 6. Contratos

El *diseño por contrato* de Meyer trata cada componente como una implementación
que cumple una especificación con obligaciones y beneficios explícitos [24].
Parnas propuso dividir un sistema según qué decisión de diseño oculta cada
módulo, para poder sustituir uno sin tocar los demás [25].

La evidencia de 2026 les da un papel concreto: los componentes con interfaces
limpias son una de las fronteras válidas para delegar [11], y buena parte de los
fallos de CooperBench son expectativas erróneas sobre lo que hace el otro agente
[13]. *Interpretación propia:* un contrato ejecutable sustituye esas
expectativas por algo comprobable, también entre sesiones del mismo agente.

**Cómo se aplica:** el skill `contrato` exige expresar la interfaz primero en
forma ejecutable (tipos, esquemas, tests de contrato) y define cómo cambiarla.

---

## 7. Memoria entre sesiones: ADR y notas de traspaso

Nygard propuso en 2011 los *Architecture Decision Records*: documentos breves,
guardados en el repositorio, con contexto, decisión, estado y consecuencias
[29]. En 2026, Anthropic mantuvo como lección para sesiones largas de
programación el uso de artefactos estructurados para traspasar el contexto entre
sesiones [21].

**Cómo se aplica**

- El skill `adr` registra las decisiones significativas.
- `CLAUDE.md` pide una nota de traspaso al final de cada sesión en tareas largas,
  en lugar de confiar en el historial. *Interpretación propia:* es la respuesta
  práctica a la caída del cumplimiento durante la sesión [8].

---

## 8. Medir antes de adoptar

Los estudios de 2026 no coinciden entre sí ([6] frente a [7]) y miden proyectos,
tareas y modelos distintos. Gloaguen et al. recomiendan evaluar cualquier
mejora antes de adoptarla [6], y Anthropic propone crear primero un conjunto de
evaluación para decidir si se integra un subagente [18].

**Cómo se aplica:** el skill `evaluar-configuracion` compara tareas reales ya
resueltas con y sin un cambio, midiendo éxito, tokens, tiempo y falsos
"terminado".

---

## 9. Limitaciones

- La evidencia sobre archivos de contexto es reciente y en parte contradictoria
  [6][7][8].
- Las guías de Anthropic de 2026 [11][18] se basan en su experiencia con clientes
  y en mediciones puntuales, no en estudios controlados publicados.
- CooperBench [13] mide dos agentes escribiendo en paralelo; no mide un agente
  principal con un verificador de solo lectura, que es lo que se usa aquí.
- Los hooks reducen riesgos, pero las reglas de `bloquear-comandos.py` son
  patrones de texto: un comando ofuscado puede saltárselas. No sustituyen a los
  permisos ni a las copias de seguridad.
- Esta configuración no ha sido evaluada todavía con el skill
  `evaluar-configuracion`.

---

## Uso

| Ruta | Qué es |
|---|---|
| `CLAUDE.md` | Reglas que valen para cualquier tarea |
| `.claude/agents/verificador.md` | Único subagente: verificación independiente |
| `.claude/skills/` | `arquitectura`, `diseno-interfaz`, `dominio`, `contrato`, `adr`, `inicializar-proyecto`, `evaluar-configuracion` |
| `.claude/settings.json` | Permisos y registro de hooks |
| `.claude/hooks/` | Hooks en Python 3 |
| `scripts/verificar.sh` | Verificación completa del proyecto |
| `docs/autoevaluacion.html` | Test de 50 preguntas sobre esta teoría |

1. Copia `CLAUDE.md`, `.claude/` y `scripts/` a la raíz de tu proyecto.
2. Lanza el skill `inicializar-proyecto`, o rellena a mano `CLAUDE.md` y
   `scripts/verificar.sh`.
3. Comprueba que `python3` está disponible: los hooks lo necesitan.
4. Comprueba con `/agents` que aparece `verificador` y con `/hooks` que los hooks
   están registrados.

---

## Referencias

**Contexto y archivos de instrucciones**

1. Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F. y
   Liang, P. (2023). *Lost in the Middle: How Language Models Use Long
   Contexts*. arXiv:2307.03172. <https://arxiv.org/abs/2307.03172>
2. Anthropic (2025). *Effective context engineering for AI agents*.
   <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
3. Jaroslawicz, D., Whiting, B., Shah, P. y Maamari, K. (2025). *How Many
   Instructions Can LLMs Follow at Once?* NeurIPS 2025. arXiv:2507.11538.
   <https://arxiv.org/abs/2507.11538>
4. *Agent READMEs: An Empirical Study of Context Files for Agentic Coding*
   (v2, 9 de agosto de 2026). arXiv:2511.12884.
   <https://arxiv.org/abs/2511.12884>
5. *Configuring Agentic AI Coding Tools: An Exploratory Study* (2026).
   arXiv:2602.14690. <https://arxiv.org/abs/2602.14690>
6. Gloaguen, T., Mündler-Sasahara, N., Müller, M. N., Raychev, V. y Vechev, M.
   (2026). *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for
   Coding Agents?* arXiv:2602.11988. <https://arxiv.org/abs/2602.11988>
7. Lulla, J. L., Mohsenimofidi, S., Galster, M., Zhang, J. M., Baltes, S. y
   Treude, C. (2026). *On the Impact of AGENTS.md Files on the Efficiency of AI
   Coding Agents*. arXiv:2601.20404. <https://arxiv.org/abs/2601.20404>
8. McMillan, D. (2026). *Instruction Adherence in Coding Agent Configuration
   Files: A Factorial Study of Four File-Structure Variables*.
   arXiv:2605.10039. <https://arxiv.org/abs/2605.10039>
9. Anthropic. *How Claude remembers your project* (documentación de Claude
   Code). <https://code.claude.com/docs/en/memory>

**Agentes y subagentes**

10. Anthropic (2024, 19 de diciembre). *Building effective agents*.
    <https://www.anthropic.com/engineering/building-effective-agents>
11. Anthropic (2026, 23 de enero). *Building multi-agent systems: When and how
    to use them*.
    <https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them>
12. Anthropic (2025, junio). *How we built our multi-agent research system*.
    <https://www.anthropic.com/engineering/multi-agent-research-system>
13. Khatua, A., Zhu, H., Tran, P. et al. y Yang, D. (2026). *CooperBench: Why
    Coding Agents Cannot be Your Teammates Yet*. arXiv:2601.13295.
    <https://arxiv.org/abs/2601.13295>
14. Yan, W. (2025, 12 de junio). *Don't Build Multi-Agents*. Cognition.
    <https://cognition.ai/blog/dont-build-multi-agents>
15. Yan, W. (2026, 22 de abril). *Multi-Agents: What's Actually Working*.
    Cognition. <https://cognition.ai/blog/multi-agents-working>
16. Cemri, M., Pan, M. Z., Yang, S. et al. (2025). *Why Do Multi-Agent LLM
    Systems Fail?* arXiv:2503.13657. <https://arxiv.org/abs/2503.13657>
17. Anthropic. *Create custom subagents* (documentación de Claude Code).
    <https://code.claude.com/docs/en/sub-agents>
18. Sarkis, D. / Anthropic Applied AI (2026, 22 de octubre). *Building agents:
    When to fold subagents into your main agent loop*.
    <https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop>

**Verificación y hooks**

19. Huang, J., Chen, X., Mishra, S., Zheng, H. S., Yu, A. W., Song, X. y Zhou, D.
    (2024). *Large Language Models Cannot Self-Correct Reasoning Yet*. ICLR 2024.
    arXiv:2310.01798. <https://arxiv.org/abs/2310.01798>
20. Panickssery, A., Bowman, S. R. y Feng, S. (2024). *LLM Evaluators Recognize
    and Favor Their Own Generations*. NeurIPS 2024. arXiv:2404.13076.
    <https://arxiv.org/abs/2404.13076>
21. Rajasekaran, P. / Anthropic (2026, 24 de marzo). *Harness design for
    long-running application development*.
    <https://www.anthropic.com/engineering/harness-design-long-running-apps>
22. Anthropic. *Best practices for Claude Code* (documentación de Claude Code).
    <https://code.claude.com/docs/en/best-practices>
23. Anthropic. *Automate workflows with hooks* (documentación de Claude Code).
    <https://code.claude.com/docs/en/hooks-guide>

**Fundamentos de ingeniería del software**

24. Meyer, B. (1992). Applying "Design by Contract". *IEEE Computer*, 25(10),
    40–51. <https://doi.org/10.1109/2.161279>
25. Parnas, D. L. (1972). On the Criteria To Be Used in Decomposing Systems into
    Modules. *Communications of the ACM*, 15(12), 1053–1058.
    <https://doi.org/10.1145/361598.361623>
26. Shingo, S. (1986). *Zero Quality Control: Source Inspection and the
    Poka-Yoke System*. Routledge. ISBN 9780915299072.
27. Grout, J. R. y Downs, B. T. *A Brief Tutorial on Mistake-proofing,
    Poka-Yoke, and ZQC*.
    <https://mistakeproofing.com/a-brief-tutorial-on-mistake-proofing-poka-yoke-and-zqc/>
28. Minsky, Y. (2010). *Effective ML*. Conferencia en Harvard. Desarrollo del
    principio: Wlaschin, S. *Designing with types: Making illegal states
    unrepresentable*.
    <https://fsharpforfunandprofit.com/posts/designing-with-types-making-illegal-states-unrepresentable/>
29. Nygard, M. (2011, 15 de noviembre). *Documenting Architecture Decisions*.
    Cognitect.
    <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>

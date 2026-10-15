# 2. Proceso

## Proceso elegido: Kanban
Se eligió **Kanban**, un método ágil basado en visualizar el trabajo en un tablero y avanzar en flujo continuo.

- **Se adapta al cambio:** no exige planificar ciclos cerrados, por lo que la solicitud de cambio de la hora 6 puede incorporarse agregando nuevas tareas al tablero sin rehacer la planificación.
- **Es intuitivo:** un tablero con las tareas asignadas (Todo, In Progress, Done) permite ver de un vistazo qué sigue, qué falta y qué ya está listo.

## Alternativa comparada: Scrum
| Aspecto | Kanban | Scrum |
|---|---|---|
| Organización del tiempo | Flujo continuo de tareas | Sprints, normalmente de 1 a 4 semanas |
| Ceremonias | No las exige | Planificación del sprint, reunión diaria (*daily*), revisión y retrospectiva |
| Roles | No exige roles fijos | Product Owner, Scrum Master y equipo de desarrollo |
| Adecuación a este proyecto | Alta | Baja |

**Por qué se descartó Scrum:** sus ceremonias, las reuniones diarias y la coordinación con los interesados no tienen sentido para un proyecto desarrollado por una sola persona, que además no puede repartir los roles que Scrum exige, ni para un plazo de 12 horas, que es mucho más corto que la duración de un sprint promedio.

## Cómo se realizó en esta entrega
- **Especificación:** requisitos funcionales y no funcionales en `04_requisitos.md`, derivados de la tabla N01–N06 y de las voces del cliente de la guía.
- **Desarrollo:** por tareas (issues) del tablero Kanban, con commits que avanzan cada tarea.
- **Validación:** criterios de aceptación de cada RF y pruebas automatizadas (U1–U5 e I1).
- **Evolución:** incorporación de la solicitud de cambio de la hora 6, identificando la versión previa (`v1.0`) y analizando su impacto en requisitos, modelos, componentes y pruebas.

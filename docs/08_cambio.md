# 8. Solicitud de cambio (hora 6)

## Versión de partida
- **Versión anterior al cambio:** tag `v1.0` (versión inicial completa: requisitos, modelos, arquitectura, código y pruebas U1–U5 e I1).
- **Versión posterior al cambio:** tag `v2.0`.
- Documento recibido: `docs/Anexo hora 6 La ultima transmision.pdf`.

## Qué pidió el cliente
El lector debe poder deshacer su última decisión, revirtiendo todas sus consecuencias. Esta decisión reemplaza el acuerdo provisional de no implementar retroceso (ver "Conflicto: retroceso" en `04_requisitos.md`).

| Regla | Requisito |
|---|---|
| Restauración exacta de escena y variables | RF14 |
| Deshacer desde un final (E4, E5 o E6 vuelven a E3) | RF15 |
| Un solo nivel; sin rehacer | RF16 |
| Sin retroceso al iniciar; reiniciar elimina el historial | RF17 |
| Una entrada inválida no modifica la sesión ni el historial | RF18 |

## Análisis de impacto
| Elemento | ¿Cambió? | Detalle |
|---|---|---|
| `src/motor.py` (`Partida`) | Sí | Nuevo atributo `respaldo`; nuevos métodos `puede_deshacer()` y `deshacer()`; `elegir_opcion()` guarda el respaldo solo en elecciones válidas; `reiniciar()` lo vacía; `elegir_por_numero()` interpreta el 0 como deshacer. |
| `src/main.py` | Sí | Muestra "0. Deshacer la última decisión" cuando se puede deshacer, también en los finales y en el bloqueo. |
| `src/modelo.py` | No | La estructura de la historia no cambia. |
| `src/cargador.py` | No | El formato JSON no cambia. |
| `data/*.json` | No | Las historias no se modificaron. |
| Requisitos (`04_requisitos.md`) | Sí | Nuevos RF14–RF18, supuesto 4 y respuesta del cliente al conflicto. |
| Alcance (`01_fundamentos.md`) | Sí | "Deshacer la última decisión" pasa a "Incluye"; "retroceso de varios niveles y rehacer" quedan en "No incluye". |
| Modelos (`05_modelado.md`) | Sí | Casos de uso (nuevo "Deshacer la última decisión"), clases (`respaldo`, `puede_deshacer()`, `deshacer()`) y estados (transiciones con `deshacer()`). Contexto y secuencia no cambian. |
| Arquitectura (`06_arquitectura.md`) | No | Las capas y sus dependencias se mantienen. |
| Pruebas | Sí | Nueva U6; U5 e I1 ampliadas; U3 ajustada porque el 0 ahora significa deshacer. |
| Backlog | Sí | Nuevas tareas: análisis de impacto, implementación de deshacer, pruebas y actualización de requisitos y modelos. |

**Lectura del impacto:** el cambio solo afectó a `motor.py` y `main.py`. El modelo, el cargador y las historias no se tocaron, lo que confirma la decisión de separar el motor en capas (`06_arquitectura.md`).

## Evidencia de funcionamiento
| Comportamiento | Prueba |
|---|---|
| Deshacer restaura escena y variables (ejemplo de la solicitud: E2 → investigar → E3 → deshacer → E2) | `test_u6_deshacer_restaura_escena_y_variables`, `test_u6_ejemplo_de_la_solicitud_de_cambio` |
| Un solo nivel | `test_u6_deshacer_consume_el_retroceso`, `test_u6_nueva_eleccion_vuelve_a_habilitar_el_retroceso` |
| Entrada inválida preserva el historial | `test_u6_entrada_invalida_preserva_el_historial`, `test_u6_opcion_invalida_por_id_preserva_el_historial` |
| Sin retroceso al iniciar y al reiniciar | `test_u6_al_iniciar_no_hay_retroceso`, `test_u5_reiniciar_elimina_el_historial` |
| Deshacer desde un final tras cargar el archivo | `test_i1_deshacer_desde_un_final` (E4, E5 y E6) |
| El 0 en la consola | `test_u6_deshacer_con_el_numero_cero`, `test_u3_cero_sin_retroceso_disponible_es_invalido` |

# 9. Matriz de trazabilidad

Cada requisito se relaciona con su origen, los modelos donde aparece, el código que lo atiende y la evidencia que demuestra que se cumple. Las pruebas están en `test/` y su última ejecución en `docs/resultado_pruebas.txt`.

## Requisitos funcionales
| Requisito | Origen | Modelos | Código | Evidencia |
|---|---|---|---|---|
| RF01 Cargar historia | N01 | Contexto; caso de uso "Cargar una historia y revisar sus errores"; componentes | `cargador.py` → `cargar_historia()` | `test_historia_valida_se_carga`; `test_i1_segunda_historia_funciona_con_el_mismo_motor` |
| RF02 Iniciar partida | N01 | Caso de uso "Iniciar partida"; clase `Partida`; estado inicial | `motor.py` → `Partida.__init__()`, `reiniciar()` | `test_u6_al_iniciar_no_hay_retroceso` (inicia en E1); `test_u1_opcion_sin_condiciones_siempre_disponible` |
| RF03 Mostrar escena actual | N02 | Caso de uso "Ver la escena y sus opciones"; secuencia | `main.py` → `mostrar_escena()` | Recorrido en consola (video de demostración) |
| RF04 Mostrar solo opciones habilitadas | N02 | Caso de uso "Ver la escena y sus opciones"; clases `Opcion`, `Partida`; secuencia | `modelo.py` → `Opcion.esta_habilitada()`; `motor.py` → `opciones_disponibles()` | `test_u1_condiciones_habilitan_solo_las_opciones_correspondientes` (con y sin investigar) |
| RF05 Aplicar efectos | N03 | Clase `Partida`; secuencia | `motor.py` → `elegir_opcion()` | `test_u2_eleccion_valida_aplica_efectos_y_avanza` |
| RF06 Avanzar a la escena destino | N03 | Secuencia; estados | `motor.py` → `elegir_opcion()` | `test_u2_eleccion_valida_aplica_efectos_y_avanza`; `test_u2_eleccion_por_numero_valida` |
| RF07 Rechazar entradas inválidas | N03 | Secuencia (rama de entrada inválida); estados | `motor.py` → `elegir_por_numero()`, `elegir_opcion()` | `test_u3_opcion_invalida_por_id_deja_el_estado_intacto` (incluye CA02); `test_u3_entrada_invalida_por_numero_deja_el_estado_intacto`; `test_u3_cero_sin_retroceso_disponible_es_invalido` |
| RF08 Recordar el estado de la partida | N04 | Clase `Partida` (`variables`) | `motor.py` → `elegir_opcion()` | `test_u1_condiciones_habilitan_solo_las_opciones_correspondientes`; `test_i1_recorrido_completo_hasta_cada_final` |
| RF09 Reconocer el final | N05 | Caso de uso (extensión "Llegar a un final"); clase `EscenaFinal`; estado "En escena final" | `motor.py` → `en_escena_final()`; `main.py` → `jugar()` | `test_escena_final_no_tiene_opciones_disponibles`; `test_i1_recorrido_completo_hasta_cada_final` (E4, E5, E6) |
| RF10 Comenzar nueva partida | N05 | Caso de uso "Comenzar una nueva partida"; estados (`reiniciar()`) | `motor.py` → `reiniciar()`; `main.py` → `ofrecer_nueva_partida()` | `test_u5_reiniciar_restaura_escena_y_variables`; `test_u5_reiniciar_no_modifica_las_variables_iniciales_de_la_historia` |
| RF11 Validar el contenido antes de jugar | N06 | Caso de uso "Cargar una historia y revisar sus errores"; clases `EscenaIntermedia`, `EscenaFinal`; componentes | `cargador.py`; `modelo.py` → constructores de escena | `test_u4_contenido_invalido_se_rechaza_con_mensaje_claro` (13 variantes, incluida CA03); `test_u4_archivo_ilegible`; `test_u4_archivo_inexistente`; `test_u4_archivo_que_no_es_un_objeto` |
| RF12 Informar la causa del error | N06 | Contexto (mensajes de error a la escritora); clase `ErrorDeContenido` | `modelo.py` → `ErrorDeContenido`; `cargador.py`; `main.py` → `main()` | `test_u4_contenido_invalido_se_rechaza_con_mensaje_claro` (el mensaje contiene el ID o campo) |
| RF13 Informar bloqueo | N02, N05 | Caso de uso (extensión "Informar bloqueo"); estado "Sin opciones disponibles" | `motor.py` → `sin_opciones_disponibles()`; `main.py` → `jugar()` | `test_bloqueo_escena_no_final_sin_opciones_habilitadas` |
| RF14 Deshacer la última decisión | Solicitud de cambio | Caso de uso "Deshacer la última decisión"; clase `Partida` (`respaldo`, `deshacer()`); estados | `motor.py` → `elegir_opcion()` (guarda el respaldo), `deshacer()` | `test_u6_deshacer_restaura_escena_y_variables`; `test_u6_ejemplo_de_la_solicitud_de_cambio`; `test_u6_deshacer_con_el_numero_cero` |
| RF15 Deshacer desde un final | Solicitud de cambio | Estados ("En escena final" → `deshacer()`) | `motor.py` → `deshacer()`; `main.py` → `ofrecer_nueva_partida()` | `test_i1_deshacer_desde_un_final` (E4, E5, E6) |
| RF16 Un solo nivel de retroceso | Solicitud de cambio | Clase `Partida` (`puede_deshacer()`) | `motor.py` → `deshacer()` | `test_u6_deshacer_consume_el_retroceso`; `test_u6_nueva_eleccion_vuelve_a_habilitar_el_retroceso` |
| RF17 Sin retroceso al iniciar ni al reiniciar | Solicitud de cambio | Clase `Partida` | `motor.py` → `reiniciar()` | `test_u6_al_iniciar_no_hay_retroceso`; `test_u5_reiniciar_elimina_el_historial` |
| RF18 Entrada inválida conserva el retroceso | Solicitud de cambio | Secuencia; clase `Partida` | `motor.py` → `elegir_opcion()` (respaldo solo en elecciones válidas) | `test_u6_entrada_invalida_preserva_el_historial`; `test_u6_opcion_invalida_por_id_preserva_el_historial` |

## Requisitos no funcionales
| Requisito | Origen | Modelos | Código | Evidencia |
|---|---|---|---|---|
| RNF01 Claridad de errores | Voz de la coordinadora | Contexto; clase `ErrorDeContenido` | `cargador.py`; `modelo.py` | `test_u4_*` (16 casos con mensaje que identifica el ID o campo); `docs/resultado_pruebas.txt` |
| RNF02 Facilidad de uso (interfaz en español) | Voces del cliente; supuesto 2 | Componentes (capa de interfaz) | `main.py` (todos los textos) | Revisión de los textos de la interfaz en el recorrido de los tres finales, una entrada inválida y un error de carga (ver "Verificación de los RNF") |
| RNF03 Confiabilidad | Voz de la coordinadora | Secuencia; estados | `motor.py` → `elegir_por_numero()`; `main.py` → `main()` (captura de Ctrl + C y errores inesperados) | `test_u3_entrada_invalida_por_numero_deja_el_estado_intacto` (7 variantes); `test_u3_cero_sin_retroceso_disponible_es_invalido`; prueba manual en consola |

## Verificación de los RNF
RNF01 se verifica con las pruebas automatizadas `test_u4_*` (ver `docs/resultado_pruebas.txt`). RNF02 y RNF03 requieren además una revisión en la consola, que se registra a continuación.

**Cómo se hizo:** se ejecutó `python src/main.py` con la historia principal y se recorrieron los tres finales. En el camino se escribieron entradas inválidas, se usó la opción de deshacer y se cargaron archivos con errores.

### RNF02: textos de la interfaz en español
| Texto mostrado por el motor | Cuándo aparece | ¿En español? |
|---|---|---|
| `=== La última transmisión ===` (título de la historia) | En cada escena | Sí |
| `1. Investigar archivo`, `2. Cortar comunicación`… (opciones numeradas) | En cada escena no final | Sí |
| `0. Deshacer la última decisión` | Cuando hay una decisión que deshacer | Sí |
| `Elige una opción:` | Al pedir una entrada | Sí |
| `Entrada no válida. Escribe el número de una de las opciones.` | Ante una entrada inválida | Sí |
| `*** FIN DE LA HISTORIA ***` | Al llegar a un final | Sí |
| `1. Comenzar una nueva partida` | Después de un final o un bloqueo | Sí |
| `No hay opciones disponibles en esta escena; la historia no puede continuar.` | En una escena sin opciones habilitadas | Sí |
| `No se pudo cargar la historia.` seguido de la causa (por ejemplo: `La opción 'O1' de la escena 'E1' lleva a la escena 'E99', que no existe.`) | Al cargar un archivo con errores | Sí |
| `No se encontró el archivo 'data/no_existe.json'.` | Al cargar un archivo que no existe | Sí |
| `Partida terminada. ¡Hasta pronto!` | Al cerrar con Ctrl + C | Sí |
| `Ocurrió un error inesperado y la partida no puede continuar.` | Ante un error no previsto | Sí |

**Resultado:** 12 de 12 textos en español (100 %). No se muestran trazas técnicas de Python en ningún caso.

### RNF03: entradas inválidas en la consola
| Entrada | Escena | Resultado esperado | Resultado obtenido |
|---|---|---|---|
| `abc` (texto) | E1 | Aviso; la escena y las variables no cambian | Cumple |
| Vacía (solo Enter) | E1 | Aviso; sin cambios | Cumple |
| `9` (fuera de rango) | E1 | Aviso; sin cambios | Cumple |
| `-1` (negativo) | E1 | Aviso; sin cambios | Cumple |
| `1.5` (decimal) | E1 | Aviso; sin cambios | Cumple |
| `0` sin decisión que deshacer | E1 | Aviso; sin cambios | Cumple |
| `x` después de deshacer | E3 | Aviso; sin cambios | Cumple |
| Ctrl + C | Cualquiera | Despedida, sin traza de error | Cumple |

Una opción no habilitada no se muestra con número, así que escribir su posición equivale a un número fuera de rango; ese caso se cubre con `9`.

**Resultado:** 0 cierres inesperados. El programa solo termina cuando el lector lo cierra (código de salida 0) o cuando el archivo de historia tiene errores (código de salida 1, con el mensaje correspondiente).

**Evidencia:** captura de la consola en `docs/images/verificacion_consola.png`.

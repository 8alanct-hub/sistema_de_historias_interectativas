# 4. Requisitos

## Necesidades del cliente (voces)

| Voz | Necesidad | Atributo / tipo de requisito |
|---|---|---|
| Escritora principal | Agregar o cambiar escenas y decisiones sin modificar el programa. Para ello necesita que se le explique el formato JSON de las historias. | Modificabilidad (RNF) |
| Diseñador de la experiencia | Que las decisiones tengan consecuencias y que algunas opciones aparezcan solo cuando el lector haya descubierto cierta información. | Funcional (RF) |
| Coordinadora del festival | Si una historia contiene un error, saber qué corregir; y que el lector nunca se encuentre con un cierre inesperado del programa. | Claridad de errores y confiabilidad (RNF) |

## Requisitos funcionales
| ID | Requisito | Necesidad (N01–N06) | Criterio de aceptación |
|---|---|---|---|
| RF01 | **Cargar historia:** el motor carga una historia desde un archivo JSON indicado al iniciar el programa. | N01 | Se carga `la_ultima_transmision.json` y también `segunda_historia.json` sin modificar el código. |
| RF02 | **Iniciar partida:** el motor comienza en la escena de inicio definida en el archivo, con las variables en sus valores iniciales. | N01 | Al cargar la historia principal, la partida comienza en E1 con `conoce_origen` y `confia_en_la_voz` en falso. |
| RF03 | **Mostrar escena actual:** el motor muestra el texto de la escena en la que se encuentra el lector. | N02 | Al iniciar se muestra el texto de E1. |
| RF04 | **Mostrar solo opciones habilitadas:** el motor muestra únicamente las opciones de la escena actual cuyas condiciones se cumplen. | N02 | En E3 con `conoce_origen` en verdadero se muestran exactamente "Activar con código" y "Cortar comunicación"; con falso, "Activar sin verificar" y "Cortar comunicación". |
| RF05 | **Aplicar efectos:** al elegir una opción válida, el motor asigna a las variables los valores definidos en sus efectos. | N03 | Elegir "Investigar archivo" en E2 deja `conoce_origen` en verdadero. |
| RF06 | **Avanzar a la escena destino:** al elegir una opción válida, el motor pasa a la escena destino de esa opción. | N03 | Elegir "Revisar señal" en E1 lleva a E2. |
| RF07 | **Rechazar entradas inválidas:** si el lector elige una opción inexistente o no habilitada, el motor la rechaza sin cerrarse y sin cambiar la escena ni las variables. | N03 | En E3 sin conocer el origen, intentar "activar_codigo" deja la partida en E3 con las mismas variables. |
| RF08 | **Recordar el estado de la partida:** el motor conserva los valores de las variables durante toda la partida, para que las elecciones posteriores dependan de las anteriores. | N04 | Tras "Investigar archivo" en E2, al llegar a E3 está disponible "Activar con código". |
| RF09 | **Reconocer el final:** al llegar a una escena final, el motor indica que la historia terminó y no ofrece opciones de avance. | N05 | Al llegar a E4, E5 o E6 se muestra el final y no hay opciones para continuar. |
| RF10 | **Comenzar nueva partida:** después de un final, el motor permite comenzar otra partida sin conservar información de la anterior. | N05 | Tras llegar a E4 y reiniciar, la partida vuelve a E1 con ambas variables en falso. |
| RF11 | **Validar el contenido antes de jugar:** al cargar un archivo, el motor lo revisa y lo rechaza, sin abrir una partida, si tiene alguno de los errores de la sección "Validación y errores" de la guía. | N06 | Una copia de la historia con un destino E99 inexistente se rechaza y no se inicia la partida. |
| RF12 | **Informar la causa del error:** cuando rechaza un archivo, el motor muestra un mensaje con la causa y el campo o ID involucrado. | N06 | Con el destino E99, el mensaje indica que el destino no existe e identifica la opción y la escena donde está. |
| RF13 | **Informar bloqueo:** si durante una partida una escena no final no tiene opciones habilitadas, el motor informa el bloqueo y permite reiniciar. | N02, N05 | Con una historia de prueba donde la única opción de una escena no final tiene una condición imposible, se muestra el aviso de bloqueo y la opción de reiniciar. |

### Requisitos agregados por la solicitud de cambio (hora 6)
| ID | Requisito | Origen | Criterio de aceptación |
|---|---|---|---|
| RF14 | **Deshacer la última decisión:** el motor restaura exactamente la escena y todas las variables de antes de la última elección válida. | Solicitud de cambio | Desde E2, "Investigar archivo" lleva a E3 con `conoce_origen` verdadero; deshacer devuelve E2 con `conoce_origen` falso. |
| RF15 | **Deshacer desde un final:** se puede deshacer estando en una escena final. | Solicitud de cambio | Desde E4, E5 o E6, deshacer vuelve a E3 con los valores previos a esa elección. |
| RF16 | **Un solo nivel de retroceso:** después de deshacer, no se puede volver a deshacer hasta hacer una nueva elección válida. No se ofrece rehacer. | Solicitud de cambio | Un segundo intento de deshacer no cambia nada; tras una nueva elección válida, se puede deshacer otra vez. |
| RF17 | **Sin retroceso al iniciar ni al reiniciar:** al comenzar no hay nada que deshacer, y reiniciar elimina el historial. | Solicitud de cambio | Al iniciar no se puede deshacer; tras llegar a E4 y reiniciar, tampoco. |
| RF18 | **Entrada inválida conserva el retroceso:** una entrada inválida no modifica la partida ni reemplaza lo que se puede deshacer. | Solicitud de cambio | Tras elegir "Investigar archivo" y escribir una entrada inválida en E3, deshacer sigue devolviendo E2. |

## Requisitos no funcionales
| ID | Atributo | Medida | Procedimiento | Evidencia |
|---|---|---|---|---|
| RNF01 | Claridad de errores | El 100 % de los 9 tipos de error de contenido definidos en la guía produce un mensaje en español que indica la causa y el campo o ID afectado, sin mostrar trazas técnicas de Python. | Se prepara un archivo de historia con cada tipo de error, se carga en el motor y se revisa el mensaje obtenido. | Prueba automatizada que cubre los 9 tipos de error y registro de su última ejecución. |
| RNF02 | Facilidad de uso | El 100 % de los textos que muestra la interfaz (instrucciones, opciones del motor, avisos de final, bloqueo y errores) está en español. El uso del motor se explica en el README; no se incluye tutorial dentro del programa. | Se recorren los tres finales de la historia principal, se provoca una entrada inválida y un error de carga, y se revisa cada texto mostrado por el motor. | Grabación o capturas del recorrido y lista de los textos revisados. |
| RNF03 | Confiabilidad | 0 cierres inesperados del programa ante entradas inválidas del lector: texto en lugar de número, número fuera de rango, entrada vacía y opción no habilitada. En todos los casos el motor muestra un aviso y conserva la escena y las variables. | Se ejecuta una prueba automatizada que envía cada tipo de entrada inválida en distintas escenas y comprueba que el estado no cambia; además, se prueba manualmente en la consola. | Registro de ejecución de la prueba automatizada y captura de la prueba manual en consola. |

## Conflicto: retroceso
- **Conflicto:** la escritora quiere permitir retroceder siempre; el diseñador quiere que las decisiones sean irreversibles.
- **Pregunta de aclaración (propuesta al cliente):** ¿Les parece bien que, al iniciar, el lector elija entre dos modos: **"Modo historia"**, donde las decisiones son definitivas, y **"Modo libre"**, donde puede retroceder y cambiar sus elecciones? Así se respetan tanto la visión de la escritora como la del diseñador.
- **Acuerdo provisional (versión 1, `v1.0`):** no se implementa retroceso hasta que el cliente responda la pregunta de aclaración; no se presupone su decisión.
- **Respuesta del cliente (solicitud de cambio, hora 6):** el lector debe poder deshacer su última decisión, revirtiendo todas sus consecuencias, con un solo nivel de retroceso. No se adoptan los dos modos propuestos. Esta decisión reemplaza el acuerdo provisional y se implementa con RF14–RF18.

## Preguntas y respuestas / supuestos
1. **Supuesto:** no se analizan automáticamente todos los caminos posibles de la historia (la guía no lo exige, pág. 4). Los bloqueos se detectan durante la partida (RF13) y no al cargar el archivo.
2. **Supuesto:** todos los usuarios del motor (el lector, la escritora principal, el diseñador de la experiencia y la coordinadora del festival) saben leer en español. Por eso la interfaz, los mensajes y las historias están solo en español (RNF02) y no se incluye traducción (ver Alcance en `01_fundamentos.md`).
3. **Supuesto:** el lector elige una opción escribiendo en la consola el número con el que aparece en pantalla (1, 2, 3…), como es habitual en los menús de consola. Solo se numeran las opciones habilitadas (RF04). Cualquier otra entrada se considera inválida (RF07, RNF03).
4. **Supuesto (agregado con la solicitud de cambio):** cuando se puede deshacer, aparece la opción **"0. Deshacer la última decisión"**, también en los finales y en el bloqueo. Si no se puede deshacer, el 0 se trata como entrada inválida (RF07).

## Ambigüedad o defecto detectado y su corrección
- **Defecto:** en el primer planteamiento, varios requisitos funcionales no eran atómicos; cada uno mezclaba varios comportamientos. Por ejemplo, el requisito "seguir cronología" incluía avanzar a la escena destino, aplicar los efectos de la opción y rechazar entradas erróneas; y el de "final" incluía reconocer el final y comenzar una nueva partida.
- **Corrección:** se dividieron en requisitos independientes, cada uno con un solo comportamiento observable y su propio criterio de aceptación (RF05, RF06 y RF07; RF09 y RF10). Así cada requisito puede verificarse con una prueba concreta.

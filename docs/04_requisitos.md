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
| RF01 | **Cargar historia:** el sistema carga una historia desde un archivo JSON indicado al iniciar el programa. | N01 | Se carga `la_ultima_transmision.json` y también `segunda_historia.json` sin modificar el código. |
| RF02 | **Iniciar partida:** el sistema comienza en la escena de inicio definida en el archivo, con las variables en sus valores iniciales. | N01 | Al cargar la historia principal, la partida comienza en E1 con `conoce_origen` y `confia_en_la_voz` en falso. |
| RF03 | **Mostrar escena actual:** el sistema muestra el texto de la escena en la que se encuentra el lector. | N02 | Al iniciar se muestra el texto de E1. |
| RF04 | **Mostrar solo opciones habilitadas:** el sistema muestra únicamente las opciones de la escena actual cuyas condiciones se cumplen. | N02 | En E3 con `conoce_origen` en verdadero se muestran exactamente "Activar con código" y "Cortar comunicación"; con falso, "Activar sin verificar" y "Cortar comunicación". |
| RF05 | **Aplicar efectos:** al elegir una opción válida, el sistema asigna a las variables los valores definidos en sus efectos. | N03 | Elegir "Investigar archivo" en E2 deja `conoce_origen` en verdadero. |
| RF06 | **Avanzar a la escena destino:** al elegir una opción válida, el sistema pasa a la escena destino de esa opción. | N03 | Elegir "Revisar señal" en E1 lleva a E2. |
| RF07 | **Rechazar entradas inválidas:** si el lector elige una opción inexistente o no habilitada, el sistema la rechaza sin cerrarse y sin cambiar la escena ni las variables. | N03 | En E3 sin conocer el origen, intentar "activar_codigo" deja la partida en E3 con las mismas variables. |
| RF08 | **Recordar el estado de la partida:** el sistema conserva los valores de las variables durante toda la partida, para que las elecciones posteriores dependan de las anteriores. | N04 | Tras "Investigar archivo" en E2, al llegar a E3 está disponible "Activar con código". |
| RF09 | **Reconocer el final:** al llegar a una escena final, el sistema indica que la historia terminó y no ofrece opciones de avance. | N05 | Al llegar a E4, E5 o E6 se muestra el final y no hay opciones para continuar. |
| RF10 | **Comenzar nueva partida:** después de un final, el sistema permite comenzar otra partida sin conservar información de la anterior. | N05 | Tras llegar a E4 y reiniciar, la partida vuelve a E1 con ambas variables en falso. |
| RF11 | **Validar el contenido antes de jugar:** al cargar un archivo, el sistema lo revisa y lo rechaza, sin abrir una partida, si tiene alguno de los errores de la sección "Validación y errores" de la guía. | N06 | Una copia de la historia con un destino E99 inexistente se rechaza y no se inicia la partida. |
| RF12 | **Informar la causa del error:** cuando rechaza un archivo, el sistema muestra un mensaje con la causa y el campo o ID involucrado. | N06 | Con el destino E99, el mensaje indica que el destino no existe e identifica la opción y la escena donde está. |
| RF13 | **Informar bloqueo:** si durante una partida una escena no final no tiene opciones habilitadas, el sistema informa el bloqueo y permite reiniciar. | N02, N05 | Con una historia de prueba donde la única opción de una escena no final tiene una condición imposible, se muestra el aviso de bloqueo y la opción de reiniciar. |

## Requisitos no funcionales
| ID | Atributo | Medida | Procedimiento | Evidencia |
|---|---|---|---|---|
| RNF01 |  |  |  |  |
| RNF02 |  |  |  |  |
| RNF03 |  |  |  |  |

## Conflicto: retroceso
- **Conflicto:** la escritora quiere permitir retroceder siempre; el diseñador quiere que las decisiones sean irreversibles.
- **Pregunta de aclaración:** _(pendiente — formularla)_
- **Acuerdo provisional:** en la versión 1 no se implementa retroceso. Se mantiene así hasta que el cliente responda la pregunta de aclaración; no se presupone su decisión.

## Preguntas y respuestas / supuestos
1.
2.
3.

## Ambigüedad o defecto detectado y su corrección

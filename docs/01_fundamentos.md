# 1. Fundamentos

## Problema
Un colectivo de escritores prepara una experiencia de ficción interactiva para un festival universitario. En sus historias, el lector toma decisiones y llega a desenlaces distintos según lo que elige.

El colectivo no sabe programar, pero necesita:
- Crear y modificar las historias en archivos, sin cambiar el programa.
- Que las opciones dependan de lo ocurrido antes en la partida.
- Detectar los errores del contenido antes de que alguien juegue, sin que el lector se encuentre con un cierre inesperado.

La solución es un motor que interpreta historias escritas en archivos JSON, valida su contenido y permite jugarlas en consola.

## Actores e interesados
| Actor | Rol |
|---|---|
| Lector | Juega la historia: lee las escenas, elige opciones, llega a un final y puede comenzar otra partida. |
| Escritora principal | Crea y modifica las historias editando los archivos JSON; no programa. |
| Diseñador de la experiencia | Define las condiciones y consecuencias de las decisiones dentro de las historias. |
| Coordinadora del festival | Necesita saber qué corregir cuando una historia tiene errores y que el lector nunca vea un cierre inesperado. |

## Alcance
### Incluye
- Cargar y validar historias desde archivos JSON antes de jugar.
- Jugar una partida en consola: mostrar la escena actual, mostrar solo las opciones habilitadas, aplicar efectos y avanzar.
- Recordar el estado de la partida (variables booleanas) mientras dura.
- Rechazar entradas inválidas sin cerrar el programa.
- Reconocer los finales, informar bloqueos y comenzar una nueva partida.
- Deshacer la última decisión, con un solo nivel de retroceso (agregado por la solicitud de cambio, ver `08_cambio.md`).
- Interfaz en español.

### No incluye
- Traducción de la interfaz a otros idiomas.
- Traducción de las historias.
- Menú o interfaz visual fuera de la consola.
- Retroceso de varios niveles y rehacer una decisión deshecha (la solicitud de cambio solo pide deshacer la última decisión).
- Límites del ejercicio definidos en la guía (pág. 2): cuentas de usuario, base de datos, guardado entre ejecuciones, conexión a internet, editor visual, audio, imágenes y lenguaje de expresiones.

## Riesgos y mitigaciones
| Riesgo | Mitigación |
|---|---|
| **Mensajes de error poco claros:** el motor detecta un error en el archivo de la historia, pero el mensaje no permite a la escritora entender qué está mal ni dónde corregirlo. | Definir un mensaje en español para cada uno de los 9 tipos de error de contenido, que indique siempre la causa y el campo o ID afectado (RF12, RNF01). Verificarlo con una prueba automatizada por cada tipo de error y revisar los mensajes leyéndolos como lo haría la escritora. |
| **Cierre inesperado por un caso no contemplado:** una entrada del lector o una situación de la partida que no se probó hace que el programa se cierre. | Validar toda entrada del lector antes de usarla y, si no es válida, mostrar un aviso sin cambiar el estado (RF07). Capturar en la interfaz cualquier error inesperado para mostrar un mensaje controlado y permitir reiniciar. Probar con entradas inválidas de distintos tipos en varias escenas (RNF03). |

## Priorización de atributos de calidad
Se prioriza la experiencia del usuario final (el lector), porque es quien usa el motor durante el festival:

1. **Confiabilidad (RNF03):** lo más importante es que la experiencia no se interrumpa. Un cierre inesperado arruina la partida del lector, y es justo lo que la coordinadora pide evitar.
2. **Facilidad de uso (RNF02):** toda la interfaz en español, para que cualquier lector del festival que sepa leer en español pueda entender las escenas, las opciones y los avisos sin ayuda (ver supuesto 2 en `04_requisitos.md`).
3. **Claridad de errores (RNF01):** es importante para la escritora, pero la afecta mientras prepara la historia, no al lector durante el festival. Además, al estar la interfaz en español, los mensajes ya son legibles, y desde una correcta lectura se puede intuir dónde está el error.

## Decisión de responsabilidad profesional
**Categoría:** datos.

- **Decisión:** el motor no pide ni guarda ningún dato del lector: ni nombre, ni registro, ni historial de partidas.
- **Por qué:** en el festival lo juega público general. Pedir datos no aporta nada a la experiencia y la interrumpiría, que es justo lo que se quiere evitar al priorizar la confiabilidad y la inmersión del lector. Además, al no recoger datos no existe riesgo de exponer información personal.
- **Evidencia:** no hay guardado entre ejecuciones (ver Alcance) y al comenzar una nueva partida se borra todo el estado de la anterior (RF10).

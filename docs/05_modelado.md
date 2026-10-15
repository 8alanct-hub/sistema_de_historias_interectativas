# 5. Modelado

## Diagrama de contexto
El motor se muestra como una caja cerrada. Alrededor están las entidades externas que intercambian información con él. Las historias no forman parte del motor: se leen desde archivos externos.

![Diagrama de contexto](diagramas/contexto.png)

*Fuente editable: `diagramas/contexto.mmd` (Mermaid).*

- La **coordinadora del festival** no aparece porque no intercambia información con el motor; sus necesidades se cubren con los requisitos (RF12, RNF01 y RNF03).
- La **escritora** no programa: edita el archivo JSON siguiendo el formato explicado en el README y ejecuta el motor con un comando para cargar su historia y ver si tiene errores.

## Casos de uso
Solo aparecen los actores que usan el motor directamente. El diseñador de la experiencia y la coordinadora del festival no interactúan con el motor, por lo que no tienen casos de uso.

![Diagrama de casos de uso](diagramas/casos_de_uso.png)

*Fuente editable: `diagramas/casos_de_uso.mmd` (Mermaid).*

| Caso de uso | Actor | Requisitos |
|---|---|---|
| Iniciar partida | Lector | RF01, RF02 |
| Ver la escena y sus opciones | Lector | RF03, RF04 |
| Elegir una opción | Lector | RF05, RF06, RF07, RF08 |
| Comenzar una nueva partida | Lector | RF10 |
| Deshacer la última decisión | Lector | RF14–RF18 (solicitud de cambio) |
| Cargar una historia y revisar sus errores | Escritora principal | RF11, RF12 |

Llegar a un final (RF09) e informar un bloqueo (RF13) no son casos de uso que el lector solicite: son resultados posibles de elegir una opción, por eso se representan como extensiones («extend») de "Elegir una opción".

## Clases del dominio
![Diagrama de clases del dominio](diagramas/clases.png)

*Fuente editable: `diagramas/clases.mmd` (Mermaid).*

| Clase | Responsabilidad | Requisitos |
|---|---|---|
| `Historia` | Contiene el título, la escena de inicio, las variables iniciales y todas las escenas. | RF01, RF02 |
| `Escena` (abstracta) | Datos comunes de toda escena: id y texto. | RF03 |
| `EscenaIntermedia` | Escena no final; ofrece una o más opciones. | RF04, RF11 |
| `EscenaFinal` | Escena final; no tiene opciones. | RF09, RF11 |
| `Opcion` | Texto visible, escena destino, condiciones y efectos; sabe si está habilitada con las variables actuales. | RF04, RF05, RF06 |
| `Partida` | Estado de la partida en curso (escena actual, variables y respaldo de la última elección válida); muestra las opciones habilitadas, procesa la elección (`elegir_por_numero()` recibe lo que escribe el lector y valida que sea un número dentro del rango; `elegir_opcion()` recibe un id y valida que la opción exista y esté habilitada), detecta el final y el bloqueo, y reinicia. `sin_opciones_disponibles()` es verdadero solo si la escena actual no es final y ninguna de sus opciones está habilitada (bloqueo, RF13); en una escena final no se considera bloqueo. | RF02, RF04–RF10, RF13, RF14–RF18 |

- **Solicitud de cambio:** `Partida` guarda en `respaldo` la escena y una copia de las variables antes de cada elección válida. `deshacer()` las restaura y vacía el respaldo (un solo nivel); `reiniciar()` también lo vacía. En `elegir_por_numero()`, el 0 significa deshacer (supuesto 4).
- `Historia.obtener_escena()` y la excepción `ErrorDeContenido` (que lanzan las escenas al crearse con una cantidad de opciones incorrecta) se agregaron al diagrama para que coincida con el código.
- Las variables, las condiciones y los efectos se modelan como atributos de tipo diccionario (nombre → verdadero/falso), igual que en el formato JSON.
- La escena se divide en `EscenaIntermedia` y `EscenaFinal` (ver la decisión de diseño en `07_implementacion.md`). El formato JSON no cambia: el cargador crea una u otra según el campo `"final"`.
- Se usa la convención de Python: clases en PascalCase y atributos y métodos en snake_case, igual que las claves del JSON (`conoce_origen`).

## Secuencia: elegir una opción
![Diagrama de secuencia: elegir una opción](diagramas/secuencia_elegir_opcion.png)

*Fuente editable: `diagramas/secuencia_elegir_opcion.mmd` (Mermaid).*

- **La interfaz solo muestra y recibe.** Pasa a la partida el texto que escribió el lector, sin procesarlo. Toda la validación ocurre en `Partida`, de modo que la regla "una entrada inválida no altera la partida" está en un solo lugar y puede probarse sin la consola (RF07, RNF03).
- **Dos niveles de validación.** `elegir_por_numero()` valida el formato y el rango de la entrada (supuesto 3). `elegir_opcion()` vuelve a comprobar que la opción exista y esté habilitada, aunque la consola solo muestre las habilitadas. Así el motor rechaza una opción no habilitada aunque se envíe su identificador directamente (CA02).
- **Después de cada elección válida**, la interfaz consulta si la partida está en una escena final (RF09) o sin opciones disponibles (bloqueo, RF13), y en ambos casos ofrece una nueva partida (RF10).

## Estados de una partida
![Diagrama de estados de una partida](diagramas/estados_partida.png)

*Fuente editable: `diagramas/estados_partida.mmd` (Mermaid).*

| Estado | Cuándo | Se comprueba con |
|---|---|---|
| En curso | La escena actual es intermedia y tiene opciones disponibles. | `opciones_disponibles()` |
| En escena final | La partida llegó a una escena final (RF09). | `en_escena_final()` |
| Sin opciones disponibles | La escena actual es intermedia, pero ninguna de sus opciones está habilitada (bloqueo, RF13). | `sin_opciones_disponibles()` |

- Los nombres de los estados coinciden con los métodos de `Partida`, para mantener el mismo vocabulario.
- Se usa "Sin opciones disponibles" en lugar de "Bloqueada" porque el bloqueo no es culpa del lector: no dejó de hacer nada, simplemente la historia no ofrece opciones habilitadas en ese punto.
- Desde "En escena final" y "Sin opciones disponibles" el lector puede comenzar una nueva partida (`reiniciar()`, RF10).
- **Solicitud de cambio:** desde cualquier estado, si hay una decisión previa, `deshacer()` devuelve la partida a "En curso" con la escena y las variables anteriores (RF14, RF15). Después de deshacer no se puede volver a deshacer hasta otra elección válida (RF16).
- Si el archivo de la historia tiene errores, la partida no llega a crearse (RF11, CA03). Eso ocurre en el cargador, antes de este diagrama, por lo que no se representa aquí.

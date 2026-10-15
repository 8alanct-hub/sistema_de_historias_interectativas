# 6. Arquitectura

## Diagrama de componentes
![Diagrama de componentes por capas](diagramas/arquitectura.png)

*Fuente editable: `diagramas/arquitectura.mmd` (Mermaid).*

| Componente | Capa | Responsabilidad | Usa a |
|---|---|---|---|
| `src/main.py` | Interfaz | Muestra escenas, opciones y avisos; pasa a la partida lo que escribe el lector, sin validarlo. | `cargador.py`, `motor.py` |
| `src/motor.py` | Reglas | `Partida`: estado de la partida (escena actual y variables); valida entradas, aplica efectos, detecta el final y el bloqueo, y reinicia. | `modelo.py` |
| `src/modelo.py` | Reglas | `Historia`, `Escena`, `EscenaIntermedia`, `EscenaFinal` y `Opcion`: estructura fija de la historia, que no cambia mientras se juega. | — |
| `src/cargador.py` | Carga | Lee el archivo JSON, valida su contenido (RF11, RF12) y crea los objetos del modelo. | `modelo.py` |
| `data/*.json` | Contenido | Historias escritas por la escritora y el diseñador. No contienen código. | — |

**Regla de dependencias:** cada capa solo usa a las de abajo. `motor.py` y `modelo.py` no conocen la consola ni los archivos.

## Decisión 1: arquitectura en capas
- **Contexto:** la escritora necesita cambiar historias sin modificar el programa, y el motor debe poder cargar una segunda historia sin cambios en su código. Además, la solicitud de cambio de la hora 6 puede afectar a cualquier parte del sistema.
- **Alternativas:**
  - *Todo en un solo archivo (monolito):* más rápido al principio, pero cualquier cambio toca todo y las reglas quedan mezcladas con la consola y con la lectura del JSON.
  - *Modelo–Vista–Controlador (MVC):* también separa responsabilidades, pero agrega un controlador intermedio que en un programa de consola tan pequeño no aporta beneficios.
- **Elección:** arquitectura en capas: interfaz (`main.py`), reglas (`motor.py` y `modelo.py`), carga (`cargador.py`) y contenido (`data/`).
- **Consecuencias:**
  - Las historias están fuera del código: cargar otra historia no requiere modificar ningún archivo de `src/`.
  - Las reglas pueden probarse sin la consola y sin archivos reales.
  - Se podría cambiar la consola por otra interfaz sin tocar las reglas.
  - El costo es tener más archivos y definir bien qué hace cada uno.

## Decisión 2: la validación de las entradas está en la Partida
- **Contexto:** el lector escribe en la consola el número de una opción (supuesto 3) y puede escribir cualquier cosa. Además, el motor debe rechazar una opción no habilitada aunque se envíe su identificador directamente (CA02).
- **Alternativas:**
  - *Validar en la interfaz:* `main.py` revisa que la entrada sea un número válido antes de llamar a la partida. La interfaz tendría lógica, y cualquier otra interfaz debería repetir esa validación.
  - *Validar en ambas:* duplica la misma regla en dos lugares.
- **Elección:** la interfaz solo muestra y recibe. `Partida` valida en dos niveles: `elegir_por_numero()` revisa el formato y el rango de la entrada, y `elegir_opcion()` comprueba que la opción exista y esté habilitada.
- **Consecuencias:**
  - La regla "una entrada inválida no altera la partida" (RF07, RNF03) está en un solo lugar y puede probarse sin la consola.
  - El motor se protege solo, sin importar quién lo use (CA02).
  - `main.py` queda muy simple: solo muestra textos y lee la entrada.

## Separación entre contenido, reglas e interfaz
- **Contenido** (`data/`): la escritora y el diseñador editan los archivos JSON sin tocar el código.
- **Reglas** (`motor.py` y `modelo.py`): no conocen la consola ni los archivos; solo trabajan con los objetos que crea el cargador.
- **Interfaz** (`main.py`): no contiene reglas del juego; solo muestra y recibe.

**Evidencia:** la segunda historia (`data/segunda_historia.json`, "El último algoritmo") se carga y se juega con el mismo motor, sin modificar ningún archivo de `src/`.

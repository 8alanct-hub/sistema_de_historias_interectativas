# 7. Implementación

## Decisión de diseño detallado
Decisión tomada durante el modelado de clases y confirmada en la implementación (`modelo.py` y `cargador.py`).

**Decisión:** separar la escena en dos clases, `EscenaIntermedia` y `EscenaFinal`, que heredan de una clase general `Escena` (id y texto).

- **Contexto:** la guía exige que las escenas finales tengan cero opciones y que las no finales tengan al menos una. En el archivo JSON ambas son el mismo elemento, diferenciado solo por el campo `"final"`.
- **Alternativa descartada:** una sola clase `Escena` con un atributo `es_final`. Es idéntica al JSON y más sencilla, pero la regla quedaría escondida en un atributo que habría que revisar en cada parte del motor.
- **Elección:** dos clases. `EscenaIntermedia` tiene una o más opciones y `EscenaFinal` no tiene opciones.
- **Consecuencias:**
  - La regla queda en la propia estructura del código: cada clase exige, al crearse, la cantidad de opciones que le corresponde.
  - La validación del error "escena final con opciones" o "escena no final sin opciones" ocurre en un solo lugar, al crear cada escena, lo que simplifica su detección y diagnóstico.
  - El cargador decide qué clase crear según el campo `"final"` del JSON. El formato de las historias no cambia, así que la escritora sigue escribiendo exactamente lo mismo.
  - El costo es una clase más y un paso adicional en el cargador.

## Bibliotecas y licencias
| Biblioteca | Tipo | Licencia | Uso |
|---|---|---|---|
| `json` | Biblioteca estándar de Python | PSF License | Leer los archivos de historia (`cargador.py`). |
| `sys` | Biblioteca estándar de Python | PSF License | Leer la ruta de la historia indicada al ejecutar el programa y terminarlo con un código de salida (`main.py`). |
| `os` | Biblioteca estándar de Python | PSF License | Limpiar la consola entre escenas, con `cls` en Windows y `clear` en Mac o Linux (`main.py`). |
| `pytest` 8.3.3 | Biblioteca externa (se instala con `pip`) | MIT | Ejecutar las pruebas automatizadas (`test/`). Solo se usa para las pruebas, no para jugar. |

Las bibliotecas estándar vienen incluidas con Python, por lo que no requieren instalación adicional. El motor no depende de bibliotecas externas; `pytest` solo se necesita para ejecutar las pruebas y está en `requirements.txt`.

# 7. Implementación

## Decisión de diseño detallado
> **Borrador:** decisión tomada durante el modelado de clases. Se confirmará o ajustará cuando se implementen el cargador y el motor.

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
|  |  |  |  |

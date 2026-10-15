# Motor de historias interactivas

Motor de consola que carga historias interactivas desde archivos JSON, valida su contenido y permite jugarlas: el lector elige opciones, las decisiones cambian lo que aparece después y cada historia puede tener varios finales. Proyecto del parcial práctico de Ingeniería de Software, con la historia **"La última transmisión"**.

**Integrante:** Alan Chiquillo Torres

## Versiones requeridas
- Python 3.11 (probado con Python 3.11.9 en Windows)
- pytest 8.3.3 (solo para ejecutar las pruebas; se instala dentro de un entorno virtual, ver Instalación)

El motor solo usa la biblioteca estándar de Python (`json`, `sys`, `os`).

## Instalación
El proyecto se entrega en el archivo `Parcial_ChiquilloAlan.zip`. No requiere internet para jugar.

1. **Descomprimir** el archivo ZIP (clic derecho → *Extraer todo…*).
2. **Abrir una consola en la carpeta descomprimida**, la que contiene `README.md`, `src/` y `data/`.
   En Windows: abrir la carpeta en el Explorador, escribir `cmd` en la barra de direcciones y pulsar Enter.
3. **Comprobar que Python está instalado** (debe mostrar 3.11 o superior):
   ```
   python --version
   ```
   Si no está instalado, descargarlo desde python.org y marcar la opción *Add Python to PATH* durante la instalación.
4. **Crear el entorno virtual** (solo la primera vez):
   ```
   python -m venv .venv
   ```
5. **Activar el entorno virtual** (cada vez que se abra una consola nueva):

   | Consola | Comando |
   |---|---|
   | Símbolo del sistema (`cmd`) | `.venv\Scripts\activate` |
   | PowerShell | `.venv\Scripts\Activate.ps1` |
   | Mac o Linux | `source .venv/bin/activate` |

   Cuando el entorno está activo, la consola muestra `(.venv)` al inicio de la línea.
6. **Instalar la dependencia de las pruebas** dentro del entorno:
   ```
   python -m pip install -r requirements.txt
   ```

### Por qué un entorno virtual
El entorno virtual (`.venv`) es una carpeta dentro del proyecto con su propia copia de Python y sus propias bibliotecas. Así `pytest` se instala solo para este proyecto: no se mezcla con lo que ya tenga instalado el equipo donde se revisa y no cambia la versión de `pytest` de otros proyectos. El motor solo usa la biblioteca estándar, por lo que el entorno solo es necesario para ejecutar las pruebas; aun así se recomienda usarlo para todos los comandos.

La carpeta `.venv` no se incluye en el ZIP ni en el repositorio (está en `.gitignore`), porque depende del equipo donde se crea; cada persona la crea con el paso 4.

### Si PowerShell no permite activar el entorno
Si al activar aparece un error que dice que la ejecución de scripts está deshabilitada, hay dos opciones que no requieren cambiar la configuración del equipo:
- Abrir la consola con `cmd` (paso 2) y activar con `.venv\Scripts\activate`.
- No activar el entorno y usar su Python directamente, anteponiendo `.venv\Scripts\` a cada comando. Por ejemplo:
  ```
  .venv\Scripts\python -m pip install -r requirements.txt
  .venv\Scripts\python src/main.py
  .venv\Scripts\python -m pytest -v
  ```

El repositorio también está disponible en GitHub: https://github.com/8alanct-hub/sistema_de_historias_interectativas

## Ejecución
Siempre desde la carpeta descomprimida del proyecto y con el entorno virtual activado:

| Qué | Comando |
|---|---|
| Jugar "La última transmisión" | `python src/main.py` |
| Jugar la segunda historia ("El último algoritmo") | `python src/main.py data/segunda_historia.json` |
| Cargar cualquier otra historia | `python src/main.py ruta/al/archivo.json` |
| Ver el mensaje de un archivo con errores (destino inexistente) | `python src/main.py data/error_destino_inexistente.json` |
| Ejecutar las pruebas | `python -m pytest -v` |
| Guardar el registro de las pruebas (PowerShell) | `python -m pytest -v \| Out-File -Encoding utf8 docs/resultado_pruebas.txt` |

Si `python` no se reconoce como comando en Windows, use `py` en su lugar.

## Cómo jugar
- Escriba el **número** de la opción y pulse Enter.
- **0** deshace la última decisión (aparece solo cuando hay algo que deshacer; un solo nivel).
- En un final, **1** comienza una nueva partida y **0** deshace la última decisión.
- **Ctrl + C** cierra el programa.

## Rutas para llegar a cada final
Historia principal (`python src/main.py`):

| Final | Elecciones | Recorrido |
|---|---|---|
| **E4 – Rescate** | 1 → 1 → 1 | Revisar señal → Investigar archivo → Activar con código |
| **E5 – El eco** | 1 → 2 → 1 | Revisar señal → Continuar sin investigar → Activar sin verificar |
| **E6 – Silencio** | 1 → 2 → 2 | Revisar señal → Continuar sin investigar → Cortar comunicación |

**Cómo una condición cambia las opciones:** en E3 aparece "Activar con código" solo si en E2 se eligió "Investigar archivo"; si no, aparece "Activar sin verificar".

**Deshacer desde un final:** en E4, E5 o E6, escriba 0 para volver a E3 con los valores anteriores.

## Formato del contenido (JSON)
Cada historia es un archivo JSON con esta estructura:

```json
{
  "titulo": "Nombre de la historia",
  "inicio": "E1",
  "variables": { "tiene_llave": false },
  "escenas": [
    {
      "id": "E1",
      "texto": "Texto que lee el lector.",
      "final": false,
      "opciones": [
        {
          "id": "tomar_llave",
          "texto": "Tomar la llave",
          "destino": "E2",
          "condiciones": {},
          "efectos": { "tiene_llave": true }
        }
      ]
    },
    { "id": "E2", "texto": "Fin de la historia.", "final": true, "opciones": [] }
  ]
}
```

| Campo | Significado |
|---|---|
| `titulo` | Nombre de la historia. |
| `inicio` | ID de la escena donde comienza la partida. |
| `variables` | Variables de la historia con su valor inicial (`true` o `false`). |
| `escenas` | Lista de escenas. |
| `id` (escena) | Identificador único de la escena. |
| `texto` | Lo que lee el lector. |
| `final` | `true` si la escena es un final; `false` si no. |
| `opciones` | Lista de opciones. Vacía si la escena es final; al menos una si no lo es. |
| `id` (opción) | Identificador único dentro de su escena. |
| `texto` (opción) | Lo que ve el lector como opción. |
| `destino` | ID de la escena a la que lleva. Debe existir. |
| `condiciones` | Variables que deben tener cierto valor para que la opción aparezca. Vacío = siempre aparece. Deben cumplirse todas. |
| `efectos` | Valores que se asignan a las variables al elegir la opción. Vacío = no cambia nada. |

Al cargar un archivo, el motor lo rechaza si tiene algún error (archivo ilegible, campos faltantes, inicio o destinos inexistentes, IDs repetidos, variables no declaradas, valores no booleanos o finales con opciones) y muestra un mensaje en español con la causa y el ID afectado. Por ejemplo:

```
No se pudo cargar la historia.
La opción 'revisar' de la escena 'E1' lleva a la escena 'E99', que no existe.
```

## Estructura del proyecto
```
src/
  main.py        Interfaz de consola
  motor.py       Partida: reglas del juego y deshacer
  modelo.py      Historia, Escena, EscenaIntermedia, EscenaFinal y Opcion
  cargador.py    Lectura y validación del JSON
data/            Historias (JSON) y un ejemplo con error (error_destino_inexistente.json)
test/            Pruebas automatizadas (pytest)
docs/            Documentación, diagramas, capturas y registro de pruebas
herramientas/    Script que genera este README
```

## Versiones
- `v1.0`: versión inicial, antes de la solicitud de cambio.
- `v2.0`: versión con la solicitud de cambio implementada (deshacer la última decisión).

## Limitaciones conocidas
- El motor no analiza todos los caminos posibles de una historia al cargarla; por ejemplo, no detecta finales inalcanzables. Los bloqueos se informan durante la partida.
- Solo se puede deshacer la última decisión (un nivel) y no existe rehacer.
- No hay guardado entre ejecuciones: al cerrar el programa se pierde la partida.
- Solo funciona en consola y en español.

## Video de demostración
_(Enlace pendiente)_

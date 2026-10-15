# sistema_de_historias_interectativas
Motor que permite cargar narraciones desde archivos, ofreciendo opciones que pueden afectar al desarrollo de la historia

## Versiones requeridas
- Python 3.11 (probado con Python 3.11.9 en Windows)
- pytest 8.3.3 (solo para ejecutar las pruebas; se instala con `pip install -r requirements.txt`)

## Limitaciones conocidas
- El motor no analiza todos los caminos posibles de una historia al cargarla; por ejemplo, no detecta finales inalcanzables. Los bloqueos se informan durante la partida.

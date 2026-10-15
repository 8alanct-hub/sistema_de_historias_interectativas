"""Configuración común de las pruebas.

Agrega la carpeta src/ al camino de importación y ofrece datos de prueba
reutilizables (fixtures).
"""

import copy
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from cargador import cargar_historia  # noqa: E402
from motor import Partida  # noqa: E402

RUTA_HISTORIA = RAIZ / "data" / "la_ultima_transmision.json"
RUTA_SEGUNDA_HISTORIA = RAIZ / "data" / "segunda_historia.json"


@pytest.fixture
def datos_historia():
    """Contenido del JSON de la historia principal, como diccionario."""
    with open(RUTA_HISTORIA, encoding="utf-8") as archivo:
        return json.load(archivo)


@pytest.fixture
def partida():
    """Una partida nueva de la historia principal."""
    return Partida(cargar_historia(RUTA_HISTORIA))


@pytest.fixture
def escribir_historia(tmp_path):
    """Escribe una historia (diccionario) en un archivo temporal y devuelve su ruta."""

    def _escribir(datos):
        ruta = tmp_path / "historia.json"
        ruta.write_text(json.dumps(copy.deepcopy(datos)), encoding="utf-8")
        return ruta

    return _escribir

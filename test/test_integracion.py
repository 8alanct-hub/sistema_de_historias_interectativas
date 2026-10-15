"""Prueba de integración I1: archivo real + cargador + motor, hasta llegar a un final."""

import pytest

from cargador import cargar_historia
from conftest import RUTA_HISTORIA, RUTA_SEGUNDA_HISTORIA
from motor import Partida


# I1. La lectura de un archivo real y el motor funcionan juntos hasta alcanzar un final.
@pytest.mark.parametrize(
    "elecciones, final_esperado",
    [
        (["1", "1", "1"], "E4"),   # revisar → investigar → activar con código
        (["1", "2", "1"], "E5"),   # revisar → continuar → activar sin verificar
        (["1", "2", "2"], "E6"),   # revisar → continuar → cortar
    ],
    ids=["final_E4_rescate", "final_E5_eco", "final_E6_silencio"],
)
def test_i1_recorrido_completo_hasta_cada_final(elecciones, final_esperado):
    partida = Partida(cargar_historia(RUTA_HISTORIA))

    for entrada in elecciones:
        assert partida.elegir_por_numero(entrada) is True

    assert partida.escena_actual.id == final_esperado
    assert partida.en_escena_final()


def test_i1_segunda_historia_funciona_con_el_mismo_motor():
    partida = Partida(cargar_historia(RUTA_SEGUNDA_HISTORIA))

    assert partida.elegir_opcion("O1") is True   # hablar con EVA → ia_autonoma
    assert [o.id for o in partida.opciones_disponibles()] == ["O1", "O2", "O3"]
    assert partida.elegir_opcion("O1") is True   # permitir que EVA estudie
    assert partida.escena_actual.id == "S5"
    assert partida.en_escena_final()


def test_i1_segunda_historia_condicion_no_cumplida():
    partida = Partida(cargar_historia(RUTA_SEGUNDA_HISTORIA))

    partida.elegir_opcion("O3")   # revisar registros sin hablar con EVA

    assert [o.id for o in partida.opciones_disponibles()] == ["O2", "O3"]

"""Pruebas unitarias del cargador: U4 y cobertura de validación.

Cada error de contenido debe rechazar el archivo antes de crear una partida,
con un mensaje que indique la causa y el campo o ID involucrado (RF11, RF12, RNF01).
"""

import pytest

from cargador import cargar_historia
from modelo import ErrorDeContenido


def quitar(clave):
    return lambda d: d.pop(clave)


def poner(ruta, valor):
    """Devuelve una función que cambia un valor dentro del diccionario de la historia."""

    def _modificar(datos):
        destino = datos
        for paso in ruta[:-1]:
            destino = destino[paso]
        destino[ruta[-1]] = valor

    return _modificar


VARIANTES_INVALIDAS = [
    # (nombre, modificación, fragmento esperado en el mensaje)
    ("falta_titulo", quitar("titulo"), "'titulo'"),
    ("falta_escenas", quitar("escenas"), "'escenas'"),
    ("falta_campo_en_opcion", lambda d: d["escenas"][0]["opciones"][0].pop("destino"), "'destino'"),
    ("estructura_incorrecta", poner(["escenas"], "no es una lista"), "'escenas'"),
    ("inicio_inexistente", poner(["inicio"], "E0"), "'E0'"),
    ("escena_duplicada", poner(["escenas", 1, "id"], "E1"), "'E1'"),
    ("opcion_duplicada", poner(["escenas", 1, "opciones", 1, "id"], "investigar"), "'investigar'"),
    ("destino_inexistente_CA03", poner(["escenas", 0, "opciones", 0, "destino"], "E99"), "'E99'"),
    ("variable_no_declarada", poner(["escenas", 1, "opciones", 0, "efectos"], {"xx": True}), "'xx'"),
    ("valor_no_booleano_efecto", poner(["escenas", 1, "opciones", 0, "efectos"], {"conoce_origen": "si"}), "'conoce_origen'"),
    ("valor_no_booleano_inicial", poner(["variables", "conoce_origen"], 0), "'conoce_origen'"),
    ("final_con_opciones", lambda d: d["escenas"][3].__setitem__("opciones", list(d["escenas"][0]["opciones"])), "'E4'"),
    ("no_final_sin_opciones", poner(["escenas", 0, "opciones"], []), "'E1'"),
]


# U4. Los errores de contenido obligatorios producen un rechazo controlado.
@pytest.mark.parametrize(
    "modificar, fragmento",
    [(v[1], v[2]) for v in VARIANTES_INVALIDAS],
    ids=[v[0] for v in VARIANTES_INVALIDAS],
)
def test_u4_contenido_invalido_se_rechaza_con_mensaje_claro(datos_historia, escribir_historia, modificar, fragmento):
    modificar(datos_historia)
    ruta = escribir_historia(datos_historia)

    with pytest.raises(ErrorDeContenido) as error:
        cargar_historia(ruta)

    mensaje = str(error.value)
    assert fragmento in mensaje
    assert "Traceback" not in mensaje


def test_u4_archivo_ilegible(tmp_path):
    ruta = tmp_path / "roto.json"
    ruta.write_text("{ esto no es json", encoding="utf-8")

    with pytest.raises(ErrorDeContenido) as error:
        cargar_historia(ruta)

    assert "no es un JSON válido" in str(error.value)


def test_u4_archivo_inexistente(tmp_path):
    with pytest.raises(ErrorDeContenido) as error:
        cargar_historia(tmp_path / "no_existe.json")

    assert "No se encontró el archivo" in str(error.value)


def test_u4_archivo_que_no_es_un_objeto(tmp_path):
    ruta = tmp_path / "lista.json"
    ruta.write_text("[1, 2, 3]", encoding="utf-8")

    with pytest.raises(ErrorDeContenido) as error:
        cargar_historia(ruta)

    assert "estructura del archivo es incorrecta" in str(error.value)


def test_historia_valida_se_carga(datos_historia, escribir_historia):
    historia = cargar_historia(escribir_historia(datos_historia))

    assert historia.titulo == "La última transmisión"
    assert len(historia.escenas) == 6

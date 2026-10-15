"""Pruebas unitarias del motor (clase Partida): U1, U2, U3, U5 y bloqueo."""

import pytest

from cargador import cargar_historia
from motor import Partida


def ids(opciones):
    return [opcion.id for opcion in opciones]


def llevar_a_e3(partida, investigar):
    """Lleva la partida desde E1 hasta E3, investigando o no el archivo."""
    partida.elegir_opcion("revisar")
    partida.elegir_opcion("investigar" if investigar else "continuar")


# U1. Las condiciones cumplidas y no cumplidas habilitan únicamente las opciones correspondientes.
@pytest.mark.parametrize(
    "investigar, esperadas",
    [
        (True, ["activar_codigo", "cortar"]),
        (False, ["activar_sin_verificar", "cortar"]),
    ],
)
def test_u1_condiciones_habilitan_solo_las_opciones_correspondientes(partida, investigar, esperadas):
    llevar_a_e3(partida, investigar)

    assert partida.escena_actual.id == "E3"
    assert ids(partida.opciones_disponibles()) == esperadas


def test_u1_opcion_sin_condiciones_siempre_disponible(partida):
    assert ids(partida.opciones_disponibles()) == ["revisar"]


# U2. Una elección válida aplica los efectos y avanza al destino correcto.
def test_u2_eleccion_valida_aplica_efectos_y_avanza(partida):
    partida.elegir_opcion("revisar")

    resultado = partida.elegir_opcion("investigar")

    assert resultado is True
    assert partida.escena_actual.id == "E3"
    assert partida.variables == {"conoce_origen": True, "confia_en_la_voz": False}


def test_u2_eleccion_por_numero_valida(partida):
    resultado = partida.elegir_por_numero("1")

    assert resultado is True
    assert partida.escena_actual.id == "E2"


# U3. Una opción inexistente o no habilitada deja intacto el estado.
@pytest.mark.parametrize(
    "id_opcion",
    ["activar_codigo", "no_existe", "revisar"],
    ids=["no_habilitada_CA02", "inexistente", "de_otra_escena"],
)
def test_u3_opcion_invalida_por_id_deja_el_estado_intacto(partida, id_opcion):
    llevar_a_e3(partida, investigar=False)
    variables_antes = dict(partida.variables)

    resultado = partida.elegir_opcion(id_opcion)

    assert resultado is False
    assert partida.escena_actual.id == "E3"
    assert partida.variables == variables_antes


@pytest.mark.parametrize(
    "entrada",
    ["hola", "", "   ", "3", "-1", "1.5", "99"],
    ids=["texto", "vacia", "espacios", "fuera_de_rango", "negativo", "decimal", "muy_grande"],
)
def test_u3_entrada_invalida_por_numero_deja_el_estado_intacto(partida, entrada):
    llevar_a_e3(partida, investigar=False)
    variables_antes = dict(partida.variables)

    resultado = partida.elegir_por_numero(entrada)

    assert resultado is False
    assert partida.escena_actual.id == "E3"
    assert partida.variables == variables_antes


def test_u3_cero_sin_retroceso_disponible_es_invalido(partida):
    """Desde la solicitud de cambio, el 0 significa deshacer; sin nada que deshacer es inválido."""
    resultado = partida.elegir_por_numero("0")

    assert resultado is False
    assert partida.escena_actual.id == "E1"
    assert partida.variables == {"conoce_origen": False, "confia_en_la_voz": False}


# U5. Reiniciar restaura la escena y las variables iniciales.
def test_u5_reiniciar_restaura_escena_y_variables(partida):
    llevar_a_e3(partida, investigar=True)
    partida.elegir_opcion("activar_codigo")
    assert partida.en_escena_final()

    partida.reiniciar()

    assert partida.escena_actual.id == "E1"
    assert partida.variables == {"conoce_origen": False, "confia_en_la_voz": False}
    assert not partida.en_escena_final()


def test_u5_reiniciar_elimina_el_historial(partida):
    llevar_a_e3(partida, investigar=True)
    partida.elegir_opcion("activar_codigo")
    assert partida.puede_deshacer()

    partida.reiniciar()

    assert not partida.puede_deshacer()
    assert partida.deshacer() is False
    assert partida.escena_actual.id == "E1"


def test_u5_reiniciar_no_modifica_las_variables_iniciales_de_la_historia(partida):
    partida.elegir_opcion("revisar")
    partida.elegir_opcion("investigar")
    partida.reiniciar()

    assert partida.historia.variables_iniciales == {"conoce_origen": False, "confia_en_la_voz": False}


# Finales y bloqueo (RF09, RF13).
def test_escena_final_no_tiene_opciones_disponibles(partida):
    llevar_a_e3(partida, investigar=False)
    partida.elegir_opcion("cortar")

    assert partida.en_escena_final()
    assert partida.opciones_disponibles() == []
    assert not partida.sin_opciones_disponibles()


def test_bloqueo_escena_no_final_sin_opciones_habilitadas(escribir_historia):
    datos = {
        "titulo": "Historia con bloqueo",
        "inicio": "A",
        "variables": {"llave": False},
        "escenas": [
            {"id": "A", "texto": "Inicio", "final": False, "opciones": [
                {"id": "ir", "texto": "Ir a la puerta", "destino": "B",
                 "condiciones": {}, "efectos": {}}]},
            {"id": "B", "texto": "Una puerta cerrada", "final": False, "opciones": [
                {"id": "abrir", "texto": "Abrir", "destino": "C",
                 "condiciones": {"llave": True}, "efectos": {}}]},
            {"id": "C", "texto": "Final", "final": True, "opciones": []},
        ],
    }
    partida = Partida(cargar_historia(escribir_historia(datos)))

    partida.elegir_opcion("ir")

    assert partida.escena_actual.id == "B"
    assert partida.sin_opciones_disponibles()
    assert not partida.en_escena_final()

    partida.reiniciar()
    assert partida.escena_actual.id == "A"


# U6. Deshacer restaura escena y variables y consume la posibilidad de retroceder (solicitud de cambio).
def test_u6_deshacer_restaura_escena_y_variables(partida):
    partida.elegir_opcion("revisar")
    partida.elegir_opcion("investigar")
    assert partida.escena_actual.id == "E3"
    assert partida.variables["conoce_origen"] is True

    resultado = partida.deshacer()

    assert resultado is True
    assert partida.escena_actual.id == "E2"
    assert partida.variables == {"conoce_origen": False, "confia_en_la_voz": False}


def test_u6_deshacer_consume_el_retroceso(partida):
    partida.elegir_opcion("revisar")
    partida.elegir_opcion("investigar")
    partida.deshacer()

    segundo_intento = partida.deshacer()

    assert segundo_intento is False
    assert partida.escena_actual.id == "E2"
    assert partida.variables["conoce_origen"] is False


def test_u6_ejemplo_de_la_solicitud_de_cambio(partida):
    """Desde E2: investigar, deshacer, deshacer otra vez y continuar sin investigar."""
    partida.elegir_opcion("revisar")
    partida.elegir_opcion("investigar")
    partida.deshacer()
    partida.deshacer()

    partida.elegir_opcion("continuar")

    assert partida.escena_actual.id == "E3"
    assert ids(partida.opciones_disponibles()) == ["activar_sin_verificar", "cortar"]


def test_u6_al_iniciar_no_hay_retroceso(partida):
    assert not partida.puede_deshacer()
    assert partida.deshacer() is False
    assert partida.escena_actual.id == "E1"


@pytest.mark.parametrize(
    "entrada_invalida",
    ["hola", "", "9", "-1"],
    ids=["texto", "vacia", "fuera_de_rango", "negativo"],
)
def test_u6_entrada_invalida_preserva_el_historial(partida, entrada_invalida):
    partida.elegir_opcion("revisar")
    partida.elegir_opcion("investigar")

    assert partida.elegir_por_numero(entrada_invalida) is False
    assert partida.deshacer() is True
    assert partida.escena_actual.id == "E2"


@pytest.mark.parametrize(
    "id_invalido",
    ["no_existe", "activar_sin_verificar"],
    ids=["inexistente", "no_habilitada"],
)
def test_u6_opcion_invalida_por_id_preserva_el_historial(partida, id_invalido):
    partida.elegir_opcion("revisar")
    partida.elegir_opcion("investigar")

    assert partida.elegir_opcion(id_invalido) is False
    assert partida.deshacer() is True
    assert partida.escena_actual.id == "E2"


def test_u6_nueva_eleccion_vuelve_a_habilitar_el_retroceso(partida):
    partida.elegir_opcion("revisar")
    partida.elegir_opcion("investigar")
    partida.deshacer()
    assert not partida.puede_deshacer()

    partida.elegir_opcion("continuar")

    assert partida.puede_deshacer()
    assert partida.deshacer() is True
    assert partida.escena_actual.id == "E2"


def test_u6_deshacer_con_el_numero_cero(partida):
    partida.elegir_por_numero("1")
    assert partida.escena_actual.id == "E2"

    assert partida.elegir_por_numero("0") is True
    assert partida.escena_actual.id == "E1"
    assert partida.elegir_por_numero("0") is False

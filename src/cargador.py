"""Carga de historias: lee el archivo JSON, valida su contenido y crea los objetos del modelo.

Si el archivo tiene cualquier error, se lanza ErrorDeContenido con un mensaje en
español que indica la causa y el campo o ID involucrado (RF11, RF12, RNF01).
La partida no se crea hasta que el archivo es válido.
"""

import json

from modelo import ErrorDeContenido, EscenaFinal, EscenaIntermedia, Historia, Opcion


CAMPOS_HISTORIA = {"titulo": str, "inicio": str, "variables": dict, "escenas": list}
CAMPOS_ESCENA = {"id": str, "texto": str, "final": bool, "opciones": list}
CAMPOS_OPCION = {
    "id": str,
    "texto": str,
    "destino": str,
    "condiciones": dict,
    "efectos": dict,
}

NOMBRES_TIPO = {str: "texto", bool: "verdadero/falso", dict: "objeto", list: "lista"}


def cargar_historia(ruta):
    """Lee el archivo de la ruta indicada y devuelve una Historia validada."""
    datos = _leer_json(ruta)
    _validar_campos(datos, CAMPOS_HISTORIA, "la historia")

    variables = datos["variables"]
    _validar_variables_iniciales(variables)

    escenas = {}
    for posicion, datos_escena in enumerate(datos["escenas"], start=1):
        escena = _crear_escena(datos_escena, posicion, variables)
        if escena.id in escenas:
            raise ErrorDeContenido(
                f"El ID de escena '{escena.id}' está repetido. "
                f"Cada escena debe tener un ID único."
            )
        escenas[escena.id] = escena

    if len(escenas) == 0:
        raise ErrorDeContenido("La historia no tiene escenas.")

    if datos["inicio"] not in escenas:
        raise ErrorDeContenido(
            f"El campo 'inicio' indica la escena '{datos['inicio']}', "
            f"pero esa escena no existe."
        )

    _validar_destinos(escenas)

    return Historia(datos["titulo"], datos["inicio"], dict(variables), escenas)


def _leer_json(ruta):
    """Abre el archivo y lo interpreta como JSON."""
    try:
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        raise ErrorDeContenido(f"No se encontró el archivo '{ruta}'.")
    except json.JSONDecodeError as error:
        raise ErrorDeContenido(
            f"El archivo '{ruta}' no es un JSON válido "
            f"(línea {error.lineno}, columna {error.colno})."
        )
    except (OSError, UnicodeDecodeError):
        raise ErrorDeContenido(f"No se pudo leer el archivo '{ruta}'.")

    if not isinstance(datos, dict):
        raise ErrorDeContenido(
            "La estructura del archivo es incorrecta: "
            "debe ser un objeto con 'titulo', 'inicio', 'variables' y 'escenas'."
        )
    return datos


def _validar_campos(datos, campos, donde):
    """Comprueba que estén todos los campos obligatorios y con el tipo correcto."""
    if not isinstance(datos, dict):
        raise ErrorDeContenido(f"La estructura de {donde} es incorrecta: debe ser un objeto.")
    for campo, tipo in campos.items():
        if campo not in datos:
            raise ErrorDeContenido(f"Falta el campo obligatorio '{campo}' en {donde}.")
        if not isinstance(datos[campo], tipo):
            raise ErrorDeContenido(
                f"El campo '{campo}' en {donde} debe ser de tipo {NOMBRES_TIPO[tipo]}."
            )


def _validar_variables_iniciales(variables):
    """Las variables iniciales deben tener valores booleanos."""
    for nombre, valor in variables.items():
        if not isinstance(valor, bool):
            raise ErrorDeContenido(
                f"La variable '{nombre}' tiene un valor que no es booleano: {valor!r}. "
                f"Use true o false."
            )


def _crear_escena(datos_escena, posicion, variables):
    """Valida los datos de una escena y crea la escena con sus opciones."""
    _validar_campos(datos_escena, CAMPOS_ESCENA, f"la escena número {posicion}")
    id_escena = datos_escena["id"]

    opciones = []
    ids_opciones = set()
    for datos_opcion in datos_escena["opciones"]:
        opcion = _crear_opcion(datos_opcion, id_escena, variables)
        if opcion.id in ids_opciones:
            raise ErrorDeContenido(
                f"El ID de opción '{opcion.id}' está repetido en la escena '{id_escena}'. "
                f"Cada opción debe tener un ID único dentro de su escena."
            )
        ids_opciones.add(opcion.id)
        opciones.append(opcion)

    # La cantidad de opciones se valida al crear cada tipo de escena (ver modelo.py).
    if datos_escena["final"]:
        return EscenaFinal(id_escena, datos_escena["texto"], opciones)
    return EscenaIntermedia(id_escena, datos_escena["texto"], opciones)


def _crear_opcion(datos_opcion, id_escena, variables):
    """Valida los datos de una opción y crea la opción."""
    _validar_campos(datos_opcion, CAMPOS_OPCION, f"una opción de la escena '{id_escena}'")
    id_opcion = datos_opcion["id"]

    for tipo_mapa in ("condiciones", "efectos"):
        for nombre, valor in datos_opcion[tipo_mapa].items():
            if nombre not in variables:
                raise ErrorDeContenido(
                    f"La opción '{id_opcion}' de la escena '{id_escena}' usa la variable "
                    f"'{nombre}' en sus {tipo_mapa}, pero esa variable no está declarada."
                )
            if not isinstance(valor, bool):
                raise ErrorDeContenido(
                    f"La opción '{id_opcion}' de la escena '{id_escena}' asigna a "
                    f"'{nombre}' en sus {tipo_mapa} un valor que no es booleano: {valor!r}. "
                    f"Use true o false."
                )

    return Opcion(
        id_opcion,
        datos_opcion["texto"],
        datos_opcion["destino"],
        dict(datos_opcion["condiciones"]),
        dict(datos_opcion["efectos"]),
    )


def _validar_destinos(escenas):
    """Cada opción debe llevar a una escena que exista."""
    for escena in escenas.values():
        for opcion in escena.opciones:
            if opcion.destino not in escenas:
                raise ErrorDeContenido(
                    f"La opción '{opcion.id}' de la escena '{escena.id}' lleva a la "
                    f"escena '{opcion.destino}', que no existe."
                )

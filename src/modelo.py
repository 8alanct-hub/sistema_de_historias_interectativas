"""Modelo de la historia: Historia, Escena, EscenaIntermedia, EscenaFinal y Opcion.

Estas clases representan la estructura fija de una historia. Se crean una vez,
al cargar el archivo, y no cambian mientras se juega.
"""


class ErrorDeContenido(Exception):
    """Error en el contenido de una historia.

    El mensaje siempre indica la causa y el campo o ID involucrado (RF12, RNF01).
    """


class Opcion:
    """Una opción que el lector puede elegir dentro de una escena."""

    def __init__(self, id, texto, destino, condiciones, efectos):
        self.id = id
        self.texto = texto
        self.destino = destino            # id de la escena a la que lleva
        self.condiciones = condiciones    # dict: variable -> valor requerido
        self.efectos = efectos            # dict: variable -> valor que asigna

    def esta_habilitada(self, variables):
        """Devuelve True si se cumplen todas las condiciones.

        Una opción sin condiciones siempre está habilitada.
        """
        for nombre, valor_requerido in self.condiciones.items():
            if variables.get(nombre) != valor_requerido:
                return False
        return True


class Escena:
    """Datos comunes a toda escena."""

    def __init__(self, id, texto):
        self.id = id
        self.texto = texto


class EscenaIntermedia(Escena):
    """Escena no final: ofrece una o más opciones."""

    def __init__(self, id, texto, opciones):
        super().__init__(id, texto)
        if len(opciones) == 0:
            raise ErrorDeContenido(
                f"La escena '{id}' no es final, pero no tiene opciones. "
                f"Una escena no final debe tener al menos una opción."
            )
        self.opciones = opciones


class EscenaFinal(Escena):
    """Escena final: no tiene opciones."""

    def __init__(self, id, texto, opciones=None):
        super().__init__(id, texto)
        if opciones:
            raise ErrorDeContenido(
                f"La escena '{id}' es final, pero tiene {len(opciones)} opción(es). "
                f"Una escena final no debe tener opciones."
            )
        self.opciones = []


class Historia:
    """Una historia completa, tal como se cargó desde el archivo."""

    def __init__(self, titulo, inicio, variables_iniciales, escenas):
        self.titulo = titulo
        self.inicio = inicio                              # id de la escena inicial
        self.variables_iniciales = variables_iniciales    # dict: variable -> bool
        self.escenas = escenas                            # dict: id -> Escena

    def obtener_escena(self, id_escena):
        """Devuelve la escena con ese id."""
        return self.escenas[id_escena]

"""Motor: la Partida en curso (escena actual, variables y reglas del juego).

La Partida no conoce la consola ni los archivos: recibe una Historia ya validada
y valida por sí misma todo lo que le envían (RF07, CA02).
"""

from modelo import EscenaFinal


class Partida:
    """Una partida de una historia: dónde está el lector y qué ha ocurrido."""

    def __init__(self, historia):
        self.historia = historia
        self.escena_actual = None
        self.variables = {}
        self.respaldo = None   # (escena, variables) antes de la última elección válida
        self.reiniciar()

    def reiniciar(self):
        """Vuelve a la escena de inicio con las variables iniciales (RF02, RF10).

        Se copian las variables para no conservar nada de la partida anterior.
        """
        self.escena_actual = self.historia.obtener_escena(self.historia.inicio)
        self.variables = dict(self.historia.variables_iniciales)
        self.respaldo = None   # al iniciar o reiniciar no hay nada que deshacer (RF17)

    def opciones_disponibles(self):
        """Devuelve las opciones de la escena actual cuyas condiciones se cumplen (RF04)."""
        return [
            opcion
            for opcion in self.escena_actual.opciones
            if opcion.esta_habilitada(self.variables)
        ]

    def elegir_por_numero(self, entrada):
        """Elige una opción a partir de lo que escribió el lector (supuesto 3).

        La entrada debe ser el número con el que aparece la opción entre las
        disponibles (1, 2, 3...), o 0 para deshacer la última decisión (supuesto 4).
        Si no es válida, devuelve False y la partida no cambia.
        """
        texto = str(entrada).strip()
        if not texto.isdigit():
            return False

        numero = int(texto)
        if numero == 0:
            return self.deshacer()

        disponibles = self.opciones_disponibles()
        if numero < 1 or numero > len(disponibles):
            return False

        return self.elegir_opcion(disponibles[numero - 1].id)

    def elegir_opcion(self, id_opcion):
        """Elige una opción por su id, aplica sus efectos y avanza (RF05, RF06).

        Si la opción no existe en la escena actual o no está habilitada,
        devuelve False y la partida no cambia (RF07, CA02).
        """
        for opcion in self.escena_actual.opciones:
            if opcion.id == id_opcion:
                if not opcion.esta_habilitada(self.variables):
                    return False
                # Se guarda el estado anterior solo cuando la elección es válida (RF18).
                self.respaldo = (self.escena_actual, dict(self.variables))
                self.variables.update(opcion.efectos)
                self.escena_actual = self.historia.obtener_escena(opcion.destino)
                return True
        return False

    def puede_deshacer(self):
        """Indica si hay una decisión que se pueda deshacer (RF16, RF17)."""
        return self.respaldo is not None

    def deshacer(self):
        """Restaura la escena y las variables de antes de la última elección válida (RF14, RF15).

        Solo hay un nivel de retroceso: después de deshacer no se puede volver a
        deshacer hasta hacer una nueva elección válida (RF16). Si no hay nada que
        deshacer, devuelve False y la partida no cambia.
        """
        if not self.puede_deshacer():
            return False
        escena_anterior, variables_anteriores = self.respaldo
        self.escena_actual = escena_anterior
        self.variables = dict(variables_anteriores)
        self.respaldo = None
        return True

    def en_escena_final(self):
        """Indica si la partida llegó a una escena final (RF09)."""
        return isinstance(self.escena_actual, EscenaFinal)

    def sin_opciones_disponibles(self):
        """Indica si la escena actual no es final y no tiene opciones habilitadas (RF13)."""
        return not self.en_escena_final() and len(self.opciones_disponibles()) == 0

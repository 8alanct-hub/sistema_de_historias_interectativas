"""Interfaz de consola: muestra escenas, opciones y avisos, y pasa a la partida lo que escribe el lector.

Uso:
    python src/main.py                              (carga la historia principal)
    python src/main.py data/segunda_historia.json   (carga otra historia)
"""

import os
import sys

from cargador import cargar_historia
from modelo import ErrorDeContenido
from motor import Partida


HISTORIA_POR_DEFECTO = "data/la_ultima_transmision.json"
SEPARADOR = "-" * 60


def limpiar_pantalla():
    """Limpia la consola para que solo se vea la escena actual.

    Solo se limpia cuando el programa se usa en una consola real, para no
    afectar las pruebas ni la salida redirigida a un archivo.
    """
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def mostrar_escena(partida):
    limpiar_pantalla()
    print(f"=== {partida.historia.titulo} ===")
    print()
    print(SEPARADOR)
    print(partida.escena_actual.texto)
    print(SEPARADOR)


def mostrar_opciones(partida):
    for numero, opcion in enumerate(partida.opciones_disponibles(), start=1):
        print(f"  {numero}. {opcion.texto}")


def ofrecer_nueva_partida(partida):
    """Después de un final o un bloqueo, espera a que el lector pida una nueva partida (RF10)."""
    while True:
        entrada = input("\nEscribe 1 para comenzar una nueva partida: ")
        if entrada.strip() == "1":
            partida.reiniciar()
            return
        print("Entrada no válida. Escribe 1 para comenzar una nueva partida.")


def jugar(partida):
    while True:
        mostrar_escena(partida)

        if partida.en_escena_final():
            print("\n*** FIN DE LA HISTORIA ***")
            ofrecer_nueva_partida(partida)
            continue

        if partida.sin_opciones_disponibles():
            print("\nNo hay opciones disponibles en esta escena; la historia no puede continuar.")
            ofrecer_nueva_partida(partida)
            continue

        mostrar_opciones(partida)
        while True:
            entrada = input("\nElige una opción: ")
            if partida.elegir_por_numero(entrada):
                break
            print("Entrada no válida. Escribe el número de una de las opciones.")
            mostrar_opciones(partida)


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else HISTORIA_POR_DEFECTO

    try:
        historia = cargar_historia(ruta)
    except ErrorDeContenido as error:
        print(f"No se pudo cargar la historia.\n{error}")
        sys.exit(1)

    try:
        jugar(Partida(historia))
    except (KeyboardInterrupt, EOFError):
        print("\n\nPartida terminada. ¡Hasta pronto!")
    except Exception:
        print("\nOcurrió un error inesperado y la partida no puede continuar.")
        sys.exit(1)


if __name__ == "__main__":
    main()

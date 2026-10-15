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

# Interruptor de la limpieza de la consola. Se puso en False solo para tomar las
# capturas de la verificación de los RNF, así se veía todo el recorrido en una
# sola captura. En uso normal queda en True.
LIMPIAR_PANTALLA = True


def limpiar_pantalla():
    """Limpia la consola para que solo se vea la escena actual.

    Solo se limpia cuando el programa se usa en una consola real, para no
    afectar las pruebas ni la salida redirigida a un archivo.
    """
    if LIMPIAR_PANTALLA and sys.stdout.isatty():
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
    mostrar_opcion_deshacer(partida)


def mostrar_opcion_deshacer(partida):
    """Muestra la opción 0 solo cuando hay una decisión que se pueda deshacer (supuesto 4)."""
    if partida.puede_deshacer():
        print("  0. Deshacer la última decisión")


def ofrecer_nueva_partida(partida):
    """Después de un final o un bloqueo, ofrece una nueva partida (RF10) o deshacer (RF15)."""
    while True:
        print("\n  1. Comenzar una nueva partida")
        mostrar_opcion_deshacer(partida)
        entrada = input("\nElige una opción: ")
        if entrada.strip() == "1":
            partida.reiniciar()
            return
        # En un final no hay opciones numeradas: la partida solo acepta el 0 para deshacer.
        if partida.elegir_por_numero(entrada):
            return
        print("Entrada no válida. Escribe el número de una de las opciones.")


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

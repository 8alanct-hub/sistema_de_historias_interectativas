"""Genera el README.md uniendo docs/readme_base.md con los documentos 01 a 10.

Uso (desde la carpeta del proyecto):
    python herramientas/generar_readme.py

Los documentos de docs/ son la fuente: se corrigen allí y luego se vuelve a
generar el README. Las rutas de las imágenes se ajustan para que los
diagramas también se vean desde el README, y cada documento queda dentro de
una sección desplegable (<details>) para que el README no sea tan largo.
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"
DOCUMENTOS = [
    "01_fundamentos.md",
    "02_proceso.md",
    "03_agilidad.md",
    "04_requisitos.md",
    "05_modelado.md",
    "06_arquitectura.md",
    "07_implementacion.md",
    "08_cambio.md",
    "09_trazabilidad.md",
    "10_aportes.md",
]


def ajustar_documento(texto):
    # Las rutas relativas a docs/ pasan a ser relativas a la raíz del proyecto.
    texto = re.sub(r"\]\((diagramas|images)/", r"](docs/\1/", texto)
    texto = re.sub(r"`(diagramas|images)/", r"`docs/\1/", texto)
    # Cada título baja un nivel para quedar dentro de "Documentación".
    return re.sub(r"^(#+) ", r"#\1 ", texto, flags=re.MULTILINE)


def como_desplegable(texto):
    """Pone el documento dentro de una sección desplegable con su título como resumen."""
    primera_linea, _, cuerpo = texto.partition("\n")
    titulo = primera_linea.lstrip("#").strip()
    return (
        f"<details>\n<summary><b>{titulo}</b></summary>\n\n"
        f"{ajustar_documento(cuerpo.strip())}\n\n</details>\n"
    )


def main():
    partes = [(DOCS / "readme_base.md").read_text(encoding="utf-8").rstrip()]
    partes.append("\n\n---\n\n# Documentación\n")
    partes.append(
        "Contenido de `docs/01_fundamentos.md` a `docs/10_aportes.md`. "
        "Haga clic en cada título para desplegarlo. "
        "Las fuentes y herramientas de apoyo están en `docs/fuentes.md`.\n"
    )
    for nombre in DOCUMENTOS:
        texto = (DOCS / nombre).read_text(encoding="utf-8").rstrip()
        partes.append("\n" + como_desplegable(texto))
    (RAIZ / "README.md").write_text("\n".join(partes) + "\n", encoding="utf-8")
    print("README.md generado.")


if __name__ == "__main__":
    main()

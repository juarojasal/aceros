import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


RUTA_DATOS_REACCIONES = Path(__file__).with_name("datos_reacciones.json")
RUTA_DIAGRAMA_CORTANTE = Path(__file__).with_name("diagrama_cortante_nervio1.png")
RUTA_DIAGRAMA_MOMENTO = Path(__file__).with_name("diagrama_momento_nervio1.png")


def cargar_datos_reacciones(ruta=RUTA_DATOS_REACCIONES):
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontro {ruta.name}. Ejecuta primero reacciones.py para generar los datos."
        )

    datos = json.loads(ruta.read_text(encoding="utf-8"))
    return datos["reaccionesseparadas"], datos["momentosI"], datos["momentosF"]


def calcular_tramos_cortante(reacciones, cargas):
    longitudes = (8, 3, 5)
    posiciones = (0, 8, 11, 16)

    r1 = reacciones["ra1"]
    r2 = reacciones["rb1"] + reacciones["ra2"]
    r3 = reacciones["rb2"] + reacciones["ra3"]
    r4 = reacciones["rb3"]

    w1 = cargas["oficinas1"]
    w2 = cargas["corredores"]
    w3 = cargas["oficinas2"]

    tramo1_cortante = lambda x: r1 - w1 * (x - posiciones[0])

    x1 = np.linspace(posiciones[0], posiciones[1], 300)
    y1 = tramo1_cortante(x1)

    tramo2_cortante = lambda x: y1[-1] + r2 - w2 * (x - posiciones[1])
    x2 = np.linspace(posiciones[1], posiciones[2], 300)
    y2 = tramo2_cortante(x2)

    tramo3_cortante = lambda x: y2[-1] + r3 - w3 * (x - posiciones[2])
    x3 = np.linspace(posiciones[2], posiciones[3], 300)
    y3 = tramo3_cortante(x3)

    saltos = [
        (posiciones[1], y1[-1], y1[-1] + r2),
        (posiciones[2], y2[-1], y2[-1] + r3),
        (posiciones[3], y3[-1], y3[-1] + r4),
    ]

    return {
        "longitudes": longitudes,
        "posiciones": posiciones,
        "reacciones_totales": (r1, r2, r3, r4),
        "cargas": (w1, w2, w3),
        "tramos": ((x1, y1), (x2, y2), (x3, y3)),
        "saltos": saltos,
    }


def graficar_diagrama_cortante(datos_cortante, ruta_salida=RUTA_DIAGRAMA_CORTANTE):
    fig, ax = plt.subplots(figsize=(10, 5.5), constrained_layout=True)

    color_linea = "#1b7f6b"
    color_relleno = "#8ecdb9"

    for x, y in datos_cortante["tramos"]:
        ax.plot(x, y, color=color_linea, linewidth=2)
        ax.fill_between(x, y, 0, color=color_relleno, alpha=0.45)

    for x, y_inicial, y_final in datos_cortante["saltos"]:
        ax.plot([x, x], [y_inicial, y_final], color=color_linea, linewidth=2)

    ax.axhline(0, color="gray", linewidth=1, linestyle="--", alpha=0.7)

    posiciones = datos_cortante["posiciones"]
    ax.set_xticks(posiciones)
    ax.set_xlim(posiciones[0] - 0.5, posiciones[-1] + 0.5)

    todos_y = np.concatenate([y for _, y in datos_cortante["tramos"]])
    margen_y = max(3, 0.15 * (todos_y.max() - todos_y.min()))
    ax.set_ylim(todos_y.min() - margen_y, todos_y.max() + margen_y)

    ax.set_title("Diagrama de fuerza cortante - franja 1", fontsize=13, fontweight="bold")
    ax.set_xlabel("Longitud x (m)")
    ax.set_ylabel("Cortante V (kN)")
    ax.grid(True, alpha=0.25)

    puntos_etiqueta = []
    for x, y in datos_cortante["tramos"]:
        puntos_etiqueta.append((x[0], y[0]))
        puntos_etiqueta.append((x[-1], y[-1]))
    for x, _, y_final in datos_cortante["saltos"]:
        puntos_etiqueta.append((x, y_final))

    for x, y in puntos_etiqueta:
        if abs(y) < 0.05:
            continue
        desplazamiento = 0.8 if y >= 0 else -1.2
        ax.text(
            x,
            y + desplazamiento,
            f"{y:.2f}",
            color=color_linea,
            fontsize=8,
            ha="center",
            va="bottom" if y >= 0 else "top",
        )

    fig.savefig(ruta_salida, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return ruta_salida


def calcular_tramos_momento(reacciones, cargas, momentos):
    posiciones = (0, 8, 11, 16)

    ra1 = reacciones["ra1"]
    ra2 = reacciones["ra2"]
    ra3 = reacciones["ra3"]

    w1 = cargas["oficinas1"]
    w2 = cargas["corredores"]
    w3 = cargas["oficinas2"]

    momento_8 = momentos["momento0"]
    momento_11 = momentos["momento1"]

    tramo1_momento = lambda x: ra1 * (x - posiciones[0]) - w1 * (x - posiciones[0]) ** 2 / 2
    x1 = np.linspace(posiciones[0], posiciones[1], 300)
    y1 = tramo1_momento(x1)

    tramo2_momento = lambda x: momento_8 + ra2 * (x - posiciones[1]) - w2 * (x - posiciones[1]) ** 2 / 2
    x2 = np.linspace(posiciones[1], posiciones[2], 300)
    y2 = tramo2_momento(x2)

    tramo3_momento = lambda x: momento_11 + ra3 * (x - posiciones[2]) - w3 * (x - posiciones[2]) ** 2 / 2
    x3 = np.linspace(posiciones[2], posiciones[3], 300)
    y3 = tramo3_momento(x3)

    puntos_clave = [
        (posiciones[0], float(y1[0])),
        (posiciones[1], float(y1[-1])),
        (posiciones[2], float(y2[-1])),
        (posiciones[3], float(y3[-1])),
    ]

    extremos = [
        (posiciones[0] + ra1 / w1, tramo1_momento),
        (posiciones[1] + ra2 / w2, tramo2_momento),
        (posiciones[2] + ra3 / w3, tramo3_momento),
    ]
    for x_extremo, funcion in extremos:
        if posiciones[0] <= x_extremo <= posiciones[-1]:
            puntos_clave.append((x_extremo, float(funcion(x_extremo))))

    return {
        "posiciones": posiciones,
        "tramos": ((x1, y1), (x2, y2), (x3, y3)),
        "puntos_clave": puntos_clave,
    }


def graficar_diagrama_momento(datos_momento, ruta_salida=RUTA_DIAGRAMA_MOMENTO):
    fig, ax = plt.subplots(figsize=(10, 5.5), constrained_layout=True)

    color_linea = "#325f9f"
    color_relleno = "#9bbce8"

    for x, y in datos_momento["tramos"]:
        ax.plot(x, y, color=color_linea, linewidth=2)
        ax.fill_between(x, y, 0, color=color_relleno, alpha=0.45)

    ax.axhline(0, color="gray", linewidth=1, linestyle="--", alpha=0.7)

    posiciones = datos_momento["posiciones"]
    ax.set_xticks(posiciones)
    ax.set_xlim(posiciones[0] - 0.5, posiciones[-1] + 0.5)

    todos_y = np.concatenate([y for _, y in datos_momento["tramos"]])
    margen_y = max(3, 0.15 * (todos_y.max() - todos_y.min()))
    ax.set_ylim(todos_y.min() - margen_y, todos_y.max() + margen_y)

    ax.set_title("Diagrama de momento flector - franja 1", fontsize=13, fontweight="bold")
    ax.set_xlabel("Longitud x (m)")
    ax.set_ylabel("Momento M (kN.m)")
    ax.grid(True, alpha=0.25)

    etiquetas_vistas = set()
    for x, y in datos_momento["puntos_clave"]:
        clave = (round(x, 2), round(y, 2))
        if clave in etiquetas_vistas:
            continue
        etiquetas_vistas.add(clave)

        if abs(y) < 0.05:
            continue
        desplazamiento = 0.9 if y >= 0 else -1.2
        ax.text(
            x,
            y + desplazamiento,
            f"{y:.2f}",
            color=color_linea,
            fontsize=8,
            ha="center",
            va="bottom" if y >= 0 else "top",
        )

    fig.savefig(ruta_salida, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return ruta_salida


if __name__ == "__main__":
    reacciones, cargas, momentos = cargar_datos_reacciones()
    datos_cortante = calcular_tramos_cortante(reacciones, cargas)
    datos_momento = calcular_tramos_momento(reacciones, cargas, momentos)

    ruta_cortante = graficar_diagrama_cortante(datos_cortante)
    ruta_momento = graficar_diagrama_momento(datos_momento)

    print("Diagrama de cortante guardado en:", ruta_cortante)
    print("Diagrama de momento guardado en:", ruta_momento)

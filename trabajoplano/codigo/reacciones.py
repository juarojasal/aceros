import json
from pathlib import Path
import numpy as np


RUTA_DATOS_CARGAS = Path(__file__).with_name("datos_cargas.json")
RUTA_DATOS_REACCIONES = Path(__file__).with_name("datos_reacciones.json")


def cargar_cargas_para_reacciones(ruta=RUTA_DATOS_CARGAS):
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontro {ruta.name}. Ejecuta primero cargas.py para generar los datos."
        )

    datos = json.loads(ruta.read_text(encoding="utf-8"))
    resultados = datos["resultados"]

    return {
        "oficinas": resultados["carga_diseno_oficinas"],
        "corredores": resultados["carga_diseno_corredores"],
        "unidad": datos["unidades"]["cargas"],
    }


def imprimir_cargas_usadas(cargas):
    unidad = cargas["unidad"]
    print("Cargas disponibles para calculo de reacciones:")
    print("Oficinas:", cargas["oficinas"], unidad)
    print("Corredores:", cargas["corredores"], unidad)


def caso1(cargas):
    # Calculo de reacciones para la primera franja de losa de izquierda a derecha.
    l1 = 8
    l2 = 3
    l3 = 5

    oficinas1 = cargas["oficinas"] * 0.4
    oficinas2 = cargas["oficinas"] * 0.5
    corredores = cargas["corredores"] *0.6

    # Matriz de compatibilidad.
    nodo_a00 = 3 / l1 + 4 / l2
    nodo_a01 = 2 / l2
    nodo_a10 = 2 / l2
    nodo_a11 = 4 / l2 + 3 / l3
    matriz_a = np.zeros((2, 2))
    matriz_a[0, 0] = nodo_a00
    matriz_a[0, 1] = nodo_a01
    matriz_a[1, 0] = nodo_a10
    matriz_a[1, 1] = nodo_a11

    # Matriz de cargas externas.
    nodo_b0 = (16 * oficinas1 * l1**2) / 128 - (corredores * l2**2) / 12
    nodo_b1 = (corredores * l2**2) / 12 - (16 * oficinas2 * l3**2) / 128
    matriz_b = np.zeros((2, 1))
    matriz_b[0, 0] = nodo_b0
    matriz_b[1, 0] = nodo_b1

    # np.linalg.solve devuelve un arreglo. Se convierte a float para poder
    # operar y guardar los resultados en JSON sin errores.
    rotacion = np.linalg.solve(matriz_a, matriz_b)
    rotacion_1 = float(rotacion[0, 0])
    rotacion_2 = float(rotacion[1, 0])

    # Calculo de momentos.
    momento0 = 3 / l1 * rotacion_1 - (16 * oficinas1 * l1**2) / 128
    momento1 = -(3 / l3 * rotacion_2 + (16 * oficinas2 * l3**2) / 128)

    # Calculo de reacciones con momentos y sumatoria de fuerzas en Y.
    rb1 = (oficinas1 * l1 * l1 / 2 - momento0) / l1
    ra1 = -rb1 + oficinas1 * l1
    rb2 = (corredores * l2 * l2 / 2 + momento0 - momento1) / l2
    ra2 = -rb2 + corredores * l2
    rb3 = (oficinas2 * l3 * l3 / 2 + momento1) / l3
    ra3 = -rb3 + oficinas2 * l3

    r1 = ra1
    r2 = rb1 + ra2
    r3 = rb2 + ra3
    r4 = rb3

    return {
        "franja1": {
            "unidad": "kN",
            "R1": round(float(r1), 4),
            "R2": round(float(r2), 4),
            "R3": round(float(r3), 4),
            "R4": round(float(r4), 4),
        },
        "momentosI":{
            "unidad":"KNm",
            "oficinas1":oficinas1,
            "oficinas2":oficinas2,
            "corredores":corredores

        },
        "momentosF":{
            "unidad":"KNm",
            "momento0":momento0,
            "momento1":momento1
        },
        "reaccionesseparadas":{
            "unidad": "KN",
            "rb1":rb1,
            "ra1":ra1,
            "rb2":rb2,
            "ra2":ra2,
            "rb3":rb3,
            "ra3":ra3,
        }
    }


def guardar_datos(datos, ruta=RUTA_DATOS_REACCIONES):
    ruta.write_text(json.dumps(datos, indent=4), encoding="utf-8")


if __name__ == "__main__":
    cargas = cargar_cargas_para_reacciones()
    reacciones = caso1(cargas)
    guardar_datos(reacciones)

    franja1 = reacciones["franja1"]
    print("Reacciones para la franja hecha a mano:")
    print("Reaccion en el primer apoyo:", franja1["R1"], "kN")
    print("Reaccion en el segundo apoyo:", franja1["R2"], "kN")
    print("Reaccion en el tercer apoyo:", franja1["R3"], "kN")
    print("Reaccion en el cuarto apoyo:", franja1["R4"], "kN")
    print("Datos guardados en:", RUTA_DATOS_REACCIONES)

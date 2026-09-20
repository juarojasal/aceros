import json
from pathlib import Path
import math


RUTA_DATOS = Path(__file__).with_name("datos_cargas.json")


def calcular_cargas():
    c_particiones = 2  # kN/m2
    c_acabados = 1.8  # kN/m2
    c_instalaciones = 0.5  # kN/m2
    c_oficinas = 2  # kN/m2
    c_corredores = 3  # kN/m2
    h_losa = 0.05  # m
    peso_hormigon = 24  # kN/m3

    volumen_estandar = round(h_losa, 3)
    volumen_losa = volumen_estandar

    c_losa = round(volumen_estandar * peso_hormigon, 4)

    carga_total_oficinas = 1.2 * (c_particiones + c_acabados + c_instalaciones + c_losa) + 1.6 * c_oficinas
    carga_total_corredores = 1.2 * (c_particiones + c_acabados + c_instalaciones + c_losa) + 1.6 * c_corredores
    carga_diseno_oficinas = math.ceil(carga_total_oficinas)
    carga_diseno_corredores = math.ceil(carga_total_corredores)

    return {
        "unidades": {
            "cargas": "kN/m2",
            "volumen_losa": "m3/m2",
            "volumen_estandar": "m3/m2",
        },
        "datos_entrada": {
            "particiones": c_particiones,
            "acabados": c_acabados,
            "instalaciones": c_instalaciones,
            "oficinas": c_oficinas,
            "corredores": c_corredores,
            "altura_losa": h_losa,
            "peso_hormigon": peso_hormigon,
        },
        "resultados": {
            "volumen_losa": volumen_losa,
            "volumen_estandar": volumen_estandar,
            "carga_losa": c_losa,
            "carga_total_oficinas": round(carga_total_oficinas, 2),
            "carga_total_corredores": round(carga_total_corredores, 2),
            "carga_diseno_oficinas": carga_diseno_oficinas,
            "carga_diseno_corredores": carga_diseno_corredores,
        },
    }


def guardar_datos_cargas(datos, ruta=RUTA_DATOS):
    ruta.write_text(json.dumps(datos, indent=4), encoding="utf-8")


def imprimir_resumen(datos):
    resultados = datos["resultados"]
    print("Volumen de la losa:", resultados["volumen_losa"], "m3")
    print("Volumen estandar:", resultados["volumen_estandar"], "m3/m2")
    print("Carga de la losa:", resultados["carga_losa"], "kN/m2")
    print("Carga total oficinas:", resultados["carga_total_oficinas"], "kN/m2")
    print("Carga total corredores:", resultados["carga_total_corredores"], "kN/m2")
    print("Carga de diseno oficinas:", resultados["carga_diseno_oficinas"], "kN/m2")
    print("Carga de diseno corredores:", resultados["carga_diseno_corredores"], "kN/m2")
    print("Datos guardados en:", RUTA_DATOS)


if __name__ == "__main__":
    datos_cargas = calcular_cargas()
    guardar_datos_cargas(datos_cargas)
    imprimir_resumen(datos_cargas)

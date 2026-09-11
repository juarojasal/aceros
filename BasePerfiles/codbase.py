import json
from pathlib import Path

base_json = Path(__file__).with_name("base.json")

with open(base_json, "r", encoding="utf-8") as archivo:
    perfiles= json.load(archivo)

def graficar_secciones(perfiles_filtrados):
    if not perfiles_filtrados:
        print("No hay perfiles para graficar.")
        return

    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
    except ModuleNotFoundError:
        print("Para generar graficas instala matplotlib con: python -m pip install matplotlib")
        return

    columnas = min(2, len(perfiles_filtrados))
    filas = (len(perfiles_filtrados) + columnas - 1) // columnas
    fig, axes = plt.subplots(filas, columnas, figsize=(6 * columnas, 6 * filas), constrained_layout=True)

    if len(perfiles_filtrados) == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for posicion, perfil in enumerate(perfiles_filtrados):
        ax = axes[posicion]
        tipo = str(perfil["tipo"])
        altura = float(perfil["altura_in"])
        ancho_ala = float(perfil["longitud_ala_in"])
        espesor_alma = float(perfil["espesor_alma_in"])
        espesor_ala = float(perfil["espesor_ala_in"])

        if tipo == "I":
            ax.add_patch(Rectangle((-ancho_ala / 2, altura / 2 - espesor_ala), ancho_ala, espesor_ala))
            ax.add_patch(Rectangle((-espesor_alma / 2, -altura / 2), espesor_alma, altura))
            ax.add_patch(Rectangle((-ancho_ala / 2, -altura / 2), ancho_ala, espesor_ala))
        elif tipo == "T":
            ax.add_patch(Rectangle((-ancho_ala / 2, altura / 2 - espesor_ala), ancho_ala, espesor_ala))
            ax.add_patch(Rectangle((-espesor_alma / 2, -altura / 2), espesor_alma, altura - espesor_ala))
        else:
            ax.text(0, 0, f"No hay dibujo definido para tipo {tipo}", ha="center", va="center")

        margen = max(altura, ancho_ala) * 0.12
        ax.set_xlim(-ancho_ala / 2 - margen, ancho_ala / 2 + margen)
        ax.set_ylim(-altura / 2 - margen, altura / 2 + margen)
        ax.set_aspect("equal")
        ax.set_title(perfil["nombre"])
        ax.set_xlabel("ancho (in)")
        ax.set_ylabel("altura (in)")
        ax.grid(True, alpha=0.3)

    for posicion in range(len(perfiles_filtrados), len(axes)):
        axes[posicion].axis("off")

    plt.show()

def filtro(tipo,S):
    lista=[]
    if tipo == "I":
        for i in perfiles:
            if str(i["tipo"]) == "I" and float(i["s3_top_in3"]) >= S:
                lista.append(i)
        print(lista)
        graficar_secciones(lista)
        return lista
      
    elif tipo == "T":
        for i in perfiles:
            if str(i["tipo"]) == "T" and float(i["s3_top_in3"]) >= S:
                lista.append(i)
        print(lista)
        graficar_secciones(lista)
        return lista
    
    elif tipo =="L":
        for i in perfiles:
            if str(i["tipo"]) == "L" and float(i["s3_top_in3"]) >= S:
                lista.append(i)
        print(lista)
        graficar_secciones(lista)
        return lista

    elif tipo == "C":
        for i in perfiles:
            if str(i["tipo"]) == "C" and float(i["s3_top_in3"]) >= S:
                lista.append(i)
        print(lista)
        graficar_secciones(lista)
        return lista

    elif tipo == "S":
        for i in perfiles:
            if str(i["tipo"]) == "S" and float(i["s3_top_in3"]) >= S:
                lista.append(i)
        print(lista)
        graficar_secciones(lista)
        return lista
    
    elif tipo == "O":
        for i in perfiles:
            if str(i["tipo"]) == "O" and float(i["s3_top_in3"]) >= S:
                lista.append(i)
        print(lista)
        graficar_secciones(lista)
        return lista
    else:
        print("Tipo de perfil no válido. Por favor, elija entre I, T, L, C, S u O.")
        return None

def consulta():
    consulta=str(input("Qué desea hacer filtrar o añadir   "))
    if consulta == "filtrar":
          tipo=str(input("De qué tipo desea la sección, elija entre I, T, L, C, S u O       "))
          S_top=float(input("De cuanto debe ser el parametro de diseño S superior que debe tener la sección     "))
          filtro(tipo,S_top)
    #elif consulta== "añadir":
    else:
          print("Introduzca un comando valido filtrar o añadir")
          return
          

consulta()

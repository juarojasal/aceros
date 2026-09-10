import json
import pandas as pd
from pathlib import Path

base_json = Path(__file__).with_name("base.json")

with open(base_json, "r", encoding="utf-8") as archivo:
    perfiles= json.load(archivo)

def filtro(tipo,S):
    lista=[]
    if tipo == "I":
        for i in perfiles:
            if str(i["tipo"]) == "I" and float(i["s3_top_in3"]) >= S:
                lista.append(i)
        df=pd.DataFrame(lista)
        print(df)
        return None
      
    elif tipo == "T":
        for i in perfiles:
                    if str(i["tipo"]) == "T" and float(i["s3_top_in3"]) >= S:
                        lista.append(i)
        df=pd.DataFrame(lista)
        print(df)
        return None
    
    elif tipo =="L":
                for i in perfiles:
                    if str(i["tipo"]) == "L" and float(i["s3_top_in3"]) >= S:
                        lista.append(i)
                df=pd.DataFrame(lista)
                print(df)
                return None

    elif tipo == "C":
                for i in perfiles:
                    if str(i["tipo"]) == "C" and float(i["s3_top_in3"]) >= S:
                        lista.append(i)
                df=pd.DataFrame(lista)
                print(df)
                return None

    elif tipo == "S":
                for i in perfiles:
                    if str(i["tipo"]) == "S" and float(i["s3_top_in3"]) >= S:
                        lista.append(i)
                df=pd.DataFrame(lista)
                print(df)
                return None
    
    elif tipo == "O":
                for i in perfiles:
                    if str(i["tipo"]) == "O" and float(i["s3_top_in3"]) >= S:
                        lista.append(i)
                df=pd.DataFrame(lista)
                print(df)
                return None
    else:
        print("Tipo de perfil no válido. Por favor, elija entre I, T, L, C, S u O.")
        return None

filtro("Z", 200)





import os, json, requests


URL = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/main/"

def cargar_datos_API():
    try:
        respuest_ingr = requests.get(URL + "ingredientes.json")
        respuesta_menu = requests.get(URL + "menu.json")
        respuest_ingr.raise_for_status()
        respuesta_menu.raise_for_status()
        ingredientes = respuest_ingr.json()
        menu = respuesta_menu.json()
    except Exception as e:
        print(f"Error cargando ingredientes: {e}")
        return None, None
    return ingredientes, menu


def cargar_estatus_previo(archivos=["ingredientes_nuevos.json", "ventas.json"]):
    res = []
    for archivo in archivos:
        if not os.path.exists(archivo):
            print(f"ERROR: el archivo {archivo} no existe. Por favor intente de nuevo.")
            return None, None
        with open(archivo) as f:
            res.append(json.load(f))
    return res

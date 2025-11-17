import os, json, requests


URL = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/main/"


class ManejadorData:

    def cargar_datos_API(self):
        """
        Carga los datos de ingredientes y menú desde la API.
        
        Returns:
            tuple: (ingredientes, menu) o (None, None) en caso de error
        """
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
    
    
    def cargar_archivo(self, archivo):
        """
        Carga datos desde un archivo JSON local.
        
        Args:
            archivo (str): Ruta del archivo a cargar
            
        Returns:
            dict/list: Datos cargados del archivo, o None en caso de error
        """
        if not os.path.exists(archivo):
            print(f"ERROR: el archivo {archivo} no existe. Por favor intente de nuevo.")
            return None
        with open(archivo) as f:
            return json.load(f)
        return None

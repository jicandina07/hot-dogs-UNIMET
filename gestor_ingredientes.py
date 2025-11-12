from ingrediente import Ingrediente
from helpers import obtener_opcion_usuario

class GestorIngredientes:

    def __init__(self, catalogo, menu):
        self.catalogo = catalogo
        self.menu = menu
        self.categorias = [item["Categoria"].lower() for item in self.catalogo]

    def mostrar_menu(self):
        print("")
        print("--- Gestión de ingredientes de UNIMET Hot Dogs ---")
        print("Opciones disponibles:")
        print("1. Ver todo el catálogo de ingredientes.")
        print("2. Listar productos de una categoría.")
        print("3. Añadir un ingrediente.")
        print("4. Eliminar un ingrediente.")
        print("5. Salir del gestor.")

    def gestionar(self):
        while True:
            self.mostrar_menu()
            opcion = obtener_opcion_usuario([str(i) for i in range(1, 6)])
            if opcion == '1':
                print(self.catalogo)
            # Listar productos en una categoría
            if opcion == '2':
                categoria = obtener_opcion_usuario(self.categorias)
                self.obtener_categoria(categoria, mostrar=True)
                if categoria != "salsa":
                    print("¿Desea listar productos de un tipo en esta categoría? (s/n)")
                    opcion2 = obtener_opcion_usuario(['s', 'n'])
                    if opcion2 == 's':
                        self.obtener_tipo_en_categoria(categoria, mostrar=True)
            # Agregar un ingrediente
            elif opcion == '3':
                agregado = self.agregar_ingrediente()
                if not agregado:
                    print("No se agregó ningún ingrediente nuevo.")
            # Eliminar un ingrediente
            elif opcion == '4':
                eliminado = self.eliminar_ingrediente()
                if not eliminado:
                    print("No se eliminó ningún ingrediente.")
            # Salir del gestor
            elif opcion == '5':
                print("Gestor de ingredientes terminado exitosamente.")
                break

    def obtener_categoria(self, categoria, mostrar=False):
        items = self.catalogo[self.categorias.index(categoria)]
        res = [item["nombre"] for item in items["Opciones"]]
        if mostrar:
            print("")
            print(res)
            print("")
        return res

    def obtener_tipo_en_categoria(self, categoria, mostrar=False):
        tipos_posibles, res = [], []
        indice_cat = self.categorias.index(categoria)
        # Primero obtener los tipos posibles en esta categoría
        for item in self.catalogo[indice_cat]["Opciones"]:
            if not item["tipo"] in tipos_posibles:
                tipos_posibles.append(item["tipo"])
        # Obtener el tipo deseado por el usuario
        tipo = obtener_opcion_usuario(tipos_posibles)
        # Luego obtener los ingredientes del tipo seleccionado
        for item in self.catalogo[indice_cat]["Opciones"]:
            if item["tipo"] == tipo:
                res.append(item["nombre"])
        if mostrar:
            print("")
            print(res)
            print("")
        return res

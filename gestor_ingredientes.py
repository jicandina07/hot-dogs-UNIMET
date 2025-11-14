import json
from datetime import date
from helpers import obtener_opcion_usuario

class GestorIngredientes:

    def __init__(self, catalogo):
        self.catalogo = catalogo
        self.menu = None
        self.categorias = [item["Categoria"].lower() for item in self.catalogo]
    
    def asignar_menu(self, menu):
        self.menu = menu

    def mostrar_menu_principal(self):
        print("")
        print("--- Gestión de ingredientes de UNIMET Hot Dogs ---")
        print("Opciones disponibles:")
        print("1. Ver todo el catálogo de ingredientes.")
        print("2. Listar productos de una categoría.")
        print("3. Añadir un ingrediente.")
        print("4. Eliminar un ingrediente.")
        print("5. Guardar el catálogo de ingredientes.")
        print("6. Salir del gestor de ingredientes.")

    def visualizar_todos(self):
        for i, categoria in enumerate(self.categorias):
            print("")
            print(f"----- {categoria.capitalize()} -----")
            for k, item in enumerate(self.catalogo[i]["Opciones"]):
                print(f"{k + 1}. " + item["nombre"])

    def gestionar(self):
        while True:
            # Actualizar categorías por si se añadió una nueva
            self.categorias = [item["Categoria"].lower() for item in self.catalogo]
            # Mostrar menú principal y pedir input del usuario
            self.mostrar_menu_principal()
            opcion = obtener_opcion_usuario([str(i) for i in range(1, 7)])
            # Mostrar todos los ingredientes
            if opcion == '1':
                self.visualizar_todos()
            # Mostrar productos en una categoría
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
                cat = input("Ingrese la categoría del ingrediente: ").lower()
                nombre = input("Ingrese el nombre del ingrediente: ")
                tipo = input("Ingrese el tipo del ingrediente: ")
                unidad = input("Ingrese la unidad de medida: ")
                while True:
                    try:
                        tamaño = float(input("Ingrese el tamaño del ingrediente: "))
                        if tamaño <= 0:
                            print("Por favor ingrese un número positivo para el tamaño.")
                            continue
                        break            
                    except ValueError:
                        print("Por favor ingrese un número para el tamaño.")
                if not self.agregar_ingrediente(cat, nombre, tipo, tamaño, unidad):
                    print("")
                    print("No se agregó ningún ingrediente nuevo.")
            # Eliminar un ingrediente
            elif opcion == '4':
                print("Ingrese la categoría del ingrediente a eliminar")
                categoria = obtener_opcion_usuario(self.categorias)
                print("Ingrese el nombre del ingrediente a eliminar")
                nombres = [ingr["nombre"] for ingr in self.catalogo[self.categorias.index(categoria)]["Opciones"]]
                nombre = obtener_opcion_usuario(nombres)
                if not self.eliminar_ingrediente(categoria, nombre):
                    print("")
                    print("No se eliminó ningún ingrediente.")
            # Guardar el catálogo de ingredientes
            elif opcion == '5':
                self.guardar_ingredientes()
            # Salir del gestor
            elif opcion == '6':
                print("Gestor de ingredientes cerrado exitosamente.")
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

    def agregar_ingrediente(self, cat, nombre, tipo, tamaño, unidad):
        nuevo_item = {
            "nombre": nombre,
            "tipo": tipo,
            "tamaño": tamaño,
            "unidad": unidad
        }
        # Revisar si es una categoría nueva
        if cat not in self.categorias:
            print("Parece que esa es una nueva categoría de ingrediente.")
            print("¿Desea continuar? (s/n): ")
            opcion = obtener_opcion_usuario(['s', 'n'])
            if opcion == 'n':
                return False
            self.catalogo.append({
                "Categoria": cat.capitalize(),
                "Opciones": [nuevo_item]
            })
            print(f"¡La categoría {cat.capitalize()} con el ingrediente {nombre} se añadieron exitosamente!")
        else:
            indice_cat = self.categorias.index(cat)
            for item in self.catalogo[indice_cat]["Opciones"]:
                if item == nuevo_item:
                    print("¡Ese ingrediente ya existe!")
                    return False
            self.catalogo[indice_cat]["Opciones"].append(nuevo_item)
            print(f"¡El ingrediente {nombre} se añadió exitosamente!")
        return True
    
    def eliminar_ingrediente(self, categoria, nombre):
        # Obtener el índice de la categoría
        indice_cat = self.categorias.index(categoria)
        for i, item in enumerate(self.catalogo[indice_cat]["Opciones"]):
            if nombre == item["nombre"]:
                indice_ingrediente = i
                usado_en = self.menu.obtener_hotdogs_con_ingrediente(categoria, nombre)
                if usado_en:
                    print("")
                    print(f"El ingrediente {nombre} se usa en  los hot dogs: {usado_en}")
                    print(f"Si lo elimina, también se eliminarán estos hot dogs del menú.")
                    print(f"¿Desea eliminar el ingrediente {nombre}? (s/n)")
                    if obtener_opcion_usuario(['s', 'n']) == 'n':
                        return False
                self.catalogo[indice_cat]["Opciones"].pop(indice_ingrediente)
                for hotdog in usado_en:
                    self.menu.eliminar_hotdog(hotdog, force=True)
                print(f"Se eliminaron el ingrediente {nombre} y los hotdogs {usado_en}.")
                return True
        print("No se encontró ese ingrediente en el catálogo.")
        return False
    
    def obtener_tamaño(self, categoria, nombre):
        for item in self.catalogo[self.categorias.index(categoria)]["Opciones"]:
            if item["nombre"] == nombre:
                return item["tamaño"]
        # Si no se encontró, retornar None
        return

    def guardar_ingredientes(self, output=""):
        if not output:
            fecha = date.today().strftime("%Y-%m-%d")
            output = f"ingredientes_{fecha}.json"
        with open(output, 'w') as f:
            json.dump(self.stock, f)

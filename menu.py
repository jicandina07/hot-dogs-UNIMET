from requests.exceptions import InvalidJSONError
from helpers import obtener_opcion_usuario, obtener_opciones_usuario


class Menu:

    def __init__(self, hotdogs):
        self.hotdogs = hotdogs
        self.gestor_ingredientes = None

    def asignar_gestor_ingredientes(self, gestor_ingredientes):
        self.gestor_ingredientes = gestor_ingredientes

    def asignar_inventario(self, inventario):
        self.inventario = inventario

    def mostrar_menu_principal(self):
        print("")
        print("--- Gestión del menú de hot dogs de UNIMET Hot Dogs ---")
        print("Opciones disponibles:")
        print("1. Ver todo el menú de hot dogs.")
        print("2. Ver si hay stock de ingredientes para un hot dog específico.")
        print("3. Añadir un hot dog nuevo.")
        print("4. Eliminar un hot dog.")
        print("5. Salir del gestor del menú.")

    def gestionar(self):
        while True:
            self.mostrar_menu_principal()
            opcion = obtener_opcion_usuario([str(i) for i in range(1, 6)])
            # Mostrar todos los hot dogs
            if opcion == '1':
                print("")
                print("----- Menú UNIMET Hot Dogs -----")
                for i, hotdog in enumerate(self.hotdogs):
                    print(f"{i + 1}. " + hotdog["nombre"])
                    print([f"{key}: {val}" for key, val in list(hotdog.items())[1:]])
                    print("")
                print("--------------------------------")
            # Revisar el stock de ingredientes para un hot dog
            if opcion == '2':
                hotdog = input("Por favor ingrese el nombre del hot dog: ").lower()
                for hd in self.hotdogs:
                    if hd["nombre"] == hotdog:
                        if self.validar_stock(hotdog):
                            print("")
                            print(f"¡Sí hay stock suficiente para un hot dog {hotdog}!")
                            break
                        else:
                            print("")
                            print(f"Lo sentimos, no hay stock suficiente para el hot dog {hotdog}.")
                            break
                else:
                    print("")
                    print(f"¡El hot dog {hotdog} no está en el menú!")
            # Agregar un hot dog nuevo
            elif opcion == '3':
                if not self.agregar_hotdog():
                    print("")
                    print("No se agregó ningún hot dog nuevo.")
            # Eliminar un hot dog
            elif opcion == '4':
                hotdog_elim = input("Ingrese el nombre del hot dog: ").lower()
                if not self.eliminar_hotdog(hotdog_elim):
                    print("")
                    print("No se eliminó ningún hot dog.")
            # Salir del gestor
            elif opcion == '5':
                print("Gestor del menú de hot dogs cerrado exitosamente.")
                break

    def agregar_hotdog(self):
        nombre = input("Ingrese el nombre del hot dog: ")
        categorias = [["pan", "salchicha"], ["toppings", "salsa", "acompañante"]]
        items = []
        for i in range(len(categorias)):
            for cat in categorias[i]:
                print("")
                print("-------------------------")
                print(f"Escogiendo {cat}...")
                # Pedir una o más opciones dependiendo de la categoría del ingrediente
                if i == 0:
                    item = obtener_opcion_usuario(self.gestor_ingredientes.obtener_categoria(cat))
                    # Revisar el stock
                    if not self.validar_stock(item):
                        print("")
                        print(f"Actualmente no hay stock suficiente de {item}.")
                        print(f"¿Desea continuar añadiendo el hot dog {nombre}? (s/n)")
                        if obtener_opcion_usuario(['s', 'n']) == 'n':
                            return False
                else:
                    if cat == "acompañante":
                        # Preguntar si desea añadir un acompañante
                        print("")
                        print("¿Desea añadir un acompañante a este hot dog (s/n)?")
                        if obtener_opcion_usuario(['s', 'n']) == 'n':
                            items.append('')
                            break
                    item = obtener_opciones_usuario(self.gestor_ingredientes.obtener_categoria(cat))
                    # Revisar el stock de cada ingrediente
                    for ingr in item:
                        if not self.inventario.revisar_stock(ingr):
                            print("")
                            print(f"Actualmente no hay stock suficiente de {ingr}.")
                            print(f"¿Desea continuar añadiendo el hot dog {nombre}? (s/n)")
                            if obtener_opcion_usuario(['s', 'n']) == 'n':
                                return False
                # Añadir el item a la lista
                items.append(item)
        # Validar la longitud del pan y la salchicha
        l_pan = self.gestor_ingredientes.obtener_tamaño("pan", items[0])
        l_salchicha = self.gestor_ingredientes.obtener_tamaño("salchicha", items[1])
        if not l_pan == l_salchicha:
            print("")
            print(f"Parece que el pan {items[0]} y la salchicha {items[1]} tienen tamaños distintos.")
            print(f"¿Desea continuar añadiendo el hot dog {nombre}? (s/n)")
            if obtener_opcion_usuario(['s', 'n']) == 'n':
                return False
        # Crear un nuevo diccionario con los datos dados
        hotdog_nuevo = {
            "nombre": nombre,
            "Pan": items[0],
            "Salchicha": items[1],
            "toppings": items[2],
            "salsas": items[3],
            "acompañante": items[4]
        }
        # Verificar si ya existe
        for hotdog in self.hotdogs:
            if hotdog_nuevo == hotdog:
                print("")
                print(f"¡El hot dog {nombre} ya existe!")
                return False
        self.hotdogs.append(hotdog_nuevo)
        print("")
        print(f"¡Se añadió el hot dog {nombre} exitosamente!")
        return True

    def eliminar_hotdog(self, hotdog_elim, force=False):
        for i, hotdog in enumerate(self.hotdogs):
            if hotdog_elim == hotdog["nombre"].lower():
              if not force and self.validar_stock(hotdog_elim):
                print(f"Actualmente hay stock suficiente para preparar un hot dog {hotdog_elim}.")
                print("¿Desea eliminar el hot dog? (s/n)")
                if obtener_opcion_usuario(['s', 'n']) == 'n':
                    return False
                self.hotdogs.pop(i)
                print(f"Se eliminó el hot dog {hotdog_elim} del menú.")
                return True
        print("")
        print("No se encontró ese hot dog en el catálogo.")
        return False

    def obtener_hotdogs_con_ingrediente(self, categoria, nombre_ingr):
        hotdogs_con_ingrediente = []
        if categoria == "salsa":
            categoria += 's'
        for hotdog in self.hotdogs:
            try:
                if nombre_ingr in hotdog[categoria.capitalize()]:
                    hotdogs_con_ingrediente.append(hotdog["nombre"])
            except KeyError:
                if nombre_ingr in hotdog[categoria.lower()]:
                    hotdogs_con_ingrediente.append(hotdog["nombre"])
        return hotdogs_con_ingrediente

    def validar_stock(self, hotdog):
        for hd in self.hotdogs:
            if hd["nombre"] == hotdog:
                for ingrediente in list(hd.values())[1:]:
                    if type(ingrediente) == list:
                        for item in ingrediente:
                            if not self.inventario.revisar_stock(item):
                                return False
                    else:
                        if not self.inventario.revisar_stock(ingrediente):
                            return False
        return True

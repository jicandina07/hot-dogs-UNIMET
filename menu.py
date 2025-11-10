from helpers import obtener_opcion_usuario, obtener_opciones_usuario


class Menu:

    def __init__(self, hotdogs):
        self.hotdogs = hotdogs
        self.gestor_ingredientes = None

    def asignar_gestor_ingredientes(self, gestor_ingredientes):
        self.gestor_ingredientes = gestor_ingredientes

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
                if self.revisar_stock(hotdog):
                    print(f"¡Sí hay stock suficiente para un hot dog {hotdog}!")
                else:
                    print(f"Lo sentimos, no hay stock suficiente para el hot dog {hotdog}.")
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

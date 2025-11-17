from data import ManejadorData
from gestor_ingredientes import GestorIngredientes
from menu import Menu
from inventario import Inventario
from simulador_ventas import SimuladorVentas
from helpers import obtener_opcion_usuario



class Main:
    def mostrar_menu_principal(self):
        """ Muestra el menú principal del programa. """
        print("")
        print("-------------------------------------------------")
        print("Opciones disponibles:")
        print("0. Cargar un estatus previo del programa.")
        print("1. Gestionar los ingredientes posibles.")
        print("2. Gestionar el inventario de ingredientes.")
        print("3. Gestionar el menú.")
        print("4. Simular un día de ventas.")
        print("5. Guardar el inventario actual de ingredientes.")
        print("6. Salir del programa.")
        print("-------------------------------------------------")
        print("")
    
    def main(self):
        """
        Función principal que inicializa el sistema y maneja el flujo principal.
        
        Carga los datos, inicializa los componentes y maneja el menú principal
        del sistema UNIMET Hot Dogs.
        """
        # Cargar los datos de la API e inicializar las clases
        manejador_data = ManejadorData()
        ingredientes, menu = manejador_data.cargar_datos_API()
        gestor_ingredientes, menu = GestorIngredientes(ingredientes), Menu(menu)
        # Asignar menú a gestor de ingredientes y vice versa
        gestor_ingredientes.asignar_menu(menu)
        menu.asignar_gestor_ingredientes(gestor_ingredientes)
        # Inventario y simulador
        inventario = Inventario(gestor_ingredientes, menu)
        inventario.generar_stock_aleatorio()
        # Asignar el inventario al menú
        gestor_ingredientes.asignar_inventario(inventario)
        menu.asignar_inventario(inventario)
        simulador = SimuladorVentas(gestor_ingredientes, inventario, menu)
        # Imprimir bienvenida y mostrar el menú principal
        print("¡Bienvenido a UNIMET Hot Dogs!")
        while True:
            self.mostrar_menu_principal()
            # Preguntar al usuario la acción a realizar
            opcion = obtener_opcion_usuario([str(i) for i in range(7)])
            # Cargar estatus previo del sistema
            if opcion == '0':
                print("")
                ingr_prev = input("Ingrese el nombre del archivo con los ingredientes: ")
                inventario_prev = input("Ingrese el nombre del archivo con el inventario: ")
                menu_prev = input("Ingrese el nombre del archivo con el menú de hot dogs: ")
                print("")
                ingr_prev = manejador_data.cargar_archivo(ingr_prev)
                inventario_prev = manejador_data.cargar_archivo(inventario_prev)
                menu_prev = manejador_data.cargar_archivo(menu_prev)
                if not ingr_prev or not inventario_prev or not menu_prev:
                    print("")
                    print("Error al cargar los datos suministrados.")
                    print("Continuando con los datos ya cargados...")
                    print("")
                else:
                    gestor_ingredientes.catalogo = ingr_prev
                    inventario.stock = inventario_prev
                    menu.hotdogs = menu_prev
                    print("")
                    print("¡Se cargaron los archivos exitosamente!")
            # Gestión de ingredientes
            if opcion == '1':
                gestor_ingredientes.gestionar()
            # Gestión de inventario
            elif opcion == '2':
                inventario.gestionar()
            # Gestión de menú
            elif opcion == '3':
                menu.gestionar()
            # Simulador de ventas
            elif opcion == '4':
                simulador.simular_dia()
                simulador.generar_reporte()
            # Guardar el inventario actual
            elif opcion == '5':
                archivo = input("Ingrese el nombre del archivo que desea para guardar el stock: ")
                inventario.guardar_stock(archivo)
            # Salir del programa
            elif opcion == '6':
                print("")
                print("Gracias por usar nuestro sistema. ¡Hasta pronto!")
                print("")
                break


if __name__ == "__main__":
    main = Main()
    main.main()

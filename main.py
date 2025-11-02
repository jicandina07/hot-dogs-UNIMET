from api import cargar_datos_API
from simulador import SimuladorVentas


def mostrar_menu_principal():
    print("Por favor selecciona una de las siguientes opciones: ")
    print("1. Gestionar los ingredientes posibles.")
    print("2. Gestionar el inventario de ingredientes.")
    print("3. Gestionar el menú.")
    print("4. Simular un día de ventas.")
    print("5. Salir")

def main():
    gestor_ingredientes, inventario, menu = cargar_datos_API()
    simulador = SimuladorVentas(gestor_ingredientes, inventario, menu)
    print("¡Bienvenido a UNIMET Hot Dogs!")
    while True:
        mostrar_menu_principal()
        # Preguntar al usuario la acción a realizar
        try:
            opcion = int(input("Ingresa tu opción: "))
        # Verificar que el input sea correcto
        except TypeError:
            print("Opción inválida. Por favor ingresa un número entre 1 y 5.")
        # Ejecutar la opción escogida
        if opcion == 1:
            gestor_ingredientes.gestionar()     
        elif opcion == 2:
            inventario.gestionar()
        elif opcion == 3:
            menu.gestionar()
        elif opcion == 4:
            simulador.simular_dia()
            simulador.generar_reporte()
        elif opcion == 5:
            print("Gracias por usar nuestro sistema. ¡Hasta pronto!")
            break
        else:
            print("Opción inválida. Por favor ingresa un número entre 1 y 5.")

if __name__ == "__main__":
    main()

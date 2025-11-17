import json
from helpers import *
from datetime import date
from random import randint


class Inventario:

    def __init__(self, gestor_ingredientes, menu):
        """
        Inicializa el inventario con los componentes del sistema.
        
        Args:
            gestor_ingredientes: Instancia del gestor de ingredientes
            menu: Instancia del menú
        """
        self.gestor_ingredientes = gestor_ingredientes
        self.menu = menu
    
    # Mostrar el stock de cada ingrediente
    def visualizar(self):
      """ Imprime el stock actual. """
      for ingrediente, cantidad in self.stock.items():
        print(f"Stock de {ingrediente}: {cantidad}")

    def mostrar_menu_principal(self):
        """ Muestra las opciones principales de la clase. """
        print("")
        print("--- Gestión de inventario de UNIMET Hot Dogs ---")
        print("Opciones disponibles:")
        print("1. Ver todo el inventario actual.")
        print("2. Buscar la existencia de un ingrediente específico.")
        print("3. Listar el stock de ingredientes de una categoría.")
        print("4. Actualizar el stock de un ingrediente.")
        print("5. Guardar el stock actual de ingredientes.")
        print("6. Salir del gestor de inventario.")

    def gestionar(self):
        """ Gestiona el menú principal del sistema de inventario. """
        while True:
            self.mostrar_menu_principal()
            opcion = obtener_opcion_usuario([str(i) for i in range(1, 7)])
            # Mostrar todo el inventario
            if opcion == '1':
                print("")
                print("----- Inventario UNIMET Hot Dogs -----")
                self.visualizar()
                print("--------------------------------")
            # Revisar el stock de un ingrediente
            if opcion == '2':
                ingrediente = input("Por favor ingrese el nombre del ingrediente: ")
                for ingr, cant in self.stock.items():
                    if ingr.lower() == ingrediente.lower():
                        print("")
                        print(f"Stock de {ingrediente}: {cant}")
                        break
                else:
                    print("")
                    print(f"¡El ingrediente {ingrediente} no está en el inventario!")
            # Agregar un hot dog nuevo
            elif opcion == '3':
                categoria = obtener_opcion_usuario(self.gestor_ingredientes.categorias)
                idx_cat = self.gestor_ingredientes.categorias.index(categoria)
                for ingr in self.gestor_ingredientes.catalogo[idx_cat]["Opciones"]:
                    print(f"Stock de {ingr['nombre']}: {self.stock[ingr['nombre']]}")
            # Actualizar stock de un ingrediente
            elif opcion == '4':
                ingrediente = obtener_opcion_usuario(list(self.stock.keys()))
                try:
                    cantidad = int(input(f"Ingrese el nuevo stock de {ingrediente}: "))
                    if cantidad < 0:
                        print("")
                        print("Ingrese un número no negativo.")
                        continue
                    self.stock[ingrediente] = cantidad
                    print("")
                    print(f"Se actualizó el stock de {ingrediente} a {cantidad}.")
                except ValueError:
                    print("")
                    print("Por favor ingrese un número entero.")
            # Guardar el stock actual
            elif opcion == '5':
                self.guardar_stock()
            # Salir del gestor
            elif opcion == '6':
                print("")
                print("Gestor de inventario cerrado exitosamente.")
                break

    # Verificar que haya stock disponible
    def revisar_stock(self, nombre_ingr):
        """
        Verifica si hay stock disponible de un ingrediente.
        
        Args:
            nombre_ingr (str): Nombre del ingrediente a verificar
            
        Retorna:
            bool: True si hay stock disponible, False en caso contrario
        """
        try:
            return self.stock[nombre_ingr] > 0
        except KeyError:
            return self.stock[nombre_ingr.capitalize()] > 0

    # Restar del stock una cantidad de un ingrediente
    def restar_stock(self, nombre_ingr, cantidad):
        """
        Resta una cantidad del stock de un ingrediente.
        
        Args:
            nombre_ingr (str): Nombre del ingrediente
            cantidad (int): Cantidad a restar
            
        Retorna:
            bool: True si se pudo restar, False en caso contrario
        """
        try:
          if self.stock[nombre_ingr] > 0:
            self.stock[nombre_ingr] -= 1
            return True
          else:
            print(f"No hay stock suficiente del ingrediente {nombre_ingr}")
            return False
        except KeyError:
          print(f"¡El ingrediente {nombre_ingr} no se encuentra en el inventario!")
          return False

    def guardar_stock(self, output=""):
        """
        Guarda el stock actual en un archivo JSON.
        
        Args:
            output (str): Nombre del archivo de salida. Si está vacío, 
                         genera uno automáticamente con la fecha.
        """
        # Generar un nombre del archivo con la fecha de hoy si no fue dado
        if not output:
            fecha = date.today().strftime("%Y-%m-%d")
            output = f"inventario_{fecha}.json"
        # Guardar los datos
        with open(output, 'w') as f:
            json.dump(self.stock, f)
        print("")
        print(f"Se guardó el inventario actual en el archivo {output}")

    # Generar un inventario al azar
    def generar_stock_aleatorio(self):
        """ Genera un stock aleatorio para todos los ingredientes. """
        self.stock = {}
        # Generar un número aleatorio de stock para cada ingrediente
        for item in self.gestor_ingredientes.catalogo:
            for ingrediente in item["Opciones"]:
                self.stock[ingrediente["nombre"]] = randint(0, 30)

    # Cargar estatus previo del código
    def cargar_stock_previo(self, archivo):
        """
        Carga un stock previo desde un archivo JSON.
        
        Args:
            archivo (str): Ruta del archivo a cargar
        """
        with open(archivo) as f:
            self.stock = json.load(f)

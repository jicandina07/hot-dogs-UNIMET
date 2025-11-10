from random import choice, randint


class SimuladorVentas:

    def __init__(self, gestor_ingredientes, inventario, menu):
        self.menu = menu
        self.inventario = inventario
        self.gestor_ingredientes = gestor_ingredientes
        # Número aleatorio de clientes
        self.n_clientes = randint(0, 200)
        # Número de clientes que cambiaron de opinión
        self.n_cambios = 0
        # Número de clientes que no compraron por falta de inventario
        self.n_fallos = 0
        # Diccionario para guardar las ventas y faltas de stock
        self.stats = {hotdog["nombre"]: {"ventas": 0, "fallos": 0} for hotdog in self.menu.hotdogs}
        # Set de ingredientes que causaron fallos
        self.ingredientes_fallo = set()
        # Acompañantes vendidos
        self.acomp_vendidos = set()

    def simular_dia(self):
        for i in range(self.n_clientes):
            # Número de hot dogs es aleatorio entre 0 y 5
            n_hotdogs = randint(0, 5)
            # Manejar el caso en que el cliente no compra
            if n_hotdogs == 0:
                self.n_cambios += 1
                print(f"El cliente {i} cambió de opinión.")
                continue
            # De lo contrario, tomar la orden
            orden_cliente = []
            for k in range(n_hotdogs):
                # Escoger un hot dog y acompañante aleatorio
                hotdog = choice(self.menu.hotdogs).copy()
                acomp_posibles = self.gestor_ingredientes.obtener_categoria("acompañante")
                hotdog["Acompañante"] = [choice(acomp_posibles + [''])]
                # Verificar disponibilidad de ingredientes para la orden
                falta = self.inventario.verificar_stock(hotdog)
                if falta:
                    print(f"El cliente {i} no pudo comprar {hotdog['nombre']} por falta de {falta}. Se marchó sin nada.")
                    self.n_fallos += 1
                    self.stats[hotdog["nombre"]]["fallos"] += 1
                    self.ingredientes_fallo.add(hotdog["nombre"])
                    break
                orden_cliente.append(hotdog)
            else:
                for hotdog_vendido in orden_cliente:
                    self.inventario.actualizar_stock(hotdog_vendido)
                    if hotdog_vendido["Acompañante"]:
                        self.acomp_vendidos.update(hotdog_vendido["Acompañante"])

    def generar_reporte(self):
        ventas_totales = sum([hotdog["ventas"] for hotdog in self.stats.values()])
        hotdog_mas_vendido = max(self.stats, key = lambda hotdog: self.stats[hotdog]["ventas"])
        print("")
        print("----------- Reporte de Ventas de UNIMET Hot Dogs -----------")
        print(f"Total de clientes: {self.n_clientes}")
        print(f"Clientes que cambiaron de opinión: {self.n_cambios}")
        print(f"Clientes que no pudieron comprar por falta de stock: {self.n_fallos}")
        print(f"Promedio de hot dogs por cliente: {ventas_totales / self.n_clientes}")
        print(f"Hot dog más vendido: {hotdog_mas_vendido}")
        print(f"Hot dogs que no tuvieron stock: {[hotdog for hotdog in self.stats.values() if hotdog["fallos"] > 0]}")
        print(f"Ingredientes que no tuvieron stock: {self.ingredientes_fallo}")
        print(f"Acompañantes vendidos: {self.acomp_vendidos}")            


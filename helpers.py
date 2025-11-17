def obtener_opcion_usuario(opciones):
    """
    Solicita al usuario que seleccione una opción de una lista.
    
    Args:
        opciones (list): Lista de opciones válidas
        
    Retorna:
        str: Opción seleccionada por el usuario
    """
    while True:
        print("")
        opcion = input(f"Por favor ingrese una opción de {opciones}: ")
        if opcion not in opciones:
            print("")
            print(f"Opción inválida. Por favor ingrese uno de: {opciones}")
            print("")
            continue
        break
    return opcion


def obtener_opciones_usuario(opciones):
    """
    Solicita al usuario que seleccione múltiples opciones de una lista.
    
    Args:
        opciones (list): Lista de opciones válidas
        
    Retorna:
        list: Lista de opciones seleccionadas por el usuario
    """
    res = []
    while True:
        # Preguntar si quiere seguir añadiendo si ya lo ha hecho
        if len(res) > 0:
            print("")
            print(f"¿Desea añadir más de estos items? (s/n)")
            if obtener_opcion_usuario(['s', 'n']) == 'n':
                break
        # Pedirle una opción de las opciones
        opcion = input(f"Por favor ingrese una opción de {opciones}: ")
        if opcion not in opciones:
            print("")
            print(f"Opción inválida. Por favor ingrese uno de: {opciones}")
            print("")
            continue
        # Advertir si ya se añadió previamente
        elif opcion in res:
            print("")
            print(f"¡El item {opcion} ya fue añadido previamente!")
            print("")
            continue
        else:
            res.append(opcion)
            print("")
            print(f"Se añadió {opcion} a la lista.")
            print("")
    return res

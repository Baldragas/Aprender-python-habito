def obtener_numero_con_intentos():
    """
    Solicita un entero y devuelve:
    (numero_ingresado, intentos_realizados)
    Si supera 3 intentos fallidos, devuelve (None, intentos).
    """
    intentos = 0
    while True:
        entrada = input("Introduce un número entero: ")
        try:
            numero = int(entrada)
            # ???: devuelve número y contador
            return numero, intentos
        except ValueError:
            print("⚠️  Entrada no válida. Intenta de nuevo.")
            intentos += 1
            if intentos > 3:
                # ???: devuelve None y contador
                return None, intentos

obtener_numero_con_intentos()
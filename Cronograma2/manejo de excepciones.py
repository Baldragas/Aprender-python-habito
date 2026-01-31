def convertir_a_int(cadena: str):
    """
    Intenta convertir *cadena* a entero.
    Devuelve (valor, ok):
        - valor: int convertido o None
        - ok:    True si la conversión tuvo éxito, False en caso contrario
    """
    try:
        valor = int(cadena)
        return valor, True
    except ValueError:
        return None, False
    except TypeError:
        return None, False

casos = [
    ("123", (123, True)),      # esperado
    ("xyz", (None, False)),    # esperado
    (None,  (None, False))     # esperado, explicado arriba
]

for entrada, esperado in casos:
    print(entrada, "->", convertir_a_int(entrada), "vs", esperado)
def libras_a_kg(libras):
    resultado = libras * 0.453592
    print(f"{libras} equivalen a {resultado:.2f} kg")
def ton_us_a_metrica(ton_us):
    resultado = ton_us * 0.907185
    print(f"\n[RESULTADO]: {ton_us} US Ton equivalen a {resultado:.2f} Toneladas Métricas.")


print("--- Conversor Técnico de Unidades Petroleras ---")
print("Este script convierte medidas de Unidades de Campo (Sistema Inglés)")
print("al Sistema Internacional (Métrico Decimal).")

menu = """
Seleccione la conversión deseada:
1. Masa
2. Volumen
3. Longitud
0. Salir
"""
while True:
    print(menu)
    seleccion = input("Escriba su selección: ")
    if seleccion == "0":
        print("Hasta luego...")
        break
    elif seleccion == "1":
        print("\n--- MENÚ DE MASA ---")
        print("1. Libras a Kilogramos ")
        print("2. Toneladas cortas a Toneladas Métricas")
        selctM = input("Seleccione el tipo de conversión: ")
        try:
            if selctM == "1" or "2":
                cifra = float(input("Introduzca la cifra numérica: "))
                if selctM == "1":
                    libras_a_kg(cifra)
                else:
                    ton_us_a_metrica(cifra)
            else:
                print("Opción de masa no válida.")
        except ValueError:
            print("\n¡ERROR!: Por favor introduce solo números (usa el punto para decimales).")

    elif seleccion == "2":
        print("1. Barriles a Litros")
        print("2. Galones a Litros")
        print("3. Barriles a Galones")
        selectV = input ("¿Qué tipo unidad de Volumen quiere converitir?: ")
    elif seleccion == "3":
        print("1. Pies a Metros (Profundidad)")
        print("2. Pulgadas a Milímetros (Diámetros)")
        print("3. Millas a Kilómetros (Logística)")
        selectL = input("¿Qué tipo unidad de Longitud quiere converitir?: ")
    else:
        print("Por favor introduzca un numero valido")

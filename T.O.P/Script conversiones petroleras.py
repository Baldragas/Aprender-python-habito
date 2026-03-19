print("si no saludas, no eres amable")
def libras_a_kg(libras):
    resultado = libras * 0.453592
    print(f"\n[RESULTADO]: {libras} lb equivalen a {resultado:.2f} kg")

def ton_us_a_metrica(ton_us):
    resultado = ton_us * 0.907185
    print(f"\n[RESULTADO]: {ton_us} US Ton equivalen a {resultado:.2f} Toneladas Métricas.")

def barriles_a_litros(bbl):
    resultado = bbl * 158.98
    print(f"\n[RESULTADO]: {bbl} bbl equivalen a {resultado:.2f} Litros.")

def gal_a_litros(galones):
    resultado = galones * 3.78541
    print(f"\n[RESULTADO]: {galones} gal equivalen a {resultado:.2f} Litros.")

def pies_a_metros(pies):
    resultado = pies * 0.3048
    print(f"\n[RESULTADO]: {pies} ft equivalen a {resultado:.2f} metros.")

def pulgadas_a_mm(pulgadas):
    resultado = pulgadas * 25.4
    print(f"\n[RESULTADO]: {pulgadas} in equivalen a {resultado:.2f} milímetros.")

def ppg_a_sg(ppg):
    resultado = ppg / 8.33
    print(f"\n[DENSIDAD]: {ppg} PPG equivalen a {resultado:.2f} SG (Gravedad Específica).")

def sg_a_ppg(sg):
    resultado = sg * 8.33
    print(f"\n[DENSIDAD]: {sg} SG equivalen a {resultado:.2f} PPG.")

def calcular_Ph(densidad, profundidad):
    resultado = 0.052 * densidad * profundidad
    print(f"\n[CÁLCULO TÉCNICO]:")
    print(f"Con un lodo de {densidad} ppg a {profundidad} ft de profundidad,")
    print(f"la Presión Hidrostática es de {resultado:.2f} PSI.")

# --- INICIO DEL PROGRAMA ---
print("--- Conversor Técnico de Unidades Petroleras ---")

menu_principal = """
Seleccione la categoría:
1. Masa
2. Volumen
3. Longitud
4. Densidad del Lodo
5. Presión Hidrostática
0. Salir
"""

while True:
    print(menu_principal)
    seleccion = input("Escriba su selección: ")

    if seleccion == "0":
        print("Hasta luego...")
        break

    elif seleccion == "1":
        print("\n--- MENÚ DE MASA ---")
        print("1. Libras a Kilogramos")
        print("2. Toneladas cortas a Toneladas Métricas")
        selctM = input("Seleccione: ")
        try:
            if selctM in ("1", "2"):
                cifra = float(input("Introduzca la cifra numérica: "))
                if selctM == "1":
                    libras_a_kg(cifra)
                else:
                    ton_us_a_metrica(cifra)
            else:
                print("Opción de masa no válida.")
        except ValueError:
            print("\n¡ERROR!: Por favor introduce solo números.")

    elif seleccion == "2":
        print("\n--- MENÚ DE VOLUMEN ---")
        print("1. Barriles a Litros")
        print("2. Galones a Litros")
        print("3. Barriles a Galones")
        selectV = input("Seleccione: ")
        try:
            if selectV in ("1", "2", "3"):
                cifra = float(input("Introduzca la cifra numérica: "))
                if selectV == "1":
                    barriles_a_litros(cifra)
                elif selectV == "2":
                    gal_a_litros(cifra)
                else:
                    print(f"\n[RESULTADO]: {cifra} bbl son {cifra * 42:.2f} galones.")
            else:
                print("Opción de volumen no válida.")
        except ValueError:
            print("\n¡ERROR!: Por favor introduce solo números.")

    elif seleccion == "3":
        print("\n--- MENÚ DE LONGITUD ---")
        print("1. Pies a Metros (Profundidad)")
        print("2. Pulgadas a Milímetros (Diámetros)")
        print("3. Millas a Kilómetros (Logística)")
        selectL = input("Seleccione: ")
        try:
            if selectL in ("1", "2", "3"):
                cifra = float(input("Introduzca la cifra numérica: "))
                if selectL == "1":
                    pies_a_metros(cifra)
                elif selectL == "2":
                    pulgadas_a_mm(cifra)
                else:
                    print(f"\n[RESULTADO]: {cifra} mi son {cifra * 1.60934:.2f} km.")
            else:
                print("Opción de longitud no válida.")
        except ValueError:
            print("\n¡ERROR!: Por favor introduce solo números.")
            
    elif seleccion == "4":
        print("\n--- Cálculo de densidad del lodo---")
        print("1. PPG a SG (Gravedad Específica)")
        print("2. SG a PPG")
        try:
            selectD = input("Seleccione: ")
            if selectD in ("1", "2"):
                cifra = float(input("Introduzca la cifra númerica: "))
                if selectD == "1":
                    ppg_a_sg(cifra)
                else:
                    sg_a_ppg(cifra)
            else:
                print("Opción válida, verifique su selección.")     
        except ValueError:
            print("\n¡ERROR!: Por favor introduce solo valores numéricos.")

    elif seleccion == "5":
        print("\n--- CÁLCULO DE PRESIÓN HIDROSTÁTICA ---")
        try:
            densidad = float(input("Ingrese la densidad del lodo (PPG): "))
            profundidad = float(input("Ingrese la profundidad vertical (TVD en pies): "))
            
            calcular_Ph(densidad, profundidad)
            
        except ValueError:
            print("\n¡ERROR!: Por favor introduce solo valores numéricos.")
    else:
        print("Por favor introduzca un número válido del menú.")
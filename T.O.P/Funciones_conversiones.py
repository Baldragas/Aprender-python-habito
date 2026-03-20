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

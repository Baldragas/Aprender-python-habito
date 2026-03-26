import entidades
def barra_vida(personaje, longitud=10):
    porcentaje = personaje.vida / personaje.vida_max
    relleno = int(porcentaje * longitud)
    vacio = longitud - relleno
    return f"[{'█' * relleno}{'░' * vacio}] {personaje.vida}/{personaje.vida_max}"

def mostrar_efectos(personaje):
    """Devuelve un string con los efectos activos del personaje."""
    if not personaje.efectos:
        return ""
    
    iconos = []
    for efecto in personaje.efectos:
        atributo = efecto['atributo']
        modificador = efecto['modificador']
        duracion = efecto['duracion']
        
        if atributo == 'fuerza':
            icono = '⚔️'
        elif atributo == 'defensa':
            icono = '🛡️'
        else:
            icono = '✨'  # genérico
        
        # Mostramos + o - según el modificador (positivo o negativo)
        signo = '+' if modificador > 0 else ''
        iconos.append(f"{icono}{signo}{modificador}({duracion})")
    
    return " " + " ".join(iconos)
    if not personaje.efectos:
        return ""
    iconos = []
    for e in personaje.efectos:
        if e["atributo"] == "fuerza":
            iconos.append(f"⚡+{e['modificador']}({e['duracion']})")
        # Podríamos añadir más tipos: defensa, veneno, etc.
    return " " + " ".join(iconos)

def combate(jugador, enemigo):
    print(f"\n=== Combate inicia: {jugador.nombre} vs {enemigo.nombre} ===")
    
    while jugador.esta_vivo() and enemigo.esta_vivo():
        jugador.procesar_efectos()
        print(f"Turno de {jugador.nombre} {barra_vida(jugador)}{mostrar_efectos(jugador)}")
        print(f"{enemigo.nombre} - {barra_vida(enemigo)}")
        print("Opciones:")
        print("1. Atacar")
        print("2. Usar item (ej. Poción de vida)")
        print("3. Huir (salir del combate)")
        eleccion = input("Elige (1/2/3): ").strip()
        
        if eleccion == '1':
            jugador.atacar(enemigo)
        elif eleccion == '2':
            item = input("Nombre del item a usar: ").strip()
            jugador.usar_item(item)
        elif eleccion == '3':
            print("¡Huyes del combate!")
            return "huida"
        else:
            print("Opción inválida. Turno perdido.")
            continue
        
        if not enemigo.esta_vivo():
            print(f"{enemigo.nombre} ha sido derrotado!")
            return "victoria"
        
        print(f"\nTurno de {enemigo.nombre}")
        enemigo.atacar(jugador)
        if not jugador.esta_vivo():
            print(f"{jugador.nombre} ha sido derrotado...")
            return "derrota"

    print("Combate terminado.")
    return "fin"
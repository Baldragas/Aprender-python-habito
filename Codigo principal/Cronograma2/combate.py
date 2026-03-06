import entidades

def combate(jugador, enemigo):
    print(f"\n=== Combate inicia: {jugador.nombre} vs {enemigo.nombre} ===")
    
    while jugador.esta_vivo() and enemigo.esta_vivo():
        jugador.procesar_efectos()
        print(f"\nTurno de {jugador.nombre} (Vida: {jugador._vida})")
        print(f"{enemigo.nombre} - Vida restante: {enemigo._vida}")
        print("Opciones:")
        print("1. Atacar")
        print("2. Usar item (ej. Poción de vida)")
        print("3. Huir (salir del combate)")
        eleccion = input("Elige (1/2/3): ").strip()
        
        if eleccion == '1':
            jugador.atacar(enemigo)
        elif eleccion == '2':
            item = input("Nombre del item a usar: ").strip()
            jugador.usar_item(item, 1)
        elif eleccion == '3':
            print("¡Huyes del combate!")
            break
        else:
            print("Opción inválida. Turno perdido.")
            continue
        
        if not enemigo.esta_vivo():
            print(f"{enemigo.nombre} ha sido derrotado!")
            break
        
        print(f"\nTurno de {enemigo.nombre}")
        enemigo.atacar(jugador)
        if not jugador.esta_vivo():
            print(f"{jugador.nombre} ha sido derrotado...")
            break
    
    print("Combate terminado.")
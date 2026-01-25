from entidades import Guerrero, Enemigo, Jefe, CLASES

def combate(jugador, enemigo):
    print(f"\n=== Combate inicia: {jugador.nombre} vs {enemigo.nombre} ===")
    
    while jugador.esta_vivo() and enemigo.esta_vivo():
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

def juego_principal():
    
    jugador = Guerrero("Conan", 120, 40)
    
    # Intenta cargar la partida. Si no existe, no pasa nada (imprimirá "No hay partida")
    # y Conan se quedará con sus stats originales.
    jugador.cargar_partida(CLASES)

    # NOTA: Si cargas partida, estos items se suman a lo que cargaste
    # o si no hay partida, empiezas con ellos. Está bien para aprender.
    jugador.añadir_al_inventario("Poción de vida", 5)
    jugador.añadir_al_inventario("Escudo", 3)
    
    goblin = Enemigo("Goblin", 50, 8, 30)
    dragon = Jefe("Dragón Ancianor", 200, 30)
    
    enemigos = [goblin, dragon]
    
    print("¡Bienvenido al RPG simple!")
    print("Enemigos disponibles:")
    for i, e in enumerate(enemigos):
        print(f"{i+1}. {e.nombre} (Vida: {e._vida}, Fuerza: {e.fuerza})")
    
    while True:
        if not enemigos:
            print("\n¡Victoria total! Has derrotado a todos los enemigos.")
            break
        
        eleccion = input("\nElige enemigo (número) o 's' para salir: ").strip()
        if eleccion.lower() == 's':
            print("¡Hasta la próxima aventura!")
            break
        
        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(enemigos):
                enemigo = enemigos[idx]
                combate(jugador, enemigo)
                if not enemigo.esta_vivo():
                    enemigos.pop(idx) 
                    # Guarda el progreso cada vez que ganas
                    jugador.guardar_partida()
            else:
                print("Número inválido.")
        except ValueError:
            print("Ingresa un número válido o 's' para salir.")
        
        print(f"\nEstado de {jugador.nombre}:")
        print(jugador)
        
        if not jugador.esta_vivo():
            print("GAME OVER - Partida no guardada.")
            break
        # Aquí quitamos el guardar_partida() para que solo guarde si ganas (línea 197)
        # o si tú quieres guardar manualmente antes de salir.

# Ejecuta el juego
juego_principal()
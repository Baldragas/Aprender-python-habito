# main.py
# Importamos las clases necesarias desde el archivo clases.py
from clases import Guerrero, Enemigo, Jefe

def combate(jugador, enemigo):
    print(f"\n=== Combate inicia: {jugador.nombre} vs {enemigo.nombre} ===")
    
    while jugador.esta_vivo() and enemigo.esta_vivo():
        print(f"\nTurno de {jugador.nombre} (Vida: {jugador._vida}/{jugador.vida_max})")
        print(f"{enemigo.nombre} - Vida: {enemigo._vida}/{enemigo.vida_max}")
        print("1. Atacar | 2. Usar item | 3. Huir")
        
        eleccion = input("Elige: ").strip()
        
        if eleccion == '1':
            jugador.atacar(enemigo)
        elif eleccion == '2':
            jugador.mostrar_inventario()
            item = input("Nombre del item a usar: ").strip()
            jugador.usar_item(item, 1)
        elif eleccion == '3':
            print("¡Huyes del combate!")
            return False 
        else:
            print("Opción inválida.")
            continue
        
        if not enemigo.esta_vivo():
            print(f"¡{enemigo.nombre} ha sido derrotado!")
            break
        
        print(f"\n>> Turno de {enemigo.nombre}")
        enemigo.atacar(jugador)
        if not jugador.esta_vivo():
            print(f"{jugador.nombre} ha caído en combate...")
            break
    
    print("Combate terminado.")
    return True

def juego_principal():
    jugador = Guerrero("Conan", 120, 40)
    
    # Intenta cargar partida, si falla da items iniciales
    if not jugador.cargar_partida():
        print("Iniciando inventario básico...")
        jugador.añadir_al_inventario("Poción de vida", 5)
        jugador.añadir_al_inventario("Escudo", 3)
    
    goblin = Enemigo("Goblin", 50, 8, 30)
    dragon = Jefe("Dragón Ancianor", 200, 30)
    
    enemigos = [goblin, dragon]
    
    print("\n¡Bienvenido al RPG!")
    
    while True:
        if not enemigos:
            print("\n¡Victoria total! Has derrotado a todos los enemigos.")
            break
        
        print("\nEnemigos disponibles:")
        for i, e in enumerate(enemigos):
            print(f"{i+1}. {e.nombre} (Vida: {e._vida})")
        
        eleccion = input("\nElige enemigo (número) o 's' para salir: ").strip()
        if eleccion.lower() == 's':
            jugador.guardar_partida()
            print("Partida guardada. ¡Hasta la próxima!")
            break
        
        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(enemigos):
                enemigo = enemigos[idx]
                resultado = combate(jugador, enemigo)
                
                if not enemigo.esta_vivo():
                    enemigos.pop(idx)
                    jugador.guardar_partida() 
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida.")
        
        if not jugador.esta_vivo():
            print("\nGAME OVER")
            break

if __name__ == "__main__":
    juego_principal()
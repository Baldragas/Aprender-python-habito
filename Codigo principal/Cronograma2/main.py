from entidades import Guerrero, Enemigo, Jefe, CLASES
from mapa import Habitacion, Mapa, conectar_mutua
from objetos import Item

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

def main():
    # 1. CONFIGURACIÓN DEL PERSONAJE
    jugador = Guerrero("Conan", 120, 40)
    jugador.cargar_partida(CLASES)
    jugador.añadir_al_inventario("Poción de vida", 5)

    # En main(), después de crear el jugador:
    pocion = Item.crear_pocion_menor()
    jugador.añadir_item_objeto(pocion, 2)

    # 2. CONFIGURACIÓN DEL MUNDO (Esto es lo que faltaba conectar)
    mapa_del_juego = Mapa()
    
    # Creamos al enemigo y lo metemos EN la habitación
    dragon = Jefe("Dragón Ancianor", 200, 30)
    goblin = Enemigo("Goblin de polvo", 40, 10, 5)
    goblin._vida = 8

    # Ejemplo de creación de sala con enemigo
    sala_inicio = Habitacion("Entrada", "Una cueva oscura.")
    sala_media = Habitacion("Cuarto abandonado","Un cuarto polvoriento y oscuro", enemigo=goblin)
    sala_boss = Habitacion("Altar", "El cubil del dragón.", enemigo=dragon)
    
    # Añadir objetos a las salas:
    sala_inicio.objetos.extend(["poción pequeña", "llave oxidada"])
    sala_media.objetos.append("espada rota")

    # Conectamos las salas y las añadimos al mapa
    conectar_mutua(sala_inicio, "norte", sala_media, "sur")
    conectar_mutua(sala_media, "este", sala_boss, "oeste")
    mapa_del_juego.agregar_habitacion(sala_inicio)
    mapa_del_juego.agregar_habitacion(sala_media)
    mapa_del_juego.agregar_habitacion(sala_boss)
    mapa_del_juego.habitacion_actual = sala_inicio

    # 3. BUCLE DE JUEGO (Exploración + Combate)
    jugando = True
    while jugando and jugador.esta_vivo():
        print(f"\n--- {mapa_del_juego.habitacion_actual.nombre} ---")
        print(mapa_del_juego.habitacion_actual.descripcion)

        accion = input("¿A dónde ir? (norte/sur/este/oeste/mapa/inventario/salir): ").lower()

        if accion == "salir":
            jugador.guardar_partida()
            break
        
        if accion == "inventario":
            if jugador.mostrar_inventario():
                while True:
                    usar = input("¿Quieres usar algo? (s/n)").lower().strip()
                    if usar in ("s", "si", "sí", "y", "yes"):
                        item = input("¿Qué item quieres usar?: ").strip()
                        jugador.usar_item(item, 1)
                        break
                    elif usar in ("n", "no", "salir"):
                        print("Volviendo al menú principal.")
                        break
                    else:
                        print("Respuesta no reconocida. Escribe 's' (sí) o 'n' (no).")
            continue

        if accion == "mapa":
            print(mapa_del_juego.dibujar_mapa_bonito())
            continue

        if mapa_del_juego.mover(accion):
            sala_actual = mapa_del_juego.habitacion_actual
            sala_actual.visitada = True
            
            # ¿Hay alguien aquí para pelear?
            if sala_actual.enemigo is not None:
                enemigo_presente = sala_actual.enemigo
                print(f"¡Un {enemigo_presente.nombre} aparece!")
                
                # LLAMADA AL COMBATE
                combate(jugador, enemigo_presente)
                
                if not enemigo_presente.esta_vivo():
                    # Si el enemigo muere, lo quitamos de la  para que no "reviva" al volver
                    sala_actual.enemigo = None 
                    jugador.guardar_partida()
                elif not jugador.esta_vivo():
                    print("Has caído en batalla...")
                    break
        else:
            print("No hay salida en esa dirección.")

    print("Fin de la aventura.")

if __name__ == "__main__":
    main()
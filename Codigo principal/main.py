from entidades import Guerrero, Enemigo, Jefe, CLASES
from mapa import Habitacion, Mapa

def combate(jugador, enemigo):
    # ... (Tu código de combate actual está perfecto, se queda igual) ...
    pass

def main():
    # 1. CONFIGURACIÓN DEL PERSONAJE
    jugador = Guerrero("Conan", 120, 40)
    jugador.cargar_partida(CLASES)
    jugador.añadir_al_inventario("Poción de vida", 5)

    # 2. CONFIGURACIÓN DEL MUNDO (Esto es lo que faltaba conectar)
    mapa_del_juego = Mapa()
    
    # Creamos al enemigo y lo metemos EN la habitación
    dragon = Jefe("Dragón Ancianor", 200, 30)
    goblin = Enemigo("Goblin de polvo", 20, 10, 5) 

    # Ejemplo de creación de sala con enemigo
    sala_inicio = Habitacion("Entrada", "Una cueva oscura.")
    sala_media = Habitacion("Cuarto abandonado","Un cuarto polvoriento y oscuro", enemigo=goblin)
    sala_boss = Habitacion("Altar", "El cubil del dragón.", enemigo=dragon)
    
    
    # Conectamos las salas y las añadimos al mapa
    sala_inicio.agregar_salida("norte", sala_media)
    sala_media.agregar_salida("este", sala_boss)
    mapa_del_juego.agregar_habitacion(sala_inicio)
    mapa_del_juego.agregar_habitacion(sala_media)
    mapa_del_juego.agregar_habitacion(sala_boss)
    mapa_del_juego.habitacion_actual = sala_inicio

    # 3. BUCLE DE JUEGO (Exploración + Combate)
    jugando = True
    while jugando and jugador.esta_vivo():
        print(f"\n--- {mapa_del_juego.habitacion_actual.nombre} ---")
        print(mapa_del_juego.habitacion_actual.descripcion)

        accion = input("¿A dónde ir? (norte/sur/este/oeste/salir): ").lower()

        if accion == "salir":
            jugador.guardar_partida()
            break
        
        if accion == "inventario":
            jugador.mostrar_inventario()
            continue

        if mapa_del_juego.mover(accion):
            sala_actual = mapa_del_juego.habitacion_actual
            
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
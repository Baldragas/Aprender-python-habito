from entidades import Guerrero, Enemigo, Jefe, CLASES
from mapa import Habitacion, Mapa

# TAREA CRONOGRAMA 8: Integración de lógica de victoria y limpieza de salas
def main():
    jugador = Guerrero("Conan", 120, 40)
    jugador.cargar_partida(CLASES)
    
    mapa_del_juego = Mapa()
    
    sala_inicio = Habitacion("Entrada", "Una cueva que huele a azufre.")
    sala_boss = Habitacion("Altar", "El cubil del dragón. El aire quema.")
    
    # El Jefe que marca el fin del cronograma
    dragon = Jefe("Dragón Ancianor", 200, 30)
    sala_boss.enemigo = dragon 
    
    sala_inicio.agregar_salida("norte", sala_boss)
    sala_boss.agregar_salida("sur", sala_inicio) # Conectividad bidireccional
    mapa_del_juego.agregar_habitacion(sala_inicio)
    mapa_del_juego.agregar_habitacion(sala_boss)
    mapa_del_juego.habitacion_actual = sala_inicio

    jugando = True
    print("=== COMIENZA LA AVENTURA FINAL ===")

    while jugando and jugador.esta_vivo():
        actual = mapa_del_juego.habitacion_actual
        
        # Lógica narrativa de la Semana 13
        if not actual.visitada:
            print(f"\n[NUEVA ZONA]: {actual.nombre}")
            actual.visitada = True
        
        print(f"\nUbicación: {actual.nombre}")
        print(actual.descripcion)

        accion = input("Acción (norte/sur/salir/inventario): ").lower()

        if accion == "salir":
            jugador.guardar_partida()
            break
        
        if accion == "inventario":
            jugador.mostrar_inventario()
            continue

        if mapa_del_juego.mover(accion):
            nueva_sala = mapa_del_juego.habitacion_actual
            
            if nueva_sala.enemigo:
                print(f"¡ADVERTENCIA! {nueva_sala.enemigo.nombre} bloquea el paso.")
                # Aquí se llamaría a tu función combate(jugador, nueva_sala.enemigo)
                # Simulamos que el combate ocurre:
                # nueva_sala.enemigo._vida = 0 
                
                if not nueva_sala.enemigo.esta_vivo():
                    print(f"Has derrotado a {nueva_sala.enemigo.nombre}!")
                    
                    # TAREA FINAL: Comprobar si era el Jefe para terminar el juego
                    if isinstance(nueva_sala.enemigo, Jefe):
                        print("\n******************************************")
                        print("¡HAS MATADO AL DRAGÓN! EL REINO ESTÁ A SALVO.")
                        print("******************************************")
                        jugando = False
                    
                    nueva_sala.enemigo = None
        else:
            print("Chocas contra una pared.")

    print("\n--- PROYECTO RPG FINALIZADO ---")

if __name__ == "__main__":
    main()
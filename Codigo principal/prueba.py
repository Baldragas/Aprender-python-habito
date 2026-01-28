# Basado estrictamente en tu archivo 'Polimorfismo y Bucle Principal del RPG.py'
# y la clase Mapa de 'mapa.py'

# 1. El usuario escribe una dirección
accion_usuario = input("¿Hacia dónde quieres ir? ")

# 2. El mapa intenta ejecutar el movimiento
# 'mapa_del_juego' es una instancia de la clase Mapa
if mapa_del_juego.mover(accion_usuario):
    print(f"Has avanzado hacia el {accion_usuario}.")
    # Aquí iría la lógica para comprobar si hay enemigos en la nueva sala
else:
    print("No hay camino por ahí.")

if mapa_del_juego.mover(accion_usuario):
    print(f"Has avanzado hacia el {accion_usuario}.")
    
    # 1. Obtenemos la habitación donde estamos ahora
    sala_actual = mapa_del_juego.habitacion_actual
    
    # 2. Comprobamos si el atributo 'enemigo' tiene algo (no es None)
    if sala_actual.enemigo is not None:
        enemigo_presente = sala_actual.enemigo
        print(f"¡Cuidado! Un {enemigo_presente.nombre} bloquea tu camino.")
        
        # Aquí es donde llamaremos a tu función de combate:
        # iniciar_combate(jugador, enemigo_presente)
from mapa import Habitacion, Mapa
from entidades import Enemigo # Citando el recurso entidades.py

# 1. Creamos el Mapa
mi_mapa = Mapa()
mi_mapa.mover('este')
# 2. Creamos las Habitaciones
entrada = Habitacion("Entrada del Calabozo", "Un pasillo oscuro y húmedo.")
sala_combate = Habitacion("Sala del Trono", "Una sala amplia con un trono de piedra.", Enemigo("Goblin", 30, 5, 10))

# 3. Las conectamos (Esto es lo que acabas de programar)
entrada.agregar_salida("norte", sala_combate)
sala_combate.agregar_salida("sur", entrada)

# 4. Las metemos en el mapa
mi_mapa.agregar_habitacion(entrada)
mi_mapa.agregar_habitacion(sala_combate)

# --- PRUEBA DE MOVIMIENTO ---
print(f"Estás en: {mi_mapa.habitacion_actual.nombre}")

if mi_mapa.mover("norte"):
    print("Caminas hacia el norte...")
    print(f"Ahora estás en: {mi_mapa.habitacion_actual.nombre}")
else:
    print("No puedes ir por ahí.")
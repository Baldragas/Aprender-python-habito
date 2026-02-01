
jugador = Guerrero("Test", 100, 10)
jugador.añadir_al_inventario("pocion", 2)
jugador.añadir_al_inventario("espada", 1)

print("ANTES de cargar:")
print(jugador.inventario)  # Inventario: Pocion: 2, Espada: 1
print(type(jugador.inventario.items))  # dict

# Simula lo que hace cargar_partida():
nueva = Guerrero("Temp", 100, 10)
nueva.inventario.items = {"pocion": 5, "escudo": 2}  # Solo cambia items
jugador.__dict__.update(nueva.__dict__)

print("DESPUÉS de cargar:")
print(jugador.inventario)  # ¿Qué mostrará?
print(jugador.inventario.items)  # ¿{"pocion": 5, "escudo": 2}?
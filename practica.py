# import json

# # # Datos de ejemplo
# # datos = {
# #     'nombre': 'Conan',
# #     'vida': 120,
# #     'fuerza': 40,
# #     'inventario': {'poción de vida': 5}
# # }
# # with open("partida.json", "w") as f:
# #     json.dump(datos, f, indent=4)

# # with open ("partida.json", "r") as f:
# #     datos = json.load(f)

# class Personaje:
#     def __init__(self, nombre, vida, daño):
#         self.nombre = nombre
#         self.vida = vida
#         self.daño = daño
#     pass

# jugador = Personaje("Conan", 120, 40)

# # Ejercicio 1: Convertir jugador a dict y guardar
# estado = jugador.__dict__
# with open("jugador.json", "w") as f:
#     json.dump(estado, f, indent=4)

# # Ejercicio 2: Cargar y recrear el jugador
# with open("jugador.json", "r") as f:
#     datos_cargados = json.load(f)

# nuevo_jugador = Personaje(**datos_cargados)
# # Pista: nuevo_jugador = Personaje(datos_cargados['nombre'], datos_cargados['vida'], datos_cargados['fuerza'])

# print(nuevo_jugador.nombre, nuevo_jugador.vida, nuevo_jugador.daño)
# # Debe imprimir: Conan 120 40
# Supongamos que ya tienes el dict básico guardado/cargado
# Ejercicio 1: Guardar atributos especiales en guardar_partida
# Guardar
# En guardar_partida (dentro del dict estado)
class Guerrero:
    pass
# En guardar_partida (dentro del dict estado)
estado = {
    'nombre': self.nombre,
    'vida': self._vida,
    'vida_max': self.vida_max,
    'fuerza': self.fuerza,
    'tipo_clase': type(self).__name__,
    'furia': getattr(self, 'furia', 0),
    'fuerza_base':getattr(self, 'fuerza_base', None),
    'inventario': self.inventario.items
}
with open('partida.json', 'w') as f:
    json.dump(estado, f, indent=4)
print("Partida guardada.")

# En cargar_partida
with open('partida.json', 'r') as f:
    datos_cargados = json.load(f)

tipo = datos_cargados.get('tipo_clase', 'Personaje')

# Hueco 5: Recrear el objeto según tipo (completa el if)
if tipo == 'Guerrero':
    nueva = Guerrero(**datos_cargados)
elif tipo == 'Jefe':
    nueva = Jefe(**datos_cargados)
else:
    nueva = Personaje(**datos_cargados)

if 'furia' in datos_cargados:
    nueva.furia = datos_cargados['furia']
if 'fuerza_base' in datos_cargados:
    nueva.fuerza_base = datos_cargados['fuerza_base']
if 'inventario' in datos_cargados:
    nueva.inventario.items = datos_cargados['invetario']

# Hueco 8: Restaura inventario
# ??? escribe la línea

rona.__dict__.update(nuevo.__dict__)
# ??? escribe la línea (usa __dict__.update)
print("Partida cargada.")

# creo que restaurar furia y fuerza base con if, es innecesario porque ya se puede cargar directamente a nuevo,
#gracias al unpacking que me enseñor grok recien, pero lo hago igual porque es parte del ejercicio y es lo que importa

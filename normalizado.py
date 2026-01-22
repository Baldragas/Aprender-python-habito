# En guardar_partida (dentro del dict estado)
estado = {
    'nombre': self.nombre,
    'vida': self._vida,
    'vida_max': self.vida_max,
    'fuerza': self.fuerza,
    'furia': getattr(self, 'furia', 0),
    'fuerza_base': getattr(self, 'fuerza_base', None),
    'tipo_clase': type(self).__name__,
    'inventario': self.inventario.items
}

with open('partida.json', 'w') as f:
    json.dump(estado, f, indent=4)
print("Partida guardada.")

with open('partida.json', 'r') as f:
    datos_cargados = json.load(f)

if tipo == 'Guerrero':
    nueva = Guerrero(**datos_cargados)
elif tipo == 'Jefe':
    nueva = Jefe(**datos_cargados)
else:
    nueva = Personaje(**datos_cargados)

if 'inventario' in datos_cargados:
    nueva.inventario.items = datos_cargados['inventario'] 
print("Partida cargada.")

self.__dict__.update(nueva.__dict__)
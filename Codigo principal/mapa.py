# mapa.py

class Habitacion:
    def __init__(self, nombre, descripcion, enemigo=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.enemigo = enemigo
        self.salidas = {}  # Diccionario que conecta direcciones con otras Habitaciones

    def agregar_salida(self, direccion, habitacion_destino):
        # Establece la conexión de ida
        self.salidas[direccion] = habitacion_destino

    def __str__(self):
        salidas_str = ", ".join(self.salidas.keys())
        return f"--- {self.nombre} ---\n{self.descripcion}\nSalidas: {salidas_str}"


class Mapa:
    def __init__(self):
        # Almacén de todas las habitaciones creadas
        self.habitaciones = {} 
        # El "puntero" que indica dónde está el jugador ahora mismo
        self.habitacion_actual = None

    def agregar_habitacion(self, habitacion):
        """Añade una habitación al diccionario del mapa."""
        self.habitaciones[habitacion.nombre] = habitacion
        if self.habitacion_actual is None:
            self.habitacion_actual = habitacion

    def mover(self, direccion):
        """Intenta cambiar la habitación actual según la dirección."""
        # 1. Comprobamos si la dirección existe en la habitación donde estamos
        if direccion in self.habitacion_actual.salidas:
            self.habitacion_actual = self.habitacion_actual.salidas[direccion]
            return True
        return False
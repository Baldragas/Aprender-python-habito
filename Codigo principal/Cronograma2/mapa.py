class Habitacion:
    def __init__(self, nombre, descripcion, enemigo=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.enemigo = enemigo
        self.salidas = {}
        self.objetos = []
        self.visitada = False # Para el sistema de narrativa única

    def agregar_salida(self, direccion, habitacion_destino):
        self.salidas[direccion] = habitacion_destino

    def __str__(self):
        salidas_str = ", ".join(self.salidas.keys())
        return f"--- {self.nombre} ---\n{self.descripcion}\nSalidas: {salidas_str}"

class Mapa:
    def __init__(self):
        self.habitaciones = {} 
        self.habitacion_actual = None

    def agregar_habitacion(self, habitacion):
        self.habitaciones[habitacion.nombre] = habitacion
        if self.habitacion_actual is None:
            self.habitacion_actual = habitacion

    def mover(self, direccion):
        if direccion in self.habitacion_actual.salidas:
            self.habitacion_actual = self.habitacion_actual.salidas[direccion]
            return True
        return False
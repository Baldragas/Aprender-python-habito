# Archivo: objetos.py (CREAR NUEVO)
class Item:
    def __init__(self, nombre, tipo, valor=0, **kwargs):
        self.nombre = nombre
        self.tipo = tipo  # 'poción', 'arma', 'comida', 'llave'
        self.valor = valor
        self.propiedades = kwargs
    
    def usar(self, jugador):
        """Efecto al usar el item"""
        if self.tipo == 'poción':
            # ¡HUECO 2! Acceder a 'curacion' en propiedades (default 20)
            curacion = self.propiedades.get('curacion', 20)
            jugador._vida = min(jugador.vida_max, jugador._vida + curacion)
            print(f"¡Usas {self.nombre} y recuperas {curacion} de vida!")
            return True
        elif self.tipo == 'comida':
            print(f"Comes {self.nombre}. Sabe bien.")
            return True
        else:
            print(f"No puedes usar {self.nombre} directamente.")
            return False
    
    @staticmethod
    def crear_pocion_menor():
        return Item("Poción menor", "poción", valor=10, curacion=25)
    
    @staticmethod
    def crear_pocion_mayor():
        return Item("Poción mayor", "poción", valor=30, curacion=60)
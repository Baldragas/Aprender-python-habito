
class Item:
    def __init__(self, nombre, tipo, valor=0, **kwargs):
        self.nombre = nombre
        self.tipo = tipo  # 'poción', 'arma', 'comida', 'llave'
        self.valor = valor

        propiedades_permitidas =['curacion', 'daño', 'proteccion', 'duracion']

        self.propiedades = {}

        for key, value in kwargs.items():
            if key in propiedades_permitidas:
                self.propiedades[key] = value
            else:
                print(f"⚠️ Propiedad '{key}' no permitida para Item")

    def es_pocion(self):
        tipo = self.tipo.lower().replace('ó', 'o')
        return tipo == 'pocion' and 'curacion' in self.propiedades
    
    def usar(self, jugador):
        """Efecto al usar el item"""
        if self.tipo == 'pocion':
            # ¡HUECO 2! Acceder a 'curacion' en propiedades (default 20)
            curacion = self.propiedades.get('curacion', 20)
            jugador._vida = min(jugador.vida_max, jugador._vida + curacion)
            print(f"¡Usas {self.nombre} y recuperas {curacion} de vida!")
            return True
        elif self.tipo == 'defensa':
            print(f"Te proteges con {self.nombre}, por ahora no pasa nada")
            return True
        elif self.tipo == 'comida':
            print(f"Comes {self.nombre}. Sabe bien.")
            return True
        else:
            print(f"No puedes usar {self.nombre} directamente.")
            return False
    
    def __str__(self):
        return f"{self.nombre} (tipo: {self.tipo})"
    
    @staticmethod
    def crear_pocion_menor():
        return Item("Poción menor", "poción", valor=10, curacion=25)
    
    @staticmethod
    def crear_pocion_mayor():
        return Item("Poción mayor", "poción", valor=30, curacion=60)
    
    @staticmethod
    def crear_escudo():
        return Item("Escudo de madera", "defensa", valor=15, proteccion=5)
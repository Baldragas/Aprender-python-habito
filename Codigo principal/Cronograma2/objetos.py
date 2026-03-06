
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
        tipo = self.tipo.lower().replace('ó', 'o')
        if tipo == 'pocion':
            curacion = self.propiedades.get('curacion', 20)
            jugador.curar(curacion)
            return True

        elif tipo == 'defensa':
            jugador.defensa_activa = True
            print(f"Te cubres con {self.nombre}. El próximo ataque hará menos daño")
            return True
    
        elif tipo == 'comida':
            curacion = self.propiedades.get("curacion", 10)   # ← ya está
            recuperado = jugador.curar(curacion)
            print(f"*Ñam, que rica comida*. Recuperaste {recuperado} de vida.")
            return True
        
        elif tipo == 'buff':
            efecto = {
                "atributo": self.propiedades.get("atributo", "fuerza"),
                "modificador": self.propiedades.get("modificador", 5),
                "duracion": self.propiedades.get("duracion", 3)
            }
            jugador.aplicar_efecto(efecto)
            return True
        else:
            print(f"No puedes usar {self.nombre} directamente.")
            return False
    
    def __str__(self):
        return f"{self.nombre} (tipo: {self.tipo})"
    
    @staticmethod
    def crear_pocion_fuerza():
        return Item(
            "Poción de fuerza", 
            "buff", 
            valor=25,
            atributo="fuerza",
            modificador=10,
            duracion=3
        )
    
    @staticmethod
    def crear_pocion_menor():
        return Item("Poción menor", "poción", valor=10, curacion=25)
    
    @staticmethod
    def crear_pocion_mediana():
        return Item("Pocion mediana", "pocion", valor=20, curacion=45)
    
    @staticmethod
    def crear_pocion_mayor():
        return Item("Poción mayor", "pocion", valor=30, curacion=60)
    
    @staticmethod
    def crear_escudo():
        return Item("Escudo de madera", "defensa", valor=15, proteccion=5)
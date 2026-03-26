class Item:
    def __init__(self, nombre, tipo, valor=0, **kwargs):
        self.nombre = nombre
        self.tipo = tipo  # 'curacion', 'defensa', 'buff'
        self.valor = valor
        self.propiedades = {k: v for k, v in kwargs.items() if k in ['curacion', 'proteccion', 'duracion']}

    def aplicar_uso(self, usuario):
        if self.tipo == "curacion":
            if usuario.vida >= usuario.vida_max:
                print(f"❤️ {usuario.nombre} ya tiene la salud al máximo.")
                return False
            usuario.vida += self.valor
            print(f"✨ {usuario.nombre} usa {self.nombre} y recupera {self.valor} HP.")
            return True
        
        elif self.tipo == "buff":
            # Extraemos los datos del diccionario 'propiedades'
            efecto = {
                "atributo": self.propiedades.get("atributo", "fuerza"),
                "modificador": self.propiedades.get("modificador", 5),
                "duracion": self.propiedades.get("duracion", 3)
            }
            usuario.aplicar_efecto(efecto)
            print(f"🧪 {usuario.nombre} consume {self.nombre}.")
            return True
        
        print(f"❓ El objeto {self.nombre} no se puede usar así.")
        return False

    def to_dict(self):
        return {"nombre": self.nombre, "tipo": self.tipo, "valor": self.valor, "propiedades": self.propiedades}

    @staticmethod
    def crear_pocion_menor():
        return Item("Poción menor", "curacion", valor=25)

    @staticmethod
    def crear_pocion_mediana():
        return Item("Pocion mediana", "curacion", valor=45)
        
    @staticmethod
    def crear_pocion_mayor():
        return Item("Poción mayor", "curacion", valor=60)

    @staticmethod
    def crear_escudo():
        return Item("Escudo de madera", "defensa", valor=15, proteccion=5, duracion=3)
    
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
    
    
    
import unicodedata
import json

def normalize(text: str) -> str:
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()

class Inventario:
    def __init__(self):
        self.items = {}
    
    def agregar_item(self, nombre, cantidad=1):
        key = normalize(nombre)
        if key in self.items:
            self.items[key] += cantidad
        else:
            self.items[key] = cantidad
        print(f"Se añadió {cantidad} {nombre} al inventario")

    def quitar_item(self, nombre, cantidad=1):
        key = normalize(nombre)
        if key in self.items and self.items[key] >= cantidad:
            self.items[key] -= cantidad
            if self.items[key] <= 0:
                self.items.pop(key)
            return True
        else:
            return False
            
    def __str__(self):
        if not self.items:
            return "Inventario vacío"
        return "Inventario: " + ", ".join(f"{key.capitalize()}: {cant}" for key, cant in self.items.items())

class Personaje:
    def __init__(self, nombre, vida, fuerza):
        self.nombre = nombre
        self._vida = vida
        self.fuerza = fuerza
        self.inventario = Inventario()
        # CORRECCIÓN 1: La vida máxima es igual a la vida con la que nace el personaje
        self.vida_max = vida 
    
    def añadir_al_inventario(self, nombre, cantidad=1):
        print(f"{self.nombre} encuentra {cantidad} {nombre}")
        self.inventario.agregar_item(nombre, cantidad)

    def usar_item(self, nombre, cantidad=1):
        key = normalize(nombre)
        if key not in self.inventario or self.invetario[key] < cantidad:
            print(f"No tienes suficiente {nombre}")
            return False

        if "pocion de vida" in key:
            curacion = 40 * cantidad
            self._vida = min(self.vida_max, self._vida + curacion)
            print(f"{self.nombre} recupera {curacion} de vida, ahora tiene {self._vida}")
            return True

        self.inventario.quitar_item(key, cantidad)
        print(f"Usas {nombre}, pero no tiene efecto especial aún.")
        return True

    def mostrar_inventario(self):
        print(self.inventario)
        return bool(self.inventario.items)
    
    def recibir_daño(self, cantidad):
        daño_real = cantidad
        if "escudo" in self.inventario.items:
            daño_real = cantidad // 2 
            print(f"{self.nombre} bloquea con escudo! Daño reducido a {daño_real}")
            self.inventario.quitar_item("Escudo", 1) 
        self._vida = max(0, self._vida - daño_real)
        print(f"{self.nombre} recibe {daño_real} de daño. Vida restante: {self._vida}")

    def esta_vivo(self):
        return self._vida > 0

    def atacar(self, objetivo):
        print(f"{self.nombre} ataca a {objetivo.nombre} causando {self.fuerza} de daño")
        objetivo.recibir_daño(self.fuerza)

    def __str__(self):
        return f"{self.nombre} (Vida: {self._vida}, Fuerza: {self.fuerza})\n{self.inventario}"

    def guardar_partida(self, archivo='partida.json'):
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
        with open(archivo, 'w') as f:
            json.dump(estado, f, indent=4)
        print("Partida guardada.")

    def cargar_partida(self, diccionario_clases, archivo='partida.json'):
        try:
            with open(archivo, 'r') as f:
                estado = json.load(f)

            args_init = {
                'nombre': estado.get('nombre'),
                'vida': estado.get('vida'),
                'fuerza': estado.get('fuerza')
                }

            tipo = estado.get('tipo_clase', 'Personaje')
            Clase = diccionario_clases.get(tipo, Personaje) 
            nueva = Clase(**args_init)
            
            # Copiar atributos de nueva a self, excepto inventario
            for attr, value in nueva.__dict__.items():
                if attr != 'inventario' and hasattr(self, attr):
                    setattr(self, attr, value)
            
            # Cargar atributos especiales desde el estado
            if 'furia' in estado:
                self.furia = estado['furia']
            if 'fuerza_base' in estado:
                self.fuerza_base = estado['fuerza_base']
            if 'vida_max' in estado:
                self.vida_max = estado['vida_max']
            
            # Cargar inventario: actualizar el diccionario items del inventario actual
            if 'inventario' in estado:
                self.inventario.items.clear()
                self.inventario.items.update(estado['inventario'])
            
            print("Partida cargada.")
        except FileNotFoundError:
            print("No hay partida guardada.")

class Guerrero(Personaje):
    def __init__(self, nombre, vida, fuerza):
        super().__init__(nombre, vida, fuerza)
        self.furia = 0 

    def atacar(self, objetivo):
        super().atacar(objetivo)
        self.furia += 1
        print(f"¡{self.nombre} gana 1 punto de furia! (Total: {self.furia})")

    def __str__(self):
        return f"{self.nombre} (Vida: {self._vida}, Fuerza: {self.fuerza}, Furia: {self.furia})"


class Enemigo(Personaje): 
    # Quitaste los ???, la herencia está bien hecha.
    def __init__(self, nombre, vida, fuerza, experiencia_otorgada):
        super().__init__(nombre, vida, fuerza)
        self.experiencia = experiencia_otorgada
        
    def otorgar_experiencia(self):
        if not self.esta_vivo():
            return self.experiencia
        else:
            return 0

    def __repr__(self):
        # Retorna un string que muestre el nombre y la vida de forma técnica
        return f"Enemigo(nombre = '{self.nombre}', vida = {self._vida})"

class Jefe(Personaje): 
    def __init__(self, nombre, vida, fuerza_base):
        super().__init__(nombre, vida, fuerza_base)
        self.fuerza_base = fuerza_base 

    def atacar(self, objetivo):
        daño = 1.5 * self.fuerza_base
        print(f"{self.nombre} ataca con furia a {objetivo.nombre} causando {daño} de daño")
        objetivo.recibir_daño(daño)

CLASES = {
    'Personaje': Personaje,
    'Enemigo': Enemigo,
    'Guerrero': Guerrero,
    'Jefe': Jefe
}
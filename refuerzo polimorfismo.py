import unicodedata

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
        self.vida_max = 100
    
    def añadir_al_inventario(self, nombre, cantidad=1):
        print(f"{self.nombre} encuentra {cantidad} {nombre}")
        self.inventario.agregar_item(nombre, cantidad)

    def usar_item(self, nombre, cantidad=1):
        key = normalize(nombre)
        if self.inventario.quitar_item(key, cantidad):
            print(f"{self.nombre} usa {cantidad} {nombre}")
            if "pocion de vida" in key:
                curacion = 20 * cantidad
                self._vida = min(self.vida_max, self._vida + curacion)
                print(f"{self.nombre} recupera {curacion} de vida, ahora tiene {self._vida}")
        else:
            print(f"No tienes suficiente {nombre} para gastar")

    def mostrar_inventario(self):
        print(self.inventario)  # Usa el __str__ del inventario
    
    def recibir_daño(self, cantidad):
        self._vida = max(0, self._vida - cantidad)
        print(f"{self.nombre} recibe {cantidad} de daño. Vida restante: {self._vida}")

    def esta_vivo(self):
        return self._vida > 0

    def atacar(self, objetivo):
        print(f"{self.nombre} ataca a {objetivo.nombre} causando {self.fuerza} de daño")
        objetivo.recibir_daño(self.fuerza)

    def __str__(self):
        return f"{self.nombre} (Vida: {self._vida}, Fuerza: {self.fuerza})\n{self.inventario}"


class Enemigo(Personaje):  # ??? Herencia aquí
    def __init__(self, nombre, vida, fuerza, experiencia_otorgada):
        super().__init__(nombre, vida, fuerza)
        self.experiencia = experiencia_otorgada
        

    # Nuevo método específico de Enemigo
    def otorgar_experiencia(self):
        if not self.esta_vivo():
            return self.experiencia
        else:
            return 0

class Guerrero(Personaje):
    def __init__(self, nombre, vida, fuerza):
        super().__init__(nombre, vida, fuerza)
        self.furia = 0  # Nuevo atributo: empieza en 0

    def atacar(self, objetivo):
         # ??? Completa aquí:
        super().atacar(objetivo)
        self.furia += 1
        print(f"¡{self.nombre} gana 1 punto de furia! (Total: {self.furia})")

    def __str__(self):
        return f"{self.nombre} (Vida: {self._vida}, Fuerza: {self.fuerza}, Furia: {self.furia})"

class Jefe(Personaje):  # ??? Declarar herencia
    def __init__(self, nombre, vida, fuerza_base):
        super().__init__(nombre, vida, fuerza_base)
        self.fuerza_base = fuerza_base  # Guardar la fuerza original

    def atacar(self, objetivo):
        daño = 2 * self.fuerza_base
        print(f"{self.nombre} ataca con furia a {objetivo.nombre} causando {daño} de daño")
        objetivo.recibir_daño(daño)

heroe = Personaje("Arthur", 40, 20)
heroe.añadir_al_inventario("Poción de vida", 3)

heroe.usar_item("Poción de vida", 2)
# → Arthur bebe 2 Poción de vida y recupera 40 vida. Vida actual: 80

heroe.recibir_daño(50)
# → Vida baja a 30

heroe.usar_item("pocion de vida", 1)  # ignora mayúsculas
# → Arthur bebe 1 poción de vida y recupera 20 vida. Vida actual: 50

heroe.usar_item("Escudo")
# → Arthur usa 1 Escudo (sin efecto de vida)
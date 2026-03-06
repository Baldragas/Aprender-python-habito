import unicodedata
import json
from objetos import Item

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
        if vida <= 0:
            raise ValueError("La vida debe ser mayor a cero (fue {vida})")
        
        # Validar fuerza
        if fuerza < 1:  # Asumimos que fuerza mínima es 1
            raise ValueError("La fuerza debe ser al menos 1")
        
        self.nombre = nombre
        self._vida = vida
        self.fuerza = fuerza
        self.inventario = Inventario()
        self.items_objetos = {}
        self.vida_max = vida
        self.defensa_activa = False
        self.efectos = []

    def aplicar_efecto(self, efecto):
        """Registra un efecto y aplica su modificador al atributo correspondiente."""
        # 1. Guardar el efecto en la lista
        self.efectos.append(efecto)

        # 2. Obtener el atributo y el modificador
        atributo = efecto["atributo"]
        modificador = efecto["modificador"]

        # 3. Aplicar el cambio al atributo
        valor_actual = getattr(self, atributo)
        setattr(self, atributo, valor_actual + modificador)

        # 4. Mensaje informativo (opcional)
        print(f"⚡ Efecto aplicado: {atributo} {modificador:+d} durante {efecto['duracion']} turnos. Ahora {atributo} = {getattr(self, atributo)}")
        
    def procesar_efectos(self):
        efectos_a_eliminar = []
        for efecto in self.efectos:
            efecto['duracion'] -= 1
            if efecto['duracion'] <= 0:
                # Revertir el efecto
                atributo = efecto['atributo']
                modificador = efecto['modificador']
                valor_actual = getattr(self, atributo)
                setattr(self, atributo, valor_actual - modificador)
                efectos_a_eliminar.append(efecto)
                print(f"⚡ Efecto de {atributo} ha terminado. Ahora {atributo} = {getattr(self, atributo)}")
        # Eliminar los efectos terminados
        for efecto in efectos_a_eliminar:
            self.efectos.remove(efecto)

    def curar(self, cantidad):
        """
        Aumenta la vida del personaje en 'cantidad' sin superar vida_max.
        Devuelve la cantidad real de vida recuperada.
        """
        vida_anterior = self._vida
        self._vida = min(self.vida_max, self._vida + cantidad)
        recuperado = self._vida - vida_anterior
        if recuperado > 0:
            print(f"{self.nombre} recupera {recuperado} puntos de vida. Vida actual {self._vida}")
        else:
            print(f"{self.nombre} ya está al máximo de vida.")
        return recuperado

    def añadir_item_objeto(self, item_obj, cantidad=1):
        print(f"{self.nombre} encuentra {cantidad} {item_obj.nombre}")
        # Por ahora, solo prueba almacenando como string
        self.inventario.agregar_item(item_obj.nombre, cantidad)
        print(f"(Objeto Item detectado: cura {item_obj.propiedades.get('curacion', 0)})")
        key = normalize(item_obj.nombre)
        self.items_objetos[key] = item_obj
        
    def añadir_al_inventario(self, nombre, cantidad=1):
        print(f"{self.nombre} encuentra {cantidad} {nombre}")
        self.inventario.agregar_item(nombre, cantidad)

    def usar_item(self, nombre, cantidad=1):
        key = normalize(nombre)

        if key not in self.inventario.items or self.inventario.items[key] < cantidad:
            print(f"No tienes suficiente {nombre}")
            return False

        if key in self.items_objetos:
            item_obj = self.items_objetos[key]
            # Aplicar el efecto tantas veces como cantidad
            for _ in range(cantidad):
                item_obj.usar(self)   # <--- DELEGACIÓN
            self.inventario.quitar_item(key, cantidad)
            return True
        else:
            # Si no hay objeto Item asociado (solo string), lo tratamos como ítem genérico
            self.inventario.quitar_item(key, cantidad)
            print(f"Usas {nombre}, pero no tiene efecto especial aún.")
            return True

    def mostrar_inventario(self):
        print(self.inventario)
        return bool(self.inventario.items)
    
    def recibir_daño(self, cantidad):
        if self.defensa_activa:  
            daño_real = cantidad // 2
            print(f"{self.nombre} bloquea con el escudo! Daño reducido a {daño_real}")
            self.defensa_activa = False
        else:
            daño_real = cantidad
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
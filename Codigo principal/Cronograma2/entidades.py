import unicodedata
import json
from objetos import Item

def normalize(text: str) -> str:
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()

class Inventario:
    def __init__(self):
        self.items = {}

    def agregar_item(self, item_obj, cantidad=1):
        key = normalize(item_obj.nombre)
        
        if key in self.items:
            self.items[key]["cantidad"] += cantidad
        else:
            self.items[key] = {
                "objeto": item_obj,      
                "cantidad": cantidad  
            }
        print(f"Se añadió {cantidad}x {item_obj.nombre} al inventario.")

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
        # Usar la versión sin guion activa el @setter inmediatamente
        self.vida = vida 
        self.fuerza = fuerza
        self.vida_max = vida
        self.inventario = Inventario()
        self.efectos = []
        self.defensa_activa = False

    # --- ADUANA DE VIDA ---
    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, valor_nuevo):
        if valor_nuevo < 0:
            self._vida = 0
        else:
            self._vida = valor_nuevo

    # --- ADUANA DE FUERZA ---
    @property
    def fuerza(self):
        return self._fuerza

    @fuerza.setter
    def fuerza(self, valor_nuevo):
        if valor_nuevo < 1:
            self._fuerza = 1
        elif valor_nuevo > 100:
            self._fuerza = 100
        else:
            self._fuerza = valor_nuevo

    def esta_vivo(self):
        # Usamos la propiedad pública 'vida'
        return self.vida > 0

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
        vida_anterior = self.vida
        self.vida = min(self.vida_max, self.vida + cantidad)
        recuperado = self.vida - vida_anterior
        if recuperado > 0:
            print(f"{self.nombre} recupera {recuperado} puntos de vida. Vida actual {self.vida}")
        else:
            print(f"{self.nombre} ya está al máximo de vida.")
        return recuperado

    def añadir_item_objeto(self, item_obj, cantidad=1):
        print(f"{self.nombre} encuentra {cantidad} {item_obj.nombre}")
        self.inventario.agregar_item(item_obj, cantidad)
        
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
        for key, datos in self.inventario.items.items():
            objeto_real = datos["objeto"]
            cantidad = datos["cantidad"]
            # Accedemos al atributo .nombre del objeto
            print(f"- {objeto_real.nombre}: {cantidad}")
        return bool(self.inventario.items)
    
    def recibir_daño(self, cantidad):
        if self.defensa_activa:  
            daño_real = cantidad // 2
            print(f"{self.nombre} bloquea con el escudo! Daño reducido a {daño_real}")
            self.defensa_activa = False
        else:
            daño_real = cantidad
        self.vida = max(0, self.vida - daño_real)
        print(f"{self.nombre} recibe {daño_real} de daño. Vida restante: {self.vida}")

    def esta_vivo(self):
        return self.vida > 0

    def atacar(self, objetivo):
        print(f"{self.nombre} ataca a {objetivo.nombre} causando {self.fuerza} de daño")
        objetivo.recibir_daño(self.fuerza)

    def __str__(self):
        return f"{self.nombre} (Vida: {self.vida}, Fuerza: {self.fuerza})\n{self.inventario}"

    def guardar_partida(self, archivo='partida.json'):
        inventario_serializado = {}
        for key, datos in self.inventario.items.items():
            inventario_serializado[key] = {
                "objeto": datos["objeto"].to_dict(),
                "cantidad": datos["cantidad"]
            }

        estado = {
            'nombre': self.nombre,
            'vida': self.vida,
            'vida_max': self.vida_max,
            'fuerza': self.fuerza,
            'furia': getattr(self, 'furia', 0), 
            'fuerza_base': getattr(self, 'fuerza_base', None),
            'tipo_clase': type(self).__name__,
            'inventario': inventario_serializado 
        }
        
        with open(archivo, 'w') as f:
            json.dump(estado, f, indent=4)
        print(f"¡Partida de {self.nombre} guardada con éxito!")
        
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
            
            if 'inventario' in estado:
                self.inventario.items.clear()
                
                for key, info in estado['inventario'].items():
                    # Re-hidratamos el objeto Item desde el diccionario
                    nuevo_item = Item(
                        nombre=info["objeto"]["nombre"],
                        tipo=info["objeto"]["tipo"],
                        valor=info["objeto"]["valor"],
                        propiedades=info["objeto"]["propiedades"]
                    )
                    
                    # Lo metemos al inventario usando nuestro método oficial
                    self.inventario.agregar_item(nuevo_item, info["cantidad"])
            
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
        return f"{self.nombre} (Vida: {self.vida}, Fuerza: {self.fuerza}, Furia: {self.furia})"


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
        return f"Enemigo(nombre = '{self.nombre}', vida = {self.vida})"

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
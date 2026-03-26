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
            self.items[key] = {"objeto": item_obj, "cantidad": cantidad}

    def quitar_item(self, nombre_item, cantidad=1):
        key = normalize(nombre_item)
        if key in self.items:
            if self.items[key]["cantidad"] >= cantidad:
                self.items[key]["cantidad"] -= cantidad
                if self.items[key]["cantidad"] <= 0:
                    del self.items[key]
                return True
        return False

    def __str__(self):
        if not self.items: return "Inventario vacío"
        return "\n".join([f"- {v['objeto'].nombre} (x{v['cantidad']})" for v in self.items.values()])

class Personaje:
    def __init__(self, nombre, vida, fuerza):
        self.nombre = nombre
        self.vida_max = vida
        self._vida = vida
        self.fuerza = fuerza
        self.inventario = Inventario()
        self.equipo = {"escudo": None, "arma": None}
        self.defensa_activa = False
        self.efectos = []

    @property
    def vida(self): return self._vida

    @vida.setter
    def vida(self, nuevo_valor):
        if nuevo_valor < 0: self._vida = 0
        elif nuevo_valor > self.vida_max: self._vida = self.vida_max
        else: self._vida = nuevo_valor

    def esta_vivo(self): return self.vida > 0

    def usar_item(self, nombre_buscado):
        key = normalize(nombre_buscado)
        if key in self.inventario.items:
            item_obj = self.inventario.items[key]["objeto"]
            if item_obj.aplicar_uso(self):
                self.inventario.quitar_item(key, 1)
        else:
            print(f"❌ No tienes '{nombre_buscado}' en el inventario.")
    
    def mostrar_inventario(self):
        print(f"\n🎒 Inventario de {self.nombre}:")
        print(self.inventario)

    def equipar_item(self, nombre_buscado):
        key = normalize(nombre_buscado)
        if key in self.inventario.items:
            item_obj = self.inventario.items[key]["objeto"]
            if item_obj.tipo == "defensa":
                self.equipo["escudo"] = item_obj
                self.inventario.quitar_item(key, 1)
                print(f"🛡️ {item_obj.nombre} equipado.")

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

    def usar_item(self, nombre_buscado):
        key = normalize(nombre_buscado)
        
        # 1. Verificamos si existe en el diccionario
        if key in self.inventario.items:
            datos = self.inventario.items[key]
            item_obj = datos["objeto"]
            
            # 2. Intentamos usarlo (la lógica de curación/buff)
            if item_obj.aplicar_uso(self):
                # 3. Si se usó con éxito, lo quitamos de la caja
                self.inventario.quitar_item(key, 1)
        else:
            print(f"❌ No tienes '{nombre_buscado}' en tu inventario.")

    def mostrar_inventario(self):
        for key, datos in self.inventario.items.items():
            objeto_real = datos["objeto"]
            cantidad = datos["cantidad"]
            # Accedemos al atributo .nombre del objeto
            print(f"- {objeto_real.nombre}: {cantidad}")
        return bool(self.inventario.items)
    
    def recibir_daño(self, cantidad):
        escudo = self.equipo["escudo"]
        
        if escudo and escudo.propiedades.get("duracion", 0) > 0:
            proteccion = escudo.propiedades.get("proteccion", 0)
            daño_real = max(0, cantidad - proteccion)
            
            # Aplicamos el desgaste
            escudo.propiedades["duracion"] -= 1
            print(f"🛡️ El {escudo.nombre} bloquea {proteccion} de daño. (Quedan {escudo.propiedades['duracion']} usos)")
            
            # Si se rompe, lo quitamos del equipo
            if escudo.propiedades["duracion"] <= 0:
                print(f"💥 ¡Tu {escudo.nombre} se ha hecho pedazos!")
                self.equipo["escudo"] = None 
        else:
            daño_real = cantidad
            
        self.vida -= daño_real

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
        self.vida_max = vida
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
        self.vida_max = vida
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
        self.vida_max = vida
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
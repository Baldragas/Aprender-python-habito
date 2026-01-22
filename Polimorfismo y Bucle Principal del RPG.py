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
        if self.inventario.quitar_item(key, cantidad):
            print(f"{self.nombre} usa {cantidad} {nombre}")
            if "pocion de vida" in key:
                curacion = 40 * cantidad
                self._vida = min(self.vida_max, self._vida + curacion)
                print(f"{self.nombre} recupera {curacion} de vida, ahora tiene {self._vida}")
        else:
            print(f"No tienes suficiente {nombre} para gastar")

    def mostrar_inventario(self):
        print(self.inventario) 
    
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

    def cargar_partida(self, archivo='partida.json'):
        try:
            with open(archivo, 'r') as f:
                estado = json.load(f)

            args_init = {
                'nombre': estado.get('nombre'),
                'vida': estado.get('vida'),
                'fuerza': estado.get('fuerza')
                }

            # CORRECCIÓN 2: Eliminé las líneas repetidas que tenías aquí
            tipo = estado.get('tipo_clase', 'Personaje')
            Clase = CLASES.get(tipo, Personaje) 
            nueva = Clase(**args_init)
            
            if 'furia' in estado:
                nueva.furia = estado['furia']
            if 'fuerza_base' in estado:
                nueva.fuerza_base = estado['fuerza_base']
            if 'inventario' in estado:
                nueva.inventario.items = estado['inventario']
            if 'vida_max' in estado:
                nueva.vida_max = estado['vida_max']
            
            self.__dict__.update(nueva.__dict__)
            
            print("Partida cargada.")
        except FileNotFoundError:
            print("No hay partida guardada.")

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

class Jefe(Personaje): 
    def __init__(self, nombre, vida, fuerza_base):
        super().__init__(nombre, vida, fuerza_base)
        self.fuerza_base = fuerza_base 

    def atacar(self, objetivo):
        daño = 1.5 * self.fuerza_base
        print(f"{self.nombre} ataca con furia a {objetivo.nombre} causando {daño} de daño")
        objetivo.recibir_daño(daño)

CLASES ={
    'Personaje': Personaje,
    'Enemigo': Enemigo,
    'Guerrero': Guerrero,
    'Jefe': Jefe
}

def combate(jugador, enemigo):
    print(f"\n=== Combate inicia: {jugador.nombre} vs {enemigo.nombre} ===")
    
    while jugador.esta_vivo() and enemigo.esta_vivo():
        print(f"\nTurno de {jugador.nombre} (Vida: {jugador._vida})")
        print(f"{enemigo.nombre} - Vida restante: {enemigo._vida}")
        print("Opciones:")
        print("1. Atacar")
        print("2. Usar item (ej. Poción de vida)")
        print("3. Huir (salir del combate)")
        eleccion = input("Elige (1/2/3): ").strip()
        
        if eleccion == '1':
            jugador.atacar(enemigo)
        elif eleccion == '2':
            item = input("Nombre del item a usar: ").strip()
            jugador.usar_item(item, 1)
        elif eleccion == '3':
            print("¡Huyes del combate!")
            break
        else:
            print("Opción inválida. Turno perdido.")
            continue
        
        if not enemigo.esta_vivo():
            print(f"{enemigo.nombre} ha sido derrotado!")
            break
        
        print(f"\nTurno de {enemigo.nombre}")
        enemigo.atacar(jugador)
        if not jugador.esta_vivo():
            print(f"{jugador.nombre} ha sido derrotado...")
            break
    
    print("Combate terminado.")

def juego_principal():
    
    jugador = Guerrero("Conan", 120, 40)
    
    # Intenta cargar la partida. Si no existe, no pasa nada (imprimirá "No hay partida")
    # y Conan se quedará con sus stats originales.
    jugador.cargar_partida()

    # NOTA: Si cargas partida, estos items se suman a lo que cargaste
    # o si no hay partida, empiezas con ellos. Está bien para aprender.
    jugador.añadir_al_inventario("Poción de vida", 5)
    jugador.añadir_al_inventario("Escudo", 3)
    
    goblin = Enemigo("Goblin", 50, 8, 30)
    dragon = Jefe("Dragón Ancianor", 200, 30)
    
    enemigos = [goblin, dragon]
    
    print("¡Bienvenido al RPG simple!")
    print("Enemigos disponibles:")
    for i, e in enumerate(enemigos):
        print(f"{i+1}. {e.nombre} (Vida: {e._vida}, Fuerza: {e.fuerza})")
    
    while True:
        if not enemigos:
            print("\n¡Victoria total! Has derrotado a todos los enemigos.")
            break
        
        eleccion = input("\nElige enemigo (número) o 's' para salir: ").strip()
        if eleccion.lower() == 's':
            print("¡Hasta la próxima aventura!")
            break
        
        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(enemigos):
                enemigo = enemigos[idx]
                combate(jugador, enemigo)
                if not enemigo.esta_vivo():
                    enemigos.pop(idx) 
                    # Guarda el progreso cada vez que ganas
                    jugador.guardar_partida()
            else:
                print("Número inválido.")
        except ValueError:
            print("Ingresa un número válido o 's' para salir.")
        
        print(f"\nEstado de {jugador.nombre}:")
        print(jugador)
        
        if not jugador.esta_vivo():
            print("GAME OVER - Partida no guardada.")
            break
        # Aquí quitamos el guardar_partida() para que solo guarde si ganas (línea 197)
        # o si tú quieres guardar manualmente antes de salir.

# Ejecuta el juego
juego_principal()
# CORRECCIÓN 3: Aquí borré la línea "quitar_item" que sobraba.
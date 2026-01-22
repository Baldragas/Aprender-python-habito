import unicodedata
import json
import os # Importado para verificar si existe el archivo de guardado

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
        # CORRECCIÓN: La vida máxima se basa en la vida inicial
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
                print(f"{self.nombre} recupera {curacion} de vida, ahora tiene {self._vida}/{self.vida_max}")
        else:
            print(f"No tienes suficiente {nombre} para gastar")

    def mostrar_inventario(self):
        print(self.inventario)
    
    def recibir_daño(self, cantidad):
        daño_real = cantidad
        # CORRECCIÓN: Verifica si hay escudo antes de calcular daño
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
        return f"{self.nombre} (Vida: {self._vida}/{self.vida_max}, Fuerza: {self.fuerza})\n{self.inventario}"

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
        print(">> Partida guardada.")

    def cargar_partida(self, archivo='partida.json'):
        if not os.path.exists(archivo):
            print("No hay partida guardada. Iniciando juego nuevo...")
            return False

        try:
            with open(archivo, 'r') as f:
                estado = json.load(f)

            # Reconstrucción de argumentos básicos
            args_init = {
                'nombre': estado.get('nombre'),
                'vida': estado.get('vida'),
                'fuerza': estado.get('fuerza')
            }

            # CORRECCIÓN: Eliminadas líneas duplicadas
            tipo = estado.get('tipo_clase', 'Personaje')
            Clase = CLASES.get(tipo, Personaje)
            nueva = Clase(**args_init)
            
            # Restaurar atributos específicos
            if 'furia' in estado:
                nueva.furia = estado['furia']
            if 'fuerza_base' in estado:
                nueva.fuerza_base = estado['fuerza_base']
            if 'inventario' in estado:
                nueva.inventario.items = estado['inventario']
            if 'vida_max' in estado:
                nueva.vida_max = estado['vida_max']
            
            # Actualizar el objeto actual
            self.__dict__.update(nueva.__dict__)
            print(">> Partida cargada exitosamente.")
            return True
        except Exception as e:
            print(f"Error al cargar partida: {e}")
            return False

class Enemigo(Personaje):
    def __init__(self, nombre, vida, fuerza, experiencia_otorgada):
        super().__init__(nombre, vida, fuerza)
        self.experiencia = experiencia_otorgada

    def otorgar_experiencia(self):
        if not self.esta_vivo():
            return self.experiencia
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
        return f"{self.nombre} (Vida: {self._vida}/{self.vida_max}, Fuerza: {self.fuerza}, Furia: {self.furia})\n{self.inventario}"

class Jefe(Personaje):
    def __init__(self, nombre, vida, fuerza_base):
        super().__init__(nombre, vida, fuerza_base)
        self.fuerza_base = fuerza_base

    def atacar(self, objetivo):
        daño = int(1.5 * self.fuerza_base) # Convertido a int para limpieza visual
        print(f"{self.nombre} ataca con FURIA a {objetivo.nombre} causando {daño} de daño")
        objetivo.recibir_daño(daño)

# Diccionario para mapear nombres de clases a tipos
CLASES = {
    'Personaje': Personaje,
    'Enemigo': Enemigo,
    'Guerrero': Guerrero,
    'Jefe': Jefe
}

def combate(jugador, enemigo):
    print(f"\n=== Combate inicia: {jugador.nombre} vs {enemigo.nombre} ===")
    
    while jugador.esta_vivo() and enemigo.esta_vivo():
        print(f"\nTurno de {jugador.nombre} (Vida: {jugador._vida}/{jugador.vida_max})")
        print(f"{enemigo.nombre} - Vida: {enemigo._vida}/{enemigo.vida_max}")
        print("1. Atacar | 2. Usar item | 3. Huir")
        
        eleccion = input("Elige: ").strip()
        
        if eleccion == '1':
            jugador.atacar(enemigo)
        elif eleccion == '2':
            jugador.mostrar_inventario()
            item = input("Nombre del item a usar: ").strip()
            jugador.usar_item(item, 1)
        elif eleccion == '3':
            print("¡Huyes del combate!")
            return False # Indica que huyó
        else:
            print("Opción inválida.")
            continue
        
        if not enemigo.esta_vivo():
            print(f"¡{enemigo.nombre} ha sido derrotado!")
            break
        
        # Turno del enemigo
        print(f"\n>> Turno de {enemigo.nombre}")
        enemigo.atacar(jugador)
        if not jugador.esta_vivo():
            print(f"{jugador.nombre} ha caído en combate...")
            break
    
    print("Combate terminado.")
    return True # Indica combate finalizado normalmente

def juego_principal():
    # Inicializamos jugador base
    jugador = Guerrero("Conan", 120, 40)
    
    # Intentamos cargar. Si devuelve False (no existe archivo), le damos items iniciales.
    # Si devuelve True, usamos lo que viene en el archivo.
    if not jugador.cargar_partida():
        print("Iniciando inventario básico...")
        jugador.añadir_al_inventario("Poción de vida", 5)
        jugador.añadir_al_inventario("Escudo", 3)
    
    goblin = Enemigo("Goblin", 50, 8, 30)
    dragon = Jefe("Dragón Anciano", 200, 30)
    
    enemigos = [goblin, dragon]
    
    print("\n¡Bienvenido al RPG!")
    
    while True:
        if not enemigos:
            print("\n¡Victoria total! Has derrotado a todos los enemigos.")
            # Borrar partida al ganar para reiniciar en el futuro (opcional)
            # if os.path.exists('partida.json'): os.remove('partida.json')
            break
        
        print("\nEnemigos disponibles:")
        for i, e in enumerate(enemigos):
            print(f"{i+1}. {e.nombre} (Vida: {e._vida})")
        
        eleccion = input("\nElige enemigo (número) o 's' para salir: ").strip()
        if eleccion.lower() == 's':
            jugador.guardar_partida()
            print("Partida guardada. ¡Hasta la próxima!")
            break
        
        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(enemigos):
                enemigo = enemigos[idx]
                resultado = combate(jugador, enemigo)
                
                # Si huyó (resultado False), no hacemos nada
                # Si murió el enemigo, lo sacamos de la lista
                if not enemigo.esta_vivo():
                    enemigos.pop(idx)
                    # Guardado automático al vencer
                    jugador.guardar_partida() 
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida.")
        
        if not jugador.esta_vivo():
            print("\nGAME OVER")
            # Opcional: Borrar partida al morir
            break

if __name__ == "__main__":
    juego_principal()
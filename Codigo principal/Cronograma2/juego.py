import entidades
import mapa
from combate import combate
from entidades import normalize
from entidades import Item
import random

class Juego:
    def __init__(self):
        self.jugador = None
        self.mapa = None
        self.jugando = True

    def validar_item(self, nombre_objeto: str) -> bool:
        """
        Devuelve True si el ítem está disponible en la habitación actual.
        """
        sala = self.mapa.habitacion_actual
        nombre_norm = normalize(nombre_objeto)
        return any(normalize(obj.nombre) == nombre_norm for obj in sala.objetos)
        

    def configurar(self):
        self.crear_jugador()
        self.crear_items_iniciales()
        enemigos = self.crear_enemigos()
        self.crear_mapa_y_habitaciones(enemigos)

    # ------------------------------------------------------------
    # MÉTODOS AUXILIARES (privados)
    # ------------------------------------------------------------
    def crear_jugador(self):
        self.jugador = entidades.Guerrero("Conan", 120, 40)
        self.jugador.cargar_partida(entidades.CLASES)
    def crear_items_iniciales(self):
        # Escudo (nuevo: se añade al inventario)
        escudo = entidades.Item.crear_escudo()
        self.jugador.añadir_item_objeto(escudo, 1)
        print(f"Escudo añadido: {escudo} (protección {escudo.propiedades.get('proteccion', 0)})")

        # Pociones
        pocion_fuerza = entidades.Item.crear_pocion_fuerza()
        self.jugador.añadir_item_objeto(pocion_fuerza, 2)
        pocion_menor = entidades.Item.crear_pocion_menor()
        self.jugador.añadir_item_objeto(pocion_menor, 2)
        

    def crear_enemigos(self):
        ent = entidades.Enemigo("Ent anciano", 120, 25, 30)
        esqueleto = entidades.Enemigo("Esqueleto guerrero", 80, 18, 20)
        pez = entidades.Enemigo("Pez grande", 50, 15, 10)
        dragon = entidades.Jefe("Dragón Ancianor", 200, 30)
        goblin = entidades.Enemigo("Goblin de polvo", 40, 10, 5)
        slime = entidades.Enemigo("Slime mediano", 60, 20, 15)
        # Podríamos devolver un dict para identificarlos fácilmente
        return {
            "dragon": dragon,
            "goblin": goblin,
            "slime": slime,
            "ent": ent,
            "esqueleto": esqueleto,
            "pez": pez
        }

    def crear_mapa_y_habitaciones(self, enemigos):
        # Crear habitaciones con los enemigos
        sala_inicio = mapa.Habitacion("Entrada", "Una cueva oscura.")
        sala_media = mapa.Habitacion(
            "Cuarto abandonado",
            "Un cuarto polvoriento y oscuro",
            enemigo=enemigos["goblin"]
        )
        sala_oeste = mapa.Habitacion("Sala de slimes", 
        "Una sala en ruinas invadida por telas de araña y slime's",
        enemigo=enemigos["slime"])
        pocion_mediana = entidades.Item.crear_pocion_mediana()
        sala_oeste.objetos.append(pocion_mediana)
        sala_boss = mapa.Habitacion(
            "Altar",
            "El cubil del dragón.",
            enemigo=enemigos["dragon"]
        )
        sala_bosque = mapa.Habitacion("Bosque encantado", "Un bosque con árboles que susurran.", enemigo = enemigos["ent"])
        sala_cripta = mapa.Habitacion("Cripta", "Una tumba antigua con ecos de batallas.", enemigo=enemigos["esqueleto"])
        sala_laguna = mapa.Habitacion("Laguna subterranéa", "Un lago oscuro con aguas misteriosas.", enemigo=enemigos["pez"])

        # Añadir objetos a las salas
        sala_inicio.objetos.extend([
            Item("Poción pequeña", "poción", curacion=20),
            Item("Llave oxidada", "llave")
        ])
        sala_media.objetos.append(Item("Espada rota", "arma", daño=20))
        sala_bosque.objetos.extend([
            Item("FLor amarilla", "tesoro", 80),
            entidades.Item.crear_pocion_mayor()
        ])
        sala_cripta.objetos.extend([
            Item("Collar de oro", "tesoro", valor=80),
            Item("Espada oxidada", "arma", daño=15)
        ])
        sala_laguna.objetos.extend([
            Item("Pocion de defensa", "defensa", proteccion=5),
            Item("Perla", "tesoro", valor=60)
        ])
        # Conectar habitaciones
        mapa.conectar_mutua(sala_inicio, "norte", sala_media, "sur")
        mapa.conectar_mutua(sala_media, "este", sala_boss, "oeste")
        mapa.conectar_mutua(sala_media, "oeste", sala_oeste, "este")
        mapa.conectar_mutua(sala_inicio, "este", sala_bosque, "oeste")
        mapa.conectar_mutua(sala_boss, "sur", sala_cripta, "norte")
        mapa.conectar_mutua(sala_oeste,"sur", sala_laguna, "norte")

        # Agregar al mapa
        self.mapa = mapa.Mapa()
        self.mapa.agregar_habitacion(sala_inicio)
        self.mapa.agregar_habitacion(sala_media)
        self.mapa.agregar_habitacion(sala_oeste)
        self.mapa.agregar_habitacion(sala_boss)
        self.mapa.agregar_habitacion(sala_bosque)
        self.mapa.agregar_habitacion(sala_cripta)
        self.mapa.agregar_habitacion(sala_laguna)
        self.mapa.habitacion_actual = sala_inicio

    def _examinar_habitacion(self):
        sala = self.mapa.habitacion_actual  # ¿Cómo obtenemos la sala actual?
        if not sala.objetos:
            print("No hay objetos aquí.")
        else:
            print("Ves en el suelo:")
            for objeto in sala.objetos:
                print(f"  - {objeto.nombre}")

    def recoger_objeto(self, nombre_objeto):
        sala = self.mapa.habitacion_actual
        nombre_norm = normalize(nombre_objeto)
        encontrado = None
        for obj in sala.objetos:
            if normalize(obj.nombre) == nombre_norm:
                encontrado = obj
                break
        if encontrado:
            sala.objetos.remove(encontrado)
            self.jugador.añadir_item_objeto(encontrado, 1)
            print(f"Recoges {encontrado.nombre}.")
        else:
            print(f"No hay ningún {nombre_objeto} aquí")
        
    def gestionar_movimiento(self, direccion):
        # 1. Intentamos mover al personaje usando el método de Mapa
        if self.mapa.mover(direccion):
            sala_actual = self.mapa.habitacion_actual
            sala_actual.visitada = True
            
            # 2. Verificamos si hay un enemigo vivo en la nueva sala
            if sala_actual.enemigo and sala_actual.enemigo.esta_vivo():
                print(f"¡Un {sala_actual.enemigo.nombre} aparece!")
                
                # 3. Llamamos al combate (importado de combate.py)
                resultado = combate(self.jugador, sala_actual.enemigo)
                
                if resultado == "victoria":
                    sala_actual.enemigo = None
                    self.jugador.guardar_partida()
                
                elif resultado == "huida":
                    opciones = list(sala_actual.salidas.keys())
                    escape = random.choice(opciones)
                    self.mapa.mover(escape)
                    print(f"¡Huyes despavorido y terminas en: {self.mapa.habitacion_actual.nombre}!")
                
                elif resultado == "derrota":
                    print("Has caído en batalla...")
                    self.jugando = False
            return True
        else:
            print(f"No hay salida hacia el {direccion}.")
            return False

    def bucle_principal(self):
        while self.jugando and self.jugador.esta_vivo():
            print(f"\n--- {self.mapa.habitacion_actual.nombre} ---")
            print(self.mapa.habitacion_actual.descripcion)
            
            entrada = input("\n¿Qué quieres hacer?: ").lower().strip()
            partes = entrada.split(" ", 1) # Separa "usar pocion" en ["usar", "pocion"]
            comando = partes[0]
            argumento = partes[1] if len(partes) > 1 else None

            if comando == "salir":
                self.jugador.guardar_partida()
                break

            elif comando == "inventario":
                self.jugador.mostrar_inventario()

            elif comando == "usar" and argumento:
                # Acceso directo: "usar pocion"
                self.jugador.usar_item(argumento)

            elif comando == "equipar" and argumento:
                # Nuevo comando: "equipar escudo"
                self.jugador.equipar_item(argumento)

            elif comando == "recoger" and argumento:
                self.recoger_objeto(argumento)

            elif comando in ["norte", "sur", "este", "oeste"]:
                self.gestionar_movimiento(comando)
            
        print("Fin de la aventura.")
                # Usa self.jugador y self.mapa

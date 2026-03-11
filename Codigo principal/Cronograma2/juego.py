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

    def bucle_principal(self):
        while self.jugando and self.jugador.esta_vivo():
            print(f"\n--- {self.mapa.habitacion_actual.nombre} ---")
            print(self.mapa.habitacion_actual.descripcion)
            print("Comandos: norte/sur/este/oeste/mapa/inventario/examinar/recoger <objeto>/salir")
            accion = (input("¿A dónde ir?: ")).lower().strip()
            if accion == "salir":
                self.jugador.guardar_partida()
                break
            
            elif accion == "inventario":
                if self.jugador.mostrar_inventario():
                    while True:
                        usar = input("¿Quieres usar algo? (s/n)").lower().strip()
                        if usar in ("s", "si", "sí", "y", "yes"):
                            item = normalize(input("¿Qué item quieres usar?: "))
                            self.jugador.usar_item(item, 1)
                            break
                        elif usar in ("n", "no", "salir"):
                            print("Volviendo al menú principal.")
                            break
                        else:
                            print("Respuesta no reconocida. Escribe 's' (sí) o 'n' (no).")
                continue

            elif accion == "mapa":
                print(self.mapa.dibujar_mapa_bonito())
                continue

            elif accion == "examinar":
                self._examinar_habitacion()

            elif accion.startswith("recoger "):
                nombre_objeto = accion[8:].strip()
                self.recoger_objeto(nombre_objeto)

            elif self.mapa.mover(accion):
                sala_actual = self.mapa.habitacion_actual
                sala_actual.visitada = True
                
                # ¿Hay alguien aquí para pelear?
                if sala_actual.enemigo is not None:
                    enemigo_presente = sala_actual.enemigo
                    print(f"¡Un {enemigo_presente.nombre} aparece!")
                    resultado = combate(self.jugador, enemigo_presente)   # <--- guardamos resultado
                    if resultado == "huida":
                        salidas = list(sala_actual.salidas.keys())  # sala_actual es la del combate
                        if salidas:
                            direccion = random.choice(salidas)
                            self.mapa.mover(direccion)
                            print(f"¡Escapas en dirección {direccion}!")
                            
                            # AHORA comprobamos la NUEVA sala
                            sala_nueva = self.mapa.habitacion_actual
                            if sala_nueva.enemigo is not None and sala_nueva.enemigo.esta_vivo():
                                print(f"¡Y caes justo donde {sala_nueva.enemigo.nombre} te espera!")
                                resultado2 = combate(self.jugador, sala_nueva.enemigo)
                                if resultado2 == "victoria":
                                    sala_nueva.enemigo = None
                                elif resultado2 == "derrota":
                                    break
                        else:
                            print("¡No hay salida! Estás atrapado.")
                    
                    elif resultado == "derrota":
                        print("Has caído en batalla...")
                        break
                    
                    elif resultado == "victoria":
                        # El enemigo ha muerto, lo quitamos de la sala
                        sala_actual.enemigo = None
                        self.jugador.guardar_partida()
            else:
                print(f"No hay salida en la dirección: {accion} (o comando no reconocido)")
        print("Fin de la aventura.")
                # Usa self.jugador y self.mapa

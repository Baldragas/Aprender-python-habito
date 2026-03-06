import entidades
import mapa
from combate import combate
from entidades import normalize
from entidades import Item

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
        self._crear_jugador()
        self._crear_items_iniciales()
        enemigos = self._crear_enemigos()
        self._crear_mapa_y_habitaciones(enemigos)

    # ------------------------------------------------------------
    # MÉTODOS AUXILIARES (privados)
    # ------------------------------------------------------------
    def _crear_jugador(self):
        self.jugador = entidades.Guerrero("Conan", 120, 40)
        self.jugador.cargar_partida(entidades.CLASES)
    def _crear_items_iniciales(self):
        # Escudo (nuevo: se añade al inventario)
        escudo = entidades.Item.crear_escudo()
        self.jugador.añadir_item_objeto(escudo, 1)
        print(f"Escudo añadido: {escudo} (protección {escudo.propiedades.get('proteccion', 0)})")

        # Pociones
        pocion_fuerza = entidades.Item.crear_pocion_fuerza()
        self.jugador.añadir_item_objeto(pocion_fuerza, 2)
        pocion_menor = entidades.Item.crear_pocion_menor()
        self.jugador.añadir_item_objeto(pocion_menor, 2)
        

    def _crear_enemigos(self):
        dragon = entidades.Jefe("Dragón Ancianor", 200, 30)
        goblin = entidades.Enemigo("Goblin de polvo", 40, 10, 5)
        slime = entidades.Enemigo("Slime mediano", 60, 20, 15)
        # Podríamos devolver un dict para identificarlos fácilmente
        return {
            "dragon": dragon,
            "goblin": goblin,
            "slime": slime
        }

    def _crear_mapa_y_habitaciones(self, enemigos):
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

        # Añadir objetos a las salas
        sala_inicio.objetos.extend([
            Item("Poción pequeña", "poción", curacion=20),
            Item("Llave oxidada", "llave")
        ])
        sala_media.objetos.append(Item("Espada rota", "arma", daño=20))

        # Conectar habitaciones
        mapa.conectar_mutua(sala_inicio, "norte", sala_media, "sur")
        mapa.conectar_mutua(sala_media, "este", sala_boss, "oeste")
        mapa.conectar_mutua(sala_media, "oeste", sala_oeste, "este")

        # Agregar al mapa
        self.mapa = mapa.Mapa()
        self.mapa.agregar_habitacion(sala_inicio)
        self.mapa.agregar_habitacion(sala_media)
        self.mapa.agregar_habitacion(sala_boss)
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
            accion = (input("¿A dónde ir?: "))
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
                    
                    # LLAMADA AL COMBATE
                    combate(self.jugador, enemigo_presente)
                    
                    if not enemigo_presente.esta_vivo():
                        # Si el enemigo muere, lo quitamos de la  para que no "reviva" al volver
                        sala_actual.enemigo = None 
                        self.jugador.guardar_partida()
                    elif not self.jugador.esta_vivo():
                        print("Has caído en batalla...")
                        break
            else:
                print("No hay salida en esa dirección.")

        print("Fin de la aventura.")
                # Usa self.jugador y self.mapa

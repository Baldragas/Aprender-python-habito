from entidades import Guerrero, Enemigo, Jefe, CLASES
from mapa import Habitacion, Mapa, conectar_mutua
from objetos import Item
from combate import combate
from juego import Juego


if __name__ == "__main__":
    print("no olvides programar mañana, cara e monda")
    juego = Juego()
    juego.configurar()
    juego.bucle_principal()
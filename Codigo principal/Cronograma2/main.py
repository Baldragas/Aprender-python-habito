from entidades import Guerrero, Enemigo, Jefe, CLASES
from mapa import Habitacion, Mapa, conectar_mutua
from objetos import Item
from combate import combate
from juego import Juego


if __name__ == "__main__":
    juego = Juego()
    juego.configurar()
    juego.bucle_principal()
print(f"recuerda programar mañanana bastardo, basura")
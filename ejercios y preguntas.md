import json
#EJERCICIO 1:

# datos_nave = {'piloto': 'Useless',
# 'combustible': 40
# }


# estado = json.dumps(datos_nave)
# print(f"guardado estado: {estado}")


# # super().__init__("Nave de Carga", 100)
# # inventario.pop("combustible")

#Ejercicio 2:

# class Personaje:

#     def __init__(self, nombre, vida):
#         self.nombre = nombre
#         self.vida = vida


#     def guardar(self, nombre_archivo):
#         datos = {
#             'nombre': self.nombre,
#             'vida': self.vida
#         }

#         with open ('guardado.json', 'w') as f:
#             estado = json.dump(datos, f)

# En el bucle principal de tu juego, si quieres que el programa no se rompa cuando el usuario escribe una letra en lugar de un número, 
# ¿qué bloque de "control de errores" deberías usar?
# Realmente no lo se, quizas agregar un try y una excepcion si el usuario escribe un letra, 
# en el codigo principal hay while true que hace que vuelva a pedir una entrada si salta una excepcion, 
# pero realmente yo solo rellene huecos de codigo, no cree la logica, asi que tengo mucha idea.

#Ejercicio 3:

class Personaje:
    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida
    
    def guardar(self, nombre_archivo):
        datos = {
            'nombre': self.nombre,
            'vida': self.vida
        }

        with open ('guardado.json', 'w') as f:
            estado = json.dump(datos, f, indent=4)

    def cargar(self, nombre_archivo):
        with open ('guardado.json', 'r') as f:
            datos = json.load(f)
       
            self.nombre = datos['nombre']
            self.vida = datos['vida']
            
            print("¡Datos cargados con éxito!")

Heroe = Personaje('Conan', 100)
Heroe.guardar('guardado.json')
Heroe.cargar('guardado.json')


# Si quieres que una clase Guerrero use exactamente la misma lógica de __init__ que Personaje,
# pero añadiendo un atributo nuevo llamado furia,
# ¿cómo escribirías esa línea de super() que corregimos antes?
# super().__init__(nombre, vida, furia):



#El Import: ¿Cómo traes la clase Personaje desde el archivo entidades.py al archivo main.py?
from entidades import Personaje
#La Ejecución: Tienes limpiar_pantalla() en herramientas.py. ¿Cómo la importas y cómo la activas?
from herramientas import limpiar_pantalla
#Spacing (Memoria de 7 días): ¿Qué método especial (__???__) se usa para que un objeto se imprima como texto bonito y no como <__main__.Objeto at 0x...>?
__str__


from personaje import Guerrero
import personaje
#No se a que te refieres con acceder quiero decir, podria crear un objeto Guerrero
player = Guerrero("Conan", 100, 40)

import json: # en entidades

from entidades import Guerrero, Enemigo, Jefe: main, pero falta personaje, no?

import unicodedata: #entidades

¿Qué pasa si olvidas poner import json en el archivo donde está el método guardar_partida?

Que no puedo usar el modulo de json y por tanto fallaria el sistema de guardado y carga que hace uso de ese modulo

¿Qué clase creará el sistema por defecto según tu código? (Pista: Mira el segundo argumento de tu .get()).
Python
Esta respuesta la se, aunque tu "pista" tecnicamente da de manera directa la respuesta, en fin, la clase por defecto que se crea es Personaje

¿En qué archivo escribirías la definición del método def grito_de_guerra(self):?
en entidades por supuesto que es donde esta la clase guerrero, bueno y todas las demas.
Si en main.py tienes un objeto enemigo = Enemigo(...), ¿podrías llamar a enemigo.grito_de_guerra()? ¿Por qué?
No podria porque grito de guerra es una funcion unica de la clase guerrero, aunque, si enemigo heredara a guerrero si que podria, pero este no es el caso.
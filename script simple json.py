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

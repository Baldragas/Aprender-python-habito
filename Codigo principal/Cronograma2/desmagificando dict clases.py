import entidades
class Guerrero:
    def __init__(self, nombre):
        self.nombre = nombre

print(type(Guerrero))  #class 'type', entiendo que es una clase, pero no entiendo el type en lo que imprime
print(Guerrero)        #<class '__main__.Guerrero'>
print(Guerrero("Conan"))  #<__main__.Guerrero object at 0x0000025BF32E8050>
# Para mi la mayoria de estos prints de arriba son ilegibles, quiero decir, lo unico que entiendo es que son tipo clase,
#
clases_dict = {'Guerrero': Guerrero}
print(clases_dict['Guerrero']) #<class '__main__.Guerrero'>

# ¿Qué crees que hace esto?
ClaseElegida = clases_dict['Guerrero']
personaje = ClaseElegida("Conan")
print(personaje.nombre)  # Conan


# VERSIÓN A: Tu diccionario CLASES
def crear_personaje_diccionario(tipo, nombre, vida, fuerza):
    Clase = CLASES.get(tipo, Personaje)
    return Clase(nombre, vida, fuerza)

# VERSIÓN B: If/elif tradicional  
def crear_personaje_if(tipo, nombre, vida, fuerza):
    if tipo == 'Personaje':
        return Personaje(nombre, vida, fuerza)
    elif tipo == 'Guerrero':
        return Guerrero(nombre, vida, fuerza)
    elif tipo == 'Enemigo':
        return Enemigo(nombre, vida, fuerza, experiencia=10)
    elif tipo == 'Jefe':
        return Jefe(nombre, vida, fuerza)
    else:
        return Personaje(nombre, vida, fuerza)

# En guardar_partida() (línea ~78):
# 'estado': {
#     'nombre': self.nombre,
#     'vida': self._vida,
#     'fuerza': self.fuerza,
#     'tipo_clase': type(self).__name__,
#     'inventario': self.inventario.items
#     # ¿Dónde está experiencia_otorgada?
# }

#📈 ACTUALIZACIÓN DE COMPRENSIÓN:

# Lo que YA sabes:

#     Las clases son objetos en Python

#     Puedes guardarlas en diccionarios

#     El diccionario CLASES mapea strings a clases

# Lo que VAMOS a desmagificar:

#     Cómo manejar argumentos diferentes por clase

#     Cómo serializar/deserializar atributos específicos de cada clase

#     Patrones de diseño para sistemas extensibles
class Habitacion:
    def __init__(self, nombre, descripcion, enemigo=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.enemigo = enemigo
        self.salidas = {}
        self.objetos = []  # Nuevo: lista de nombres de objetos
        self.visitada = False
    
    def agregar_objeto(self, nombre_objeto):
        self.objetos.append(nombre_objeto)
    
    def tiene_objetos(self):
        return len(self.objetos) > 0

def buscar_objeto(self, nombre_objeto):
    if nombre_objeto in self.objetos:
        return True


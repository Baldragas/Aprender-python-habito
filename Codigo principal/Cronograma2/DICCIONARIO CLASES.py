# if tipo == 'Guerrero':
#     nueva = Guerrero(**args_init)
# elif tipo == 'Enemigo':
#     nueva = Enemigo(**args_init)
# elif tipo == 'Jefe':
#     nueva = Jefe(**args_init)
# else:
#     nueva = Personaje(**args_init)

class Guerrero:
    def __init__(self, nombre):
        self.nombre = nombre

print("1.", type(Guerrero))
print("2.", Guerrero) 
print("3.", Guerrero("Conan"))

palabra = "Tu quiere sexo mami?"
print(f"{palabra:10.10}")

def mostrar_info(**kwargs):
    # Completa: ¿Cómo iterar sobre kwargs?
    for clave, valor in kwargs.items():
        print(f"{clave}: {valor}")

mostrar_info(vida=100, fuerza=20, defensa=5)
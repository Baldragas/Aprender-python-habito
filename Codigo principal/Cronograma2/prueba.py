# class Personaje:
#     def __init__(self, nombre, vida, fuerza):
#         self.nombre = nombre
#         # Usamos el nombre "público" para que pase por la aduana desde el inicio
#         self.vida = vida
#         self.fuerza = fuerza

#     # 1. LA ADUANA DE SALIDA (Getter)
#     # Sirve para leer el valor. Se usa el decorador @property
#     @property
#     def vida(self):
#         # Aquí devolvemos el valor real que está oculto en _vida
#         return self.vida

#     # 2. LA ADUANA DE ENTRADA (Setter)
#     # Aquí es donde pones las reglas de seguridad.
#     @vida.setter
#     def vida(self, valor_nuevo):
#         print(f"DEBUG: Intentando cambiar vida a {valor_nuevo}...")
        
#         if valor_nuevo < 0:
#             print("  ¡Alarma! Intento de vida negativa. Ajustando a 0.")
#             self.vida = 0
#         elif valor_nuevo > 200:
#             self.vida = 200
#         else:
#             self.vida = valor_nuevo
#     @property
#     def fuerza(self):
#             return self.fuerza

#     @fuerza.setter
#     def fuerza(self, valor_nuevo):
#         print(f"DEBUG: Intentando cambiar fuerza a {valor_nuevo}...")
#         if valor_nuevo < 1:
#             print("La fuerza no puede ser menor a uno reajustando a valor por defecto: 1")
#             self.fuerza = 1
#         elif valor_nuevo > 100:
#             print("No se puede tener fuerza mayor a 100, reajustando a 100")
#             self.fuerza = 100
#         else:
#             self.fuerza = valor_nuevo
# # --- PRUEBA DE FUEGO ---

# heroe = Personaje("Arturo", 100, 250)

# # El usuario no sabe que hay una aduana, él solo escribe:
# heroe.vida = 200

# print(f"Resultado final: La vida de {heroe.nombre} es {heroe.vida}")

@vida.setter
    def vida(self, valor_nuevo):
        if valor_nuevo < 0:
            self.vida = 0
        else:
            self.vida = 0

    @fuerza.setter
    def fuerza(self, valor_nuevo):
        if valor_nuevo < 1:
            self.fuerza = 1
        elif valor_nuevo > 100:
            self.fuerza = 100
        else:
            self.fuerza = valor_nuevo
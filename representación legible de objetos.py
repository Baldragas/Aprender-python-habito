class Personaje:
    def __init__(self, nombre, vida, fuerza):
        self.nombre = nombre
        self.vida = vida
        self.fuerza = fuerza
    
    def recibir_daño(self, cantidad):
        self.vida = max(0, self.vida - cantidad)
        print(f"{self.nombre} recibe {cantidad} de daño. Vida restante: {self.vida}")

    def esta_vivo(self):
        return self.vida > 0

    def atacar(self, objetivo):
        print(f"{self.nombre} ataca a {objetivo.nombre} causando {self.fuerza} de daño")
        objetivo.recibir_daño(self.fuerza)

    def __str__(self):
        return f"{self.nombre} (Vida: {self.vida}, Fuerza: {self.fuerza})"
# --- Prueba del código (no modifiques esta parte) ---
heroe = Personaje("Arthur", 70, 20)
enemigo = Personaje("Goblin", 10, 8)

print(heroe)      # → Arthur (Vida: 70, Fuerza: 20)
print(enemigo)    # → Goblin (Vida: 10, Fuerza: 8)

heroe.atacar(enemigo)
print(enemigo)    # → Goblin (Vida: 0, Fuerza: 8)
class Habitacion:
    def __init__(self, nombre, descripcion, enemigo=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.enemigo = enemigo
        self.salidas = {}
        self.objetos = []
        self.visitada = False # Para el sistema de narrativa única

    def agregar_salida(self, direccion, habitacion_destino):
        self.salidas[direccion] = habitacion_destino

    def __str__(self):
        salidas_str = ", ".join(self.salidas.keys())
        return f"--- {self.nombre} ---\n{self.descripcion}\nSalidas: {salidas_str}"

class Mapa:
    def __init__(self):
        self.habitaciones = {} 
        self.habitacion_actual = None

    def agregar_habitacion(self, habitacion):
        self.habitaciones[habitacion.nombre] = habitacion
        if self.habitacion_actual is None:
            self.habitacion_actual = habitacion

    def mover(self, direccion):
        if direccion in self.habitacion_actual.salidas:
            self.habitacion_actual = self.habitacion_actual.salidas[direccion]
            return True
        return False
    def dibujar_mapa_bonito(self):
        """Versión simplificada pero visual del mapa"""
        # Primero, verificar si hay habitaciones visitadas
        habitaciones_visitadas = [h for h in self.habitaciones.values() if h.visitada]
        
        if not habitaciones_visitadas:
            return "Aún no has explorado nada del mapa."
        
        # Construir el marco del mapa
        mapa_str = "┌───────────────────────────────────┐\n"  # Más ancho
        mapa_str += "│           MAPA DEL                 │\n"
        mapa_str += "│           CALABOZO                 │\n"
        mapa_str += "├───────────────────────────────────┤\n"
        
        for hab in habitaciones_visitadas:
            simbolo = "★" if hab is self.habitacion_actual else "○"
            enemigo = " "
            if hab.enemigo and hasattr(hab.enemigo, 'esta_vivo'):
                if hab.enemigo.esta_vivo():
                    # Verificar si está herido (vida < 50% de vida máxima)
                    if hasattr(hab.enemigo, '_vida') and hasattr(hab.enemigo, 'vida_max'):
                        vida_actual = hab.enemigo._vida
                        vida_maxima = hab.enemigo.vida_max
                        
                        if vida_maxima > 0 and vida_actual < vida_maxima * 0.5:
                            enemigo = "🩸"  # Enemigo herido
                        else:
                            enemigo = "⚔"   # Enemigo saludable
                    else:
                        enemigo = "⚔"  # No podemos calcular porcentaje
            # NUEVA lógica:
            if hasattr(hab, 'objetos') and hab.objetos:
                objetos = f"🎒x{len(hab.objetos)}"
            else:
                objetos = " "
            
            # Más espacio para nombres (18 caracteres)
            nombre_truncado = hab.nombre[:18] if len(hab.nombre) > 18 else hab.nombre
            
            # Ajustar formato para el nuevo ancho
            mapa_str += f"│ {simbolo} {nombre_truncado:18} {enemigo}{objetos} │\n"
        
        mapa_str += "└───────────────────────────────────┘\n"
        mapa_str += "Leyenda: ★=Tú  ○=Visitada  ⚔=Enemigo  🩸=Enemigo herido  🎒=Objetos\n"
        
        return mapa_str
        
def conectar_mutua(hab1, direccion1, hab2, direccion2):
    """Conecta dos habitaciones en ambas direcciones."""
    hab1.agregar_salida(direccion1, hab2)
    hab2.agregar_salida(direccion2, hab1)
    
    
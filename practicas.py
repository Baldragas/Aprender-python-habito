# clases.py

    def cargar_partida(self, archivo='partida.json'):
        if not os.path.exists(archivo):
            return False

        try:
            with open(archivo, 'r') as f:
                estado = json.load(f)

            # 1. Identificar la clase necesaria (Escalabilidad)
            tipo = estado.get('tipo_clase', 'Personaje')
            Clase = CLASES.get(tipo, Personaje)# ??? [cite_start]Accede al diccionario global CLASES usando la variable 'tipo' [cite: 312]

            # 2. Reinstanciación técnica para asegurar métodos limpios
            # Extraemos los datos básicos del diccionario 'estado'
            nombre = estado.get('nombre')
            vida = estado.get('vida')
            fuerza = estado.get('fuerza')
            
            # Creamos el objeto temporal con los argumentos correctos
            temporal = Clase(nombre, vida, fuerza)# ??? [cite_start]Instancia la 'Clase' con nombre, vida y fuerza [cite: 312]

            # 3. Sincronización profunda del Inventario
            # No queremos copiar el objeto, queremos copiar sus DATOS
            if 'inventario' in estado:
                temporal.inventario.items = estado['inventario']
                # El estado['inventario'] es un dict de items
                # Debemos asignar ese dict directamente a la propiedad .items del inventario de 'temporal'
                # ??? [cite_start]Accede a temporal.inventario.items y asígnale estado['inventario'] [cite: 294, 312]
            
            # 4. Transferencia de estado final al objeto actual
            self.__dict__.update(temporal.__dict__)
            
            print(f">> Sistema: Datos de {self.nombre} ({tipo}) restaurados.")
            return True
        except Exception as e:
            print(f"CRITICAL_ERROR en persistencia: {e}")
            return False
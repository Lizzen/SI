class State:
    def __init__(self, state_id):
        self.id = state_id  # Usamos snake_case para seguir convenciones Python
    
    def Start(self):
        print(f"Inicio del estado: {self.id}")  # Corregido f-string
    
    def Update(self, perception):
        # Devuelve una tupla con (acción, disparo)
        # Acción 0 = ninguna, disparo = False por defecto
        return 0, False  # Valor más seguro por defecto
    
    def Transit(self, perception):
        # Por defecto mantiene el mismo estado
        return self.id
    
    def End(self):
        print(f"Fin del estado: {self.id}")  # Corregido f-string
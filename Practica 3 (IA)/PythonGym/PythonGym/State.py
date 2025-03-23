# David Ferreras Díaz y Pablo Padial Iniesta
class State:
    def __init__(self, state_id):
        self.id = state_id
    
    #Metodo que se llama al iniciar el estado
    def Start(self):
        print(f"Inicio del estado: {self.id}")  
    
    #Metodo que se llama en cada actualización del estado
    #devuelve las acciones (actuadores) que el agente realiza
    def Update(self, perception):
        return 0, False
    
     #método que se llama para decidir la transición del estado. Devuelve el id del estado nuevo
    def Transit(self, perception):
        return self.id
    
    #Metodo que se llama al finalizar el estado
    def End(self):
        print(f"Fin del estado: {self.id}") 

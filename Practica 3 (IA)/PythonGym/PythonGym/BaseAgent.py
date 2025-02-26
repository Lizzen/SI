import random
class BaseAgent:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    #Devuelve el nombre del agente
    def Name(self):
        return self.name
    #Devuelve el id del agente
    def Id(self):
        return self.id
    #Metodo que se llama al iniciar el agente. No devuelve nada y sirve para contruir el agente
    def Start(self):
        print("Inicio del agente ")

    #Metodo que se llama en cada actualización del agente, y se proporciona le vector de percepciones
    #Devuelve la acción u el disparo si o no
    def Update(self, perception):
        print("Toma de decisiones del agente")
        print(perception)
        action = 0 
        fire = False

        if perception[8] > perception[12]:
            action = 3
        elif perception[13] > perception[9]:
            action = 2
        elif perception[8] < perception[12]:
            action = 4
        elif perception[9] < perception[13]:
            action = 1

        if perception[14] and (perception[8] == perception[12] or perception[9] == perception[13]):
            fire = True

        return action, fire
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        print("Agente finalizado")
        print("Victoria ",win)
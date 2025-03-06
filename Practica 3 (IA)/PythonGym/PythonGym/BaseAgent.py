import random
import time
class State:
    def update(self, perception):
        raise NotImplementedError("Cada estado debe implementar el método 'update'.")

# Detecta base
class Explore_base(State):
    def Update(self, perception):
        action = 0 
        fire = False
        diferencia_x = abs(perception[10] - perception[12])
        diferencia_y = abs(perception[11] - perception[13])
        for i in range(0,4):
            if action == 0:
                if i == 0 and perception[10] > perception[12]:  # Der
                    if perception[2] == 0 or perception[6] > 1.00:
                        action = 3
                    elif perception[2] == 1 or perception[6] > 1.00:
                        action = 3
                        fire = True
                elif i == 2 and perception[13] > perception[11]: # Abajo
                    if perception[1] == 0 or perception[5] > 1.00:
                        action = 2
                elif i == 3 and perception[10] < perception[12]: # Izq
                    if perception[3] == 0 or perception[7] > 1.00:
                        action = 4
                elif i == 1 and perception[13] < perception[11]: # Arriba
                    if perception[0] == 0 or perception[4] > 1.00:
                        action = 1
        return action, False

#Gira y dispara
class Turn_shoot(State):
    def update(self, perception):

#detecta player
class Protect(State):
    def update(self, perception):


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

        for i in range(0,4):
            if action == 0:
                if i == 2 and perception[10] > perception[12]:  # Der
                    if perception[2] == 0 or perception[6] > 1.00:
                        action = 3
                elif i == 0 and perception[13] > perception[11]: # Abajo
                    if perception[1] == 0 or perception[5] > 1.00:
                        action = 2
                elif i == 3 and perception[10] < perception[12]: # Izq
                    if perception[3] == 0 or perception[7] > 1.00:
                        action = 4
                elif i == 1 and perception[13] < perception[11]: # Arriba
                    if perception[0] == 0 or perception[4] > 1.00:
                        action = 1

        if perception[14] and (int(perception[8]) == int(perception[12]) or int(perception[9]) == int(perception[13]) or int(perception[10]) == int(perception[12]) or int(perception[11]) == int(perception[13])): #Puede dispara y le tiene a tiro
            fire = True


        return action, fire
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        print("Agente finalizado")
        print("Victoria ",win)
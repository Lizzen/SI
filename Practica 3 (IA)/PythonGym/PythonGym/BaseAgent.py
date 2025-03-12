import random
import time
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
        action = random.randint(0,4)
        return action, True
    
    #Metodo que se llama al finalizar el agente, se pasa el estado de terminacion
    def End(self, win):
        print("Agente finalizado")
        print("Victoria ",win)

import math

class SmartAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.state = "EXPLORE"
        self.last_player_position = (0, 0)
        self.path = []
        self.shell_threat = False

    def Update(self, perception):
        # Procesar percepción
        player_pos = (perception[8], perception[9])
        command_center_pos = (perception[10], perception[11])
        agent_pos = (perception[12], perception[13])
        objects = (perception[0], perception[1], perception[2], perception[3])
        can_fire = perception[14] == 1
        health = perception[15]

        # Detección de amenazas
        shell_detected = self._detect_shell(perception)
        
        # Máquina de estados principal
        if shell_detected:
            self.state = "EVADE"
        elif self._player_visible(perception):
            self.state = "ATTACK_PLAYER"
        elif self._command_center_accessible(perception):
            self.state = "ATTACK_COMMAND"
        else:
            self.state = "EXPLORE"

        # Ejecutar lógica del estado actual
        if self.state == "ATTACK_PLAYER":
            action, fire = self._attack_player(agent_pos, player_pos, can_fire, objects)
        elif self.state == "ATTACK_COMMAND":
            action, fire = self._attack_command(agent_pos, command_center_pos, can_fire, objects)
        elif self.state == "EVADE":
            action, fire = self._evade_shell(perception)
        else:
            action, fire = self._explore(agent_pos, command_center_pos, objects)

        return action, fire

    def _detect_shell(self, perception):
        # Detectar balas cercanas en las 4 direcciones
        for i in range(4):
            if perception[i] == 5 and perception[i+4] < 3:
                return True
        return False

    def _player_visible(self, perception):
        return perception[0] == 4 or perception[1] == 4 or perception[2] == 4 or perception[3] == 4

    def _command_center_accessible(self, perception):
        return perception[0] == 3 or perception[1] == 3 or perception[2] == 3 or perception[3] == 3

    def _calculate_path(self, start, end, objects):
        # Implementación simplificada de A* para demostración
        # En una implementación real se usaría el mapa completo
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        action = 0
        fire = False

        if abs(dx) > abs(dy):
            if dx > 0:
                action = 3
            else:
                action = 4

            if ((action == 3 and  objects[2] == 2) or (action == 4 and  objects[3] == 2)):
                fire = True 
        else:
            if dy > 0 and objects[0] != 1:
                action = 1
            else:
                action = 2

            if ((action == 1 and  objects[0] == 2) or (action == 2 and  objects[1] == 2)):
                fire = True 

        return action, fire



    def _attack_player(self, agent_pos, player_pos, can_fire, objects):
        # Calcular dirección hacia el jugador
        move_action, fire = self._calculate_path(agent_pos, player_pos, objects)
        return move_action, can_fire

    def _attack_command(self, agent_pos, command_pos, can_fire, objects):
        # Calcular dirección hacia el command center
        move_action, fire = self._calculate_path(agent_pos, command_pos, objects)
        return move_action, can_fire

    def _evade_shell(self, perception):
        # Movimiento evasivo aleatorio
        return random.choice([1, 2, 3, 4]), False

    def _explore(self, agent_pos, command_pos, objects):
        # Navegar hacia el command center
        move_action, fire = self._calculate_path(agent_pos, command_pos, objects)
        return move_action, fire

    def _distance(self, pos1, pos2):
        return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
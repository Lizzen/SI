import random
from State import State
from StateMachine import StateMachine

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



class ExploreState(State):
    def __init__(self):
        super().__init__("EXPLORE")
        self.last_position = None
        self.agent = None
    
    def Update(self, perception):
        agent = (int(perception[12]), int(perception[13]))
        command_center = (int(perception[10]), int(perception[11]))
        
        dx = command_center[0] - agent[0]
        dy = command_center[1] - agent[1]
        
        preferred_directions = []
        if abs(dx) > abs(dy):
            preferred_directions.append(3 if dx > 0 else 4)
            preferred_directions.append(1 if dy > 0 else 2)
        else:
            preferred_directions.append(1 if dy > 0 else 2)
            preferred_directions.append(3 if dx > 0 else 4)

        for direction in preferred_directions:
            fire = False
            if not self._has_obstacle(direction-1, perception):  # -1 porque las direcciones empiezan en 0
                """fire = self._shoot_command(direction - 1, agent, command_center, perception)
                print(fire)
                if fire:
                    return self._rotation_planetar(agent, command_center, dx, dy, direction),"""
                self.last_position = direction
                self.agent = agent
                return direction, fire
        
        # Si todas las direcciones están bloqueadas, elegir aleatoria
        return self._same_move(preferred_directions, agent), True
    
    def _same_move(self, array, agent):
        for i in range(0, 2):
            if array[i] != self.last_position:
                self.last_position = array[i]
                self.agent = agent
                return array[i]
        return 0
    
#Dispara si está en la misma posicion del agente o command center
    def _shoot_command(self, direction, agent_pos, command_pos, perception):
        if (direction > 2 and agent_pos[0] == command_pos[0]) or (direction < 3 and agent_pos[1] == command_pos[1]):
            return True
        return False
    
#hay obstaculo
    def _has_obstacle(self, direction_index, perception):
        return perception[direction_index] in [1.0, 2.0] and perception[direction_index+4] <= 0.5
    
# rota para disparar
    def _rotation_planetar(self, start, target, dx, dy, direction):
        if (target[0] == start[0]):
            if dx > 0:
                return 2
            else: return 1
        elif (target[1] == start[1]):
            if dy > 0:
                return 4
            else: return 3
        return direction

            
    def Transit(self, perception):
        if any(perception[i] == 5 and perception[i+4] < 3 for i in range(4)):
            return "EVADE"
        if any(perception[i] == 4 for i in range(4)):
            return "ATTACK_PLAYER"
        if any(perception[i] == 3 for i in range(4)):
            return "ATTACK_COMMAND"
        return self.id
    
#Dispara si está en la misma posicion del agente o command center
    def _shoot_command(self, direction, agent_pos, command_pos, perception):
        if (direction > 2 and agent_pos[0] == command_pos[0]) or (direction < 3 and agent_pos[1] == command_pos[1]):
            return True
        return False
    
#hay obstaculo
    def _has_obstacle(self, direction_index, perception):
        return perception[direction_index] in [1.0, 2.0] and perception[direction_index+4] <= 1.5
    
# rota para disparar
    def _rotation_planetar(self, start, target, dx, dy, direction):
        if (target[0] == start[0]):
            if dx > 0:
                return 2
            else: return 1
        elif (target[1] == start[1]):
            if dy > 0:
                return 4
            else: return 3
        return direction

            
    def Transit(self, perception):
        if any(perception[i] == 5 and perception[i+4] < 3 for i in range(4)):
            return "EVADE"
        if any(perception[i] == 4 for i in range(4)):
            return "ATTACK_PLAYER"
        if any(perception[i] == 3 for i in range(4)):
            return "ATTACK_COMMAND"
        return self.id


class EvadeState(State):
    def __init__(self):
        super().__init__("EVADE")
    
    def Update(self, perception):
        return random.choice([1, 2, 3, 4]), False
    
    def Transit(self, perception):
        if not any(perception[i] == 5 for i in range(4)):
            return "EXPLORE"
        return self.id

class AttackPlayerState(State):
    def __init__(self):
        super().__init__("ATTACK_PLAYER")
    
    def Update(self, perception):
        agent = (int(perception[12]), int(perception[13]))
        player = (int(perception[12]), int(perception[13]))
        
        dx = player[0] - agent[0]
        dy = player[1] - agent[1]
        
        preferred_directions = []
        if abs(dx) > abs(dy):
            preferred_directions.append(3 if dx > 0 else 4)
            preferred_directions.append(1 if dy > 0 else 2)
        else:
            preferred_directions.append(1 if dy > 0 else 2)
            preferred_directions.append(3 if dx > 0 else 4)
        return preferred_directions[0], True  # Quieto y disparando
    
    def Transit(self, perception):
        if not any(perception[i] == 4 for i in range(4)):
            return "EXPLORE"
        if any(perception[i] == 5 and perception[i+4] < 3 for i in range(4)):
            return "EVADE"
        return self.id

class AttackCommandState(State):
    def __init__(self):
        super().__init__("ATTACK_COMMAND")
    
    def Update(self, perception):
        agent_pos = (int(perception[12]), int(perception[13]))
        command_pos = (int(perception[10]), int(perception[11]))
        dx = command_pos[0] - agent_pos[0]
        dy = command_pos[1] - agent_pos[1]
        
        if abs(dx) > abs(dy):
            action = 3 if dx > 0 else 4
        else:
            action = 1 if dy > 0 else 2
        return action, True
    
    def Transit(self, perception):
        if not any(perception[i] == 3 for i in range(4)):
            return "EXPLORE"
        if any(perception[i] == 5 and perception[i+4] < 3 for i in range(4)):
            return "EVADE"
        return self.id

class SmartAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.state_machine = StateMachine(id, states={
            "EXPLORE": ExploreState(),
            "EVADE": EvadeState(),
            "ATTACK_PLAYER": AttackPlayerState(),
            "ATTACK_COMMAND": AttackCommandState(),
            #"DESTROY_OBSTACLE": DestroyObstacleState()
        }, initial="EXPLORE")

    def Start(self):
        self.state_machine.Start()

    def Update(self, perception):
        # Convertir valores críticos a enteros
        perception = [int(x) if i in [8,9,10,11,12,13,14,15] else x 
                     for i, x in enumerate(perception)]
        return self.state_machine.Update(perception)

    def End(self, win):
        self.state_machine.End()

""""class DestroyObstacleState(State):
    def __init__(self):
        super().__init__("DESTROY_OBSTACLE")
        self.obstacle_direction = None
    
    def Update(self, perception):
        # Disparar solo a obstáculos rompibles (tipo 2)
        for i in range(4):
            if perception[i] == 2.0 and perception[i+4] <= 1.5:
                self.obstacle_direction = i
                return 0, True  # Quieto y disparando
        
        # Si el obstáculo es irrompible (tipo 1), buscar ruta alternativa
        return random.choice([1, 2, 3, 4]), False
    
    def Transit(self, perception):
        if not any(perception[i] == 2.0 for i in range(4)):
            return "EXPLORE"
        return self.id"""
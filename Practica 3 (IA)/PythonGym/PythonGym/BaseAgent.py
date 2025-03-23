
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


# In perception = 0.20 the IA works well but the best results are in the value 0.18
class ExploreState(State):
    def __init__(self):
        super().__init__("EXPLORE")
        self.last_position = None       # Save the agent's last direction choice
        self.agent = None               # Save the last position of the agent
    
    # greedy algorithm
    def Update(self, perception):
        # Deploying A* with Manhattan using an Array that has the best choices
        agent = perception[12], perception[13]              # POS_X, POS_Y
        command_center = perception[10], perception[11]     # POS_X, POS_Y
        
        dx = command_center[0] - agent[0]       # Distance_X
        dy = command_center[1] - agent[1]       # Distance_Y
        
        preferred_directions = []       # Array which contains the best choices
        if abs(dx) > abs(dy):
            preferred_directions.append(3 if dx > 0 else 4)
            preferred_directions.append(1 if dy > 0 else 2)
        else:
            preferred_directions.append(1 if dy > 0 else 2)
            preferred_directions.append(3 if dx > 0 else 4)

        # if there are no obstacles 
        if (not self._has_obstacle(preferred_directions[0]-1, perception) and dx != 0 and dy != 0):
            self.last_position = preferred_directions[0]
            return preferred_directions[0], False
        elif (not self._has_obstacle(preferred_directions[1]-1, perception) and dx != 0 and dy != 0):
            self.last_position = preferred_directions[1]
            return preferred_directions[1], False
        # if there ara breakable walls
        elif (perception[preferred_directions[0]-1] == 2.0):
            self.last_position = preferred_directions[0]
            return preferred_directions[0], True
        elif (perception[preferred_directions[1]-1] == 2.0):
            self.last_position = preferred_directions[1]
            return preferred_directions[1], True            
        
        # If all directions are blocked, choose one that you have not previously chosen
        return self._same_move(preferred_directions), True
    
    def _same_move(self, array):
        for i in range(0, 2):
            if array[i] != self.last_position:
                self.last_position = array[i]
                return array[i]
        return 0
    
    def _has_obstacle(self, direction_index, perception):
        return (perception[direction_index] == 1.0 or perception[direction_index] == 2.0)  and perception[direction_index+4] <= 0.75

            
    def Transit(self, perception):
        if any(perception[i] == 5 and perception[i+4] < 6 for i in range(4)):
            return "EVADE"
        if any(perception[i] == 3 for i in range(4)) or abs(perception[10] - perception[12]) <= 0.5 or abs(perception[11] - perception[13]) <= 0.5:
            return "ATTACK_COMMAND"
        if any(perception[i] == 4 for i in range(4)) or abs(perception[8] - perception[12]) <= 0.15 or abs(perception[9] - perception[13]) <= 0.15:
            return "ATTACK_PLAYER"
        return self.id


class EvadeState(State):
    def __init__(self):
        super().__init__("EVADE")
        self.DIRECTIONS = [1, 2, 3, 4]  # Array with the directions
    
    def Update(self, perception):

        for direction in self.DIRECTIONS:
            if perception[direction-1] == 4: 
                return direction, True 
            
        return random.choice(self.DIRECTIONS), True
    
    def Transit(self, perception):
        if not any(perception[i] == 5 for i in range(4)):
            return "EXPLORE"
        if any(perception[i] == 4 for i in range(4)) or abs(perception[8] - perception[12]) <= 0.15 or abs(perception[9] - perception[13]) <= 0.15:
            return "ATTACK_PLAYER"
        if any(perception[i] == 3 for i in range(4)) or abs(perception[10] - perception[12]) <= 0.5 or abs(perception[11] - perception[13]) <= 0.5:
            return "ATTACK_COMMAND"
        return self.id

class AttackPlayerState(State):
    def __init__(self):
        super().__init__("ATTACK_PLAYER")
    
    def Update(self, perception):
        # Deploying A* with Manhattan
        agent_pos = perception[12], perception[13]
        player_pos = perception[8], perception[9]
        dx = player_pos[0] - agent_pos[0]
        dy = player_pos[1] - agent_pos[1]
        
        if abs(dx) > abs(dy):
            action = 3 if dx > 0 else 4
        else:
            action = 1 if dy > 0 else 2

        return action, True
    
    def Transit(self, perception):
        if any(perception[i] == 5 and perception[i+4] < 6 for i in range(4)):
            return "EVADE"        
        if not (any(perception[i] == 4 for i in range(4)) or abs(perception[8] - perception[12]) <= 0.15 or abs(perception[9] - perception[13]) <= 0.15):
            return "EXPLORE"
        if any(perception[i] == 3 for i in range(4)) or abs(perception[10] - perception[12]) <= 0.5 or abs(perception[11] - perception[13]) <= 0.5:
            return "ATTACK_COMMAND"
        return self.id

class AttackCommandState(State):
    def __init__(self):
        super().__init__("ATTACK_COMMAND")
    
    def Update(self, perception):
        # Deploying A* with Manhattan
        agent_pos = perception[12], perception[13]
        command_pos = perception[10], perception[11]
        dx = command_pos[0] - agent_pos[0]
        dy = command_pos[1] - agent_pos[1]
        
        if abs(dx) > abs(dy):
            action = 3 if dx > 0 else 4
        else:
            action = 1 if dy > 0 else 2
        return action, True
    
    def Transit(self, perception):
        if any(perception[i] == 5 and perception[i+4] < 6 for i in range(4)):
            return "EVADE"
        if not (any(perception[i] == 3 for i in range(4)) or abs(perception[10] - perception[12]) <= 1 or abs(perception[11] - perception[13]) <= 1):
            return "EXPLORE"
        if any(perception[i] == 4 for i in range(4)) and abs(perception[8] - perception[12]) <= 0.2 and abs(perception[9] - perception[13]) <= 0.2:
            return "ATTACK_PLAYER"

        return self.id

class SmartAgent(BaseAgent):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.state_machine = StateMachine(id, states={
            "EXPLORE": ExploreState(),
            "EVADE": EvadeState(),
            "ATTACK_PLAYER": AttackPlayerState(),
            "ATTACK_COMMAND": AttackCommandState(),
        }, initial="EXPLORE")

    def Start(self):
        self.state_machine.Start()

    def Update(self, perception):
        # Convert critical values to integers (Así va mejor el código pero no lo hemos implementado ya que nos parecio un poco trampa)
        """perception = [int(x) if i in [8,9,10,11,12,13,14,15] else x 
                     for i, x in enumerate(perception)]"""
        return self.state_machine.Update(perception)

    def End(self, win):
        self.state_machine.End()

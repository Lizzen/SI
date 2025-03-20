from State import State

class StateMachine(State):
    def __init__(self, id, states, initial):
        super().__init__(id)
        self.states = states  # Diccionario {id: instancia_de_State}
        self.curentState = initial
    
    def Start(self):
        print(f"Iniciando máquina de estados: {self.id}")
        self.states[self.curentState].Start()

    def Update(self, perception):
        # Obtener acciones del estado actual
        action, fire = self.states[self.curentState].Update(perception)
        
        # Determinar transición de estado
        newState = self.states[self.curentState].Transit(perception)
        
        # Realizar transición si es necesaria
        if newState != self.curentState and newState in self.states:
            self._perform_transition(newState)
        
        return action, fire

    def _perform_transition(self, new_state_id):
        print(f"Transición: {self.curentState} -> {new_state_id}")
        self.states[self.curentState].End()
        self.curentState = new_state_id
        self.states[self.curentState].Start()

    def End(self):
        print(f"Finalizando máquina de estados: {self.id}")
        self.states[self.curentState].End()
from State import State

class StateMachine(State):
    def __init__(self, id, states, initial):
        super().__init__(id)
        self.states = states        # Diccionary {id: State}
        self.curentState = initial
    
    #Metodo que se llama al iniciar la máquina de estado
    def Start(self):
        print(f"Iniciando máquina de estados: {self.id}")
        self.states[self.curentState].Start()

    #Metodo que se llama en cada actualización del estado
    #devuelve las acciones (actuadores) que el agente realiza
    def Update(self, perception):
        # Obtiene acciones del estado actual
        action, fire = self.states[self.curentState].Update(perception)
        
        # Determina la transicion de estado
        newState = self.states[self.curentState].Transit(perception)
        
        # Realiza la transicion si es necesaria
        if newState != self.curentState and newState in self.states:
            self._perform_transition(newState)
        
        return action, fire

    # Realiza la transicion y la imprime por consola
    def _perform_transition(self, new_state_id):
        print(f"Transición: {self.curentState} -> {new_state_id}")
        self.states[self.curentState].End()
        self.curentState = new_state_id
        self.states[self.curentState].Start()

    #Metodo que se llama al finalizar la máquina de estado
    def End(self):
        print(f"Finalizando máquina de estados: {self.id}")
        self.states[self.curentState].End()
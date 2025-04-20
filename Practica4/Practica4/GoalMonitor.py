import random
from States.AgentConsts import AgentConsts
from MyProblem.BCProblem import BCProblem

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    def __init__(self, problem, goals):
        self.goals = goals
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False

    def ForceToRecalculate(self):
        self.recalculate = True

    #determina si necesitamos replanificar
    def NeedReplaning(self, perception, map, agent):
        """
        Devuelve True cuando el agente debe calcular un nuevo plan.

        Criterios:
        1.  self.recalculate  →  ha sido forzado externamente.
        2.  Ha pasado un intervalo fijo (3 s) desde el último plan.
        3.  La salud del agente es 1 o menos.
        """
        # 1) Re‑planificación forzada desde fuera
        if self.recalculate:
            self.recalculate = False
            self.lastTime = perception[AgentConsts.TIME]
            return True

        # 2) Re‑planificación periódica (cada 3 segundos)
        currentTime = perception[AgentConsts.TIME]
        if self.lastTime < 0:
            self.lastTime = currentTime           # primera llamada
        elif currentTime - self.lastTime > 1.0:   # intervalo cumplido
            self.lastTime = currentTime
            return True

        # 3) Poca vida: necesito un nuevo plan YA
        if perception[AgentConsts.HEALTH] <= 1:
            self.lastTime = currentTime           # reinicia contador
            return True

        return False

    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        """
        Elige la meta más conveniente en cada momento.

        Prioridad:
        1) JUGADOR (slot 2) si está a <=4 casillas.
        2) VIDA     (slot 1) si la salud es 1 o menos.
        3) COMMAND CENTER (slot 0) por defecto.
        """
        # --- recuperamos metas de la lista -----------------
        goalCommand = self.goals[GoalMonitor.GOAL_COMMAND_CENTRER]   # 0
        goalLife    = self.goals[GoalMonitor.GOAL_LIFE]              # 1
        goalPlayer  = self.goals[GoalMonitor.GOAL_PLAYER]            # 2

        # ---------------------------------------------------
        # 1) Jugador a la vista y “cerca”
        # ---------------------------------------------------
        if goalPlayer is not None:
            # distancia Manhattan entre el jugador y el agente actual
            # (convertimos la posición del agente en mapa)
            xA, yA = BCProblem.WorldToMapCoord(
                        perception[AgentConsts.AGENT_X],
                        perception[AgentConsts.AGENT_Y],
                        agent.problem.ySize)

            distPlayer = abs(goalPlayer.x - xA) + abs(goalPlayer.y - yA)

            if distPlayer <= 3:
                return goalPlayer

        # ---------------------------------------------------
        # 2) Necesito vida urgentemente
        # ---------------------------------------------------
        if perception[AgentConsts.HEALTH] <= 1 and perception[AgentConsts.AGENT_X] != -1:
            return goalLife

        # ---------------------------------------------------
        # 3) Por defecto, seguimos atacando el Command Center
        # ---------------------------------------------------
        return goalCommand


    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
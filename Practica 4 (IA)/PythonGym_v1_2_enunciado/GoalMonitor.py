import random
from States.AgentConsts import AgentConsts

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
        elif currentTime - self.lastTime > 3.0:   # intervalo cumplido
            self.lastTime = currentTime
            return True

        # 3) Poca vida: necesito un nuevo plan YA
        if perception[AgentConsts.HEALTH] <= 1:
            self.lastTime = currentTime           # reinicia contador
            return True

        return False

    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        #TODO definir la estrategia del cambio de meta
        print("TODO aqui faltan cosas :)")
        return self.goals[random.randint(0, len(self.goals) - 1)]

    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
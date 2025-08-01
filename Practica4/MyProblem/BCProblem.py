#import sys
#sys.path.insert(1, '../AStar')
from AStar.Problem import Problem
from MyProblem.BCNode import BCNode
from States.AgentConsts import AgentConsts
import sys
import numpy as np

#Clase que implementa el problema especifico que queremos resolver y que hereda de la calse
#Problema genérico.
class BCProblem(Problem):
    

    def __init__(self, initial, goal, xSize, ySize):
        super().__init__(initial, goal)
        self.map = np.zeros((xSize,ySize),dtype=int)
        self.xSize = xSize
        self.ySize = ySize
    
    #inicializa un mapa con el mapa proveniente del entorno Vector => Matriz
    def InitMap(self,m):
        for i in range(len(m)):
            x,y = BCProblem.Vector2MatrixCoord(i,self.xSize,self.ySize)
            self.map[x][y] = m[i]

    #Muestra el mapa por consola
    def ShowMap(self):
        for j in range(self.ySize):
            s = ""
            for i in range(self.xSize):
                s += ("[" + str(i) + "," + str(j) + "," + str(self.map[i][j]) +"]")
            print(s)

    #Calcula la heuristica del nodo en base al problema planteado (Se necesita reimplementar)
    def Heuristic(self, node):
        # #TODO: heurística del nodo
        # print("Aqui falta ncosas por hacer :) ")
        # return np.sqrt((node.x - self.xSize)**2 + (node.y - self.ySize)**2)
        # BCProblem.py   :contentReference[oaicite:2]{index=2}&#8203;:contentReference[oaicite:3]{index=3}
        dx = abs(node.x - self.goal.x)
        dy = abs(node.y - self.goal.y)
        return dx + dy      # Manhattan

     # muro -> intransitable

    #Genera la lista de sucesores del nodo (Se necesita reimplementar)
    def GetSucessors(self, node):
        # successors = []
        # # #TODO: sucesores de un nodo dado
        # print("Aqui falta ncosas por hacer :) ")
        # possible_moves = [
        #     (node.x+1, node.y), (node.x-1, node.y),    # Right, Left
        #     (node.x, node.y+1), (node.x, node.y-1),    # Up, Down
        #     (node.x+1, node.y+1), (node.x-1, node.y-1),  # Diagonal moves
        #     (node.x+1, node.y-1), (node.x-1, node.y+1)
        # ]

        # for nx, ny in possible_moves:
        #     if self.xSize > nx >= 0 and self.ySize > ny >= 0 and self.map[nx, ny] == 0:
        #         self.CreateNode(successors, node, nx, ny)

        # return successors
        successors = []

        # Desplazamientos (Δx, Δy)  ──>  derecha, izquierda, arriba, abajo
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in moves:
            nx, ny = node.x + dx, node.y + dy

            # 1) Permanecer dentro del tablero
            if 0 <= nx < self.xSize and 0 <= ny < self.ySize:

                # 2) Mirar el tipo de casilla para saber el coste
                value = self.map[nx][ny]
                if BCProblem.GetCost(value) < sys.maxsize:
                    # 3) Es transitable → creamos y añadimos el sucesor
                    self.CreateNode(successors, node, nx, ny)

        return successors
    
    #métodos estáticos
    #nos dice si podemos movernos hacia una casilla, se debe poner el valor de la casilla como
    #parámetro
    @staticmethod
    def CanMove(value):
        return value != AgentConsts.UNBREAKABLE and value != AgentConsts.SEMI_UNBREKABLE and value != AgentConsts.SEMI_UNBREKABLE
    
    #convierte coordenadas mapa en formato vector a matriz
    @staticmethod
    def Vector2MatrixCoord(pos,xSize,ySize):
        x = pos % xSize
        y = pos // ySize #division entera
        return x,y

    #convierte coordenadas mapa en formato matriz a vector
    @staticmethod
    def Matrix2VectorCoord(x,y,xSize):
        return y * xSize + x
    
    #convierte coordenadas del mapa en coordenadas del entorno (World) (nótese que la Y está invertida)
    @staticmethod
    def MapToWorldCoord(x,y,ySize):
        xW = x * 2
        yW = (ySize - y - 1) * 2
        return xW, yW

    #convierte coordenadas del entorno (World) en coordenadas mapa (nótese que la Y está invertida)
    @staticmethod
    def WorldToMapCoord(xW,yW,ySize):
        x = xW // 2
        y = yW // 2
        y = ySize - y - 1
        return x, y
    
    #versión real del método anterior, que nos ayuda a buscar los centros de las celdas.
    #aqui nos dirá los decimales, es decir como de cerca estamos de la esquina superior derecha
    #un valor de 1.9,1.9 nos dice que estamos en la casilla 1,1 muy cerca de la 2,2
    #en realidad, lo que buscamos es el punto medio de la casilla, es decir la 1.5, 1.5 en el caso
    #de la casilla 1,1
    @staticmethod
    def WorldToMapCoordFloat(xW,yW,ySize):
        x = xW / 2
        invY = (ySize*2) - yW
        invY = invY / 2
        return x, invY

    #se utiliza para calcular el coste de cada elemento del mapa 
    @staticmethod
    def GetCost(value):
        #TODO: debes darle un coste a cada tipo de casilla del mapa.
        """
        Devuelve el coste de entrar en una celda que contiene 'value'.
        Un coste MUY alto (sys.maxsize) se interpreta como muro intransitable.
        """

        # -------- Transitables -----------------------------
        if value == AgentConsts.NOTHING:           # suelo libre
            return 1

        if value == AgentConsts.COMMAND_CENTER:    # casilla objetivo
            return 1

        if value == AgentConsts.BRICK:             # ladrillo (1 disparo)
            return 3                              # prueba con 2‑4

        if value == AgentConsts.SEMI_BREKABLE:     # varios disparos
            return 5                               # ajusta a tu gusto

        # -------- Intransitables ---------------------------
        if value in (AgentConsts.UNBREAKABLE,
                    AgentConsts.SEMI_UNBREKABLE): # acero o pared dura
            return sys.maxsize

        # Por si llegara un valor inesperado
        return sys.maxsize
    
    #crea un nodo y lo añade a successors (lista) con el padre indicado y la posición x,y en coordenadas mapa 
    def CreateNode(self,successors,parent,x,y):
        value=self.map[x][y]
        g=BCProblem.GetCost(value)
        rightNode = BCNode(parent,g,value,x,y)
        rightNode.SetH(self.Heuristic(rightNode))
        successors.append(rightNode)

    #Calcula el coste de ir del nodo from al nodo to (Se necesita reimplementar)
    def GetGCost(self, nodeTo):
        return BCProblem.GetCost(nodeTo.value)
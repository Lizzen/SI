

#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node
class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.precessed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem #problema a resolver

    def GetPlan(self):
        findGoal = False
        #TODO implementar el algoritmo A*
        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
        self.open.clear()
        self.precessed.clear()
        self.open.append(self.problem.Initial())
        path = []
        start = self.problem.Initial()
        goal = self.problem.GetGoal()
        start.SetG(0)
        start.SetH(self.problem.Heuristic(start))
        start.SetParent(None)
        path.append(start)
        while self.open:
            self.open.sort(key=lambda nodo: nodo.F())
            current = self.open[0]

            if current == goal:
                return self.ReconstructPath(current)
            
            self.open.remove(current)
            self.precessed.add(current)

            for neighbor in self.problem.GetSucessors(current):
                if neighbor in self.precessed:
                    continue

                tentative_g = current.G() + self.Manhattan(current, neighbor)
                if neighbor not in self.open:
                    self.open.append(neighbor)
                elif tentative_g >= neighbor.G():
                    continue

                neighbor.SetParent(current)
                neighbor.SetG(tentative_g)
                neighbor.SetH(self.problem.Heuristic(self.problem.GetGoal()))
                path.append(neighbor)

        #mientras no encontremos la meta y haya elementos en open....
        #TODO implementar el bucle de búsqueda del algoritmo A*
        return path
    
    def Manhattan(self, current , other):
        return abs(other.x - current.x) + abs(other.y - current.y)

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        #TODO Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSucesorInOpen(self,sucesor):
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == sucesor:
                found = node
        return found


    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        path = []
        #TODO: devuelve el path invertido desde la meta hasta que el padre sea None.
        while goal is not None:
            path.append(goal)
            goal = goal.GetParent()
            print(goal)
        return path




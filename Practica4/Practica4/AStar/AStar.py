

# #Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
# #la calse Problem que tenga como nodos hijos de la clase Node
# class AStar:

#     def __init__(self, problem):
#         self.open = [] # lista de abiertos o frontera de exploración
#         self.precessed = set() # set, conjunto de cerrados (más eficiente que una lista)
#         self.problem = problem #problema a resolver

#     def GetPlan(self):
#         findGoal = False
#         #TODO implementar el algoritmo A*
#         #cosas a tener en cuenta:
#         #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
#         #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
#         #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
#         #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
#         #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
#         self.open.clear()
#         self.precessed.clear()
#         self.open.append(self.problem.Initial())
#         path = []
#         start = self.problem.Initial()
#         goal = self.problem.GetGoal()
#         start.SetG(0)
#         start.SetH(self.problem.Heuristic(start))
#         start.SetParent(None)
#         path.append(start)
#         while self.open:
#             self.open.sort(key=lambda nodo: nodo.F())
#             current = self.open[0]

#             if current == goal:
#                 return self.ReconstructPath(current)
            
#             self.open.remove(current)
#             self.precessed.add(current)

#             for neighbor in self.problem.GetSucessors(current):
#                 if neighbor in self.precessed:
#                     continue

#                 tentative_g = current.G() + self.Manhattan(current, neighbor)
#                 if neighbor not in self.open:
#                     self.open.append(neighbor)
#                 elif tentative_g >= neighbor.G():
#                     continue

#                 neighbor.SetParent(current)
#                 neighbor.SetG(tentative_g)
#                 #neighbor.SetH(self.problem.Heuristic(self.problem.GetGoal()))
#                 neighbor.SetH(self.problem.Heuristic(neighbor))  # Usar el nodo vecino, no el objetivo
#                 path.append(neighbor)

#         #mientras no encontremos la meta y haya elementos en open....
#         #TODO implementar el bucle de búsqueda del algoritmo A*
#         return path
    
#     def Manhattan(self, current , other):
#         return abs(other.x - current.x) + abs(other.y - current.y)

#     #nos permite configurar un nodo (node) con el padre y la nueva G
#     def _ConfigureNode(self, node, parent, newG):
#         node.SetParent(parent)
#         node.SetG(newG)
#         #TODO Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)

#     #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
#     #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
#     def GetSucesorInOpen(self,sucesor):
#         i = 0
#         found = None
#         while found == None and i < len(self.open):
#             node = self.open[i]
#             i += 1
#             if node == sucesor:
#                 found = node
#         return found


#     #reconstruye el path desde la meta encontrada.
#     def ReconstructPath(self, goal):
#         # path = []
#         # #TODO: devuelve el path invertido desde la meta hasta que el padre sea None.
#         # while goal is not None:
#         #     path.append(goal)
#         #     goal = goal.GetParent()
#         #     print(goal)
#         # return path
#         path = []
#         current = goal
#         while current is not None:
#             path.append(current)
#             current = current.GetParent()
#         return path[::-1]  # Invertir para obtener start -> goal

class AStar:

    def __init__(self, problem):
        self.open = []       # lista de abiertos / frontera de exploración
        self.precessed = set()  # conjunto de cerrados, más eficiente que lista
        self.problem = problem

class AStar:

    def __init__(self, problem):
        self.open = []       # lista de abiertos / frontera de exploración
        self.precessed = set()  # conjunto de cerrados, más eficiente que lista
        self.problem = problem

    def GetPlan(self):
        # Limpiamos estructuras
        self.open.clear()
        self.precessed.clear()

        # Nodo inicial y configuraciones base
        start = self.problem.Initial()
        start.SetG(0)                          # Coste G desde el inicio a sí mismo
        start.SetH(self.problem.Heuristic(start))  # Heurística (definida en BCProblem)
        start.SetParent(None)

        # Añadimos el nodo inicial a la frontera (open)
        self.open.append(start)

        # Bucle principal de búsqueda
        while self.open:
            # 1) Escogemos el nodo con menor F (G+H)
            self.open.sort(key=lambda nodo: nodo.F())
            current = self.open[0]

            # 2) Si current es la meta, reconstruimos el camino
            if self.problem.IsASolution(current):
                return self.ReconstructPath(current)

            # 3) Movemos current de open a processed (cerrados)
            self.open.remove(current)
            self.precessed.add(current)

            # 4) Obtenemos sucesores
            neighbors = self.problem.GetSucessors(current)
            if len(neighbors) == 0:
                # Si no hay sucesores, seguimos con el siguiente nodo en open
                # (puede indicar que no hay solución desde este camino, no el global)
                continue

            for successor in neighbors:
                # Si ya está en cerrados, lo saltamos
                if successor in self.precessed:
                    continue

                # Calculamos coste tentativo desde current hasta successor
                # Puedes cambiarlo por problem.GetGCost(successor) u otra fórmula
                # si lo deseas; en algunos ejemplos se usa una "distancia Manhattan" o euclidiana.
                tentative_g = current.G() + self.problem.GetGCost(successor)

                # Vemos si el sucesor ya está en open
                existing = self.GetSucesorInOpen(successor)
                if existing is None:
                    # No está en open: lo configuramos y lo añadimos
                    self._ConfigureNode(successor, current, tentative_g)
                    self.open.append(successor)
                else:
                    # Sí está en open: comprobamos si hemos encontrado un camino mejor
                    if tentative_g < existing.G():
                        self._ConfigureNode(existing, current, tentative_g)
                        # No hace falta re-insertarlo en self.open, ya está allí

        # Si salimos del while sin haber retornado un plan, no hay solución:
        return []

    def _ConfigureNode(self, node, parent, newG):
        # Configura el nodo con su padre y la G nueva
        node.SetParent(parent)
        node.SetG(newG)
        # Actualiza la heurística con la del problema
        node.SetH(self.problem.Heuristic(node))

    def GetSucesorInOpen(self, sucesor):
        """
        Devuelve el objeto 'Node' que sea igual a 'sucesor' (mismas coords, etc.)
        si ya está en 'self.open'. Caso contrario, devuelve None.
        """
        found = None
        for node in self.open:
            if node == sucesor:
                found = node
                break
        return found

    def ReconstructPath(self, goal):
        # Reconstruimos la ruta desde 'goal' hacia atrás siguiendo los padres
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = current.GetParent()
        # Lo devolvemos invertido: inicio -> meta
        #path.append(path[path.index - 1])
        return path[::-1]

    # Ejemplo de distancia Manhattan si la quisieras usar (opcional)
    def Manhattan(self, n1, n2):
        return abs(n1.x - n2.x) + abs(n1.y - n2.y)


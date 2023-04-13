import graph
from utils import *


# prio queue only accepts edges
class Queue:
    procedure = 'lifo'
    structeredData = list()

    def __init__(self, procedure):
        if (procedure in {'lifo', 'fifo', 'prio'}):
            self.procedure = procedure
            self.structeredData = list()
        else:
            print("Invalid Constructor Parameter")

    def push(self, data):
        if (self.procedure == 'lifo'):
            self.structeredData.insert(0, data)
        elif (self.procedure == 'fifo'):
            self.structeredData.append(data)
        elif (self.procedure == 'prio'):
            index = 0
            while (index < len(self.structeredData) and int(self.structeredData[index].value) < int(data.value)):
                index += 1
            if (index >= len(self.structeredData)):
                self.structeredData.append(data)
            else:
                self.structeredData.insert(index, data)

    def pop(self):
        if (not self.structeredData):  # empty Queue
            print('Queue is empty!!')
            return None
        else:
            return self.structeredData.pop(0)

    def empty(self):
        return (not self.structeredData)

    def contains(self, val):
        return val in self.structeredData

    def print(self):
        for element in self.structeredData:
            print(element, end=' , ')
        print('')


class Node:
    start = None
    end = None
    romania = None
    explored = None
    visitable = None
    path = None

    def __init__(self):
        self.explored = set()
        self.path = []
        self.romania = romania = graph.Graph(['Or', 'Ne', 'Ze', 'Ia', 'Ar', 'Si', 'Fa',
                                              'Va', 'Ri', 'Ti', 'Lu', 'Pi', 'Ur', 'Hi',
                                              'Me', 'Bu', 'Dr', 'Ef', 'Cr', 'Gi'],
                                             [
            ('Or', 'Ze', 71), ('Or', 'Si', 151),
            ('Ne', 'Ia', 87), ('Ze', 'Ar', 75),
            ('Ia', 'Va', 92), ('Ar', 'Si', 140),
            ('Ar', 'Ti', 118), ('Si', 'Fa', 99),
            ('Si', 'Ri', 80), ('Fa', 'Bu', 211),
            ('Va', 'Ur', 142), ('Ri', 'Pi', 97),
            ('Ri', 'Cr', 146), ('Ti', 'Lu', 111),
            ('Lu', 'Me', 70), ('Me', 'Dr', 75),
            ('Dr', 'Cr', 120), ('Cr', 'Pi', 138),
            ('Pi', 'Bu', 101), ('Bu', 'Gi', 90),
            ('Bu', 'Ur', 85), ('Ur', 'Hi', 98),
            ('Hi', 'Ef', 86)
        ])

    def updateStart(self, node):
        if (node.start == []):
            node.start = [node.end]
        else:
            node.start.append(node.end)

    def updatePath(self, path):
        for node in path:
            self.path.append(node)

    def getAdjacetsWhichNotMarked(self, prototypeEdge):
        for edges in self.romania.nodes:
            if edges.name == prototypeEdge:
                source = edges.name
                adjacets = []
                for edge in edges.edges:
                    if (source == edge.end.name and not edge.start.name in self.explored.name):
                        adjacets.append(
                            graph.Edge([edge.end.name, edge.start.name, edge.value]))

                    elif (source == edge.start.name and not edge.end.name in self.explored):
                        adjacets.append(
                            graph.Edge([edge.start.name, edge.end.name, edge.value]))
                return adjacets
        return []

    def printExplored(self):
        for i, node in enumerate(self.explored):
            print("NR. ", i+1, " Explored ", node)

    def printPath(self):
        for i, node in enumerate(self.path):
            print("NR. ", i+1, " Explored ", node)
        print("With cost of : ", self.getPathCost())

    def getPathCost(self):
        sum = 0
        for i in range(0, len(self.path) - 1):
            sum += self.romania.getWeight(self.path[i], self.path[i+1])
        return sum

    def BFS(self, start, end):

        self.explored = set()
        self.path = []
        self.visitable = Queue('fifo')
        self.visitable.push(graph.Edge([[], start, 0]))

        while (True):
            if (self.visitable.empty()):
                return False
            node = None
            while (not self.visitable.empty()):
                node = self.visitable.pop()
                if (not node in self.explored):
                    break
            else:
                return False

            self.explored.add(node.end)

            if (node.end == end):
                node.start.append(node.end)
                self.updatePath(node.start)
                return True

            self.updateStart(node)

            for adjacent in self.getAdjacetsWhichNotMarked(node.end):
                self.visitable.push(graph.Edge(
                    [node.start.copy(), adjacent.end, adjacent.value]))

    def DFS(self, start, end):
        self.explored = {start}
        self.path = [start]
        self.DFS_recusive(self.romania.getNode(start), start, end)

    def DFS_recusive(self, node, start, end):
        if (node.name == end):
            return True
        for adjacent in self.romania.getAdjacent(node):
            if (not adjacent.name in self.explored):
                self.explored.add(adjacent.name)
                self.path.append(adjacent.name)
                if (self.DFS_recusive(adjacent, start, end)):
                    return True
                self.path.pop()
                self.explored.remove(adjacent.name)
        if (node.name == start):
            return False

    def UCS(self, start, end):
        self.visitable = Queue('prio')
        self.explored = set()
        self.visitable.push(graph.Edge([[], start, 0]))
        self.path = []

        while (True):
            if (self.visitable.empty()):
                return False

            edge = self.visitable.pop()
            self.explored.add(edge.end)

            if (edge.end == end):
                edge.start.append(edge.end)
                self.updatePath(edge.start)
                self.pathCost = edge.value
                return True

            self.updateStart(edge)

            for adjacent in self.getAdjacetsWhichNotMarked(edge.end):
                self.visitable.push(graph.Edge(
                    [edge.start.copy(), adjacent.end, adjacent.value+edge.value]))

    def aStar(self, start, end):
        g = {start: 0}
        parent = {start: start}
        self.visitable = Queue('prio')
        self.visitable.push(graph.Node(start))
        self.explored = set()
        self.path = []


        while(not self.visitable.empty()):
            current = self.visitable.pop()
            if(current == start):
                return True
            self.explored.add(current.name)
            for adjacent in self.getAdjacetsWhichNotMarked(current.name):
                if (not adjacent.end in self.explored and not adjacent.end in self.visitable):
                    g = {current.name: float('inf')}
                    parent = {current: None}
                if(g[current.name]+self.romania.getWeight(current.name, adjacent.name) < g[adjacent.name]):
                    g[adjacent.name] = g[current.name] + self.romania.getWeight(current.name, adjacent.name)
                    parent[adjacent.name] = current.name
                    if(adjacent.name in self.visitable):
                        node = self.visitable.pop(adjacent)
                        node.value = g[adjacent.name]
                        self.visitable.push(node)



test = Node()
test.BFS('Bu', 'Ti')
test.printPath()
print("-------")
test.DFS('Bu', 'Ti')
test.printPath()
print("-------")
test.UCS('Bu', 'Ti')
test.printPath()
print("-------")
test.aStar('Bu', 'Ti')
test.printExplored()


# test = Queue('prio')
# test.push(1)
# test.print()
# test.push(6)
# test.print()
# test.push(9)
# test.print()
# test.push(3)
# test.print()
# test.push(14)
# test.print()
# test.push(11)
# test.print()
# test.push(7)
# test.print()
# test.push(8)
# test.print()
# test.push(9)
# test.print()

# print(test.pop())
# print(test.pop())
# print(test.pop())
# print(test.pop())
# print(test.pop())
# print(test.pop())

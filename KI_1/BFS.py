from graph import *
from utils import *


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
            while (index < len(self.structeredData) and int(self.structeredData[index]) < int(data)):
                index += 1
            if (not index):
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

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.explored = set()
        self.path = []
        self.romania = romania = Graph(['Or', 'Ne', 'Ze', 'Ia', 'Ar', 'Si', 'Fa',
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

    def BFS(self):

        self.explored = set()
        self.path = []
        self.visitable = Queue('fifo')
        self.visitable.push(self.start)

        while (True):
            if (self.visitable.empty()):
                self.printExplored(False)
                return False
            node = None
            while (True):
                if (self.visitable.empty()):
                    self.printExplored(False)
                    return False
                node = self.visitable.pop()
                if (not node in self.explored):
                    break

            self.explored.add(node)
            self.path.append(node)

            for adjacent in self.romania.getAdjacent(node):
                if (not adjacent in self.explored):
                    self.visitable.push(adjacent)
            if (node == self.end):
                self.printExplored(True)
                return True

    def printExplored(self, condition):
        for i, node in enumerate(self.path):
            print("NR. ", i+1, " Explored ", node)
        print("Reachable" if condition else "Unreachable")

    def DFS(self):
        self.explored = {self.start}
        self.path = [self.start]
        self.printExplored(self.DFS_recusive(self.start))

    def DFS_recusive(self, node):
        if (node == self.end):
            return True
        for adjacent in self.romania.getAdjacent(node):
            if (not adjacent in self.explored):
                self.explored.add(adjacent)
                self.path.append(adjacent)
                return self.DFS_recusive(adjacent)
        return False


test = Node('Or', 'Ti')
test.BFS()
print("-------")
test.DFS()

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

from prettytable import PrettyTable
from utils import *


class Node:

    def __init__(self, name):
        self.parent = 0
        self.name = name
        self.edges = []
        self.value = 0

    def getName(self):    #return name of node
        return self.name



class Edge:

    def __init__(self, edge):
        self.start = edge[0]
        self.end = edge[1]
        self.value = edge[2]
    def getEnd(self):
        return self.end
    def getStart(self):
        return self.start


class Graph:
    nodes = []

    def __init__(self, node_list, edges):
        for name in node_list:
            self.nodes.append(Node(name))

        for e in edges:
            e = (getNode(e[0], self.nodes), getNode(e[1], self.nodes), e[2])

            self.nodes[next((i for i, v in enumerate(self.nodes)
                            if v.name == e[0].name), -1)].edges.append(Edge(e))
            self.nodes[next((i for i, v in enumerate(
                self.nodes) if v.name == e[1].name), -1)].edges.append(Edge((e[1], e[0], e[2])))



    def getAdjacent(self, node):
        nameList = []
        for x in self.nodes:
            if x == node:
                for adjacent in x.edges:
                    nameList.append(adjacent.end)
        return nameList
    
    def getNode(self, name):    #name of node gives Node object back
        for v in self.nodes:
            if v.name == name:
                return v
        return None
    

    def print(self):
        node_list = self.nodes

        t = PrettyTable(['  '] + [i.name for i in node_list])
        for node in node_list:
            edge_values = ['X'] * len(node_list)
            for edge in node.edges:
                edge_values[next((i for i, e in enumerate(
                    node_list) if e.name == edge.end.name), -1)] = edge.value
            t.add_row([node.name] + edge_values)
        print(t)

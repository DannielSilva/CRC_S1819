import graph
import random

class Erdos_Renyi_Graph(graph.Graph):

    def __init__(self, prob, numNodes):
        self.prob = prob
        self.numNodes = numNodes

    def build(self):
        for node in range(self.numNodes):
            for node2 in range(self.numNodes):
                if node != node2:
                    if random.random() <= self.prob:
                        if node not in self.graph or (node in self.graph and node2 not in self.graph[node]):
                            print("bruna")
                            self.addEdge(node, node2)
            if node not in self.graph:
                self.graph[node] = []
                self.degree[node] = 0

    def avg_numEdges(self):
        return len(self.graph) * (len(self.graph) - 1) // 2

x = Erdos_Renyi_Graph(1, 5)
x.build()
print(x.graph)
print(x.degrees())
print(x.avg_numEdges())
print(x.numEdges)
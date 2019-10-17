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
                        print("bruna")
                        self.addEdge(node, node2)
            if node not in self.graph:
                self.graph[node] = []
                self.degree[node] = 0

    def avg_numEdges(self):
        return len(self.graph) * (len(self.graph) - 1) // 2 * self.prob

    def avg_degree(self):
        return self.prob * (len(self.graph) - 1)

x = Erdos_Renyi_Graph(1/6, 12)
x.build()
print(x.graph)
print(x.degrees())
print(x.avg_numEdges())
print(x.numEdges)
print("<k>", x.avg_degree())
x.degree_dist()
import graph
import random

class Regular(graph.Graph):

    def __init__(self, z, numNodes):
        self.z = z
        self.numNodes = numNodes
        self.stubs = {node : self.z for node in range(self.numNodes)}
        print(self.stubs)

    def build(self):

        for node in range(self.numNodes):
            while self.stubs[node] > 0:
                viz = random.choice(range(self.numNodes))
                
                if node != viz and self.stubs[viz] > 0:
                    n = self.addEdge(node, viz)

                    if n != -1:
                        self.stubs[node] -= 1
                        self.stubs[viz] -= 1

x = Regular(5,20)
x.build()
print(x.graph)
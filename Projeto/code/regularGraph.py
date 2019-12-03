import graph
import random

class Regular(graph.Graph):

    def __init__(self, z, numNodes):
        self.z = z
        self.numNodes = numNodes
        self.stubs = {node : self.z for node in range(self.numNodes)}
        #print(self.stubs)

    def build(self):
        available = list(range(self.numNodes))
        for node in range(self.numNodes):
            #print("node", node, self.graph)
            while self.stubs[node] > 0:
                viz = random.choice(available)
                
                if node != viz and self.stubs[viz] > 0:
                    n = self.addEdge(node, viz)

                    if n != -1:
                        #print("added")
                        self.stubs[node] -= 1
                        self.stubs[viz] -= 1
                    #else:
                        #print("not", self.graph)

                    if self.stubs[node] == 0:
                        #print("removed", available)
                        available.remove(node)

                    if self.stubs[viz] == 0:
                        #print("removed viz", available)
                        available.remove(viz)

x = Regular(4,1000)
print(x.graph)
x.build()
print(x.graph)
x.saveGraphToFile("../graphs/regular.edges")
print("het",x.heterogenity())
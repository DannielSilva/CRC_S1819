import graph
import random
import erdos
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

class Barabasi_Albert_Graph(graph.Graph):

    def __init__(self, initNodes, m, numNodesAdded):
        self.numNodesAdded = numNodesAdded
        self.m = m
        self.initNodes = initNodes
        mm = erdos.Erdos_Renyi_Graph(1,initNodes)
        mm.build()
        print(mm.graph)
        self.graph = mm.graph

    def build(self):
        for node in range(self.initNodes, self.numNodesAdded + self.initNodes):
            added = 0
            while added < self.m:
                probability = self.calcProb()
                no = random.choices(population=list(self.graph.keys()),weights=probability,k=1)
                no = no[0]
                n = self.addEdge(node, no)
                print("Trying to connect ", node, no)
                #print("With probability ", probability[no])
                #print("Probability ", probability)

                if(n != -1):
                    print("Connected")
                    added += 1
            if node not in self.graph:
                self.graph[node] = []
                self.degree[node] = 0
    

    def calcProb(self):
        prob = []
        for node in self.degree:
            prob.append(self.degree[node] / self.sumDegree())
        return prob

    def loglogplot(self, info):
        x = list(info.keys())
        y = list(info.values())
        plt.loglog(x, y, 'og')
        plt.show()
        x = np.log(x)
        y = np.log(y)
        print(linregress(x ,y))

x = Barabasi_Albert_Graph(10,6,500)
x.build()
x.saveGraphToFile("bara.edges")
print(x.graph)
print("Nodes: ", len(x.graph))
print("Expected: ", x.initNodes + x.numNodesAdded )
print(x.degrees())
degs = x.degree_dist()
x.loglogplot(degs)
print("Edges: ",x.numEdges)
print("Expected: ", x.m * x.numNodesAdded )
print("<k> real: ", x.averageDegree())
print("<k> expected: ", 2 * x.m)
print("clust real: ", x.averageClust())
print("clust expected: ", ( np.log(len(x.graph)) )**2 / len(x.graph))
print("APL: ", x.averagePathLength())
print("APL expected", np.log(len(x.graph)) / (np.log(np.log(len(x.graph))) ))
# print("<k> expected", x.expected_avg_degree())
# print("<k> real", x.averageDegree())
# print("clust: ", x.averageClust())
# #print(list(x.graph))
# #x.saveGraphToFile("erdos.edges")
# x.degree_dist()
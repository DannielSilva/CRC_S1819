import graph
import random
import matplotlib.pyplot as plt
#from scipy.stats import binom, poisson
from numpy import linspace, arange
import numpy as np
from math import log

class Erdos_Renyi_Graph(graph.Graph):

    def __init__(self, prob, numNodes):
        self.prob = prob
        self.numNodes = numNodes

    def build(self):
        for node in range(self.numNodes):
            for node2 in range(self.numNodes):
                if node != node2 and node < node2:
                    if random.random() <= self.prob:
                        self.addEdge(node, node2)
            if node not in self.graph:
                self.graph[node] = []
                self.degree[node] = 0

    def avg_numEdges(self):
        return len(self.graph) * (len(self.graph) - 1) // 2 * self.prob

    def expected_avg_degree(self):
        return self.prob * (len(self.graph) - 1)

    def plot_dists(self):
        degree_dist = self.degree_dist()
        degrees = list(degree_dist.keys())
        plt.scatter(degrees, list(degree_dist.values()), label=f'degree')

        x_binom = arange(
            binom.ppf(0.01, self.numNodes - 1, self.prob),
            binom.ppf(0.99, self.numNodes - 1, self.prob)
        )
        plt.plot(x_binom,
                          binom.pmf(x_binom, self.numNodes - 1, self.prob), 'g',
                          label=f'binomial')
        
        poisson_average = (self.numNodes - 1) * self.prob
        x_poisson = arange(
            poisson.ppf(0.01, poisson_average),
            poisson.ppf(0.99, poisson_average)
        )
        plt.plot(x_poisson, poisson.pmf(x_poisson, poisson_average), label=f'poisson')
        plt.legend(["Poisson", "Binomial", "Degree"], loc='best', fancybox = True, shadow = True)
        plt.legend(loc='best', frameon=False)
        plt.show()
    
    def small_world(self):
        return log(len(self.graph)) / log(self.averageDegree())
# nodes = 200
# x = Erdos_Renyi_Graph(1/20, nodes)
# x.build()
# string = "../graphs/erdos_" + str(nodes)+ ".edges"
# x.saveGraphToFile(string)



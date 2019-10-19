import graph
import random
import matplotlib.pyplot as plt
from scipy.stats import binom, poisson
from numpy import linspace, arange
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
                        #print("bruna")
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
        print("----", len(degrees))
        print("----", len(degree_dist))
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
        #plt.legend(["Poisson", "Binomial", "Degree"], loc='best', fancybox = True, shadow = True)
        plt.legend(loc='best', frameon=False)
        plt.show()
        
        # print(degree_dist)
        # # Generate some data for this demonstration.

        # # Fit a normal distribution to the data:
        # mu, std = norm.fit(list(degree_dist.values()))

        # # Plot the histogram.
        # plt.hist(list(degree_dist.values()), bins=25, density=True, alpha=0.6, color='g')
        # #plt.plot(list(degree_dist.keys()), list(degree_dist.values()), 'og')

        # # Plot the PDF.
        # xmin, xmax = plt.xlim()
        # print("xmin/max", xmin, xmax)
        # x = linspace(xmin, xmax, 100)
        # p = norm.pdf(x, mu, std)
        # plt.plot(x, p, 'k', linewidth=2)
        # title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
        # plt.title(title)

        # plt.show()

        #print(list(degree_dist.values()))
        # mean, sigma = norm.fit(list(degree_dist.values()))
        # print("mean, sigma:", mean, sigma)
        # plt.plot(list(degree_dist.keys()), list(degree_dist.values()), 'og')
        # plt.plot(list(degree_dist.keys()), norm.pdf(list(degree_dist.values()), mean, sigma))
        # plt.show()
    
    def small_world(self):
        return log(len(self.graph)) / log(self.averageDegree())
#x = Erdos_Renyi_Graph(1/6, 500)
#x.build()
#x.saveGraphToFile("erdos.edges")
#print(x.graph)
#print(x.degrees())
# print("<E> expected", x.avg_numEdges())
# print("E real", x.numEdges)
# print("<k> expected", x.expected_avg_degree())
# print("<k> real", x.averageDegree())
# print("Average Cluster: ", x.averageClust() )
# print("Average path lenght: ", x.averagePathLength())
# print("distance: ", x.distance)
# print("small world: ", x.small_world())
#print(list(x.graph))
#x.degree_dist()

#x.plot_dists()
x = Erdos_Renyi_Graph(1/6,1000)
x.build()
# x.addEdge(0,1)
# x.addEdge(2,3)
# x.addEdge(0,2)
x.saveGraphToFile("erdos.edges")
#print("Average path lenght: ", x.averagePathLength())
#print(x.lenCounts)
#x.plot_info(x.lenCounts)
#print(x.adjencyList())
#print(x.degrees())
print("Number of nodes : ",len(x.graph))
print("<E> expected", x.avg_numEdges())
print("E real", x.numEdges)
print("<k> expected", x.expected_avg_degree())
print("<k> real", x.averageDegree())
print("Average degree: ", x.averageDegree())
#print("Cluster of node 0: ", x.clusterringCoeff("0") )
print("Average Cluster: ", x.averageClust() )
#print("Path from 1 to 8", list(x.bfs("0","8")))
#print("Average path lenght of node 11 ", x.nodePathLength("11"))
#print("Average path lenght: ", x.averagePathLength())
#print("distance: ", x.distance)
print("small world: ", x.small_world())
x.plot_dists()
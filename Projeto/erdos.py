import graph
import random
import matplotlib.pyplot as plt
from scipy.stats import binom, poisson
from numpy import linspace, arange

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
        plt.scatter(degrees, list(degree_dist.values()))

        x_binom = arange(
            binom.ppf(0.01, self.numNodes - 1, self.prob),
            binom.ppf(0.99, self.numNodes - 1, self.prob)
        )
        plt.plot(x_binom,
                          binom.pmf(x_binom, self.numNodes - 1, self.prob), 'g',
                          label='binomial')
        
        poisson_average = (self.numNodes - 1) * self.prob
        x_poisson = arange(
            poisson.ppf(0.01, poisson_average),
            poisson.ppf(0.99, poisson_average)
        )
        plt.plot(x_poisson, poisson.pmf(x_poisson, poisson_average), label=f'poisson')
        #plt.legend(["Poisson", "Binomial", "Degree"], loc='best', fancybox = True, shadow = True)
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
x = Erdos_Renyi_Graph(1/6, 2000)
x.build()
#print(x.graph)
#print(x.degrees())
print(x.avg_numEdges())
print(x.numEdges)
print("<k> expected", x.expected_avg_degree())
print("<k> real", x.averageDegree())
#print(list(x.graph))
#x.saveGraphToFile("erdos.edges")
x.degree_dist()
x.plot_dists()
import graph
import random
import erdos
import matplotlib.pyplot as plt
import numpy as np
#from sklearn.linear_model import LinearRegression

class Barabasi_Albert_Graph(graph.Graph):

    def __init__(self, initNodes, m, numNodesAdded):
        self.numNodesAdded = numNodesAdded
        self.m = m
        self.initNodes = initNodes
        mm = erdos.Erdos_Renyi_Graph(1,initNodes)
        mm.build()
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

    def expected_clust(self):
        return ((np.log(len(self.graph)) )**2 / len(self.graph))
    
    def expected_avg_path(self):
        return np.log(len(self.graph)) / (np.log(np.log(len(self.graph))) )

    def expected_avg_degree(self):
        return  2 * self.m
    
    def loglogplot(self, info):
        x = sorted(list(info.keys()))
        y = [info[k] for k in x]
        xlog = np.log(x)
        ylog = np.log(y)
        ax = plt.gca()
        plt.scatter(xlog, ylog, linewidth=2.5, color='navy')
        
        print(np.array(x).shape)
        print(np.array(x))
        print(-3*np.array(x))
        #plt.plot(xlog, -3*np.array(xlog))

        linear_regressor = LinearRegression()  # create object for the class
        linear_regressor.fit(xlog.reshape((-1, 1)), ylog)  # perform linear regression
        Y_pred = linear_regressor.predict(xlog.reshape((-1, 1)))
        plt.plot(xlog, Y_pred, color='red')
        print('slope:', linear_regressor.coef_)

        plt.xlabel(r'log(x)')
        plt.ylabel(r'log(y)')
        ax.grid(True)
        plt.title(r'Log-Log plot')
        plt.show()
        plt.clf()

# nodes = 1000
# x = Barabasi_Albert_Graph(5,5,nodes)
# x.build()
# string = "../graphs/init_5_m_as_5_baraba_" + str(nodes) + ".edges"
# x.saveGraphToFile(string)
#degrees = x.degree_dist()
#x.plot_info(degrees)
#x.loglogplot(degrees)
#x.loglogplot(degrees)

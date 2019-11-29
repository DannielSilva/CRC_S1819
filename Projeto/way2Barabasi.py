import graph
import random
import erdos
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

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
                #print(probability)
                #print(probability.shape)
                randchosen = random.randint(0,100)
                print("randchosen", randchosen)
                #exit(0)
                #no = random.choices(population=list(self.graph.keys()),weights=probability,k=1)
                #no = no[0]

                threshold = 0
                for i in range(probability.shape[0]):
                    threshold += probability[i]
                    if randchosen < threshold:
                        no = i
                        break
                print("aa",i)

                n = self.addEdge(node, no)
                print("Trying to connect ", node, no)

                if(n != -1):
                    print("Connected")
                    added += 1
                else:
                    print("Nopeeeeeeeeeeeeeeeeeeeeddds")
            if node not in self.graph:
                print("entrei")
                exit(0)
                self.graph[node] = []
                self.degree[node] = 0
            '''if node == 10:
                print(self.graph)
                print(probability)
                exit(0)'''

    def calcProb(self):
        prob = []
        for node in self.degree:
            prob.append(self.degree[node] / self.sumDegree())
        return np.array(prob) * 100

    def expected_clust(self):
        return ((np.log(len(self.graph)) )**2 / len(self.graph))
    
    def expected_avg_path(self):
        return np.log(len(self.graph)) / (np.log(np.log(len(self.graph))) )

    def expected_avg_degree(self):
        return  2 * self.m
    
    def 

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
        plt.plot(xlog, -3*np.array(xlog))

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

x = Barabasi_Albert_Graph(2,2,1000)
x.build()
degrees = x.degree_dist()
x.plot_info(degrees)
x.loglogplot(degrees)
#x.loglogplot(degrees)
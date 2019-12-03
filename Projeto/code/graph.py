import matplotlib.pyplot as plt
import numpy as np
import queue
import matplotlib.pyplot as plt
#from sklearn.linear_model import LinearRegression

class Graph:
    numNodes = 0
    numEdges = 0
    graph = {}
    degree = {}
    lenCounts = {}
    undirected = True
    backEdge = True
    distance = 0
    discovered = {}
    
    def loadGraphFromFile(self, filename):
        with open(filename) as f:
            edge = f.readline()
            while edge:
                pair = edge.split()
                self.addEdge(pair[0], pair[1])
                edge = f.readline()
    
    def saveGraphToFile(self, filename):
        aux = dict(self.graph)
        with open(filename, "w") as f:
            for node in aux:
                for viz in aux[node]:
                    string = str(node) + " " + str(viz) +"\n"
                    f.write(string)
                    if node in aux[viz]:
                        aux[viz].remove(node)
        f.close()

    def addEdge(self, begin, end):
        if begin not in self.graph or (begin in self.graph and end not in self.graph[begin]):
            self.addEdge_aux(begin, end)
            self.numEdges +=1
        
            if self.undirected:
                self.addEdge_aux(end, begin)
        else:
            return -1

    def addEdge_aux(self, begin, end):
        if begin in self.graph:
            self.graph[begin].append(end)
            self.degree[begin] +=1
        else:
            self.graph[begin] = [end]
            self.degree[begin] = 1

    def removeEdge(self, begin, end):
        if begin in self.graph:
            if end in self.graph[begin]:
                self.graph[begin].remove(end)
                self.degree[begin] -= 1
                self.numEdges -=1

                if self.degree[begin] == 0:
                    del self.graph[begin]
                    del self.degree[begin]
    
    def averageDegree(self):
        return 2 * self.numEdges / len(self.graph)

    def sumDegree(self):
        sum = 0
        for node in self.degree:
            sum += self.degree[node]
        return sum
        


    def averageClust(self):
        count = 0
        sum = 0 
        for node in self.graph:
            sum += self.clusterringCoeff(node)
            count += 1
        return sum / count

    def clusterringCoeff(self, node):
        if(node in self.graph):
            neig = len(self.graph[node])
            if neig <=1: return 0
            cluster = self.edgesBetweenNeig(node) / ( neig * ( neig - 1 ) / 2 )
        return cluster

    def edgesBetweenNeig(self,node):
        edges = 0
        if(node in self.graph):
            for viz in self.graph[node]:
                if(viz in self.graph):
                    for vizOfviz in self.graph[viz]:
                        if viz < vizOfviz and vizOfviz in self.graph[node]:
                            edges += 1                   
                            
        return edges

    #code adapted from https://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
    def bfs(self, begin, end):
        queue = [ (begin, [begin])]
        while queue:
            (v, path) = queue.pop(0)
            here = [x for x in self.graph[v] if x not in path]
            for nxt in here:
                if nxt == end:
                    if len(path) > self.distance:
                        self.distance = len(path)
                    return path 
                else:
                    queue.append((nxt, path + [nxt]))
        return []

    def nodePathLength(self, begin):
        sum = 0
        
        for node in self.graph:
            ll = 0
            key = str(node) + "-" + str(begin) 
            if key in self.discovered:
                sum += self.discovered[key]
            elif node != begin:
                ll += len(list(self.bfs(begin, node))) #here
                sum += ll #here
                index = str(begin) + "-" + str(node)
                self.discovered[index] = ll #here
                if(ll in self.lenCounts):
                    self.lenCounts[ll] += 1
                else:
                    self.lenCounts[ll] = 1
        return sum

    def averagePathLength(self):
        sum = 0
        for node in self.graph:
            sum += self.nodePathLength(node)
        return sum / (len(self.graph) * (len(self.graph) - 1)) 

        

    def adjencyList(self):
        return self.graph

    def degrees(self):
        return self.degree

    def draw(self):
        plt.bar(range(len(self.degree)), list(self.degree.values()), align='center')
        plt.xticks(range(len(self.degree)), list(self.degree.keys()))
        plt.show()

    def graph_degree_eachnode(self):
        self.plot_info(self.degree)
        plt.show()
    
    def degree_dist(self):
        info = {}
        for node, degree in self.degree.items():
            if degree in info:
                info[degree] +=1
            else:
                info[degree] = 1
        #print("degree", info)
        #info.update({degree: occurence / (len(self.graph)) for degree, occurence in info.items()})
        #self.plot_info(info)
        #print("degreeeee", info)
        return info

    def plot_info(self, info):
        x = sorted(list(info.keys()))
        y = [info[k] for k in x]
        plt.plot(x, list(y), 'og')
        plt.show()
    
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
    
    def heterogenity(self):
        info = self.degree_dist()
        first = 0
        second = 0
        for degree, Ndegree in info.items():
            first += (degree ** 2) * Ndegree
            second += degree * Ndegree
        first = first / len(self.graph)
        second = second / len(self.graph)
        second = second ** 2
        return first - second



# x = Graph()
#x.build()
# x.loadGraphFromFile("../graphs/baraba_2000.edges")
# print("hete: ",x.heterogenity())
# degrees = x.degree_dist()
# #x.plot_info(degrees)
# d=x.degree
# print("\n")
# print(sorted(d, key=d.get))
# print(sorted(d, key=d.get)[-round(len(x.graph) * 0.05):])
#x.loglogplot(degrees)
    # Code used to compute charts for barabasi analysis
    # def loglogplot(self,title, info):
    #     x = list(info.keys())
    #     z = np.linspace(0,3500,100)
    #     y = list(info.values())
    #     if(title == "clust"):
    #         func = np.power(np.log(z),2)/z
    #         plt.loglog((z), 1/z, '^r', label=f'1/N')
    #     if(title == "apl"):
    #         func = np.log(z)/np.log(np.log(z))
    #         plt.loglog((z), (np.log(z)), '^r',label=f'log(N)')
    #     plt.loglog(z,func, 'ob',label=f'log(N) / log(log(N))' ) #label=f'log(N)^2 / N' OR label=f'log(N) / log(log(N))' )
    #     plt.loglog((x), (y), 'og', label=f'apl')# OR label=f'clust')
    #     plt.title(title)
    #     plt.legend(loc='best', frameon=False)
    #     plt.show()


#Code to build graph from barabasi and analize APL e clust coefficient
# x = Graph()
# x.loadGraphFromFile("barabasi500.edges")
# x.plot_dists()
# dict_clust = {}
# dict_clust[250] = 0.12
# dict_clust[500] = 0.078
# dict_clust[750] = 0.057
# dict_clust[1000] = 0.054
# dict_clust[1500] = 0.04
# dict_clust[2000] = 0.035
# dict_clust[3000] = 0.025
# x.plot_info(dict_clust)
# x.loglogplot("clust",dict_clust)

# dict_apl = {}
# dict_apl[250] = 2.55
# dict_apl[500] = 2.77
# dict_apl[750] = 2.87
# dict_apl[1000] = 2.96
# dict_apl[1500] = 3.038
# dict_apl[2000] = 3.148
# dict_apl[3000] = 3.26
# x.plot_info(dict_apl)
# x.loglogplot("apl",dict_apl)


import matplotlib.pyplot as plt
import numpy as np
import queue

class Graph:
    numNodes = 0
    numEdges = 0
    graph = {}
    degree = {}
    undirected = True
    backEdge = True
    distance = 0
    
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
        edges = []
        if(node in self.graph):
            for viz in self.graph[node]:
                if(viz in self.graph):
                    for vizOfviz in self.graph[viz]:
                        if(vizOfviz in self.graph[node]):
                            if((viz,vizOfviz) not in edges):
                                if((vizOfviz, viz) not in edges):
                                    edges.append((viz,vizOfviz))                    
                            
        return len(edges)

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

    def nodePathLength(self, begin):
        sum = 0
        vistos = {}
        lenght = 0
        for node in self.graph:
            if (node,begin) in vistos:
                sum += vistos[(begin,node)]
            if node != begin:
                length = len(list(self.bfs(begin, node)))
                sum += len(list(self.bfs(begin, node)))
                vistos[(begin,node)] = lenght
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
        info.update({degree: occurence / (len(self.graph)) for degree, occurence in info.items()})
        self.plot_info(info)
        return info

    def plot_info(self, info):
        plt.plot(range(len(info)), list(info.values()), 'og')
        plt.show()
#x = Graph()
# x.addEdge(0,1)
# x.addEdge(2,3)
# x.addEdge(0,2)
#x.loadGraphFromFile("erdos.edges")
#print(x.adjencyList())
#print(x.degrees())
#print("Number of edges : ",x.numEdges)
#print("Number of nodes : ",len(x.graph))
#print("Average degree: ", x.averageDegree())
#print("Cluster of node 0: ", x.clusterringCoeff("0") )
#print("Average Cluster: ", x.averageClust() )
#print("Path from 1 to 8", list(x.bfs("0","8")))
#print("Average path lenght of node 11 ", x.nodePathLength("11"))
#print("Average path lenght: ", x.averagePathLength())
#print("distance: ", x.distance)
# #x.draw()
#x.degree_dist()
# x.removeEdge(0,1)
# x.removeEdge(0,2)
# print(x.adjencyList())
# print(x.degrees())

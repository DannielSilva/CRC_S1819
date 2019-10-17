import matplotlib.pyplot as plt

class Graph:
    numNodes = 0
    numEdges = 0
    graph = {}
    degree = {}
    undirected = True
    backEdge = True
    
    def loadGraphFromFile(self, filename):
        with open(filename) as f:
            edge = f.readline()
            while edge:
                pair = edge.split()
                print(pair)
                self.addEdge(pair[0], pair[1])
                edge = f.readline()

    def addEdge(self, begin, end):
        self.addEdge_aux(begin, end)
        self.numEdges +=1
        
        if self.undirected:
            self.addEdge_aux(end, begin)

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

    def adjencyList(self):
        return self.graph

    def degrees(self):
        return self.degree

    def draw(self):
        plt.bar(range(len(self.degree)), list(self.degree.values()), align='center')
        plt.xticks(range(len(self.degree)), list(self.degree.keys()))
        plt.show()

    def degree_dist(self):
        plt.plot(range(len(self.degree)), list(self.degree.values()), 'og')
        plt.show()

# x = Graph()
# x.addEdge(0,1)
# x.addEdge(2,3)
# x.addEdge(0,2)
# x.loadGraphFromFile("aves-weaver-social-01.edges")
# print(x.adjencyList())
# print(x.degrees())
# print(x.numEdges)
# print("removing")
# x.degree_dist()
# x.removeEdge(0,1)
# x.removeEdge(0,2)
# print(x.adjencyList())
# print(x.degrees())

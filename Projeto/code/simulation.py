import graph
import random
import math
import matplotlib.pyplot as plt

class Cooperation_Simulation:

    def __init__(self, net, value_T=2, value_S=-1):
        self.options = ["C","D"]
        self.payoff = {"C-C":1, "C-D":value_S, "D-D":0, "D-C": value_T} #R,S,P,T
        print(self.payoff)
        #exit(0)
        self.network = net
        self.strategy_of_node = self.alternateStrategy()
        print(self.strategy_of_node)
       
        self.new_strategy_of_node = self.strategy_of_node
        self.scores = {node: 0 for node in self.network.graph.keys()}
        self.results = []

    def reset_simulation(self):
        self.scores = {node: 0 for node in self.network.graph.keys()}
        self.strategy_of_node = self.alternateStrategy()
        self.new_strategy_of_node = self.strategy_of_node

    def initStrategy(self):
        Cs = random.sample(population=list(self.network.graph.keys()),k=len(list(self.network.graph.keys()))//2,)
        # print(list(self.network.graph.keys()))
        # exit(0)
        return {node: "C" if node in Cs else "D" for node in self.network.graph.keys()}
    
    def alternateStrategy(self):
        return {node: "C" if int(node)%2 == 0 else "D" for node in self.network.graph.keys()}

    def staticStrategy(self):
        return {node: "C" if int(node) < len(self.network.graph) //2 else "D" for node in self.network.graph.keys()}

    def run(self, numGes, numSims):
        for s in range(numSims):
            self.reset_simulation()
            self.computeFit()
            for g in range(numGes):
                print("s,g", s, g)
                numDs, node = self.iterateReplicatorFormulla(10)
                self.computeFitForNodeAndViz(node)
            self.results.append(numDs / len(self.network.graph))
        plt.figure()
        plt.plot(list(range(len(self.results))),self.results)
        plt.show()
        return sum(self.results) / len(self.results)

            


    def computeFit(self):
        for node in self.scores:
            self.scores[node] = self.computeFitNode(node)
    
    def computeFitForNodeAndViz(self, node):
        self.scores[node] = self.computeFitNode(node)
        for viz in self.network.graph[node]:
            self.scores[viz] = self.computeFitNode(viz)


    def computeFitNode(self, node):
        score = 0
        lista = []
        if(node in self.network.graph):
            for viz in self.network.graph[node]:
                # print(node)
                # print(viz)
                # print(type(viz))
                
                interation = self.strategy_of_node[node] + "-" + self.strategy_of_node[viz]
                score += self.payoff[interation]
                lista.append(str(interation) + " = " + str(self.payoff[interation]))
            lista.append("Final Score: " + str(score))
        # print(lista)
        # exit(0)
        return score
    
    def iterateGreedNeig(self):
        self.strategy_of_node = self.new_strategy_of_node
        #print(sum( value == "D" for value in self.strategy_of_node.values()))
        for node in self.strategy_of_node:
            self.iterateGreedNeigNode(node)
        numDs = sum( value == "D" for value in self.strategy_of_node.values())
        #print(numDs)
        return numDs
            
    def iterateGreedNeigNode(self,node):
        max_score = 0 #self.scores[node]
        toReplicate = node
        for viz in self.network.graph[node]:
            if max_score < self.scores[viz]:
                max_score = self.scores[viz]
                toReplicate = viz
        #print("\nPrevious strategy: ",self.strategy_of_node[node] )
        self.new_strategy_of_node[node] = self.strategy_of_node[toReplicate]
        #print("\nNew strategy: ",self.new_strategy_of_node[node] )

    def iterateReplicatorFormulla(self,beta):
        self.strategy_of_node = self.new_strategy_of_node
        print(sum( value == "D" for value in self.strategy_of_node.values()))
        # for node in self.strategy_of_node:
        #     self.iterateReplicatorFormullaNode(node,beta)
        ''''''
        node = random.choice(list(self.strategy_of_node.keys()))
        self.iterateReplicatorFormullaNode(node,beta)
        ''''''
        numDs = sum( value == "D" for value in self.strategy_of_node.values())
        #print(numDs)
        return numDs, node

    def iterateReplicatorFormullaNode(self,node,beta):
        fitA = self.scores[node]
        # fitB = 0
        # for viz in self.network.graph[node]:
        #     fitB += self.scores[viz]
        # fitB = fitB / len(self.network.graph[node])
        viz = random.choice(self.network.graph[node])
        fitB = self.scores[viz]
        prob = 1 / (1 + math.exp(-beta * (fitB - fitA)))
        toChoose = {}
        toChoose[self.strategy_of_node[node]] = 1-prob
        inverse = [x for x in self.options if x != self.strategy_of_node[node]]
        inverse = inverse[0]
        toChoose[self.strategy_of_node[node]]=1-prob
        toChoose[inverse]=prob
        strategy = random.choices(list(toChoose.keys()),weights = list(toChoose.values()), k = 1)
        strategy = strategy[0]
        self.new_strategy_of_node[node] = strategy
        #print("\nPrevious strategy: ",self.strategy_of_node[node] )
        #self.new_strategy_of_node[node] = self.strategy_of_node[toReplicate]




x = graph.Graph()
x.loadGraphFromFile("../graphs/complete.edges")

y = Cooperation_Simulation(x,1,0)
#print(y.scores)
#y.computeFit()
#print(y.scores)
#y.iterateGreedNeig()
res = y.run(10000,3)
print("res",res)
#beta = 0.1
#print(y.iterateReplicatorFormulla(10))
#print(sum( value == "D" for value in y.strategy_of_node.values()))

#Introduzir um erro, fazer tipo uma funcao q faz o switch de C para D
#em vez de fazer o switch em cada iterate

#os graus do random e da scale free têm de ser iguais
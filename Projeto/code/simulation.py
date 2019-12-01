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
        self.strategy_of_node = self.selectTopHubs(0.05)
        print(self.strategy_of_node)
       
        self.new_strategy_of_node = self.strategy_of_node
        self.scores = {node: 0 for node in self.network.graph.keys()}
        self.results = []
        self.fitDelta = 0

    def reset_simulation(self):
        self.strategy_of_node = self.selectTopHubs(0.05)
        self.new_strategy_of_node = self.strategy_of_node

    def randomStrategy(self):
        Cs = random.sample(population=list(self.network.graph.keys()),k=len(list(self.network.graph.keys()))//2,)
        # print(list(self.network.graph.keys()))
        # exit(0)
        return {node: "C" if node in Cs else "D" for node in self.network.graph.keys()}
    
    def selectTopHubs(self, fraction, niceHubs=True):
        d = self.network.degree
        top = round(len(self.network.graph) * fraction)
        hubs = sorted(d, key=d.get)[-top:]
        print("hubs",hubs)
        print("lenhubs",len(hubs))
        # exit(0)
        #['3', '10', '19', '9', '6', '5', '11', '8', '1', '0', '2', '7', '4']
        return {node: "C" if niceHubs and node in hubs else "D" for node in self.network.graph.keys()}

    def alternateStrategy(self):
        return {node: "C" if int(node)%2 == 0 else "D" for node in self.network.graph.keys()}

    def staticStrategy(self):
        return {node: "C" if int(node) < len(self.network.graph) //2 else "D" for node in self.network.graph.keys()}

    def run(self, numGes, numSims):
        for s in range(numSims):
            grow = []
            self.reset_simulation()
            for g in range(numGes):
                self.computeFit()
                if self.fitDelta==0:
                    print("Someone has taken over")
                    break
                numDs = self.iterateReplicatorFormulla(0.001)
                grow.append(numDs)
                if numDs == 0:
                    print("C's has taken over")
                    break
                if numDs == len(self.network.graph):
                    print("D's has taken over")
                    exit(0)
                print("s,g", s, g)
                #print("fitdelta", self.fitDelta)
            self.results.append(numDs / len(self.network.graph))
        plt.figure()
        plt.plot(list(range(len(self.results))),self.results)
        plt.show()

        return sum(self.results) / len(self.results)

            


    def computeFit(self):
        i = 0
        fitMax = 0
        fitMin = 0
        for node in self.scores:
            fitScore = self.computeFitNode(node)
            self.scores[node] = fitScore
            if i == 0:
                fitMax = fitScore
                fitMin = fitScore
                i+=1
            if fitScore > fitMax:
                fitMax = fitScore
            if fitScore < fitMin:
                fitMin = fitScore
        self.fitDelta = fitMax - fitMin
            
    
    # def computeFitForNodeAndViz(self, node):
    #     self.scores[node] = self.computeFitNode(node)
    #     for viz in self.network.graph[node]:
    #         self.scores[viz] = self.computeFitNode(viz)


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
        for node in self.strategy_of_node:
            self.iterateReplicatorFormullaNodeExponential(node,beta)
            #self.iterateReplicatorFormullaNodeDelta(node,beta)
        # ''''''
        # node = random.choice(list(self.strategy_of_node.keys()))
        # self.iterateReplicatorFormullaNode(node,beta)
        # ''''''
        numDs = sum( value == "D" for value in self.strategy_of_node.values())
        #print(numDs)
        return numDs

    def iterateReplicatorFormullaNodeExponential(self,node,beta):
        fitA = self.scores[node]
        # fitB = 0
        # for viz in self.network.graph[node]:
        #     fitB += self.scores[viz]
        # fitB = fitB / len(self.network.graph[node])
        viz = random.choice(self.network.graph[node])
        fitB = self.scores[viz]
        prob = 1 / (1 + math.exp(-beta * (fitB - fitA)))
        #prob = (fitB - fitA) / self.fitDelta
        if prob < 0:
            prob = 0
        toChoose = {}
        toChoose[self.strategy_of_node[node]] = 1-prob
        inverse = [self.strategy_of_node[viz]]
        inverse = inverse[0]
        toChoose[inverse]=prob
        strategy = random.choices(list(toChoose.keys()),weights = list(toChoose.values()), k = 1)
        strategy = strategy[0]
        self.new_strategy_of_node[node] = strategy
        #print("\nPrevious strategy: ",self.strategy_of_node[node] )
        #self.new_strategy_of_node[node] = self.strategy_of_node[toReplicate]

    def iterateReplicatorFormullaNodeDelta(self,node,beta):
        fitA = self.scores[node]
        # fitB = 0
        # for viz in self.network.graph[node]:
        #     fitB += self.scores[viz]
        # fitB = fitB / len(self.network.graph[node])
        viz = random.choice(self.network.graph[node])
        fitB = self.scores[viz]
        #prob = 1 / (1 + math.exp(-beta * (fitB - fitA)))
        prob = (fitB - fitA) / self.fitDelta
        if prob < 0:
            prob = 0
        toChoose = {}
        toChoose[self.strategy_of_node[node]] = 1-prob
        inverse = [self.strategy_of_node[viz]]
        inverse = inverse[0]
        toChoose[inverse]=prob
        strategy = random.choices(list(toChoose.keys()),weights = list(toChoose.values()), k = 1)
        strategy = strategy[0]
        self.new_strategy_of_node[node] = strategy
        #print("\nPrevious strategy: ",self.strategy_of_node[node] )
        #self.new_strategy_of_node[node] = self.strategy_of_node[toReplicate]




x = graph.Graph()
string = "complete.edges"
x.loadGraphFromFile("../graphs/" + string)

y = Cooperation_Simulation(x,2,-1)
#print(y.scores)
#y.computeFit()
#print(y.scores)
#y.iterateGreedNeig()
name = "../reports/"+string + ".txt"
report = string + " heteroginity: " + str(x.heterogenity())
f = open(name, "w")
f.write(report)
f.close()
res = y.run(10000000,5)
print("res",res)
#beta = 0.1
#print(y.iterateReplicatorFormulla(10))
#print(sum( value == "D" for value in y.strategy_of_node.values()))

#Introduzir um erro, fazer tipo uma funcao q faz o switch de C para D
#em vez de fazer o switch em cada iterate

#os graus do random e da scale free têm de ser iguais
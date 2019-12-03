import graph
import random
import matplotlib.pyplot as plt
import numpy as np
from math import log

class Lattice_Square(graph.Graph):

    def __init__(self, size):
        self.size = size

    def build(self):
        chumbo = self.size*self.size
        print(chumbo)
        '''for id in range(chumbo):
            if id not in self.graph:
                self.graph[id] = []
                self.degree[id] = 0'''
        for id in range(chumbo):
            first = (id % self.size)
            second = ((id+1) % self.size)
            if second > first:
                self.addEdge(id, id+1)
            if second < first:
                self.addEdge(id, (id//self.size)*self.size)
            
            term = (id // self.size) + 1
            if term != self.size:
                self.addEdge(id, id+self.size)
            if term == self.size:
                self.addEdge(id, (id%self.size))
            #self.addEdge(id, id-1)
            #self.addEdge(id, id - self.size)

x = Lattice_Square(32)
x.build()
x.saveGraphToFile("lattice.edges")
print(x.heterogenity())
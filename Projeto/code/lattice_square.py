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
            if id%self.size != self.size-1:
                self.addEdge(id, id+1)
            if id//self.size != self.size-1:
                self.addEdge(id, id + self.size)
            #self.addEdge(id, id-1)
            #self.addEdge(id, id - self.size)

x = Lattice_Square(10)
x.build()
x.saveGraphToFile("lattice.edges")
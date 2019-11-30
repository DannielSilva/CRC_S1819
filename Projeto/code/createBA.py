import networkx as nx

G = nx.barabasi_albert_graph(1000,2)
nx.write_edgelist(G, "model.edgelist")

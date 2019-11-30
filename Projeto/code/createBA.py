import networkx as nx

G = nx.barabasi_albert_graph(750,2)
nx.write_edgelist(G, "model.edgelist")

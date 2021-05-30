import networkx as nx
import matplotlib.pyplot as plt


port = {
    'A': 6000,
    'B': 6001,
    'C': 6002,
    'D': 6003,
    'E': 6004,
    'F': 6005,
    'G': 6006,
    'H': 6007,
    'I': 6008,
    'J': 6009,
}

# Create networkx object
# G = nx.Graph()
# G is empty graph

# add edges with weights
# edge labesl can be anything
# here weight is an attribute
# can use anyname instead of weight
# G.add_edge('A', 'B', weight=0.4)
# G.add_edge('A', 'G', weight=2.2)
# G.add_edge('A', 'F', weight=2.3)
# G.add_edge('B', 'C', weight=6.5)
# G.add_edge('B', 'D', weight=0.7)
# G.add_edge('B', 'G', weight=0.2)
# G.add_edge('C', 'F', weight=3.2)
# G.add_edge('C', 'D', weight=1.1)
# G.add_edge('C', 'H', weight=0.1)
# G.add_edge('E', 'H', weight=0.5)
# G.add_edge('E', 'F', weight=4.5)
# G.add_edge('E', 'D', weight=1.5)
# G.add_edge('I', 'D', weight=1.5)
# G.add_edge('I', 'J', weight=3.5)
# G.add_edge('F', 'J', weight=5.4)

# choose a plot size
# plt.figure(figsize =(9, 9))

# get the coordinates for the g4raph nodes
# we can also give this manually
# pos=nx.spring_layout(G)

# draw the graph
# it only draws vertices and connections between them, there are no edge label till now
# nx.draw_networkx(G,pos)

# get edge labels
# labels = nx.get_edge_attributes(G,'weight')

# draw the edges labels with the parameters
# label_pos is used to avoid the label overlap
# nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, label_pos=0.3)
# plt.show()

# shortest_path is inbuilt function which has dijikstra implemenation
# it find the shortest path using weight as parameter
# print(nx.single_source_dijkstra_path_length(G, source='A', weight='weight'))

# for i in port.keys():
#     print(nx.single_source_dijkstra(G, source=i))
# it find the shortest path length using weight as parameter

import random

G = nx.gnm_random_graph(10, 15)
for (u, v, w) in G.edges(data=True):
    w['weight'] = random.randint(1, 50)

mapping = {0: "A", 1: "B", 2: "C", 3: 'D', 4: "E", 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}
G = nx.relabel_nodes(G, mapping)

# choose a plot size
plt.figure(figsize=(9, 9))

# get the coordinates for the graph nodes
# we can also give this manually
pos = nx.spring_layout(G)

# draw the graph
# it only draws vertices and connections between them, there are no edge label till now
nx.draw_networkx(G, pos)

# get edge labels
labels = nx.get_edge_attributes(G, 'weight')

# draw the edges labels with the parameters
# label_pos is used to avoid the label overlap
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.3)
plt.show()

port = {
    'A': 6000,
    'B': 6001,
    'C': 6002,
    'D': 6003,
    'E': 6004,
    'F': 6005,
    'G': 6006,
    'H': 6007,
    'I': 6008,
    'J': 6009,
}

for node in G.nodes():
    f = open("{}config.txt".format(node), "w")
    neighbours = G[node]
    f.write(str(len(neighbours)))
    f.write("\n")
    for i in neighbours:
        f.write("{} {} {}\n".format(i, G[node][i]['weight'], port[i]))

# print(nx.single_source_dijkstra_path_length(G, source='A', weight='weight'))

for i in port.keys():
    print(nx.single_source_dijkstra(G, source=i))
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pickle

file = open("airports\\global-cities.dat", "r")

#build list of node ids
node_ids = []
#build dictionary to retrieve airport names with node ids
node_dict = dict()

for line in file:

    node_items = line.split("|")

    node_id = node_items[1]
    node_name = node_items[2].strip()

    node_dict[node_id] = node_name

    node_ids.append(node_items[1])

file.close()

#F is a graph with all nodes and links including isolated nodes
F: nx.Graph = nx.read_edgelist('airports\\global-net.dat')
F.add_nodes_from(node_ids)

#print to get size for Q1
print("The airport network is a:", F)

F_component_iter = nx.connected_components(F)

F_sorted_components = sorted(F_component_iter, key=len, reverse=True)

print("The number of compoents in the airport network is:", len(F_sorted_components))

G: nx.Graph = F.subgraph(F_sorted_components[0])

print("The largest componet in the airport network is a:", G)

G_sorted_degree = sorted(G.degree(), key=lambda tup: tup[1], reverse = True)

G_top_ten = G_sorted_degree[0:10]

nodes_top_ten = set()

for id, count in G_top_ten:

    node_neighbours_iter = G.neighbors(id)

    nodes_top_ten.add(id)

    [nodes_top_ten.add(n) for n in node_neighbours_iter]

    print(node_dict[id],"|", count)

print(len(nodes_top_ten))

x = range(1, 251)
xys = [(x_i, len([n for n in G_sorted_degree if n[1] == x_i]) / (G.number_of_nodes())) for x_i in x]

xys = [xy_i for xy_i in xys if xy_i[1] > 0]

x, y = zip(*xys)

plt.plot(x, y)
plt.title("Degree distribution")
plt.xlabel("Degree")
plt.ylabel("Percentage of nodes")
plt.show()

plt.plot(np.log10(x), np.log10(y))
plt.title("log - log scale Degree")
plt.xlabel("log_10 Degree")
plt.ylabel("log_10 Percentage of nodes")
plt.show()



print(nx.diameter(G=G))

G_shortest_paths = nx.shortest_path(G)

#with open("G_shortest_paths.pkl", "wb") as f:
#    pickle.dump(G_shortest_paths, f)


#with open("G_shortest_paths.pkl", "rb") as f:
#    G_shortest_paths = pickle.load(f)

'''
for k1 in G_shortest_paths:
    for k2 in G_shortest_paths[k1]:

        if(len(G_shortest_paths[k1][k2]) == 18):
            #print(len(G_shortest_paths[k1][k2]))
            #print(G_shortest_paths[k1][k2])
            print("--")
            for n in G_shortest_paths[k1][k2]:
                print("|", node_dict[n], "|")
'''



#CBR id is "501" and Cape town is 635

CBR_CPT_shortest_path = G_shortest_paths["501"]["635"]

for n in CBR_CPT_shortest_path:
    print("|",node_dict[n],"|")

#G_betweenness = nx.betweenness_centrality(G)
#with open("G_betweeness.pkl", "wb") as f:
#    pickle.dump(G_betweenness, f)

with open("G_betweeness.pkl", "rb") as f:
    G_betweeness = pickle.load(f)

top_ten = sorted(G_betweeness, key=lambda k: G_betweeness[k], reverse=True)[:10]


for t in top_ten:
    print("|", node_dict[t], "|", G_betweeness[t], "|")





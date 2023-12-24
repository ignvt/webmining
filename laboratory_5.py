import random
import time

import matplotlib.pyplot as plt
import networkx as nx
import requests

edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
G = nx.Graph()
DG = nx.DiGraph()
G.add_edges_from(edges)
nx.draw(G, with_labels=True)
plt.show()

hypercube = nx.hypercube_graph(3)
cycle_basis_hypercube = nx.cycle_basis(hypercube)
print("cycles:")
for cycle in cycle_basis_hypercube:
    print(cycle)
for i, cycle in enumerate(cycle_basis_hypercube, start=1):
    H = hypercube.subgraph(cycle)
    plt.subplot(2, 3, i)
    nx.draw(H, with_labels=True)
    plt.title(i)
plt.tight_layout()
plt.show()

for edge in edges:
    DG.add_edge(edge[0], edge[1])
    DG.add_edge(edge[1], edge[0])
cycles_in_directed_graph = list(nx.simple_cycles(DG))
print("cycles:")
for cycle in cycles_in_directed_graph:
    print(cycle)
for i, cycle in enumerate(cycles_in_directed_graph, start=1):
    subgraph_nodes = set(cycle)
    H = DG.subgraph(subgraph_nodes)
    plt.subplot(4, 3, i)
    nx.draw_circular(H, with_labels=True)
    plt.title(i)
plt.tight_layout()
plt.show()

pos = nx.spring_layout(hypercube)
nx.draw(hypercube, pos, with_labels=True)
plt.tight_layout()
plt.show()

random_graph = nx.Graph()
random_graph.add_nodes_from(range(10))
for i in range(10):
    for j in range(i + 1, 10):
        if random.uniform(0, 1) < 0.1:
            random_graph.add_edge(i, j)

pos = nx.spring_layout(random_graph)
nx.draw(random_graph, pos, with_labels=True)
plt.show()

probabilities = []
largest_component_sizes = []
for _ in range(1000):
    p_i = random.uniform(0.005, 0.03)
    probabilities.append(p_i)
    G = nx.erdos_renyi_graph(100, p_i)
    connected_components = list(nx.connected_components(G))
    largest_component_size = max(len(component) for component in connected_components)
    largest_component_sizes.append(largest_component_size)
plt.scatter(probabilities, largest_component_sizes)
plt.xlabel("p_i")
plt.ylabel("best s_i")
plt.show()


# "https://oauth.vk.com/authorize?client_id=???&display=page&scope=friends&response_type=token&v=5.199&state=123456")
def get_friends_ids(user_id):
    friends_url = f"https://api.vk.com/method/friends.get?user_id={user_id}&v=5.199&access_token=???"
    json_response = requests.get(friends_url.format(user_id)).json()
    if json_response.get("error"):
        print(json_response.get("error"))
        return list()
    print(json_response[u"response"]["items"])
    return json_response[u"response"]["items"]


graph = {}
friend_ids = get_friends_ids(2761603)
for friend in friend_ids[:2]:
    graph[friend] = get_friends_ids(friend)
    time.sleep(2)

g = nx.Graph(directed=False)
for i in graph:
    g.add_node(i, label=i)
    for j in graph[i]:
        if i != j and i in friend_ids and j in friend_ids:
            g.add_edge(i, j)

pos = nx.spring_layout(g)
nx.draw(g, pos, with_labels=True)
plt.tight_layout()
plt.show()

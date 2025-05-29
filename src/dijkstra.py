import networkx as nx
import re
import matplotlib.pyplot as plt
from graphe import G

start = ("Bondy (E)")
end = ("Nanterre-Universite (A)")

try:
    path = nx.shortest_path(G, source=start, target=end, weight='weight')
    distance = nx.shortest_path_length(G, source=start, target=end, weight='weight')

    print(f"Distance : {distance:.2f} km")
    print("Chemin :")
    for i, node in enumerate(path):
        station, ligne = re.match(r"^(.*) \((.*)\)$", node).groups()
        print(f"{i + 1:02d}. {station:<30} Ligne {ligne}")

except nx.NetworkXNoPath:
    print(f"Aucun chemin trouvé entre {start} et {end}")
except nx.NodeNotFound as e:
    print(e)

# === Création d'un sous-graphe avec uniquement les stations du chemin ===
G_path = nx.Graph()

# On ajoute les nœuds du chemin avec leurs attributs
for node in path:
    G_path.add_node(node, **G.nodes[node])

# On ajoute les arêtes dans l'ordre du chemin
for i in range(len(path) - 1):
    u, v = path[i], path[i+1]
    edge_data = G.get_edge_data(u, v)
    G_path.add_edge(u, v, **edge_data)

# === Position des nœuds selon leur géolocalisation ===
pos = {node: (G_path.nodes[node]['lon'], G_path.nodes[node]['lat']) for node in G_path.nodes}
node_colors = [G_path.nodes[node]['couleur'] for node in G_path.nodes]

# === Affichage ===
plt.figure(figsize=(10, 8))
nx.draw(G_path, pos, node_color=node_colors, edge_color="black",
        node_size=150, with_labels=True, font_size=7)
plt.title(f"Chemin entre {start} et {end}")
plt.axis('off')
plt.show()
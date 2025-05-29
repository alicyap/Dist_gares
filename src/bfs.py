import networkx as nx
import matplotlib.pyplot as plt
import re
from graphe import G

start = "Bondy (E)"
end = "Nanterre-Universite (A)"

def afficher_chemin(path, titre="Chemin", couleur="green"):
    print(f"\n{titre} ({len(path)} stations) :")
    for i, node in enumerate(path):
        station, ligne = re.match(r"^(.*) \((.*)\)$", node).groups()
        print(f"{i + 1:02d}. {station:<30} Ligne {ligne}")

    # Graphe du chemin uniquement
    G_path = nx.Graph()
    for node in path:
        G_path.add_node(node, **G.nodes[node])
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        edge_data = G.get_edge_data(u, v)
        G_path.add_edge(u, v, **edge_data)

    pos = {node: (G_path.nodes[node]['lon'], G_path.nodes[node]['lat']) for node in G_path.nodes}
    node_colors = [G_path.nodes[node]['couleur'] for node in G_path.nodes]

    plt.figure(figsize=(10, 8))
    nx.draw(G_path, pos, node_color=node_colors, edge_color=couleur, node_size=150,
            with_labels=True, font_size=7)
    plt.title(titre)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# === BFS : plus court chemin en nombre de stations
try:
    path_bfs = nx.shortest_path(G, source=start, target=end)  # sans poids
    print(f"Chemin BFS trouvé (nombre de stations : {len(path_bfs)})")
    afficher_chemin(path_bfs, titre="🟢 BFS - Chemin le plus court en nombre d'étapes", couleur="green")
except nx.NetworkXNoPath:
    print("Aucun chemin trouvé avec BFS.")
except nx.NodeNotFound as e:
    print(e)
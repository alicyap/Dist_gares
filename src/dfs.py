import networkx as nx
import matplotlib.pyplot as plt
import re
from graphe import G

start = "Bondy (E)"
end = "Nanterre-Universite (A)"

def afficher_chemin(path, titre="Chemin DFS", couleur="purple"):
    print(f"\n{titre} ({len(path)} stations) :")
    for i, node in enumerate(path):
        match = re.match(r"^(.*) \((.*)\)$", node)
        station, ligne = match.groups() if match else (node, "")
        print(f"{i + 1:02d}. {station:<30} Ligne {ligne}")

    # Graphe restreint au chemin
    G_path = nx.Graph()
    for node in path:
        G_path.add_node(node, **G.nodes[node])
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        edge_data = G.get_edge_data(u, v)
        if edge_data:
            G_path.add_edge(u, v, **edge_data)

    pos = {node: (G_path.nodes[node]['lon'], G_path.nodes[node]['lat']) for node in G_path.nodes}
    node_colors = [G_path.nodes[node]['couleur'] for node in G_path.nodes]

    plt.figure(figsize=(10, 8))
    nx.draw(G_path, pos=pos, node_color=node_colors, edge_color=couleur, node_size=150,
            with_labels=True, font_size=7)
    plt.title(titre)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# === Fonction DFS pour trouver un chemin
def dfs_path(graph, start, end, path=None, visited=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path = path + [start]

    if start == end:
        return path

    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            new_path = dfs_path(graph, neighbor, end, path, visited)
            if new_path:
                return new_path
    return None

# === Application de DFS
try:
    path_dfs = dfs_path(G, start, end)
    if path_dfs:
        print("✅ Chemin trouvé avec DFS.")
        afficher_chemin(path_dfs, titre="🟣 DFS - Chemin exploratoire", couleur="purple")
    else:
        print("❌ Aucun chemin trouvé avec DFS.")
except nx.NodeNotFound as e:
    print(e)
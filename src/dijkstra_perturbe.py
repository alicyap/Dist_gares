import networkx as nx
import matplotlib.pyplot as plt
import re
from graphe import G

start = "Nanterre-Universite (A)"
end = "Bondy (E)"
noeud_supprime = "Noisy-le-Sec (E)"

def afficher_chemin(path, titre="Chemin", couleur="black"):
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
    plt.show()

# === Chemin initial
try:
    path_original = nx.shortest_path(G, source=start, target=end, weight='weight')
    distance_original = nx.shortest_path_length(G, source=start, target=end, weight='weight')
    print(f"Distance originale : {distance_original:.2f} km")
    afficher_chemin(path_original, titre="🔵 Chemin sans perturbation", couleur="blue")
except nx.NetworkXNoPath:
    print("Aucun chemin trouvé dans le graphe original.")
except nx.NodeNotFound as e:
    print(e)

# === Chemin avec arrêt supprimé
print(f"\n❌ Perturbation simulée : arrêt retiré → {noeud_supprime}")
G_modif = G.copy()
if noeud_supprime in G_modif.nodes:
    G_modif.remove_node(noeud_supprime)

    try:
        path_alt = nx.shortest_path(G_modif, source=start, target=end, weight='weight')
        distance_alt = nx.shortest_path_length(G_modif, source=start, target=end, weight='weight')
        print(f"Distance alternative : {distance_alt:.2f} km")
        afficher_chemin(path_alt, titre="🔴 Chemin alternatif (sans Noisy-le-Sec)", couleur="red")
    except nx.NetworkXNoPath:
        print("❌ Aucun chemin possible sans cet arrêt.")
    except nx.NodeNotFound as e:
        print(e)
else:
    print("🚫 Noeud déjà absent du graphe.")
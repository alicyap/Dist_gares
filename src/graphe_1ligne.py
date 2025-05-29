import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math
from pathlib import Path

# Dossier contenant le script
current_dir = Path(__file__).resolve().parent

# Dossier "data" au même niveau que "src"
base_path = current_dir.parent / "data"

# Chemins vers les fichiers
fichier_gares = base_path / "gares_ok.csv"
fichier_couleurs = base_path / "color_mapping.csv"

# Chargement des données
df_gares = pd.read_csv(fichier_gares, sep=';')
df_couleurs = pd.read_csv(fichier_couleurs, sep=';')

# === Conversion des indices en chaînes de caractères ===
df_gares["indice_lig"] = df_gares["indice_lig"].astype(str)
df_couleurs["indice"] = df_couleurs["indice"].astype(str)

# === Jointure pour récupérer la couleur des lignes ===
df_gares = df_gares.merge(df_couleurs[["indice", "ColourWeb_hexa"]],
                          left_on="indice_lig", right_on="indice", how="left")
df_gares["ColourWeb_hexa"] = df_gares["ColourWeb_hexa"].fillna("gray")

# === Extraction des coordonnées ===
df_gares[['lat', 'lon']] = df_gares['Geo Point'].str.split(',', expand=True).astype(float)

# === Moyenne des coordonnées par station ===
df_grouped = df_gares.groupby(["nom_long", "indice_lig"]).agg({
    "lat": "mean",
    "lon": "mean",
    "ColourWeb_hexa": "first"
}).reset_index()

# === Fonction de distance Haversine ===
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# === Fonction pour connecter une ligne ===
def connecter_stations_ligne(G, stations, rayon=100):
    sous_graphe = G.subgraph(stations).copy()
    composants = list(nx.connected_components(sous_graphe))

    while len(composants) > 1:
        min_dist = float("inf")
        paire = (None, None)

        for comp1 in composants:
            for comp2 in composants:
                if comp1 == comp2:
                    continue
                for s1 in comp1:
                    for s2 in comp2:
                        lat1, lon1 = G.nodes[s1]['lat'], G.nodes[s1]['lon']
                        lat2, lon2 = G.nodes[s2]['lat'], G.nodes[s2]['lon']
                        d = haversine(lat1, lon1, lat2, lon2)
                        if d <= rayon and d < min_dist:
                            min_dist = d
                            paire = (s1, s2)

        if paire != (None, None):
            G.add_edge(*paire, weight=min_dist)
            composants = list(nx.connected_components(G.subgraph(stations).copy()))
        else:
            print("❌ Impossible de connecter complètement la ligne (trop de distance entre certains points).")
            break

# === Filtres uniquement une ligne ===
df_ligne = df_grouped[df_grouped["indice_lig"] == "L"]

# === Création du graphe pour la ligne sélectionée ===
G = nx.Graph()
for _, row in df_ligne.iterrows():
    station = row["nom_long"]
    G.add_node(station, lat=row["lat"], lon=row["lon"], ligne=row["indice_lig"], couleur=row["ColourWeb_hexa"])

stations_e = df_ligne["nom_long"].tolist()
connecter_stations_ligne(G, stations_e, rayon=100)

# === Affichage ===
pos = {node: (G.nodes[node]['lon'], G.nodes[node]['lat']) for node in G.nodes}
node_colors = [G.nodes[node]["couleur"] for node in G.nodes]

plt.figure(figsize=(12, 10))
nx.draw(G, pos=pos, node_color=node_colors, edge_color="gray", node_size=100, with_labels=True, font_size=7)
plt.title("Connexion complète")
plt.axis('off')
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
plt.show()
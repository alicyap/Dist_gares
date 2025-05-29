import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math

# === Chargement des données ===
df_gares = pd.read_csv(r"C:\Users\meowy\OneDrive\Bureau\L3Miage\Dist_gares\data\gares_ok.csv", sep=';')
df_couleurs = pd.read_csv(r"C:\Users\meowy\OneDrive\Bureau\L3Miage\Dist_gares\data\color_mapping.csv", sep=';')

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
    R = 6371  # rayon terrestre en km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# === Fonction pour connecter les stations d'une même ligne ===
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
            print("❌ Ligne non complètement connectée : certaines stations sont trop éloignées.")
            break

# === Création du graphe global ===
G = nx.Graph()

# === Itération sur chaque ligne ===
for ligne, df_ligne in df_grouped.groupby("indice_lig"):
    stations_ligne = df_ligne["nom_long"].tolist()

    # Ajout des noeuds pour cette ligne
    for _, row in df_ligne.iterrows():
        station = row["nom_long"]
        G.add_node(station, lat=row["lat"], lon=row["lon"], ligne=row["indice_lig"], couleur=row["ColourWeb_hexa"])

    # Connexion des stations de cette ligne uniquement
    connecter_stations_ligne(G, stations_ligne, rayon=100)

# === Affichage final ===
pos = {node: (G.nodes[node]['lon'], G.nodes[node]['lat']) for node in G.nodes}
node_colors = [G.nodes[node]["couleur"] for node in G.nodes]

plt.figure(figsize=(16, 14))
nx.draw(G, pos=pos, node_color=node_colors, edge_color="lightgray", node_size=100, with_labels=False, font_size=6)
plt.title("Connexion des stations par ligne (aucune interconnexion entre lignes)")
plt.axis('off')
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
plt.show()
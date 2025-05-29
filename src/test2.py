import pandas as pd
import networkx as nx
import math
import matplotlib.pyplot as plt

# === Chargement des données ===
df_gares = pd.read_csv(r"C:\Users\meowy\OneDrive\Bureau\L3Miage\Dist_gares\data\gares_ok.csv", sep=';')
df_couleurs = pd.read_csv(r"C:\Users\meowy\OneDrive\Bureau\L3Miage\Dist_gares\data\color_mapping.csv", sep=';')
df_gares["indice_lig"] = df_gares["indice_lig"].astype(str)
df_couleurs["indice"] = df_couleurs["indice"].astype(str)

# Merge des couleurs
df_gares = df_gares.merge(df_couleurs[["indice", "ColourWeb_hexa"]],
                          left_on="indice_lig", right_on="indice", how="left")
df_gares["ColourWeb_hexa"] = df_gares["ColourWeb_hexa"].fillna("gray")

# Extraction des coordonnées
df_gares[['lat', 'lon']] = df_gares['Geo Point'].str.split(',', expand=True).astype(float)

# === Graphe enrichi ligne-aware ===
G = nx.Graph()

# Fonction Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# === Ajout des nœuds (station, ligne) ===
for _, row in df_gares.iterrows():
    key = (row["nom_long"], row["indice_lig"])
    G.add_node(key, lat=row["lat"], lon=row["lon"], couleur=row["ColourWeb_hexa"])

# === Ajout des arêtes entre stations proches sur la même ligne ===
grouped = df_gares.groupby("indice_lig")
for ligne, group in grouped:
    coords = group.set_index("nom_long")[["lat", "lon"]].to_dict("index")
    stations = list(coords.keys())

    for i in range(len(stations)):
        s1 = stations[i]
        lat1, lon1 = coords[s1]["lat"], coords[s1]["lon"]
        min_dist = float('inf')
        closest_station = None

        for j in range(len(stations)):
            if i == j:
                continue
            s2 = stations[j]
            lat2, lon2 = coords[s2]["lat"], coords[s2]["lon"]
            d = haversine(lat1, lon1, lat2, lon2)
            if d < min_dist and d <= 100:
                min_dist = d
                closest_station = s2

        if closest_station:
            G.add_edge((s1, ligne), (closest_station, ligne), weight=min_dist)

# === Ajout des correspondances (même station, lignes différentes) ===
station_lignes = df_gares.groupby("nom_long")["indice_lig"].unique()
for station, lignes in station_lignes.items():
    for i in range(len(lignes)):
        for j in range(i + 1, len(lignes)):
            G.add_edge((station, lignes[i]), (station, lignes[j]), weight=5)  # pénalité correspondance
# pénalité correspondance

print(f"{len(G.nodes())} nœuds et {len(G.edges())} arêtes dans le graphe enrichi.")
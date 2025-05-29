# 🚆 Analyse du Réseau Ferré en Île-de-France (RER, Métro, Tram, Transilien)

Ce projet modélise le réseau ferré francilien comme un graphe afin d’analyser les connexions entre stations et de calculer des trajets optimaux.
Il s’appuie sur des données open data pour inclure RER, métro, tramways et Transilien.

---

## 📚 Sources des données

Les données utilisées proviennent du site [Île-de-France Mobilités – Open Data](https://data.iledefrance-mobilites.fr/), notamment :

- 📍 **Localisation des gares et stations** : https://data.iledefrance-mobilites.fr/explore/dataset/emplacement-des-gares-idf/information/
- 🎨 **Codes couleurs des lignes** : https://data.iledefrance-mobilites.fr/explore/dataset/traces-du-reseau-ferre-idf/information/

Ces données sont publiées sous licence [Etalab Open Licence 2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence), permettant leur libre réutilisation sous réserve de mention de la source.

---

## 🧩 Modèle et limitations

Le modèle de graphe construit dans ce projet est conçu spécifiquement pour répondre aux besoins des algorithmes d’optimisation de chemin (comme Dijkstra).
Pour cela, certaines simplifications ont été faites, par exemple :
- Les stations multi-lignes sont modélisées avec des sous-nœuds et des arêtes de correspondance,
- Les connexions entre stations sont parfois "forcées" pour assurer la connectivité du graphe,
- Le graphe produit peut donc légèrement différer du plan réel des lignes (ex : distances, itinéraires exacts).

Ce choix méthodologique permet d’obtenir des résultats cohérents en termes d’optimisation de trajets, mais implique que le modèle ne reflète pas toujours fidèlement tous les détails physiques ou géographiques du réseau réel.
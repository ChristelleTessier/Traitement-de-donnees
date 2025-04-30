from classe_joueur import Joueur
import numpy as np
from creer_joueur import creer_joueur
from afficher import afficher_joueur
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

import pandas as pd


def test_classification():

    data_rang = pd.read_csv("Donnees/atp_rankings.csv")
    max_date = data_rang["ranking_date"].max()
    data_temp = data_rang[data_rang["ranking_date"] == max_date]

    data_joueurs = pd.read_csv("Donnees/atp_players.csv")

    joueurs = []
    for joueur_id in data_temp["player"]:
            joueur = creer_joueur(id=joueur_id,info = (data_joueurs,"H"))
            if joueur is not None:
                joueurs.append(joueur)

   # Nettoyage : retirer les joueurs avec des valeurs manquantes
    joueurs_valides = [
        j for j in joueurs
        if not any(pd.isnull([
            j.nb_tournois_gagne,
            j.nb_sem_classe,
            j.prop_vic_set_1_perdu
        ]))
    ]

    X = np.array([
        [j.nb_tournois_gagne, j.nb_sem_classe, j.prop_vic_set_1_perdu]
        for j in joueurs_valides
    ])

    # PCA
    X_pca = PCA(n_components=2).fit_transform(X)


    n_clusters = 4
    # KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)

    # Visualisation
    plt.figure(figsize=(8,6))
    plt.scatter(X_pca[:,0], X_pca[:,1], c=labels, cmap='Set1', s=50)
    plt.title("Clustering des joueurs en 2D")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.grid(True)
    plt.show()

import random
import math

import pandas as pd
import numpy as np

from creer_joueur import creer_joueur

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

def liste_joueur_valide(liste_id_joueur, genre):
    """
    Prépare les données des joueurs en filtrant ceux qui ont des valeurs NaN
    dans les attributs spécifiés.

    Args:
        liste_id_joueur (list): Liste des identifiants des joueurs à considérer.
        genre (str): Le genre des joueurs ('H' pour hommes, 'F' pour femmes).

    Returns:
        list: Une liste d'objets Joueur valides (sans NaN dans les attributs vérifiés).
    """
    if genre == 'H':
        data = pd.read_csv("Donnees/atp_players.csv")
    else:
        data = pd.read_csv("Donnees/wta_players.csv")

    joueurs_valides = []  # Liste pour stocker uniquement les joueurs valides

    attributs_a_verifier = [
        "nb_tournois_gagne",
        "prop_vic_set_1_perdu",
        "prop_balle_break_sauvee",
        "nb_sem_classe"
    ]

    # Création et validation des joueurs
    for id_joueur in liste_id_joueur:
        joueur = creer_joueur(id=id_joueur, info=(data, genre))
        if joueur is not None:
            est_valide = True
            for attribut in attributs_a_verifier:
                try:
                    valeur_attribut = getattr(joueur, attribut)
                    if math.isnan(valeur_attribut):
                        est_valide = False
                        print(
                            f"Attention ! La valeur de '{attribut}' est NaN pour"
                            f" le joueur : {joueur.prenom} {joueur.nom}"
                        )
                        break  # Sortir de la boucle dès qu'un NaN est trouvé
                except AttributeError:
                    est_valide = False
                    print(
                        f"Attention ! L'attribut '{attribut}' n'existe pas pour"
                        f" le joueur : {joueur.prenom} {joueur.nom}"
                    )
                    break

            if est_valide:
                joueurs_valides.append(joueur)

    return joueurs_valides

def transformation_donnees(joueurs):
    X = []
    noms_joueurs = []

    for joueur in joueurs:
        features = [
            # Ratio victoires/tournois
            joueur.nb_tournois_gagne / joueur.nb_tournois_joue if joueur.nb_tournois_joue != 0 else 0,
            # Capacité à remonter après un set perdu
            joueur.prop_vic_set_1_perdu * 100,
            # Résistance sous pression
            joueur.prop_balle_break_sauvee * 100,
            # Proportion de temps dans le top 10
            joueur.nb_sem_1_10 / joueur.nb_sem_classe if joueur.nb_sem_classe != 0 else 0,
            # Proportion de temps dans le top 11-50
            joueur.nb_sem_11_50 / joueur.nb_sem_classe if joueur.nb_sem_classe != 0 else 0,
            # Proportion de temps dans le top 51-100
            joueur.nb_sem_51_100 / joueur.nb_sem_classe if joueur.nb_sem_classe != 0 else 0,
        ]
        X.append(features)
        noms_joueurs.append(f"{joueur.prenom} {joueur.nom}")

    # Convertir en array numpy
    X = np.array(X)

    # 3. Normaliser les données (important pour K-means)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, noms_joueurs, scaler


def preparer_donnees_classification(liste_id_joueur,genre):

    if genre == 'H':
        data = pd.read_csv("Donnees/atp_players.csv")
    else:
        data = pd.read_csv("Donnees/wta_players.csv")

    joueurs = []  # Liste d'objets Joueur

    attributs_a_verifier = [
        "nb_tournois_gagne",
        "prop_vic_set_1_perdu",
        "prop_balle_break_sauvee",
        "nb_sem_classe"
        ]

    # Création des joueurs
    for id in liste_id_joueur:
        joueur = creer_joueur(id = id, info = (data,genre))
        if joueur is not None :
            est_valide = True
            for attribut in attributs_a_verifier:
                valeur_attribut = getattr(joueur, attribut)
                if math.isnan(valeur_attribut):
                    est_valide = False
                    print(
                        f"Attention ! La valeur de '{attribut}' est NaN pour"
                        f"le joueur : {joueur.prenom} {joueur.nom}"
                        )
                    break  # Sortir de la boucle dès qu'un NaN est trouvé

            if est_valide:
                joueurs.append(joueur)

    X = []
    noms_joueurs = []

    for joueur in joueurs:
        features = [
            # Ratio victoires/tournois
            joueur.nb_tournois_gagne / joueur.nb_tournois_joue if joueur.nb_tournois_joue != 0 else 0,
            # Capacité à remonter après un set perdu
            joueur.prop_vic_set_1_perdu * 100,
            # Résistance sous pression
            joueur.prop_balle_break_sauvee * 100,
            # Proportion de temps dans le top 10
            joueur.nb_sem_1_10 / joueur.nb_sem_classe if joueur.nb_sem_classe != 0 else 0,
            # Proportion de temps dans le top 11-50
            joueur.nb_sem_11_50 / joueur.nb_sem_classe if joueur.nb_sem_classe != 0 else 0,
            # Proportion de temps dans le top 51-100
            joueur.nb_sem_51_100 / joueur.nb_sem_classe if joueur.nb_sem_classe != 0 else 0,
        ]
        X.append(features)
        noms_joueurs.append(f"{joueur.prenom} {joueur.nom}")

    # Convertir en array numpy
    X = np.array(X)

    # 3. Normaliser les données (important pour K-means)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, noms_joueurs, scaler

def k_means_visualisation(X):

    # 4. Déterminer le nombre optimal de clusters avec la méthode du coude
    inertias = []
    K_range = range(1, 11)

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)

    # Visualiser la courbe du coude
    plt.figure(figsize=(10, 6))
    plt.plot(K_range, inertias, 'bo-')
    plt.xlabel('Nombre de clusters (k)')
    plt.ylabel('Inertie')
    plt.title('Méthode du coude pour déterminer k optimal')
    plt.grid(True)
    plt.show()

def clustering(X, noms_joueurs, k_optimal, scaler):
    # 5. Appliquer K-means avec le nombre optimal de clusters
    kmeans = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)

    # 6. Visualiser les résultats avec PCA pour réduire à 2 dimensions
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    # Créer un DataFrame pour faciliter la visualisation
    import pandas as pd
    df_result = pd.DataFrame({
        'Joueur': noms_joueurs,
        'Cluster': clusters,
        'PCA1': X_pca[:, 0],
        'PCA2': X_pca[:, 1]
    })

    # Visualiser les clusters
    plt.figure(figsize=(12, 8))
    for cluster in range(k_optimal):
        cluster_data = df_result[df_result['Cluster'] == cluster]
        plt.scatter(
            cluster_data['PCA1'],
            cluster_data['PCA2'],
            label=f'Cluster {cluster}',
            alpha=0.7
        )

        # Ajouter les noms des joueurs les plus connus (optionnel)
        for idx, row in cluster_data.iterrows():
            plt.annotate(row['Joueur'], (row['PCA1'], row['PCA2']), fontsize=8)

    plt.title('Clusters de joueurs de tennis')
    plt.xlabel('Première composante principale')
    plt.ylabel('Deuxième composante principale')
    plt.legend()
    plt.grid(True)
    plt.show()

    # 7. Analyser les caractéristiques de chaque cluster
    centroids = scaler.inverse_transform(kmeans.cluster_centers_)

    # Créer un DataFrame pour les centroïdes
    colonnes = [
        'Ratio victoires',
        'Remontées après set perdu',
        'Balles de break sauvées',
        'Temps top 10',
        'Temps top 11-50',
        'Temps top 51-100'
    ]

    df_centroids = pd.DataFrame(centroids, columns=colonnes)
    df_centroids.index = [f'Cluster {i}' for i in range(k_optimal)]

    print("Caractéristiques moyennes des clusters:")
    print(df_centroids)

    return df_result, kmeans, df_centroids

def classification():

    choix = input("voulez-vous travailler avec les hommes (0) ou les femmes (1)?")

    if choix == 0:
        liste_fichier = [
            "Donnees/atp_matches_1968_2024.csv",
            "Donnees/atp_matches_futures_1992_2024.csv",
            "Donnees/atp_matches_qual_1978_2024.csv"
            ]
        genre = 'H'
    else:
        liste_fichier = [
            "Donnees/wta_matches_1968_2024.csv",
            "Donnees/wta_matches_qual_1968_2024.csv"
            ]
        genre = 'F'

    data = pd.DataFrame()
    for fichier in liste_fichier:
        data_temp = pd.read_csv(fichier, low_memory=False)
        data = pd.concat([data, data_temp], axis=0)

    data = data[data["annee"] == 2024]

    liste_id_win = list(data["winner_id"].unique())
    liste_id_los = list(data["loser_id"].unique())

    liste_id = list(set(liste_id_win + liste_id_los))

    nb_element = int(input(f"saisir le nombre d'individu (max {len(liste_id)}) : "))

    # Assurez-vous que l'ensemble contient au moins nb_element éléments
    if len(liste_id) >= nb_element:
        liste_aleatoires_id = random.sample(liste_id, nb_element)
    else:
        print(
            f"L'ensemble ne contient que {len(liste_id)} éléments."
            f"Impossible d'en sélectionner {nb_element} aléatoirement."
            )
        liste_aleatoires_id = []

    if liste_aleatoires_id != 0:
        X, noms_joueurs, scaler = preparer_donnees_classification(liste_aleatoires_id, genre)
        k_means_visualisation(X)
        k_optimal = int(input("Combien de classe ? "))
        df_result, kmeans, df_centroids = clustering(X, noms_joueurs, k_optimal, scaler)

    else:
        print("la liste est vide on ne peut rien faire")

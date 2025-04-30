import random
import math

import pandas as pd
import numpy as np

from creer_joueur import creer_joueur

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt


def preparer_donnees_classification(liste_id, genre, nb_element_cible):
    """
    Prépare les données pour la classification, en s'assurant d'avoir exactement
    nb_element_cible joueurs valides.
    """
    if genre == 'H':
        data = pd.read_csv("Donnees/atp_players.csv")
    elif genre == 'F':
        data = pd.read_csv("Donnees/wta_players.csv")
    else:
        dataH = pd.read_csv("Donnees/atp_players.csv")
        dataF = pd.read_csv("Donnees/wta_players.csv")
        data = pd.concat([dataH, dataF], axis=0)

    joueurs = []  # Liste d'objets Joueur
    ids_utilisés = set()

    attributs_numeriques_a_verifier = [
        "nb_tournois_gagne",
        "prop_vic_set_1_perdu",
        "prop_balle_break_sauvee",
        "nb_sem_classe"
    ]

    # Continuer à essayer des joueurs jusqu'à en avoir suffisamment
    while len(joueurs) < nb_element_cible:
        # Prendre des IDs qu'on n'a pas encore essayés
        ids_restants = [id for id in liste_id if id not in ids_utilisés]

        if not ids_restants:
            print(f"Plus de joueurs disponibles. Seulement {len(joueurs)} joueurs valides trouvés.")
            break

        # Prendre un lot de joueurs à essayer
        taille_lot = min(50, len(ids_restants), nb_element_cible - len(joueurs))
        lot_ids = random.sample(ids_restants, taille_lot)

        for id in lot_ids:
            ids_utilisés.add(id)
            joueur = creer_joueur(id=id, info=(data, genre))

            if joueur is not None:
                est_valide = True
                for attribut in attributs_numeriques_a_verifier:
                    try:
                        valeur_attribut = getattr(joueur, attribut)
                        if math.isnan(valeur_attribut):
                            est_valide = False
                            break  # Sortir de la boucle dès qu'un NaN est trouvé
                    except AttributeError:
                        est_valide = False
                        break

                if est_valide:
                    joueurs.append(joueur)
                    if len(joueurs) >= nb_element_cible:
                        break

    return joueurs

def prepa_features(joueur, genre):
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
        joueur.nb_sem_51_100 / joueur.nb_sem_classe if joueur.nb_sem_classe != 0 else 0]

    # Encodage one-hot pour la main dominante
    if joueur.main == 'R':
        features.extend([1, 0])  # [est_droitier, est_gaucher]
    elif joueur.main == 'L':
        features.extend([0, 1])
    else:
        features.extend([0, 0])  # Gérer les cas inconnus si nécessaire

    if genre == 'M':
        # Encodage one-hot pour le sexe
        if joueur.sexe == 'H':
            features.extend([1, 0])
        else:
            features.extend([0, 1])


    return features

def standardisation(joueurs, genre):

    X = []
    noms_joueurs = []

    for joueur in joueurs:
        features = prepa_features(joueur, genre)
        X.append(features)
        noms_joueurs.append(f"{joueur.prenom} {joueur.nom}")

    # Convertir en array numpy
    X = np.array(X)

    # Normaliser les données
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, noms_joueurs, scaler, len(joueurs)


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


def visualisation_clustering(k_optimal, df_result):
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


def clustering(X, noms_joueurs, k_optimal, scaler, genre):
    # 5. Appliquer K-means avec le nombre optimal de clusters
    kmeans = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)

    # 6. Visualiser les résultats avec PCA pour réduire à 2 dimensions
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    # Créer un DataFrame pour faciliter la visualisation
    df_result = pd.DataFrame({
        'Joueur': noms_joueurs,
        'Cluster': clusters,
        'PCA1': X_pca[:, 0],
        'PCA2': X_pca[:, 1]
    })

    # Visualiser les clusters
    visualisation_clustering(k_optimal, df_result)

    # 7. Analyser les caractéristiques de chaque cluster
    centroids = scaler.inverse_transform(kmeans.cluster_centers_)

    # Créer un DataFrame pour les centroïdes
    colonnes = [
        'Ratio victoires',
        'Remontées après set perdu',
        'Balles de break sauvées',
        'Temps top 10',
        'Temps top 11-50',
        'Temps top 51-100',
        'Main Droite',
        'Main Gauche'
    ]

    if genre == "M":
        colonnes.extend(["Sexe Homme", "Sexe Femme"])

    df_centroids = pd.DataFrame(centroids, columns=colonnes)
    df_centroids.index = [f'Cluster {i}' for i in range(k_optimal)]

    return df_result, kmeans, df_centroids

def plot_cluster(k_optimal, df_result):
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


def predire_classe_nouveau_joueur(joueur, scaler, kmeans, genre):
    """
    Prédit la classe d'un nouveau joueur en utilisant le modèle K-Means entraîné.

    Args:
        joueur (list): element de classe joueur.
        scaler (StandardScaler): Le scaler utilisé pour normaliser les données d'entraînement.
        kmeans (KMeans): Le modèle K-Means entraîné.

    Returns:
        int: L'étiquette du cluster prédit pour le nouveau joueur.
    """
    joueur_features = prepa_features(joueur, genre)

    # Convertir la liste de features en un array numpy et le redimensionner
    joueur_array = np.array(joueur_features).reshape(1, -1)

    # Normaliser les features du nouveau joueur en utilisant le même scaler
    joueur_scaled = scaler.transform(joueur_array)

    # Prédire le cluster
    classe_predite = kmeans.predict(joueur_scaled)[0]
    return classe_predite

def telechargement(choix):
    if choix == "1":
        liste_fichier = [
            "Donnees/atp_matches_1968_2024.csv",
            "Donnees/atp_matches_futures_1992_2024.csv",
            "Donnees/atp_matches_qual_1978_2024.csv"
            ]
    elif choix == "2":
        liste_fichier = [
            "Donnees/wta_matches_1968_2024.csv",
            "Donnees/wta_matches_qual_1968_2024.csv"
            ]
    else:
        liste_fichier = [
            "Donnees/atp_matches_1968_2024.csv",
            "Donnees/atp_matches_futures_1992_2024.csv",
            "Donnees/atp_matches_qual_1978_2024.csv",
            "Donnees/wta_matches_1968_2024.csv",
            "Donnees/wta_matches_qual_1968_2024.csv"
            ]

    data = pd.DataFrame()
    for fichier in liste_fichier:
        data_temp = pd.read_csv(fichier, low_memory=False)
        data = pd.concat([data, data_temp], axis=0)

    data = data[data["annee"] == 2024]

    return data

def interpretation(df_centroids, df_result, scaler, kmeans, genre, k_optimal):
    from menu import sous_menu_classification
    from fonctions_divers import sortie

    appli_marche = True

    while appli_marche:
        sous_menu_classification()
        choix = input("Entrez votre choix : ")

        if choix == "10":
            appli_marche = sortie()

        elif choix == '1':
            visualisation_clustering(k_optimal, df_result)

        elif choix == "2":
            print("Caractéristiques moyennes des clusters:")

            # Définir les options pour afficher toutes les colonnes et toutes les lignes
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)

            # Afficher le DataFrame
            print(df_centroids)

            # Réinitialiser les options d'affichage à leurs valeurs par défaut (facultatif)
            pd.reset_option('display.max_rows')
            pd.reset_option('display.max_columns')

        elif choix == "3":
            prenom = input("saisir prenom : ")
            nom = input("saisir nom : ")

            joueur = creer_joueur(nom = nom, prenom = prenom)
            if joueur is not None:
                nom_complet = joueur.prenom + ' ' + joueur.nom

                if nom_complet not in df_result["Joueur"].unique():
                    classe = predire_classe_nouveau_joueur(joueur, scaler, kmeans, genre)
                    print(f"\n{nom_complet} serait classé dans le cluster : {classe}")
                else:
                    print(f"{nom_complet} fait partie du jeu de donnée initial")
            else:
                print("Le joueur n'a pas ete trouvé")

        else:
            print("\n Valeur saisie invalide \n")

def classification(genre):

    data = telechargement(genre)

    liste_id_win = list(data["winner_id"].unique())
    liste_id_los = list(data["loser_id"].unique())

    liste_id = list(set(liste_id_win + liste_id_los))

    # Choix k_optimal
    while True:
        nb_element = input(f"saisir le nombre d'individu (max {len(liste_id)}) : ")
        try:
            nb_element_int = int(nb_element)
            if 11 <= nb_element_int <= len(liste_id):
                # Si valeur est un indice de la liste on sort
                break

            else:
                print(
                    "Valeur invalide (valeur attendue entre 11 et "
                    f"{len(liste_id)})"
                    )
        except ValueError:
            print(
                "Erreur : Veuillez entrer indice entre 11 et "
                f"{len(liste_id)} (un nombre entier)."
                )



    # Création de la liste des id des joueurs
    joueurs = preparer_donnees_classification(liste_id, genre, nb_element_int)
    X, noms_joueurs, scaler, nb_joueurs_trouves = standardisation(joueurs, genre)

    if nb_joueurs_trouves > 0:
        print(f"Analyse avec {nb_joueurs_trouves} joueurs")

        # Graphique pour visualisation coude
        k_means_visualisation(X)

        # Choix k_optimal
        while True:
            k_optimal = input("Combien de classe ? ")
            try:
                k_optimal_int = int(k_optimal)
                if 1 <= k_optimal_int <= nb_joueurs_trouves:
                    # Si valeur est un indice de la liste on sort
                    break

                else:
                    print(
                        "Valeur invalide (valeur attendue entre 1 et "
                        f"{nb_joueurs_trouves})"
                        )
            except ValueError:
                print(
                    "Erreur : Veuillez entrer indice entre 1 et "
                    f"{nb_joueurs_trouves} (un nombre entier)."
                    )

        df_result, kmeans, df_centroids = clustering(X, noms_joueurs, k_optimal_int, scaler, genre)
        interpretation(df_centroids, df_result, scaler, kmeans, genre, k_optimal_int)

    else:
        print("Aucun joueur valide trouvé, impossible de continuer")
        fonction_classification()


def fonction_classification():
    from menu import menu_classification
    from fonctions_divers import sortie

    appli_marche = True

    while appli_marche:
        menu_classification()
        choix = input("Entrez votre choix : ")

        if choix == '10':
            appli_marche = sortie()

        elif choix in ["1", "2", "3"]:
            if choix == "1":
                genre = 'H'

            elif choix == "2":
                genre = 'F'

            else:
                genre = 'M'

            classification(genre)

        else:
            print("\n Choix invalide. Veuillez réessayer. \n")

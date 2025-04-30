def preparer_donnees_classification():
    # Charger les données des joueurs
    joueurs = []  # Liste d'objets Joueur que vous aurez créés

    # Préparer les features X et les labels y
    X = []
    y = []

    for joueur in joueurs:
        # Features
        features = [
            joueur.nb_tournois_gagne / max(1, joueur.nb_tournois_joue),  # Ratio de victoires
            joueur.prop_vic_set_1_perdu,
            joueur.prop_balle_break_sauvee,
            # Autres statistiques pertinentes
        ]

        # Labels: déterminer la catégorie de classement
        if joueur.nb_sem_1_10 > 0:
            label = 0  # Élite (a été dans le top 10)
        elif joueur.nb_sem_11_50 > 0:
            label = 1  # Haut niveau (11-50)
        else:
            label = 2  # Autre niveau

        X.append(features)
        y.append(label)

    return np.array(X), np.array(y)

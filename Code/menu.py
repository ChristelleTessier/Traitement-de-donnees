def menu_principal():
    print("\n ########## Menu Principal ########## \n")
    print("Que voulez-vous faire ?")
    print("\n1. Faire de l'étude de données")
    print("2. Faire de la classification")

    print("\n10. Quitter")

def menu_joueur(joueur):
    """
    Affiche le menu principal de l'application.

    En fonction de la présence ou non d'un joueur sélectionné,
    le menu propose différentes options (sélection, affichage d'infos,
    analyses, prédiction, etc.).

    Args:
        joueur (Joueur or None):
            L'objet joueur actuellement sélectionné, ou None si aucun
            n'est sélectionné.
    """
    print("\n ########## Menu JOUEUR ########## \n")
    print("\nQue voulez-vous faire ?")
    if joueur is None:
        print("\n1. Saisir le nom/prenom d'un joueur")
    else:
        print(f"\nJoueur Sélectionné : {joueur.prenom} {joueur.nom}")
        print("1. Choisir un autre joueur ")
        print("2. Les informations du joueur")
        print("3. Les adversaires")
        print("4. Le palmares du joueur par tournois")
        print("5. L'évolution du rangs sur la carrière")

    print("\n10. Revenir au menu principal")

def sous_menu_3(joueur):
    """
    Affiche le sous-menu relatif à l'analyse des adversaires du
    joueur sélectionné.

    Args:
        joueur (Joueur):
            Le joueur sélectionné pour lequel on souhaite consulter
            les adversaires.
    """
    print("\n ########## Menu comparaison ########## \n")

    print(f"Sous menu : Les adversaires de {joueur.prenom} {joueur.nom} ?")

    print("1. Saisir un deuxième joueur")

    print("\n10. Revenir au menu joueur")

def sous_menu_32(joueur1, joueur2):
    """
    Affiche le sous-menu permettant de comparer deux joueurs.

    Ce menu donne accès aux statistiques individuelles,
    aux confrontations directes, et à l'évolution du rang des deux joueurs.

    Args:
        joueur1 (Joueur):
            Premier joueur sélectionné.
        joueur2 (Joueur):
            Deuxième joueur à comparer.
    """
    print("\n ########## Comparaison de deux joueurs ########## \n")
    print(
        f"Sous menu : Comparer {joueur1.prenom} {joueur1.nom} "
        f"et {joueur2.prenom} {joueur2.nom}"
    )
    print("1. Les statistiques des deux joueurs")
    print("2. Les rencontres des deux joueurs")
    print("3. L'évolution des rangs des deux joueurs")

    print("\n10. Revenir au menu joueur")


def sous_menu_4(joueur):
    """
    Affiche le sous-menu relatif au palmarès du joueur.

    Ce menu permet de consulter les résultats généraux et les victoires
    dans les différents tournois.

    Args:
        joueur (Joueur):
            Le joueur sélectionné pour l'affichage du palmarès.
    """
    print("\n ########## Menu PALMARES ########## \n")
    print(f"Sous menu : Le palmares de {joueur.prenom} {joueur.nom} ?")

    print("\n1. Les résultats aux différents tournois (général)")
    print("2. Les victoires aux différents tournois (général)")

    print("\n10. Revenir au menu joueur")

def menu_classification():
    print("\n ########## Menu CLASSIFICATION ########## \n")
    print('Que voulez vous classifier :')
    print("1. Un groupe d'homme")
    print("2. Un groupe de femme")
    print("3. un groupe mixte")

    print("\n10. Revenir au menu principal")

def sous_menu_classification():
    print("\n ########## Travailler sur la classification ########## \n")
    print('Que voulez vous faire ?')
    print("1. Afficher le graphique de classification")
    print("2. Afficher le tableau de répartition")
    print("3. Trouver la classe d'un nouveau joueur")

    print("\n10. Revenir au menu classification")

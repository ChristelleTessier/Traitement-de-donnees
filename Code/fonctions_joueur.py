def adversaire(joueur):
    """
    Affiche les adversaires les plus fréquents d'un joueur et
    permet de comparer avec un autre joueur.

    Cette fonction propose un sous-menu permettant de sélectionner un joueur
    adverse afin de comparer leur parcours, statistiques et confrontations.

    Args:
        joueur (Joueur):
            Instance du joueur principal.
    """

    # Importation
    from afficher import afficher_tournoi
    from menu import sous_menu_3
    from creer_joueur import creer_joueur

    data = joueur.cherche_10_joueur()

    if data is not None and not data.empty:
        afficher_tournoi(data)
    else:
        print("Aucun résultat trouvé.")

    while True:

        sous_menu_3(joueur)
        choix = input("Entrez votre choix : ")

        if choix == "1":
            prenom = input("Entrez le prénom du joueur : ")
            nom = input("Entrez le nom du joueur : ")
            joueur2 = creer_joueur(prenom=prenom, nom=nom)

            if joueur2 is not None:
                comparaison(joueur, joueur2)

        elif choix == "10":
            break

        else:
            print("\n Choix invalide. Veuillez réessayer. \n")


def comparaison(joueur1, joueur2):
    """
    Compare deux joueurs de tennis sur différents aspects (statistiques,
    confrontations, classement).

    Propose un sous-menu pour :
    - Afficher les fiches des deux joueurs.
    - Voir leurs matchs communs.
    - Visualiser leurs classements dans le temps (avec zoom possible).

    Args:
        joueur1 (Joueur):
            Premier joueur à comparer.
        joueur2 (Joueur):
            Deuxième joueur à comparer.
    """

    from afficher import afficher_nuage_point_deux_joueurs, afficher_joueur
    from afficher import afficher_matchs_rencontre
    from zoom import zoom_graph
    from menu import sous_menu_32
    from fonctions_divers import boucle_01

    while True:
        sous_menu_32(joueur1, joueur2)
        choix = input("Entrez votre choix : ")

        if choix == "1":
            afficher_joueur(joueur1)
            afficher_joueur(joueur2)

        elif choix == "2":
            data = joueur1.chercher_match_adversaire(joueur2)
            afficher_matchs_rencontre(data)

        elif choix == "3":
            data = joueur1.comparer_rang(joueur2)
            afficher_nuage_point_deux_joueurs(data, joueur1, joueur2)

            print("Voulez-vous zommer sur une période ?")
            zoomer = boucle_01()
            while zoomer == '1':
                data2 = zoom_graph(data)
                afficher_nuage_point_deux_joueurs(data2, joueur1, joueur2)
                zoomer = boucle_01()

        elif choix == "10":
            break

        else:
            print("\n Choix invalide. Veuillez réessayer. \n")


def palmares(joueur):
    """
    Affiche le palmarès d'un joueur, avec ses tournois joués et gagnés.

    Propose de :
    - Visualiser les tournois joués ou uniquement ceux gagnés.
    - Voir le parcours du joueur dans un tournoi sélectionné.
    - Afficher les matchs associés.

    Args:
        joueur (Joueur):
            Instance du joueur concerné.
    """

    # Importation
    from afficher import afficher_tournoi, afficher_matchs
    from menu import sous_menu_4
    from zoom import chercher_parcours, zoomer_tab_tournoi

    while True:

        choix = input("Entrez votre choix : ")

        if choix == "1" or choix == "2":
            if choix == "2":
                victoire = True

            else:
                victoire = False

            data = zoomer_tab_tournoi(joueur, victoire)

            if data is not None and not data.empty:
                data = data.sort_values(by="tourney_date")
                afficher_tournoi(data)
                data2 = chercher_parcours(joueur, data)
                if data2 is not None:
                    afficher_matchs(data2)
                break
            else:
                print("Aucun résultat trouvé.")

        elif choix == "3":
            print("A faire")

        elif choix == "10":
            break

        else:
            print("Choix invalide. Veuillez réessayer.")

        # Nettoyage écran
        sous_menu_4(joueur)

def fonction_joueur(joueur):
    from creer_joueur import creer_joueur
    from afficher import afficher_joueur, afficher_nuage_point
    from menu import sous_menu_4, menu_joueur
    from zoom import zoom_graph
    from fonctions_divers import sortie, boucle_01

    appli_marche = True
    joueur = None

    while appli_marche:
        menu_joueur(joueur)
        choix = input("Entrez votre choix : ")

        if choix == "10":
            appli_marche = sortie()

        elif choix == "1":
            prenom = input("Entrez le prénom du joueur : ")
            nom = input("Entrez le nom du joueur : ")
            joueur = creer_joueur(prenom=prenom, nom=nom)

            if joueur is None:
                print("❌ Aucun joueur trouvé !")

        elif joueur is None:
            print("❌ Aucun joueur créé. Créez un joueur d'abord !")

        elif choix == "2":
            afficher_joueur(joueur)

        elif choix == "3":
            adversaire(joueur)

        elif choix == "4":
            sous_menu_4(joueur)
            palmares(joueur)

        elif choix == "5":
            data = joueur.chercher_rang()
            if data is not None and not data.empty:
                data = data.sort_values(by="ranking_date")
                afficher_nuage_point(data)

            print("Voulez-vous zommer sur une période ?")
            zoomer = boucle_01()
            while zoomer == '1':
                data = zoom_graph(data)
                afficher_nuage_point(data)
                zoomer = boucle_01()

        else:
            print("\n ❌ Choix invalide. Veuillez réessayer. \n")

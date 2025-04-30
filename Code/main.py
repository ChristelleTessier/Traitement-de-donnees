from creer_joueur import creer_joueur
from test_class import test_classification


def application_tennis():
    """
    Lance l'application de gestion et d'analyse de joueurs de tennis.

    Cette fonction affiche un menu principal permettant à l'utilisateur de :
    - Créer ou sélectionner un joueur.
    - Afficher les informations du joueur.
    - Analyser ses adversaires les plus fréquents et comparer deux joueurs.
    - Consulter son palmarès (tournois joués et gagnés).
    - Visualiser l'évolution de son classement avec possibilité de zoom.
    - Quitter l'application.

    L'application continue de tourner jusqu'à ce que l'utilisateur choisisse de
    la quitter.

    Notes:
        L'utilisateur doit d'abord créer ou sélectionner un joueur pour accéder
        aux autres fonctionnalités.
    """

    # Importation
    from menu import menu_principal, sous_menu_4
    from afficher import afficher_joueur, afficher_nuage_point
    from fonctions_divers import adversaire, palmares, boucle_01
    from zoom import zoom_graph

    print("=== Bienvenue sur l'application Joueur Tennis ===")

    appli_marche = True
    joueur = None

    while appli_marche:
        menu_principal(joueur)

        choix = input("Entrez votre choix : ")

        if choix == "10":
            print("Merci d'avoir utilisé l'application ! À bientôt 👋")
            appli_marche = False

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

        elif choix == "6":
            print("A faire")

        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    #application_tennis()

    test_classification()

from creer_joueur import creer_joueur
from fonctions_classification import classification


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
    from menu import menu_principal, menu_joueur, menu_classification
    from fonctions_joueur import fonction_joueur
    from fonctions_classification import fonction_classification
    from fonctions_divers import sortie

    print("=== Bienvenue sur l'application Joueur Tennis ===")

    appli_marche = True
    joueur = None

    while appli_marche:
        menu_principal()
        choix = input("Entrez votre choix : ")

        if choix == "10":
            print("Merci d'avoir utilisé l'application ! À bientôt 👋")
            appli_marche = sortie()

        elif choix == "1":
            fonction_joueur(joueur)

        elif choix =="2":
            fonction_classification()

        else:
            print("\n ❌ Choix invalide. Veuillez réessayer.\n")


if __name__ == "__main__":
    application_tennis()

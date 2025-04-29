import pandas as pd
import os
import sys



# Récupère le chemin absolu du dossier où se trouve le script streamlit_app.py
current_dir = os.path.dirname(os.path.abspath(__file__))
code_path = os.path.abspath(os.path.join(current_dir, "..", "Code"))

# Ajout au sys.path
if code_path not in sys.path:
    sys.path.insert(0, code_path)  # Priorité plus haute

# Ensuite tu fais tes imports
from creer_joueur import creer_joueur

def application_tennis():
    # Importation
    from menu import menu_principal, sous_menu_3, sous_menu_4
    from afficher import afficher_joueur, afficher_nuage_point
    from fonctions_divers import adversaire, palmares, boucle_01
    from zoom import zoom_graph


    os.system('cls')
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

        elif joueur is None:
            print("❌ Aucun joueur créé. Créez un joueur d'abord !")

        elif choix =="2":
            afficher_joueur(joueur)

        elif choix == "3":
            sous_menu_3(joueur)
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
    application_tennis()

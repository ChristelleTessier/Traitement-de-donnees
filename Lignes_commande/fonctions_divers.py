
import os, sys
import pandas as pd

from menu import sous_menu_3,sous_menu_32
from afficher import afficher_joueur, afficher_matchs_rencontre
from zoom import zoomer_tab_tournoi

# Récupère le chemin absolu du dossier où se trouve le script streamlit_app.py
current_dir = os.path.dirname(os.path.abspath(__file__))
code_path = os.path.abspath(os.path.join(current_dir, "..", "Code"))

# Ajout au sys.path
if code_path not in sys.path:
    sys.path.insert(0, code_path)  # Priorité plus haute

# Ensuite tu fais tes imports
from creer_joueur import creer_joueur


def adversaire(joueur):
    # Importation
    from afficher import afficher_tournoi
    data = joueur.cherche_10_joueur()

    if data is not None and not data.empty:
        afficher_tournoi(data)
    else:
        print("Aucun résultat trouvé.")


    while True:

        sous_menu_3(joueur)
        choix = input("Entrez votre choix : ")

        if choix == "1" :
            prenom = input("Entrez le prénom du joueur : ")
            nom = input("Entrez le nom du joueur : ")
            joueur2 = creer_joueur(prenom=prenom, nom=nom)

            if joueur2 is not None:
                comparaison(joueur, joueur2)

        elif choix == "10":
            break

        else :
            print("Choix invalide. Veuillez réessayer.")


        input("\nAppuie sur Entrée pour voir la suite...")


def comparaison(joueur1,joueur2):
    from afficher import afficher_nuage_point_deux_joueurs
    from zoom import zoom_graph

    while True:
        sous_menu_32(joueur1,joueur2)
        choix = input("Entrez votre choix : ")

        if choix == "1":
            afficher_joueur(joueur1)
            afficher_joueur(joueur2)

        elif choix == "2":
            data = joueur1.chercher_match_adversaire(joueur2)
            afficher_matchs_rencontre(data)

        elif choix == "3":
            data = joueur1.comparer_rang(joueur2)
            print(data)
            afficher_nuage_point_deux_joueurs(data, joueur1, joueur2)

            print("Voulez-vous zommer sur une période ?")
            zoomer = boucle_01()
            while zoomer == '1':
                data2 = zoom_graph(data)
                afficher_nuage_point_deux_joueurs(data2, joueur1, joueur2)
                zoomer = boucle_01()
            input("\nAppuie sur Entrée pour voir la suite...")


        elif choix == "10":
            break

        else :
            print("Choix invalide. Veuillez réessayer.")


def palmares(joueur):
    # Importation
    from afficher import afficher_tournoi, afficher_matchs
    from menu import sous_menu_4
    from zoom import chercher_parcours

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
                data2 = chercher_parcours(joueur,data)
                if data2 is not None:
                    afficher_matchs(data2)
                break
            else:
                print("Aucun résultat trouvé.")

        elif choix == "3":
            print("A faire")

        elif choix == "10":
            break

        else :
            print("Choix invalide. Veuillez réessayer.")

        # Nettoyage écran
        sous_menu_4(joueur)


def boucle_01():
    while True:
        rep = input("0 : non, 1: oui. Votre choix ? ")
        if rep == '0' or rep == '1':
            # Réponse valide
            break
        else:
            print("Valeur saisie invalide (0 ou 1 attendu).")

    return rep

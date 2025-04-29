
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



    while True:

        choix = input("Entrez votre choix : ")

        if choix == "1" :
            data = joueur.cherche_10_joueur()

            if data is not None and not data.empty:

                afficher_tournoi(data)
            else:
                print("Aucun résultat trouvé.")



        elif choix == "2" :
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

        # Nettoyage écran
        os.system('cls')
        sous_menu_3(joueur)

def comparaison(joueur1,joueur2):

    while True:
        sous_menu_32(joueur1,joueur2)
        choix = input("Entrez votre choix : ")

        if choix == "1":
            afficher_joueur(joueur1)
            afficher_joueur(joueur2)

        elif choix == "2":
            data = joueur1.chercher_match_adversaire(joueur2.id_joueur)
            afficher_matchs_rencontre(data)


        elif choix == "10":
            break

        else :
            print("Choix invalide. Veuillez réessayer.")

        # Nettoyage écran
        os.system('cls')
        sous_menu_32(joueur1, joueur2)

def palmares(joueur):
    # Importation
    from afficher import afficher_tournoi, afficher_matchs
    from menu import sous_menu_4
    from zoom import chercher_parcours

    while True:

        choix = input("Entrez votre choix : ")

        if choix == "1" or choix == "2":
            data = zoomer_tab_tournoi(joueur,choix)

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
        os.system('cls')
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

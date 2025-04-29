import os



def menu_principal(joueur):
    print("\nQue voulez-vous faire ?")
    if joueur is None:
        print("1. Saisir le nom/prenom d'un joueur")
    else :
        print(f"\nJoueur Sélectionné : {joueur.prenom} {joueur.nom}")
        print("1. Choisir un autre joueur ")
        print("2. Les informations du joueur")
        print("3. Les adversaires les plus fréquent")
        print("4. Le palmares du joueur par tournois")
        print("5. L'évolution du rangs sur la carrière")
        print("6. Prédire le rang en 2026")

    print("\n10. Quitter")

def sous_menu_3(joueur):
    os.system('cls')
    print(f"Sous menu : Les adversaires de {joueur.prenom} {joueur.nom} ?")

    print("1. Les 10 joueurs les plus fréquent")
    print("2. Comparer deux joueurs")

    print("\n10. Revenir au menu principal")


def sous_menu_32(joueur1,joueur2):
    print(f"Sous menu : Comparer {joueur1.prenom} {joueur1.nom} et {joueur2.prenom} {joueur2.nom}")
    print("1. Les statistiques des deux joueurs")
    print("2. Les rencontres des deux joueurs")
    print("3. L'évolution des rangs des deux joueurs")
    print("\n10. Revenir au menu principal")


def sous_menu_4(joueur):
    os.system('cls')
    print(f"Sous menu : Le palmares de {joueur.prenom} {joueur.nom} ?")

    print("\n1. Les résultats aux différents tournois (général)")
    print("2. Les victoires aux différents tournois (général)")
    print("3. Le résultat à un tournoi précis (annee / nom)")

    print("\n10. Revenir au menu principal")

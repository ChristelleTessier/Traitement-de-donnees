import os
import pandas as pd


def zoom_annee(data):
    from fonctions_divers import boucle_01

    annee_liste = sorted(data['annee'].unique())

    ajout_annee = '1'
    valide = '0'
    annees = []

    while ajout_annee != '0' or valide != '1':

        texte_liste = [f" {k+1} : {date}," for k,date in enumerate(annee_liste)]
        texte = "".join(texte_liste) + ".\nIndiquer l'indice en réponse : "

        # Saisi de l'année
        while True:
            indice_annee_str = input(texte)
            try:
                annee_indice = int(indice_annee_str)
                if 1 <= annee_indice <= len(annee_liste):
                    # Si valeur est un indice de la liste on sort
                    break

                else:
                    print(f"Valeur invalide (valeur attendue entre 1 et {len(annee_liste)})")
            except :
                print(f"Erreur : Veuillez entrer indice entre 1 et {len(annee_liste)} (un nombre entier).")

        # Validation de l'annee
        print(f"Vous souhaitez des informations sur l'annee : {annee_liste[annee_indice - 1]} ?")
        valide = boucle_01()
        if valide == "1":
            annees.append(annee_liste[annee_indice-1])
            annee_liste.pop(annee_indice-1)

        print(annees)
        print("Vous souhaitez ajouter une autre année ?")
        ajout_annee = boucle_01()

        if ajout_annee == '0':
            data_restriction = pd.DataFrame()
            for annee in annees:
                data_temp =data[data['annee'] == annee]
                data_restriction = pd.concat([data_restriction, data_temp], axis=0)
            data = data_restriction.copy()

    return data



def zoom_level(data):
    from fonctions_divers import boucle_01
    # Pourquoi ce n'est pas une liste ?
    level_liste = list(data['tourney_level'].unique())

    ajout_level = '1'
    valide = '0'
    levels = []

    while ajout_level != '0' or valide != '1':

        texte_liste = [f" {k+1} : {level}," for k,level in enumerate(level_liste)]
        texte = "".join(texte_liste) + ".\nIndiquer l'indice en réponse : "

        # Saisi de l'année
        while True:
            indice_level_str = input(texte)
            try:
                indice_level = int(indice_level_str)
                if 1 <= indice_level <= len(level_liste):
                    # Si valeur est un indice de la liste on sort
                    break

                else:
                    print(f"Valeur invalide (valeur attendue entre 1 et {len(level_liste)})")
            except :
                print(f"Erreur : Veuillez entrer indice entre 1 et {len(level_liste)} (un nombre entier).")

        # Validation du level
        print(f"Vous souhaitez des informations sur le tournoi de niveau : {level_liste[indice_level-1]} ?")
        valide = boucle_01()
        if valide == "1":
            print(indice_level,level_liste[indice_level - 1])
            levels.append(level_liste[indice_level - 1])
            level_liste.pop(indice_level - 1)

        print(levels)
        print("Vous souhaitez ajouter une autre level ?")
        ajout_level = boucle_01()
        if ajout_level == '0':
            data_restriction = pd.DataFrame()
            for level in levels:
                data_temp =data[data['tourney_level'] == level]
                data_restriction = pd.concat([data_restriction, data_temp], axis=0)
            data = data_restriction.copy()

    return data


def zoom_surface(data):
    from fonctions_divers import boucle_01

    surface_liste = list(data['surface'].unique())

    ajout_surface = '1'
    valide = '0'
    surfaces = []

    while ajout_surface != '0' or valide != '1':

        texte_liste = [f" {k+1} : {surface}," for k,surface in enumerate(surface_liste)]
        texte = "".join(texte_liste) + ".\nIndiquer l'indice en réponse : "

        # Saisi de l'année
        while True:
            indice_surface_str = input(texte)
            try:
                indice_surface = int(indice_surface_str)
                if 1 <= indice_surface <= len(surface_liste):
                    # Si valeur est un indice de la liste on sort
                    break

                else:
                    print(f"Valeur invalide (valeur attendue entre 1 et {len(surface_liste)})")
            except :
                print(f"Erreur : Veuillez entrer indice entre 1 et {len(surface_liste)} (un nombre entier).")

        # Validation de la surface
        print(f"Vous souhaitez des informations sur le tournoi de niveau : {surface_liste[indice_surface-1]} ?")
        valide = boucle_01()
        if valide == "1":
            surfaces.append(surface_liste[indice_surface - 1])
            surface_liste.pop(indice_surface - 1)

        print(surfaces)
        print("Vous souhaitez ajouter une autre level ?")
        ajout_surface = boucle_01()
        if ajout_surface == '0':
            data_restriction = pd.DataFrame()
            for surface in surfaces:
                data_temp =data[data['surface'] == surface]
                data_restriction = pd.concat([data_restriction, data_temp], axis=0)
            data = data_restriction.copy()

    return data



def zoomer_tab_tournoi(joueur,indice):

    from fonctions_divers import boucle_01

    os.system('cls')
    if indice == "1":
        data = joueur.chercher_resultat()
    else :
        data = joueur.chercher_tournoi_gagne()

    print("Voulez-vous préciser des informations ?")
    choix = boucle_01()

    if choix == '1':

        print("Voulez-vous préciser la/les année(s) ?")
        choix = boucle_01()
        if choix == '1':
            data = zoom_annee(data)


        print("Voulez-vous préciser le(s) niveaux de tournois ?")
        choix = boucle_01()
        if choix == '1':
            data = zoom_level(data)


        print("Voulez-vous préciser les surface ?")
        choix = boucle_01()
        if choix == '1':
            data = zoom_surface(data)

    return data


def chercher_parcours(joueur,data):

    from fonctions_divers import boucle_01
    print("Voulez vous connaitre le parcours du joueur sur un tournoi en particulier ?")
    choix = boucle_01()

    if choix == "1":
        tournoi_id_liste = list(data["tourney_id"].unique())
        while True:
            tournoi_id = input("Saisir l'indentificant du tournois (colonne 1) : ")
            if tournoi_id in tournoi_id_liste:
                break
            else :
                print("L'identificant du tournoi doit apartenir à la liste :")
                print(tournoi_id_liste)

        os.system('cls')
        info_tournoi = data[data["tourney_id"] == tournoi_id ].values[0]
        type = info_tournoi[6]
        print(f"{info_tournoi[2]}, nom : {info_tournoi[3]}, "
                f"surface {info_tournoi[5]}, level {info_tournoi[4]}")
        data2 = joueur.chercher_parcours_tournoi(tournoi_id, type)

    else:
        data2 = None

    return data2

def zoom_graph(data):
    from fonctions_divers import boucle_01
    # S'assurer que 'ranking_date' est bien de type datetime
    data['ranking_date'] = pd.to_datetime(data['ranking_date'])

    # Extraire les années uniques et les trier
    annee_liste = sorted(data['ranking_date'].dt.year.unique())

    annees = []

    while len(annees) != 2 :


        if annees == []:
            print("Année de départ :")
        else :
            print("Année de fin :")

        texte_liste = [f" {k+1} : {date}," for k,date in enumerate(annee_liste)]
        texte = "".join(texte_liste) + ".\nIndiquer l'indice en réponse : "

        # Saisi de l'année
        while True:
            indice_annee_str = input(texte)
            try:
                annee_indice = int(indice_annee_str)
                if 1 <= annee_indice <= len(annee_liste):
                    # Si valeur est un indice de la liste on sort
                    break

                else:
                    print(f"Valeur invalide (valeur attendue entre 1 et {len(annee_liste)})")
            except :
                print(f"Erreur : Veuillez entrer indice entre 1 et {len(annee_liste)} (un nombre entier).")

        # Validation de l'annee
        if annees == []:
            print(f"Vous souhaitez que le graphique commence pour l'annee : {annee_liste[annee_indice - 1]} ?")
        else :
            print(f"Vous souhaitez que le graphique se termine pour l'annee : {annee_liste[annee_indice - 1]} ?")

        valide = boucle_01()
        if valide == "1":
            annees.append(annee_liste[annee_indice-1])
            annee_liste = annee_liste[annee_indice-1:]


        if len(annees) == 2:
            # Créer les bornes avec mois et jour au minimum / maximum
            date_debut = pd.to_datetime(f'{annees[0]}-01-01')
            date_fin = pd.to_datetime(f'{annees[1]}-12-31')

            # Filtrer le DataFrame
            data = data[(data['ranking_date'] >= date_debut) & (data['ranking_date'] <= date_fin)]

    return data

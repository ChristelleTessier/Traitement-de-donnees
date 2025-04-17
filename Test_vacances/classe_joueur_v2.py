import pandas as pd
from datetime import datetime


class Joueur:
    def __init__(self, id_joueur : int, prenom  : str, nom : str, sexe : str, date1 : int, date2 : int):
        self.id_joueur = id_joueur
        self.prenom = prenom
        self.nom = nom
        self.sexe = sexe
        self.pre_match = date1
        self.der_match = date2

    def __str__(self):
        chaine = str(self.nom) + " " + str(self.prenom)
        return chaine

    def chercher_matchs(self,annee =None):
        """ renvois un tableau avec tous les matchs de l'année """

        player_id =self.id_joueur

        # Intialisation au dataFrame
        data_result = pd.DataFrame()

        if self.sexe == 'H':
            liste_fichier = ["Donnees/atp_matches_1968_2024.csv",
                            "Donnees/atp_matches_doubles_2000_2024.csv",
                            "Donnees/atp_matches_futures_1992_2024.csv",
                            "Donnees/atp_matches_qual_1978_2024.csv"
                            ]

        else :
            liste_fichier = ["Donnees/wta_matches_1968_2024.csv",
                            "Donnees/wta_matches_qual_1968_2024.csv"
                            ]

        # Récupération du dernier match joué par tournoi
        liste_round_complet = ['R128', 'R64', 'R32', 'R16', 'QS', 'SF', 'F']

        liste_mapping  = [ [1,'128ème de finale'], [2,'64ème de finale'] ,
                        [3, '32ème de finale'], [4, '16ème de finale'], [5,'Quart de finale'],
                        [6,'Demi-finale'], [7,'Finale'] ]

        # Construire les dictionnaires à partir du mapping
        round_priority = dict(zip(liste_round_complet, [item[0] for item in liste_mapping]))
        round_label = dict(zip(liste_round_complet, [item[1] for item in liste_mapping]))

        # Parcours des fichier de matchs
        for indice,fichier in enumerate(liste_fichier):

            # Récupération du fichier
            data = pd.read_csv(fichier,low_memory=False)

            if annee is not None:
                # Filtre sur les année
                data = data[data['annee'] == annee].copy()

            if 'doubles' in fichier :

                # Selection des variables intérets
                var_interet = ["tourney_date","tourney_name","surface","round",
                                'winner1_id','winner2_id',"loser1_id",'loser2_id']

                data = data[var_interet]

                # selection des ligne ou le joueur à joué
                mask = ((data['winner1_id'] == player_id) |
                        (data['loser1_id'] == player_id) |
                        (data['winner2_id'] == player_id) |
                        (data['loser2_id'] == player_id)
                        )
                data = data[mask]

                # Création d'une variables resultat qui vaut 1 si le match est gagné et 0 sinon
                data['resultat'] = 0
                data.loc[data['winner1_id'] == player_id, 'resultat'] = 1
                data.loc[data['winner2_id'] == player_id, 'resultat'] = 1

                # Suppression "winner_id" et "loser_id"
                data = data.drop(columns=['winner1_id', 'loser1_id','winner2_id', 'loser2_id'])

            else :
                # Selection des variables intérets
                data = data[["tourney_date","tourney_name","surface","round",'winner_id','loser_id']]

                # selection des ligne ou le joueur à joué
                mask = ((data['winner_id'] == player_id) |
                        (data['loser_id'] == player_id)
                        )
                data = data[mask]

                # Création d'une variables resultat qui vaut 1 si le match est gagné et 0 sinon
                data['resultat'] = 0
                data.loc[data['winner_id'] == player_id, 'resultat'] = 1

                # Suppression "winner_id" et "loser_id"
                data = data.drop(columns=['winner_id', 'loser_id'])

            if indice == 0:
                data['type'] = 'simple'
            elif indice ==1 and self.sexe == 'H':
                data['type'] = 'double'
            elif indice == 1:
                data['type'] = 'qualificatif'
            elif indice == 2:
                data['type'] = 'espoir'
            else: # indice = 3
                data['type'] = 'qualificatif'


            # Récupération du dernier match joué du tournoi
            liste_tournoi = data["tourney_name"].unique()
            for tournoi in liste_tournoi:
                data_tournoi = data[data["tourney_name"] == tournoi].copy()

                # Ajouter les colonnes de priorité et de label
                data_tournoi["round_priority"] = data_tournoi["round"].map(round_priority)
                data_tournoi["round_label"] = data_tournoi["round"].map(round_label)

                # Garder uniquement le match le plus avancé par joueur
                match_best = data_tournoi[data_tournoi["round_priority"] == data_tournoi["round_priority"].max()]

                # Néttoyage
                match_best = match_best.drop(columns=["round_priority", "round"])

                # Ajout au tableau des dataframe
                data_result = pd.concat([data_result, match_best], axis=0)

        # Rétirer les nom de colonne commencant par 'Unnamed'
        data_result = data_result.loc[:, ~data.columns.str.startswith('Unnamed')]

        # Réordonner les colonnes
        # Liste des colonnes dans l'ordre souhaité
        colonnes_souhaitees = ['tourney_date', 'tourney_name', 'surface', 'type' , 'resultat', 'round_label']

        # Réorganiser les colonnes (en gardant seulement celles qui existent dans le DataFrame)
        colonnes_presentes = [col for col in colonnes_souhaitees if col in data_result.columns]
        data_result = data_result[colonnes_presentes]

        return data_result

    def chercher_tournois(self,annee = None):
        """ renvois un tableau avec tous tournois gagnés de l'année """

        player_id =self.id_joueur

        # Intialisation au dataFrame
        data_result = pd.DataFrame()

        if self.sexe == 'H':
            liste_fichier = ["Donnees/atp_matches_1968_2024.csv",
                            "Donnees/atp_matches_doubles_2000_2024.csv",
                            "Donnees/atp_matches_futures_1992_2024.csv",
                            "Donnees/atp_matches_qual_1978_2024.csv"
                            ]

        else :
            liste_fichier = ["Donnees/wta_matches_1968_2024.csv",
                            "Donnees/wta_matches_qual_1968_2024.csv"
                            ]

        # Parcours des fichier de matchs
        for indice,fichier in enumerate(liste_fichier):

            # Récupération du fichier
            data = pd.read_csv(fichier,low_memory=False)

            if annee is not None:
                # Filtre sur les année
                data = data[(data['annee'] == annee) & (data['round'] == 'F')].copy()
            else :
                data = data[data['round'] == 'F'].copy()

            if 'doubles' in fichier :

                # Selection des variables intérets
                var_interet = ["tourney_date","tourney_name","surface",
                                'winner1_id','winner2_id']

                data = data[var_interet]

                # selection des ligne ou le joueur à joué
                mask = ((data['winner1_id'] == player_id) |
                        (data['winner2_id'] == player_id)
                        )
                data = data[mask]

                # Suppression "winner_id"
                data = data.drop(columns=['winner1_id','winner2_id'])

            else :
                # Selection des variables intérets
                data = data[["tourney_date","tourney_name","surface",'winner_id']]

                # selection des ligne ou le joueur à joué
                mask = ((data['winner_id'] == player_id))
                data = data[mask]

                # Suppression "winner_id" et "loser_id"
                data = data.drop(columns=['winner_id'])

            if indice == 0:
                data['type'] = 'simple'
            elif indice ==1 and self.sexe == 'H':
                data['type'] = 'double'
            elif indice == 1:
                data['type'] = 'qualificatif'
            elif indice == 2:
                data['type'] = 'espoir'
            else: # indice = 3
                data['type'] = 'qualificatif'

            data_result = pd.concat([data_result, data], axis=0)

        # Rétirer les nom de colonne commencant par 'Unnamed'
        data_result = data_result.loc[:, ~data.columns.str.startswith('Unnamed')]

        # Réordonner les colonnes
        # Liste des colonnes dans l'ordre souhaité
        colonnes_souhaitees = ['tourney_date', 'tourney_name', 'surface', 'type']

        # Réorganiser les colonnes (en gardant seulement celles qui existent dans le DataFrame)
        colonnes_presentes = [col for col in colonnes_souhaitees if col in data_result.columns]
        data_result = data_result[colonnes_presentes]

        return data_result


    def chercher_rang(self):

        if self.sexe == 'H':
            data = pd.read_csv("Donnees/atp_rankings.csv",low_memory=False)
        else :
            data = pd.read_csv("Donnees/wta_rankings.csv",low_memory=False)

        data_rang = data[data["player"] == self.id_joueur]
        data = data_rang[["ranking_date","rank"]]

        return data


def creer_joueur(*,id=None, prenom=None, nom=None):
    """
    Crée un objet Joueur à partir de son ID ou de son prénom et nom.

    L'utilisation de '*' dans la liste des arguments force l'utilisateur à
    spécifier le nom de la variable lors de l'appel de la fonction (keyword-only arguments).

    Args:
        id (str, optional): L'identifiant unique du joueur. Defaults à None.
        prenom (str, optional): Le prénom du joueur. Defaults à None.
        nom (str, optional): Le nom de famille du joueur. Defaults à None.

    Returns:
        Joueur ou None: Un objet Joueur si les informations sont trouvées, sinon None.
    """
    print("debut recherche")
    if id is None and (prenom is None or nom is None):
        return None

    # Chargement des joueurs ATP/WTA
    data_homme = pd.read_csv("Donnees/atp_players_comp.csv",low_memory=False)
    data_femme = pd.read_csv("Donnees/wta_players_comp.csv",low_memory=False)

    ligne_joueur = None
    genre = None


    # Récupération de la bonne ligne
    if id is not None:
        if id in data_homme["player_id"].values:
            ligne_joueur = data_homme[data_homme["player_id"] == id]
            genre = "H"
        elif id in data_femme["player_id"].values:
            ligne_joueur = data_femme[data_femme["player_id"] == id]
            genre = "F"

    elif (prenom is not None) and (nom is not None):
        # Recherche chez les hommes
        ligne_joueur = data_homme[
            (data_homme["name_last"] == nom) & (data_homme["name_first"] == prenom)
        ]
        if not ligne_joueur.empty:
            genre = "H"

        else:
            # Recherche chez les femmes
            ligne_joueur = data_femme[
                (data_femme["name_last"] == nom) & (data_femme["name_first"] == prenom)
            ]
            if not ligne_joueur.empty:
                genre = "F"




    # Création du joueur
    if not ligne_joueur.empty:
        joueur = Joueur(id_joueur = ligne_joueur["player_id"].values[0],
                            prenom = ligne_joueur["name_first"].values[0],
                            nom = ligne_joueur["name_last"].values[0],
                            sexe = genre,
                            date1 = ligne_joueur['first_match_date'].values[0],
                            date2 = ligne_joueur['last_match_date'].values[0])

    else:
        joueur = None

    return joueur


def afficher_tableau(data):
    """Affichage evolutif du dataframe
    """

    map_nom = {
        'tourney_date' : "Date : ",
        'ranking_date' : "Date : ",
        'tourney_name' : ". Tournoi : ",
        'surface' : ", type de surface : ",
        'type' : ", match ",
        'resultat' : [". Défaite en ",". Victoire en "],
        'round_label' : "",
        'rank' : " rang : ",
    }

    noms_colonnes = data.columns

    # Classement par date croissante
    if 'tourney_date' in noms_colonnes:
        nom = 'tourney_date'
        # Transformation dde "tourney_date" ou "ranking_date" au format date
        data[nom] = pd.to_datetime(data[nom])
        data[nom] = data[nom].dt.date
    elif 'ranking_date' in noms_colonnes:
        nom = 'ranking_date'
        # Transformation dde "tourney_date" ou "ranking_date" au format date
        data[nom] = pd.to_datetime(data[nom].astype(str), format="%Y%m%d")
        data[nom] = data[nom].dt.date

    # Rétirer les nom de colonne commencant par 'Unnamed'
    data = data.loc[:, ~data.columns.str.startswith('Unnamed')]

    # Trier dans l'ordre croissant des dates
    data = data.sort_values(nom)

    # Affichage
    for row in data.itertuples(index = False):  # index=False pour ignorer l'index
        text = ''
        for nom in noms_colonnes:
            if isinstance(map_nom[nom],list):
                text += map_nom[nom][int(getattr(row,nom))]
            else:
                text += map_nom[nom] + str(getattr(row,nom))
        print(text)

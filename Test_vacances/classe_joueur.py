import pandas as pd
from datetime import datetime


class Joueur:
    def __init__(self, id_joueur : int, prenom  : str, nom : str, sexe : str):
        self.id_joueur = id_joueur
        self.prenom = prenom
        self.nom = nom
        self.sexe = sexe

    def __str__(self):
        chaine = str(self.nom) + " " + str(self.prenom)
        return chaine

    def chercher_matchs_annee(self,annee):
        """ renvois un tableau avec tous les matchs de l'année """

        player_id =self.id_joueur
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



        for indice,fichier in enumerate(liste_fichier) :

            # Récupération du dernier match joué par tournoi
            liste_round_complet = ['R128', 'R64', 'R32', 'R16', 'QS', 'SF', 'F']

            liste_mapping  = [ [1,'128ème de finale'], [2,'64ème de finale'] ,
                            [3, '32ème de finale'], [4, '16ème de finale'], [5,'Quart de finale'],
                            [6,'Demi-finale'], [7,'Finale'] ]

            # Construire les dictionnaires à partir du mapping
            round_priority = dict(zip(liste_round_complet, [item[0] for item in liste_mapping]))
            round_label = dict(zip(liste_round_complet, [item[1] for item in liste_mapping]))

            # Etape 1 : Selection des données dans le dataFrame

            # Récupération du fichier
            data = pd.read_csv(fichier,low_memory=False, index_col=False)
            if 'doubles' in fichier :

                # Filtre sur les année
                data = data[data['annee'] == annee]

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

                # Type de match : simple ou double
                data["type"] = 'double'

                # Création d'une variables resultat qui vaut 1 si le match est gagné et 0 sinon
                data['resultat'] = 0
                data.loc[data['winner1_id'] == player_id, 'resultat'] = 1
                data.loc[data['winner2_id'] == player_id, 'resultat'] = 1

                # Suppression "winner_id" et "loser_id"
                data = data.drop(columns=['winner1_id', 'loser1_id','winner2_id', 'loser2_id'])

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

            else :

                # Filtre sur les année
                data = data[data['annee'] == annee]

                # Selection des variables intérets
                data = data[["tourney_date","tourney_name","surface","round",'winner_id','loser_id']]

                # selection des ligne ou le joueur à joué
                mask = ((data['winner_id'] == player_id) |
                        (data['loser_id'] == player_id)
                        )
                data = data[mask]

                # Type de match : simple ou double
                data["type"] = 'simple'

                # Création d'une variables resultat qui vaut 1 si le match est gagné et 0 sinon
                data['resultat'] = 0
                data.loc[data['winner_id'] == player_id, 'resultat'] = 1

                # Suppression "winner_id" et "loser_id"
                data = data.drop(columns=['winner_id', 'loser_id'])

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

        return data_result

    def chercher_tournoi_annee(self,annee):
        """ renvois un tableau avec tous les tournoi gagné de l'année """

        player_id =self.id_joueur
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

        for indice,fichier in enumerate(liste_fichier) :

            # Récupération du fichier
            data = pd.read_csv(fichier,low_memory=False, index_col=False)
            if 'doubles' in fichier :

                # Filtre sur les année
                data = data[data['annee'] == annee]
                data = data[data['round'] == 'F']

                # Selection des variables intérets
                var_interet = ["tourney_date","tourney_name","surface","round",
                                'winner1_id','winner2_id']

                data = data[var_interet]
                # selection des ligne ou le joueur à joué
                mask = ((data['winner1_id'] == player_id) |
                        (data['winner2_id'] == player_id)
                        )
                data = data[mask]
                data['resultat'] = 1

                # Type de match : simple ou double
                data["type"] = 'double'


                # Suppression "winner_id" et "loser_id"
                data = data.drop(columns=['winner1_id','winner2_id'])

                # Ajout au tableau des dataframe
                data_result = pd.concat([data_result, data], axis=0)


            else :

                # Filtre sur les année
                data = data[data['annee'] == annee]
                data = data[data['round'] == 'F']

                # Selection des variables intérets
                data = data[["tourney_date","tourney_name","surface","round",'winner_id']]

                # selection des ligne ou le joueur à joué
                mask = ((data['winner_id'] == player_id)
                        )
                data = data[mask]
                data['resultat'] = 1

                # Type de match : simple ou double
                data["type"] = 'simple'

                # Suppression "winner_id"
                data = data.drop(columns=['winner_id'])

                # Ajout au tableau des dataframe
                data_result = pd.concat([data_result, data], axis=0)

        return data_result

    def palmares(self,type):
        """ type = 1 : match
            type = 2 : tournoi gagné
        """

        # Récupération 1er et dernier match
        if self.sexe == 'H':
            data = pd.read_csv("Donnees/atp_players_comp.csv",low_memory=False)
        else :
            data = pd.read_csv("Donnees/wta_players_comp.csv",low_memory=False)

        data_joueur = data[data["player_id"]==self.id_joueur]

        annee_deb = data_joueur["first_match_date"].values[0]
        annee_deb = datetime.strptime(annee_deb, "%Y-%m-%d").year

        annee_fin = data_joueur["last_match_date"].values[0]
        annee_fin = datetime.strptime(annee_fin, "%Y-%m-%d").year

        data = pd.DataFrame()

        if type == 1:
            for annee in range(annee_deb,annee_fin+1,1):
                data_annee = self.chercher_matchs_annee(annee)
                data = pd.concat([data, data_annee], axis=0)
        elif type == 2 :
            for annee in range(annee_deb,annee_fin+1,1):
                data_annee = self.chercher_tournoi_annee(annee)
                data = pd.concat([data, data_annee], axis=0)


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

    elif prenom is not None and nom is not None:
        # Recherche chez les hommes
        ligne_joueur = data_homme[
            (data_homme["name_last"] == nom) & (data_homme["name_first"] == prenom)
        ]
        if not ligne_joueur.empty:
            genre = "H"

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
                            sexe = genre)
    else:
        joueur = None

    return joueur

def afficher_tableau1(data):
    """tourney_date, tourney_level, surface, type, resultat, round_label
    """

    # Transformation dde "tourney_date" au format dataframe
    data['tourney_date'] = pd.to_datetime(data['tourney_date'])
    data['tourney_date'] = data['tourney_date'].dt.date

    # Trier dans l'ordre croissant des dates
    data = data.sort_values('tourney_date')

    # Réindexer proprement
    data = data.reset_index(drop=True)

    # Affichage
    for row in data.itertuples(index = False):  # index=False pour ignorer l'index
        if row.resultat == 1:
            print(f"Date : {row.tourney_date}, Tournoi : {row.tourney_name}"
                f" type de surface : {row.surface} match {row.type}. Victoire en Finale")
        else:
            print(f"Date : {row.tourney_date}, Tournoi : {row.tourney_name}"
                    f" type de surface : {row.surface} match {row.type}. Défaite en {row.round_label}")


joueur = creer_joueur(id = 104925)
#tabjoueur = joueur.chercher_matchs_annee(2023)
#afficher_tableau1(tabjoueur)

data = joueur.palmares(2)
afficher_tableau1(data)

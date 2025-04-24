import pandas as pd
from datetime import datetime

########## A faire ##########
## Modif __init__
# A faire après modif atp_players_comp et modif wta_players_comp
# Ajouter "nb_semaine_..."
# Ajouter "prop_match_gagne_set1_perdu"

## Créer méthode trouver_adversaire_max10
# Qui permet de trouver les 10 joueurs les plus rencontré

## Créer méthode trouver_rencontre_joueur(id_advdersaire)
# Qui permet de trouver les matchs avec un adversaire d'id donné (score, temps, prop balle break sauvé)

## Créer fonction recherche_joueur sans argument
# Récherche progressive


class Joueur:
    def __init__(self, id_joueur : int, prenom  : str, nom : str, sexe : str,
                  date_nais : datetime, main : str, date1 : datetime, date2 : datetime):
        self.id_joueur = id_joueur
        self.prenom = prenom
        self.nom = nom
        self.sexe = sexe
        self.date_nais = date_nais
        self.main = main
        self.pre_match = date1
        self.der_match = date2

    def __str__(self):
        texte = f"Joueur : {self.prenom} {self.nom}\n"
        texte += f"né(e) le : {self.date_nais} \n"
        texte += f"carrière de {self.pre_match} à {self.der_match}"
        return texte

    def chercher_resultat(self,annee = None):
        """ renvois un tableau avec tous les matchs de l'année / ou de la carrière """

        player_id = self.id_joueur

        if self.sexe == 'H':
            liste_fichier = ["../Donnees/atp_matches_1968_2024.csv",
                            "../Donnees/atp_matches_futures_1992_2024.csv",
                            "../Donnees/atp_matches_qual_1978_2024.csv"
                            ]

        else :
            liste_fichier = ["../Donnees/wta_matches_1968_2024.csv",
                            "../Donnees/wta_matches_qual_1968_2024.csv"
                            ]

        # Mapping du niveau de rencontre dans un tournoi
        liste_round_complet = ['R128', 'R64', 'R32', 'R16', 'QF', 'SF', 'F']

        liste_mapping  = [ [1,'128ème de finale'], [2,'64ème de finale'] ,
                        [3, '32ème de finale'], [4, '16ème de finale'], [5,'Quart de finale'],
                        [6,'Demi-finale'], [7,'Finale'] ]

        # Construire les dictionnaires à partir du mapping
        round_priority = dict(zip(liste_round_complet, [item[0] for item in liste_mapping]))
        round_label = dict(zip(liste_round_complet, [item[1] for item in liste_mapping]))

        # Intialisation au dataFrame vide
        data_result = pd.DataFrame()

        # Parcours des fichier de matchs
        for indice,fichier in enumerate(liste_fichier):

            # Récupération du fichier
            data = pd.read_csv(fichier)

            if annee is not None:
                # Filtre sur les année si nécessaire
                data = data[data['annee'] == annee]


            # Selection des variables intérets
            var_interet = ['tourney_id',"tourney_date","tourney_name", 'tourney_level',
                            "surface","round",'winner_id','loser_id']

            data = data[var_interet]

            # Désignation du type de rencontre
            if indice == 0:
                data['type'] = 'simple'
            elif indice ==1 and self.sexe == 'H':
                data['type'] = 'espoir'
            elif indice == 1:
                data['type'] = 'qualificatif'
            else: # indice = 2
                data['type'] = 'qualificatif'

            # selection des ligne ou le joueur à joué
            mask = ((data['winner_id'] == player_id) |
                    (data['loser_id'] == player_id)
                    )
            data = data[mask]

            # Création d'une variables resultat qui vaut 1 si le match est gagné et 0 sinon
            data['resultat'] = 0
            data.loc[data['winner_id'] == player_id, 'resultat'] = 1

            # Suppression des colonnes inutiles
            data = data.drop(columns=['winner_id','loser_id'])

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

        # Réordonner les colonnes
        # Liste des colonnes dans l'ordre souhaité
        colonnes_souhaitees = ['tourney_id','tourney_date', 'tourney_name', 'tourney_level',
                                'surface', 'type' , 'resultat', 'round_label']

        # Réorganiser les colonnes (en gardant seulement celles qui existent dans le DataFrame)
        colonnes_presentes = [col for col in colonnes_souhaitees if col in data_result.columns]
        data_result = data_result[colonnes_presentes]

        return data_result

    def chercher_tournoi_gagne(self,annee = None):
        """ renvois un tableau avec tous tournois gagnés de l'année """

        player_id =self.id_joueur

        # Intialisation au dataFrame
        data_result = pd.DataFrame()

        if self.sexe == 'H':
            liste_fichier = ["Donnees/atp_matches_1968_2024.csv",
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
                # Filtrer les match finaux
                data = data[data['round'] == 'F'].copy()

            # Selection des variables intérets
            var_interet = ["tourney_id","tourney_date","tourney_name","surface","round",
                        'winner_id',"score","minutes"]

            data = data[var_interet]

            # selection des ligne ou le joueur à joué
            mask = ((data['winner_id'] == player_id))
            data = data[mask]

            # Suppression des colonnes inutiles
            data = data.drop(columns=['winner_id'])


        if indice == 0:
            data['type'] = 'simple'
        elif indice ==1 and self.sexe == 'H':
            data['type'] = 'espoir'
        elif indice == 1:
            data['type'] = 'qualificatif'
        else: # indice = 2
            data['type'] = 'qualificatif'

        data_result = pd.concat([data_result, data], axis=0)

        # Rétirer les nom de colonne commencant par 'Unnamed'
        data_result = data_result.loc[:, ~data_result.columns.str.startswith('Unnamed')]

        # Réordonner les colonnes
        # Liste des colonnes dans l'ordre souhaité
        colonnes_souhaitees = ["tourney_id",'tourney_date', 'tourney_name', 'tourney_level',
                                 'surface', 'type' , "score", "minutes"]

        # Réorganiser les colonnes (en gardant seulement celles qui existent dans le DataFrame)
        colonnes_presentes = [col for col in colonnes_souhaitees if col in data_result.columns]
        data_result = data_result[colonnes_presentes]

        return data_result

    def chercher_parcours_tournoi(self,id_tournoi,type):

        sexe = self.sexe

        # Récupération du fichier de données
        if sexe == 'H':
            if type == 'simple':
                data = pd.read_csv("Donnees/atp_matches_1968_2024.csv")
            elif type == "espoir":
                data = pd.read_csv("Donnees/atp_matches_futures_1992_2024.csv")
            else:
                data = pd.read_csv("Donnees/atp_matches_qual_1978_2024.csv")
        else:
            if type == 'simple':
                data = pd.read_csv("Donnees/wta_matches_1968_2024.csv")
            else:
                data = pd.read_csv("Donnees/wta_matches_qual_1968_2024.csv")

        # Récupération de l'ordre des matchs
        liste_round_complet = ['R128', 'R64', 'R32', 'R16', 'QF', 'SF', 'F']

        liste_mapping  = [ [1,'128ème de finale'], [2,'64ème de finale'] ,
                        [3, '32ème de finale'], [4, '16ème de finale'], [5,'Quart de finale'],
                        [6,'Demi-finale'], [7,'Finale'] ]

        # Construire les dictionnaires à partir du mapping
        round_priority = dict(zip(liste_round_complet, [item[0] for item in liste_mapping]))
        round_label = dict(zip(liste_round_complet, [item[1] for item in liste_mapping]))

        data["round_priority"] = data["round"].map(round_priority)
        data["round_label"] = data["round"].map(round_label)

        # Trier par ordre croissant le niveau des matchs
        data = data.sort_values(by='round_priority', ascending=True)

        # Filtre sur le tournois
        data = data[data["tourney_id"] == id_tournoi ]

        data = data[(data["winner_id"] == self.id_joueur) | (data["loser_id"] == self.id_joueur) ]

        var_interet = ["winner_name","loser_name","winner_ioc",'loser_ioc',
                        "winner_rank","loser_rank",'round_label','round_priority',
                        'score','round','minutes',
                        'w_bpSaved','w_bpFaced','l_bpSaved','l_bpFaced']
        data = data[var_interet]


        return data


    







    def chercher_rang(self):

        if self.sexe == 'H':
            data = pd.read_csv("Donnees/atp_rankings.csv",low_memory=False)
        else :
            data = pd.read_csv("Donnees/wta_rankings.csv",low_memory=False)

        data_rang = data[data["player"] == self.id_joueur]
        data = data_rang[["ranking_date","rank"]]

        return data

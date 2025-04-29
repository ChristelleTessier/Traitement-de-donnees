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
                  date_nais : datetime, main : str, nb_tournois_joue : int, nb_tournois_gagne :int,
                  prop_vic_set_1_perdu : float, prop_balle_break_sauvee : float, nb_sem_classe : int,
                  nb_sem_1_10 : int, nb_sem_11_50 : int, nb_sem_51_100 : int,
                  date1 : datetime, date2 : datetime):
        self.id_joueur = id_joueur
        self.prenom = prenom
        self.nom = nom
        self.sexe = sexe
        self.date_nais = date_nais
        self.main = main
        self.nb_tournois_joue = nb_tournois_joue
        self.nb_tournois_gagne = nb_tournois_gagne
        self.prop_vic_set_1_perdu = prop_vic_set_1_perdu
        self.prop_balle_break_sauvee = prop_balle_break_sauvee
        self.nb_sem_classe = nb_sem_classe
        self.nb_sem_1_10 = nb_sem_1_10
        self.nb_sem_11_50 = nb_sem_11_50
        self.nb_sem_51_100 = nb_sem_51_100
        self.pre_match = date1
        self.der_match = date2

    def __str__(self):
        texte = f"Joueur : {self.prenom} {self.nom}\n"
        texte += f"né(e) le : {self.date_nais} \n"
        texte += f"carrière de {self.pre_match} à {self.der_match}"
        return texte

    def chercher_resultat(self,annees = None, levels = None, surfaces = None):

        """ renvois un tableau avec tous les matchs de l'année / ou de la carrière """

        player_id = self.id_joueur

        if self.sexe == 'H':
            liste_fichier = ["Donnees/atp_matches_1968_2024.csv",
                            "Donnees/atp_matches_futures_1992_2024.csv",
                            "Donnees/atp_matches_qual_1978_2024.csv"
                            ]

        else :
            liste_fichier = ["Donnees/wta_matches_1968_2024.csv",
                            "Donnees/wta_matches_qual_1968_2024.csv"
                            ]


        # Intialisation au dataFrame vide
        data_result = pd.DataFrame()

        # Parcours des fichier de matchs
        for indice,fichier in enumerate(liste_fichier):

            # Récupération du fichier
            data = pd.read_csv(fichier,low_memory=False)


            # Restriction du DataFrame si necessaire
            ####################################################
            if annees is not None:
                # Filtre sur les années
                data_restriction = pd.DataFrame()
                for annee in annees:
                    data_temp =data[data['annee'] == annee]
                    data_restriction = pd.concat([data_restriction, data_temp], axis=0)
                data = data_restriction.copy()

            if levels is not None:
                # Filtre sur les level de tournoi
                data_restriction = pd.DataFrame()
                for level in levels:
                    data_temp =data[data['tourney_level'] == level]
                    data_restriction = pd.concat([data_restriction, data_temp], axis=0)
                data = data_restriction.copy()

            if surfaces is not None:
                # Filtre sur les surfaces
                data_restriction = pd.DataFrame()
                for surface in surfaces:
                    data_temp =data[data['surface'] == surface]
                    data_restriction = pd.concat([data_restriction, data_temp], axis=0)
                data = data_restriction.copy()



            # Selection des variables intérets
            ####################################################
            var_interet = ['annee','tourney_id',"tourney_date","tourney_name", 'tourney_level',
                            "surface","round",'winner_id','loser_id']

            data = data[var_interet]

            # Désignation du type de rencontre
            ####################################################
            if indice == 0:
                data['type'] = 'simple'
            elif indice ==1 and self.sexe == 'H':
                data['type'] = 'espoir'
            elif indice == 1:
                data['type'] = 'qualificatif'
            else: # indice = 2
                data['type'] = 'qualificatif'

            # selection des ligne ou le joueur à joué
            ####################################################
            mask = ((data['winner_id'] == player_id) |
                    (data['loser_id'] == player_id)
                    )
            data = data[mask]

            # Création d'une variables resultat qui vaut 1 si le match est gagné et 0 sinon
            ####################################################
            data['resultat'] = 0
            data.loc[data['winner_id'] == player_id, 'resultat'] = 1

            # Suppression des colonnes inutiles
            ####################################################
            data = data.drop(columns=['winner_id','loser_id'])

            # Travail sur les tournois
            ####################################################

            # Parcours des différents tournois
            liste_tournoi = data["tourney_name"].unique()

            for tournoi in liste_tournoi:
                data_tournoi = data[data["tourney_name"] == tournoi].copy()

                rounds = data_tournoi["round"].unique()

                # Type de tournois
                            ####################################################

                # Tournoi au Round Robin
                if 'RR' in rounds:
                    liste_round_complet = ['RR', 'QF', 'SF', 'BR', 'F']
                    liste_mapping  = [ [5,' Tour de Ronde'], [4,'Quart de final'] ,
                        [3, 'Demi finale'], [2, 'Petite finale'], [1,'Finale'] ]

                # Eliminatoire
                else :
                    liste_round_complet = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5','R128', 'R64',
                                            'R32', 'R16', 'QF', 'SF', 'BR', 'F']
                    liste_mapping  = [[13,' 1er tour'], [12,'2ème tour'] ,
                        [11, '3ème tour'], [10, '4ème tour']  , [9, '5ème tour'],
                        [8,'128ème de finale'], [7,'64ème de finale'],
                        [6, '32ème de finale'], [5, '16ème de finale'],
                        [4,'Quart de finale'], [3,'Demi-finale'],[2, 'Petite finale'],
                        [1,'Finale'] ]

                # Construire les dictionnaires à partir du mapping
                ####################################################
                round_priority = dict(zip(liste_round_complet, [item[0] for item in liste_mapping]))
                round_label = dict(zip(liste_round_complet, [item[1] for item in liste_mapping]))

                # Ajouter les colonnes de priorité et de label
                ####################################################
                data_tournoi.loc[:, "round_priority"] = data_tournoi["round"].map(round_priority)
                data_tournoi.loc[:, "round_label"] = data_tournoi["round"].map(round_label)

                # Garder uniquement le match le plus avancé par joueur
                ####################################################
                match_best = data_tournoi[data_tournoi["round_priority"] == data_tournoi["round_priority"].min()]

                # Néttoyage
                ####################################################
                match_best = match_best.drop(columns=["round_priority", "round"])

                # Ajout au tableau des dataframe
                ####################################################
                data_result = pd.concat([data_result, match_best], axis=0)

        # Réordonner les colonnes
        # Liste des colonnes dans l'ordre souhaité
        colonnes_souhaitees = ['annee','tourney_id','tourney_date', 'tourney_name', 'tourney_level',
                                'surface', 'type' , 'resultat', 'round_label']

        # Réorganiser les colonnes (en gardant seulement celles qui existent dans le DataFrame)
        colonnes_presentes = [col for col in colonnes_souhaitees if col in data_result.columns]
        data_result = data_result[colonnes_presentes]

        return data_result


    def chercher_tournoi_gagne(self,annees = None, levels = None, surfaces = None):
        """ renvois un tableau avec tous les matchs de l'année / ou de la carrière """

        player_id = self.id_joueur

        if self.sexe == 'H':
            liste_fichier = ["Donnees/atp_matches_1968_2024.csv",
                            "Donnees/atp_matches_futures_1992_2024.csv",
                            "Donnees/atp_matches_qual_1978_2024.csv"
                            ]

        else :
            liste_fichier = ["Donnees/wta_matches_1968_2024.csv",
                            "Donnees/wta_matches_qual_1968_2024.csv"
                            ]


        # Intialisation au dataFrame vide
        data_result = pd.DataFrame()

        # Parcours des fichier de matchs
        for indice,fichier in enumerate(liste_fichier):

            # Récupération du fichier
            data = pd.read_csv(fichier,low_memory=False)


            # Restriction du DataFrame si necessaire
            ####################################################
            if annees is not None:
                # Filtre sur les années
                data_restriction = pd.DataFrame()
                for annee in annees:
                    data_temp =data[data['annee'] == annee]
                    data_restriction = pd.concat([data_restriction, data_temp], axis=0)
                data = data_restriction.copy()

            if levels is not None:
                # Filtre sur les level de tournoi
                data_restriction = pd.DataFrame()
                for level in levels:
                    data_temp =data[data['tourney_level'] == level]
                    data_restriction = pd.concat([data_restriction, data_temp], axis=0)
                data = data_restriction.copy()

            if surfaces is not None:
                # Filtre sur les surfaces
                data_restriction = pd.DataFrame()
                for surface in surfaces:
                    data_temp =data[data['surface'] == surface]
                    data_restriction = pd.concat([data_restriction, data_temp], axis=0)
                data = data_restriction.copy()

            data = data[(data['round'] == 'F') & (data['winner_id'] == player_id)].copy()


            # Selection des variables intérets
            ####################################################
            var_interet = ['annee','tourney_id',"tourney_date","tourney_name", 'tourney_level',
                            "surface"]

            data = data[var_interet]

            # Désignation du type de rencontre
            ####################################################
            if indice == 0:
                data['type'] = 'simple'
            elif indice ==1 and self.sexe == 'H':
                data['type'] = 'espoir'
            elif indice == 1:
                data['type'] = 'qualificatif'
            else: # indice = 2
                data['type'] = 'qualificatif'

            # Ajout au tableau des dataframe
            ####################################################
            data_result = pd.concat([data_result, data], axis=0)

        # Réordonner les colonnes
        # Liste des colonnes dans l'ordre souhaité
        colonnes_souhaitees = ['annee','tourney_id','tourney_date', 'tourney_name', 'tourney_level',
                                'surface', 'type' ]

        # Réorganiser les colonnes (en gardant seulement celles qui existent dans le DataFrame)
        colonnes_presentes = [col for col in colonnes_souhaitees if col in data_result.columns]
        data_result = data_result[colonnes_presentes]

        return data_result

    def chercher_parcours_tournoi(self, id_tournoi, type):

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

        data = data[data['tourney_id'] == id_tournoi]
        data = data[(data["winner_id"] == self.id_joueur) | (data["loser_id"] == self.id_joueur) ]

        rounds = data["round"].unique()

        # Type de tournois
        ####################################################

        # Tournoi au Round Robin
        if 'RR' in rounds:
            liste_round_complet = ['RR', 'QF', 'SF', 'BR', 'F']
            liste_mapping  = [ [5,' Tour de Ronde'], [4,'Quart de final'] ,
                                  [3, 'Demi finale'], [2, 'Petite finale'], [1,'Finale'] ]

        # Eliminatoire
        else :
            liste_round_complet = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5','R128', 'R64',
                                'R32', 'R16', 'QF', 'SF', 'BR', 'F']
            liste_mapping  = [[13,' 1er tour'], [12,'2ème tour'] ,
                            [11, '3ème tour'], [10, '4ème tour']  , [9, '5ème tour'],
                            [8,'128ème de finale'], [7,'64ème de finale'],
                            [6, '32ème de finale'], [5, '16ème de finale'],
                            [4,'Quart de finale'], [3,'Demi-finale'],[2, 'Petite finale'],
                            [1,'Finale'] ]

        # Construire les dictionnaires à partir du mapping
        ####################################################
        round_priority = dict(zip(liste_round_complet, [item[0] for item in liste_mapping]))
        round_label = dict(zip(liste_round_complet, [item[1] for item in liste_mapping]))

        # Ajouter les colonnes de priorité et de label
        ####################################################
        data.loc[:, "round_priority"] = data["round"].map(round_priority)
        data.loc[:, "round_label"] = data["round"].map(round_label)

        # Trier par ordre croissant le niveau des matchs
        data = data.sort_values(by='round_priority', ascending=False)

        var_interet = ['annee',"winner_name","loser_name","winner_ioc",'loser_ioc',
                        "winner_rank","loser_rank",'round_label','round_priority',
                        'score','round','minutes',
                        'w_bpSaved','w_bpFaced','l_bpSaved','l_bpFaced']
        data = data[var_interet]

        return data

    def cherche_10_joueur(self):

        return None

    def chercher_match_adversaire(self, id_joueur):

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
        for fichier in liste_fichier:

            # Récupération du fichier
            data = pd.read_csv(fichier,low_memory=False)

            data1 = data[((data['winner_id'] == player_id) & (data['loser_id'] == id_joueur))]

            data_result = pd.concat([data_result, data1], axis=0)

            data1 = data[((data['loser_id'] == player_id) & (data['winner_id'] == id_joueur))]

            data_result = pd.concat([data_result, data1], axis=0)


        # Trier par ordre croissant le niveau des matchs
        data_result = data_result.sort_values(by='tourney_date', ascending=True)

        var_interet = ["tourney_date","tourney_name","winner_name","loser_name",'round',
                        'score','minutes','w_bpSaved','w_bpFaced','l_bpSaved','l_bpFaced']
        data_result = data_result[var_interet]


        return data_result


    def chercher_rang(self):

        if self.sexe == 'H':
            data = pd.read_csv("Donnees/atp_rankings.csv",low_memory=False)
        else :
            data = pd.read_csv("Donnees/wta_rankings.csv",low_memory=False)

        data_rang = data[data["player"] == self.id_joueur]
        data = data_rang[["ranking_date","rank"]]

        return data

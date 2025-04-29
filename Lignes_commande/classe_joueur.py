import pandas as pd
from datetime import datetime

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

    def data_match(self):
        if self.sexe == 'H':
            liste_fichier = ["Donnees/atp_matches_1968_2024.csv",
                        "Donnees/atp_matches_futures_1992_2024.csv",
                        "Donnees/atp_matches_qual_1978_2024.csv"
                        ]

        else :
            liste_fichier = ["Donnees/wta_matches_1968_2024.csv",
                        "Donnees/wta_matches_qual_1968_2024.csv"
                        ]

        data_match = pd.DataFrame()
        for fichier in liste_fichier:
            data_temp = pd.read_csv(fichier,low_memory=False )
            data_match = pd.concat([data_match,data_temp], axis = 0)

        return data_match

    def data_players(self):
        if self.sexe == 'H':
            fichier = "Donnees/atp_players.csv"

        else :
            fichier = "Donnees/wta_players.csv"

        data_players = pd.read_csv(fichier,low_memory=False )
        return data_players


    def data_rankings(self):
        if self.sexe == 'H':
            fichier = "Donnees/atp_rankings.csv"

        else :
            fichier = "Donnees/wta_rankings.csv"

        data_rangs = pd.read_csv(fichier,low_memory=False )
        return data_rangs


    def chercher_resultat(self, victoire = False):
        """ renvois un tableau avec tous les matchs de l'année / ou de la carrière """

        player_id = self.id_joueur
        data = self.data_match()

        # Selection des variables intérets
        ####################################################
        var_interet = ['annee','tourney_id',"tourney_date","tourney_name", 'tourney_level',
                        "surface","round",'winner_id','loser_id']

        data = data[var_interet]

        # selection des lignes ou le joueur à joué
        ####################################################

        if victoire :
            data = data[(data["winner_id"] == player_id) & (data["round"] == "F")]

        else:
            data = data[(data["winner_id"] == player_id) | (data["loser_id"] == player_id)]

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

        data_result = pd.DataFrame()

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
                                'surface', 'resultat', 'round_label']

        # Réorganiser les colonnes (en gardant seulement celles qui existent dans le DataFrame)
        colonnes_presentes = [col for col in colonnes_souhaitees if col in data_result.columns]
        data_result = data_result[colonnes_presentes]

        return data_result

    def chercher_parcours_tournoi(self, id_tournoi, type):

        sexe = self.sexe
        data = self.data_match()

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

        id_joueur = self.id_joueur

        data = self.data_match()
        data = data[["winner_id", "loser_id"]]

        data_temp_win = data[data["winner_id"] == id_joueur]
        data_temp_loser = data[data["loser_id"] == id_joueur]


        data_temp_win.rename(columns = {"winner_id" : "joueur", "loser_id" : "adversaire"}, inplace = True)
        data_temp_loser.rename(columns = {"winner_id" : "adversaire", "loser_id" : "joueur"}, inplace = True)

        data = pd.concat([data_temp_win, data_temp_loser])


        par_adversaire = data.groupby("adversaire")['joueur'].count().rename("nb_rencontres")
        par_adversaire = par_adversaire.sort_values(ascending=False)

        par_adversaire = par_adversaire.to_frame()

        player = self.data_players()

        fusion = par_adversaire.merge(
            player,
            left_on = 'adversaire',
            right_on='player_id',
            how='left'
        )

        fusion = fusion[["name_first", "name_last","nb_rencontres"]]
        fusion.rename(columns = {"name_first" : "prénom", "name_last" : "nom"}, inplace = True)

        return fusion.head(10)


    def chercher_match_adversaire(self, joueur):

        player_id_1 =self.id_joueur
        player_id_2 =joueur.id_joueur

        data = self.data_match()

        data1 = data[((data['winner_id'] == player_id_1) & (data['loser_id'] == player_id_2))]
        data2 = data[((data['loser_id'] == player_id_1) & (data['winner_id'] == player_id_2))]

        data_result = pd.concat([data1, data2], axis=0)

        # Trier par ordre croissant le niveau des matchs
        data_result = data_result.sort_values(by='tourney_date', ascending=True)

        var_interet = ["tourney_date","tourney_name" , "winner_name", "loser_name", 'round',
                        'score','minutes','w_bpSaved','w_bpFaced','l_bpSaved','l_bpFaced']
        data_result = data_result[var_interet]

        return data_result


    def chercher_rang(self):

        data = self.data_rankings()

        data = data[data["player"] == self.id_joueur]
        data = data[['ranking_date','rank']]

        return data

    def comparer_rang(self, joueur):
        rang1 = self.chercher_rang()
        rang2 = joueur.chercher_rang()

        fusion = pd.merge(rang1, rang2, on='ranking_date', how='outer', suffixes=('joueur1', 'joueur2'))

        return fusion

import pandas as pd
import os


class MatchSimple:
    def __init__(self, id_match: int, id_tournoi: int,
                 id_vainqueur: int, id_perdant: int, nom_tournoi : str,
                 nom_vainqueur : str, nom_perdant: str,
                 round: str, nb_set: int, score: str, temps: int):
        self.id_match = id_match
        self.id_tournoi = id_tournoi
        self.id_vainqueur = id_vainqueur
        self.id_perdant = id_perdant
        self.nom_tournoi = nom_tournoi
        self.nom_vainqueur = nom_vainqueur
        self.nom_perdant = nom_perdant
        self.round = round
        self.nb_set = nb_set
        self.score = score
        self.temps = temps

    def __str__(self):
        chaine = str(self.round) + " du tournoi " + str(self.nom_tournoi) + ", vainqueur : "
        chaine += str(self.nom_vainqueur) + ", perdant : " + str(self.nom_perdant)
        chaine +=  ", victoire en " + str(self.nb_set) + " sets en " + str(self.temps) + " sets min"
        chaine += ", score final :" + str(self.score)
        return chaine

class MatchDouble:
    def __init__(self, id_match: int, id_tournoi: int,
                 id_vainqueur1: int, id_vainqueur2: int,
                 id_perdant1: int, id_perdant2: int,
                 nom_tournoi : str,
                 nom_vainqueur1 : str, nom_perdant1: str,
                 nom_vainqueur2 : str, nom_perdant2: str,
                 round: str, nb_set: int, score: str, temps: int):
        self.id_match = id_match
        self.id_tournoi = id_tournoi
        self.id_vainqueur1 = id_vainqueur1
        self.id_vainqueur2 = id_vainqueur2
        self.id_perdant1 = id_perdant1
        self.id_perdant2 = id_perdant2
        self.round = round
        self.nb_set = nb_set
        self.score = score
        self.temps = temps

    def __str__(self):
        chaine = str(self.round) + " du tournoi " + str(self.nom_tournoi) + ", vainqueur : "
        chaine += str(self.nom_vainqueur) + ", perdant : " + str(self.nom_perdant)
        chaine +=  ", victoire en " + str(self.nb_set) + "sets en " + str(self.temps) + "min"
        chaine += ", score final :" + str(self.score)
        return chaine


def creer_match(infos):
    """
    Recherche et potentiellement crée des informations sur un match de tennis
    à partir des informations fournies.

    Args:
        infos (list): Une liste contenant les informations du match dans l'ordre suivant:
                      [type (str: 'atp' ou 'wta'): représente le type de tournoi,
                        annee (str) : année lors de laquelle le match a eu lieu,
                        tournoi_id (str) : identifiant du tounoi,
                        nu_match (int) : numéro du match (Attention la nomenclature est
                        différente suivant les matchs)
                    ].

    Returns:
        MatchSimple/MatchDouble ou None: Un objet match si les informations sont trouvées, sinon None.
    """

    type, annee, tournoi_id, nu_match = infos

    indice_type = "simple"

    if type == "atp":
        liste_chemin = ["_matches_","_matches_doubles_","_matches_futures_","_matches_qual_chall_"]
        liste_fichier = os.listdir('donnees_tennis\ATP')
    else :
        liste_chemin = ["_matches_","_matches_qual_itf_"]
        liste_fichier = os.listdir('donnees_tennis\WTA')

    indice = 0

    while indice < len(liste_chemin):

        nom = type + liste_chemin[indice] + annee +".csv"
        print(nom)

        if nom in liste_fichier:
            if type == 'atp':
                nom = "donnees_tennis/ATP/" + nom
            else :
                nom = "donnees_tennis/WTA/" + nom


            data = pd.read_csv(nom, low_memory=False, encoding = "utf-8")

            ligne_match = data[
                    (data["tourney_id"] == tournoi_id) & (data["match_num"] == nu_match)
                    ]

        if ligne_match.empty:
            ligne_match = None

        elif ligne_match is None:
        # Le match n'appartient pas au dataFrame
            indice += 1
        else:
        # Le match appartient au dataFrame
            indice = 5
            if "double" in nom :
                indice_type = "double"



    # Création du joueur
    if ligne_match is not None:
        if indice_type == "simple" :
            match = MatchSimple( id_match = infos,
                                 id_tournoi = ligne_match["tourney_id"].values[0],
                                 id_vainqueur = ligne_match["winner_id"].values[0],
                                 id_perdant = ligne_match["loser_id"].values[0],
                                 nom_tournoi = ligne_match["tourney_name"].values[0],
                                 nom_vainqueur = ligne_match["winner_name"].values[0],
                                 nom_perdant = ligne_match["loser_name"].values[0],
                                 round = ligne_match["round"].values[0],
                                 nb_set = ligne_match["best_of"].values[0],
                                 score = ligne_match["score"].values[0],
                                 temps = ligne_match["minutes"].values[0])
        else :
            match = MatchDouble( id_match = infos,
                                 id_vainqueur1 = ligne_match["winner1_id"].values[0],
                                 id_vainqueur2 = ligne_match["winner2_id"].values[0],
                                 id_perdant1 = ligne_match["loser_id1"].values[0],
                                 id_perdant2 = ligne_match["loser_id2"].values[0],
                                 nom_tournoi = ligne_match["tourney_name"].values[0],
                                 nom_vainqueur1 = ligne_match["winner1_name"].values[0],
                                 nom_perdant1 = ligne_match["loser1_name"].values[0],
                                 nom_vainqueur2 = ligne_match["winner2_name"].values[0],
                                 nom_perdant2 = ligne_match["loser2_name"].values[0],
                                 round = ligne_match["round"].values[0],
                                 nb_set = ligne_match["best_of"].values[0],
                                 score = ligne_match["score"].values[0],
                                 temps = ligne_match["minutes"].values[0])


    else:
        match = None

    return match




rencontre = creer_match(['atp', '2018', '2018-M020', 271])
print(rencontre)

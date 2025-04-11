from datetime import date
import pandas as pd
import os

class Stat:
    def __init__(self, id_match: int, id_joueur: int,
                 nb_ace: int, nb_df: int, nb_point_service: int,
                 nb_premiere_balle: int, nb_point_premiere_balle: int,
                 nb_point_deuxieme_balle: int, nb_balle_break: int,
                 nb_balle_break_sauvee: int):
        self.id_match = id_match
        self.id_joueur = id_joueur
        self.nb_ace = nb_ace
        self.nb_df = nb_df
        self.nb_point_service = nb_point_service
        self.nb_premiere_balle = nb_premiere_balle
        self.nb_point_premiere_balle = nb_point_premiere_balle
        self.nb_point_deuxieme_balle = nb_point_deuxieme_balle
        self.nb_balle_break = nb_balle_break
        self.nb_balle_break_sauvee = nb_balle_break_sauvee

    def __str__(self):
        chaine = "Satistique du joueur " + "Nb ace :" + str(self.nb_ace) + "\nNb double faute : "
        chaine += str(self.nb_df) + "\nNb point service : " + str(self.nb_point_service)
        chaine += "\nNb première balle : " + str(self.nb_premiere_balle)
        chaine += "\nNb point 1er balle : " + str(self.nb_point_premiere_balle)
        chaine += "\nNb point 2eme balle : " + str(self.nb_point_deuxieme_balle)
        chaine += "\nNb balle de break : " +str(self.nb_balle_break)
        chaine += "\nNb balle de break sauvées : " +str(self.nb_balle_break_sauvee)
        return chaine


def creer_stat(id, infos):
    """
    Recherche et potentiellement crée des informations sur un match de tennis
    à partir des informations fournies.

    Args:
        id (int): identificant du joueur,
        infos (list): Une liste contenant les informations du match dans l'ordre suivant:
                      [type (str: 'atp' ou 'wta'): représente le type de tournoi,
                        annee (str) : année lors de laquelle le match a eu lieu,
                        tournoi_id (str) : identifiant du tounoi,
                        nu_match (int) : numéro du match (Attention la nomenclature est
                        différente suivant les matchs)
                    ].

    Returns:
        Stat ou None: Un objet stat si les informations sont trouvées, sinon None.
    """

    type, annee, tournoi_id, nu_match = infos
    ligne_match = None

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

        if ligne_match is None:
        # Le match n'appartient pas au dataFrame
            indice += 1
        else:
        # Le match appartient au dataFrame
            indice = 5
            if "double" in nom :
                indice_type = "double"


    # Création du match
    if ligne_match is not None:

        # Récupération de information winner, loser (winner1, winner2, loser1 ou loser2)
        if indice_type == 'simple':
            if id == ligne_match["winner_id"].values[0]:
                info_res = 'w'
            elif id == ligne_match["loser_id"].values[0]:
                info_res = 'l'
        else:
            if id == ligne_match["winner1_id"].values[0]:
                info_res = 'w1'
            elif id == ligne_match["winner2_id"].values[0]:
                info_res = 'w2'
            elif id == ligne_match["loser1_id"].values[0]:
                info_res = 'l1'
            elif id == ligne_match["loser2_id"].values[0]:
                info_res = 'l2'

        stat = Stat(id_match = infos,
                    id_joueur = id,
                    nb_ace = ligne_match[info_res + '_ace'].values[0],
                    nb_df = ligne_match[info_res + '_df'].values[0],
                    nb_point_service = ligne_match[info_res + '_svpt'].values[0],
                    nb_premiere_balle = ligne_match[info_res + '_1stIn'].values[0],
                    nb_point_premiere_balle = ligne_match[info_res + '_1stWon'].values[0],
                    nb_point_deuxieme_balle = ligne_match[info_res + '_2ndWon'].values[0],
                    nb_balle_break = ligne_match[info_res + '_bpFaced'].values[0],
                    nb_balle_break_sauvee = ligne_match[info_res + '_bpSaved'].values[0])

    else:
        stat = None

    return stat

stat = creer_stat(207669,['atp','2024','2024-M-ITF-ANG-2024-001',101])
print(stat)

from datetime import date
import pandas as pd
import os


class Joueur:
    def __init__(self, id_joueur: int, prenom: str, nom: str, sexe : str,
                 main: str, nationalite: str, date_nais: date, taille: int):
        self.id_joueur = id_joueur
        self.prenom = prenom
        self.nom = nom
        self.main = main
        self.nationalite = nationalite
        self.date_nais = date_nais
        self.taille = taille

class Tournoi:
    def __init__(self, id_tournoi: int, nom: str, level: str, surface: str):
        self.id = id_tournoi
        self.nom = nom
        self.level = level
        self.surface = surface

class MatchSimple:
    def __init__(self, id_match: int, id_tournoi: int,
                 id_vainqueur: int, id_perdant: int,
                 round: str, nb_set: int, score: str, temps: int):
        self.id_match = id_match
        self.id_tournoi = id_tournoi
        self.id_vainqueur = id_vainqueur
        self.id_perdant = id_perdant
        self.round = round
        self.nb_set = nb_set
        self.score = score
        self.temps = temps

class MatchDouble:
    def __init__(self, id_match: int, id_tournoi: int,
                 id_vainqueur1: int, id_vainqueur2: int,
                 id_perdant1: int, id_perdant2: int,
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

class Rang:
    def __init__(self, id_joueur: int, date: date,
                 rang: int, points: int):
        self.id_joueur = id_joueur
        self.date = date
        self.rang = rang
        self.points = points


def creer_match(*,id=None, prenom=None, nom=None):
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
    data_homme = pd.read_csv("Donnees/ATP_players.csv",low_memory=False)
    data_femme = pd.read_csv("Donnees/WTA_players.csv",low_memory=False)

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
    if ligne_joueur.empty:
        joueur = Joueur(id_joueur = ligne_joueur["player_id"].values[0],
                            prenom = ligne_joueur["name_first"].values[0],
                            nom = ligne_joueur["name_last"].values[0],
                            sexe = genre,
                            main = ligne_joueur["hand"].values[0],
                            nationalite = ligne_joueur["ioc"].values[0],
                            date_nais = 0,
                            taille = ligne_joueur["height"].values[0])
    else:
        joueur = None

    return joueur


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
        liste_chemin = ["_matches_","_matches_doubles_","_matches_futures","_matches_qual_chall"]
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

            data = pd.read_csv(nom, low_memory=False)

            ligne_match = data[
                    (data["tourney_id"] == tournoi_id) & (data["match_num"] == nu_match)
                ]

        if not nom.startswith("donnees"):
        # Le fichier n'appartient pas à la liste
            indice += 1
        elif ligne_match.empty:
        # Le match n'appartient pas au dataFrame
            indice += 1
        else:
        # Le match appartient au dataFrame
            indice = 5
            if "double" in nom :
                indice_type = "double"



    # Création du joueur
    if ligne_match.empty:
        if indice_type == "simple" :
            match = MatchSimple( id_match = infos,
                                 id_vainqueur = ligne_match["winner_id"].values[0],
                                 id_perdant = ligne_match["loser_id"].values[0],
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
                                 round = ligne_match["round"].values[0],
                                 nb_set = ligne_match["best_of"].values[0],
                                 score = ligne_match["score"].values[0],
                                 temps = ligne_match["minutes"].values[0])


    else:
        match = None

    return match


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

    indice_type = "simple"

    if type == "atp":
        liste_chemin = ["_matches_","_matches_doubles_","_matches_futures","_matches_qual_chall"]
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

            data = pd.read_csv(nom, low_memory=False)

            ligne_match = data[
                    (data["tourney_id"] == tournoi_id) & (data["match_num"] == nu_match)
                ]

        if not nom.startswith("donnees"):
        # Le fichier n'appartient pas à la liste
            indice += 1
        elif ligne_match.empty:
        # Le match n'appartient pas au dataFrame
            indice += 1
        else:
        # Le match appartient au dataFrame
            indice = 5
            if "double" in nom :
                indice_type = "double"

    # Récupération de information winner, loser (winner1, winner2, loser1 ou loser2)
    if indice_type == 'simple':
        if id == ligne_match["winner_id"].values[0]:
            info_res = 'winner'
        elif id == ligne_match["loser_id"].values[0]:
            info_res = 'loser'
    elif indice_type == 'double':
        if id == ligne_match["winner1_id"].values[0]:
            info_res = 'winner1'
        elif id == ligne_match["winner2_id"].values[0]:
            info_res = 'winner2'
        elif id == ligne_match["loser1_id"].values[0]:
            info_res = 'loser1'
        elif id == ligne_match["loser2_id"].values[0]:
            info_res = 'loser2'


    # Création du joueur
    if ligne_match.empty:
        stat = Stat(id_match = infos,
                    id_joueur = id,
                    nb_ace = ligne_match[info_res + '_res'].values[0],
                    nb_df = ligne_match[info_res + '_df'].values[0],
                    nb_point_service = ligne_match[info_res + '_svpt'].values[0],
                    nb_premiere_balle = ligne_match[info_res + '_1stIn'].values[0],
                    nb_point_premiere_balle = ligne_match[info_res + '_1stWon'].values[0],
                    nb_point_deuxieme_balle = ligne_match[info_res + '_2stWon'].values[0],
                    nb_balle_break = ligne_match[info_res + '_bpFaced'].values[0],
                    nb_balle_break_sauvee = ligne_match[info_res + '_bpSaved'].values[0])

    else:
        stat = None

    return stat

creer_match(['atp','2024','2024-0339',300])

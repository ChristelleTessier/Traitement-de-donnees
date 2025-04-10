from datetime import date
import pandas as pd


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
    def __init__(self, id: int, nom: str, level: str, surface: str):
        self.id = id
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


def creer_joueur(id=None, prenom=None, nom=None):
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
        match_homme = data_homme[
            (data_homme["name_last"] == nom) & (data_homme["name_first"] == prenom)
        ]
        if not match_homme.empty:
            ligne_joueur = match_homme
            genre = "H"

        # Recherche chez les femmes
        match_femme = data_femme[
            (data_femme["name_last"] == nom) & (data_femme["name_first"] == prenom)
        ]
        if not match_femme.empty:
            ligne_joueur = match_femme
            genre = "F"

    # Création du joueur
    if ligne_joueur is not None:
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

from datetime import date
import pandas as pd

def creer_joueur(id_joueur = None, prenom = None, nom = None):
    if id_joueur is None and (prenom is None or nom is None) :
        return None
    # Chargement des joueur ATP
    data_homme = pd.read_csv("Donnees\ATP_players.csv")
    # Chargement des joueur ATP
    data_femme = pd.read_csv("Donnees\WTA_players.csv")

    if id_joueur is not None:
        if id_joueur in data_homme["player_id"]:
            joueur = Joueur(id_joueur,
            data_homme(data_homme["player_id"]==id_joueur)["name_first"],
            data_homme(data_homme["player_id"]==id_joueur)["name_last"],
            data_homme(data_homme["player_id"]==id_joueur)["hand"],
            data_homme(data_homme["player_id"]==id_joueur)["ioc"],
            "test",
            data_homme(data_homme["player_id"]==id_joueur)["height"])
            return joueur







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

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

    def __str__(self):
        chaine = str(self.nom) + " " + str(self.prenom) + ", date naiss :" + str(self.date_nais)
        chaine += ", nationalité : " + str(self.nationalite) + ", taille : " + str(self.taille) + "cm"
        return chaine

class Tournoi:
    def __init__(self, id_tournoi: int, genre: str, nom: str, level: str, surface: str):
        self.id = id_tournoi
        self.nom = nom
        self.level = level
        self.surface = surface
        self.genre = genre

    def __str__(self):
        chaine = str(self.genre) + " Tournoi : " + str(self.nom) + " Level : "
        chaine += str(self.level) + ", Surface : " + str(self.surface)
        return chaine

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

        def __str__(self):
            chaine = str(self.round) + " du tournoi"
            return chaine

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

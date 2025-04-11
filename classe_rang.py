from datetime import date
import pandas as pd
import os

class Rang:
    def __init__(self, id_joueur: int, date: date,
                 rang: int, points: int):
        self.id_joueur = id_joueur
        self.date = date
        self.rang = rang
        self.points = points

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

def creer_joueur(*,id=None, prenom=None, nom=None):
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
    if not ligne_joueur.empty:
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


joueur = creer_joueur(id = 100001)
print(joueur)

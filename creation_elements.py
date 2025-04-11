import pandas as pd
import os

from structure_classe import Joueur, MatchSimple, MatchDouble, Stat, Tournoi


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

        if nom in liste_fichier:
            if type == 'atp':
                nom = "donnees_tennis/ATP/" + nom
            else :
                nom = "donnees_tennis/WTA/" + nom

            data = pd.read_csv(nom, low_memory=False)

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

            data = pd.read_csv(nom, low_memory=False)

            ligne_match = data[
                    (data["tourney_id"] == tournoi_id) & (data["match_num"] == nu_match)
                ]

            if ligne_match.empty:
                ligne_match = None

        if ligne_match is None:
        # Le fichier n'appartient pas à la liste
            indice += 1
        else:
        # Le match appartient au dataFrame
            indice = 5
            if "double" in nom :
                indice_type = "double"


    # Création du joueur
    if ligne_match is not None:

        # Récupération de information winner, loser (winner1, winner2, loser1 ou loser2)
        if indice_type == 'simple':
            if id == ligne_match["winner_id"].values[0]:
                info_res = 'winner'
            elif id == ligne_match["loser_id"].values[0]:
                info_res = 'loser'
        else:
            if id == ligne_match["winner1_id"].values[0]:
                info_res = 'winner1'
            elif id == ligne_match["winner2_id"].values[0]:
                info_res = 'winner2'
            elif id == ligne_match["loser1_id"].values[0]:
                info_res = 'loser1'
            elif id == ligne_match["loser2_id"].values[0]:
                info_res = 'loser2'

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

def creer_tournoi(id):
    """
    Recherche et potentiellement crée des informations sur un tournoi de tennis
    à partir des informations fournies.

    Args:
        id (str): identificant du tournoi

    Returns:
        Tournoi ou None: Un objet Tournoi si les informations sont trouvées, sinon None.
    """

    annee = id[0:4]

    indice = 0

    ligne_tournoi = None

    # \\ pour atp sinon interprète \a
    liste_chemin = ["atp_matches_" + annee + ".csv",
                    "atp_matches_doubles_" + annee + ".csv",
                    "atp_matches_futures_" + annee + ".csv",
                    "atp_matches_qual_chall_" + annee + ".csv",
                    "wta_matches_" + annee + ".csv",
                    "wta_matches_qual_itf_" + annee + ".csv"]

    liste_fichier = os.listdir('donnees_tennis\ATP')
    liste_fichier.append(os.listdir('donnees_tennis\WTA'))

    while indice < len(liste_chemin) :

        chemin = liste_chemin[indice]

        if chemin in liste_fichier:

            if "atp" in chemin:
                chemin = "donnees_tennis\ATP\\" + chemin
            else:
                chemin = "donnees_tennis\WTA\\" + chemin

            data = pd.read_csv(chemin, low_memory=False)

            ligne_tournoi = data[(data["tourney_id"] == id)]

            if ligne_tournoi.empty:
                ligne_tournoi = None
            else:
                ligne_tournoi = ligne_tournoi.head(1)

        if ligne_tournoi is None:
        # Le match n'appartient pas au dataFrame
            indice += 1
        else:
        # Le match appartient au dataFrame
            indice = 10

    if "atp" in chemin :
        indice_genre = "atp"
    else:
        indice_genre = "wta"

    # Création du tournoi
    if ligne_tournoi is not None:
        tournoi = Tournoi(id_tournoi = id,
                    genre = indice_genre,
                    nom = ligne_tournoi['tourney_name'].values[0],
                    level = ligne_tournoi['tourney_level'].values[0],
                    surface = ligne_tournoi['surface'].values[0])
    else:
        tournoi = None

    return tournoi

tournoi = creer_tournoi("2023-M-ITF-ARG-01A-2023")
print(tournoi)

joueur = creer_joueur(id = 100001)
print(joueur)

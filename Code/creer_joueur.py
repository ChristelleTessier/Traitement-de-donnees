import pandas as pd
from datetime import datetime
from classe_joueur import Joueur


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
    data_homme = pd.read_csv("Donnees/atp_players.csv",low_memory=False)
    data_femme = pd.read_csv("Donnees/wta_players.csv",low_memory=False)

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

    elif (prenom is not None) and (nom is not None):
        # Recherche chez les hommes
        ligne_joueur = data_homme[
            (data_homme["name_last"] == nom) & (data_homme["name_first"] == prenom)
        ]
        if not ligne_joueur.empty:
            genre = "H"

        else:
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
                            date_nais = ligne_joueur['dob'].values[0],
                            main = ligne_joueur['hand'].values[0],
                            nb_tournois_joue = ligne_joueur['nb_tournois_joue'].value[0],
                            nb_tournois_gagne = ligne_joueur['nb_tournois_gagne'].values[0],
                            prop_vic_set_1_perdu = ligne_joueur["prop_vic_set_1_perdu"].values[0],
                            prop_balle_break_sauvee = ligne_joueur["prop_balle_break_sauvee"].values[0],
                            nb_sem_classe = ligne_joueur["nb_sem_classe"].values[0],
                            nb_sem_1_10 = ligne_joueur["nb_sem_1_10"].values[0],
                            nb_sem_11_50 = ligne_joueur["nb_sem_11_50"].values[0],
                            nb_sem_51_100 = ligne_joueur["nb_sem_51_100"].values[0],
                            date1 = ligne_joueur['first_match_date'].values[0],
                            date2 = ligne_joueur['last_match_date'].values[0])

    else:
        joueur = None

    return joueur

from datetime import date
import pandas as pd
import os


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

import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def afficher_joueur(joueur):
    """
    Affiche les informations détaillées d'un joueur.

    Paramètres :
        joueur (Joueur or None) :
            Objet représentant un joueur ou None si non trouvé.
    """
    if joueur is None:
        print("❌ Joueur non trouvé.")
    else:
        print("\n✅ Joueur trouvé :")
        print(f"Nom : {joueur.prenom} {joueur.nom}")
        print(f"Sexe : {joueur.sexe}")
        print(f"Date de naissance : {joueur.date_nais}")
        print(f"Main : {joueur.main}")
        print(f"Nombre de tournois joués : {joueur.nb_tournois_joue}")
        print(f"Nombre de tournois gagnés : {joueur.nb_tournois_gagne}")
        print(
            f"Proportion victoires après set 1 perdu : "
            f"{round(joueur.prop_vic_set_1_perdu,2)} %"
            )
        print(
            f"Proportion balles de break sauvées :"
            f"{round(joueur.prop_balle_break_sauvee,2)} %"
            )
        print(f"Nombre de semaines classé : {joueur.nb_sem_classe}")
        print(f"Nombre de semaines 1-10 : {joueur.nb_sem_1_10}")
        print(f"Nombre de semaines 11-50 : {joueur.nb_sem_11_50}")
        print(f"Nombre de semaines 51-100 : {joueur.nb_sem_51_100}")
        print(f"Premier match : {joueur.pre_match}")
        print(f"Dernier match : {joueur.der_match}")

    input("\nAppuie sur Entrée pour continuer")


def afficher_tournoi(data, lignes_par_page=25):
    """
    Affiche les données d'un tournoi en les paginant.

    Paramètres :
        data (DataFrame) :
            Données des tournois à afficher.
        lignes_par_page (int) :
            Nombre de lignes à afficher par page (défaut : 25).
    """
    n = len(data)
    for i in range(0, n, lignes_par_page):
        print(data.iloc[i:i+lignes_par_page].to_string(index=False))
        if i + lignes_par_page < n:
            input("\nAppuie sur Entrée pour voir la suite...")


def afficher_matchs(data):
    """
    Affiche un résumé des matchs : round, gagnant, perdant et score.

    Paramètres :
        data (DataFrame) :
            Données contenant les informations des matchs.
    """
    for index, row in data.iterrows():
        print(
            f"{row['round_label']} : Victoire de {row['winner_name']} "
            f"contre {row['loser_name']}, score de {row['score']}"
            )


def afficher_matchs_rencontre(data, lignes_par_page=25):
    """
    Affiche les détails des matchs entre deux joueurs avec pagination.

    Paramètres :
        data (DataFrame) :
            Données des matchs entre deux joueurs.
        lignes_par_page (int) :
            Nombre de lignes à afficher par page (défaut : 25).
    """
    n = len(data)

    for i in range(0, n, lignes_par_page):
        page = data.iloc[i:i + lignes_par_page]
        for index, row in page.iterrows():
            print(
                f"📅 {row['tourney_date']} - 🎾 Tournoi de "
                f"{row['tourney_name']}, 🌀 Round : {row['round']}\n"
                f"🏆 Victoire de {row['winner_name']} contre "
                f"{row['loser_name']}, 📊 Score : {row['score']}\n"
            )
        if i + lignes_par_page < n:
            input("Appuie sur Entrée pour voir la suite...")
            os.system('cls' if os.name == 'nt' else 'clear')


def afficher_nuage_point(data):
    """
    Affiche un nuage de points représentant les classements des joueurs
     selon la date.

    Paramètres :
        data (DataFrame) :
            Données de classement avec colonnes 'ranking_date' et 'rank'.
    """
    # Conversion de la colonne 'ranking_date' en datetime
    data['ranking_date'] = pd.to_datetime(data['ranking_date'])

    plt.figure(figsize=(10, 6))  # pour un affichage plus propre

    # Définir les tranches de rangs et leurs couleurs
    conditions = [
        (data["rank"] >= 1) & (data["rank"] <= 10),
        (data["rank"] >= 11) & (data["rank"] <= 50),
        (data["rank"] >= 51) & (data["rank"] <= 100),
        (data["rank"] > 100)
    ]
    couleurs = ['black', 'green', 'blue', 'orange']
    labels = ['Top 10', '11-50', '51-100', 'Au-delà de 100']

    # Tracer chaque groupe avec sa couleur
    for condition, couleur, label in zip(conditions, couleurs, labels):
        subset = data[condition]
        plt.scatter(
            subset['ranking_date'],
            subset['rank'],
            color=couleur,
            label=label,
            s=10)

    plt.title("Nuage de points : Classement par Date")
    plt.xlabel("Année")
    plt.ylabel("Classement")

    # Inverser l'axe Y (meilleur rang en haut)
    plt.gca().invert_yaxis()

    # Formater l'axe X pour n'afficher que l'année
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # %Y = année
    ax.xaxis.set_major_locator(mdates.YearLocator())  # 1 graduation par an

    plt.gcf().autofmt_xdate()  # ajuste la rotation des labels

    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def afficher_nuage_point_deux_joueurs(data, joueur1, joueur2):
    """
    Compare graphiquement les classements de deux joueurs au fil du temps.

    Paramètres :
        data (DataFrame) :
            Données contenant les colonnes 'ranking_date',
            'rankjoueur1' et 'rankjoueur2'.
        joueur1 (Joueur) :
            Premier joueur à comparer.
        joueur2 (Joueur) :
            Deuxième joueur à comparer.
    """
    # S'assurer que la colonne 'ranking_date' est bien au format datetime
    data['ranking_date'] = pd.to_datetime(data['ranking_date'])

    # Créer le graphique
    plt.figure(figsize=(12, 6))

    # Tracer les deux courbes
    plt.plot(
        data['ranking_date'],
        data['rankjoueur1'],
        label=joueur1.nom,
        color='blue',
        marker='o',
        linewidth=1
    )
    plt.plot(
        data['ranking_date'],
        data['rankjoueur2'],
        label=joueur2.nom,
        color='red',
        marker='o',
        linewidth=1
    )

    # Titre et axes
    plt.title(f"Comparaison des Classements : {joueur1.nom} vs {joueur2.nom}")
    plt.xlabel("Date")
    plt.ylabel("Classement")
    plt.gca().invert_yaxis()  # meilleur classement en haut
    plt.grid(True)

    # Formater les dates
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    plt.gcf().autofmt_xdate()

    plt.legend()
    plt.tight_layout()
    plt.show()

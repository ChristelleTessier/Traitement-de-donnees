import streamlit as st
import pandas as pd
import altair as alt
import os
import sys
import math

# Utiliser le répertoire courant pour Streamlit
base_path = os.getcwd()
code_path = os.path.join(base_path, "Code")

# Ajouter au sys.path
if code_path not in sys.path:
    sys.path.append(code_path)

# Maintenant importer
from classe_joueur import Joueur
from creer_joueur import creer_joueur

def afficher_match(match,type):

    # Remplacer les valeurs manquantes par des ?
    match = match.fillna('?')

    if type == 'double':
        texte = f"{match['round_label']} {match['winner1_name']} "
        texte += f"({match['winner1_ioc']}"
        if match['winner1_rank'] != '?':
            texte += f", rg : {str(int(match['winner1_rank']))}"
        texte += f") et {match['winner2_name']} ({match['winner2_ioc']}"
        if match['winner2_rank'] != '?':
            texte += f", rg : {str(int(match['winner2_rank']))}"
        texte += f") contre {match['loser1_name']} ({match['loser1_ioc']}"
        if match['loser1_rank'] != "?":
            texte += f", rg : {str(int(match['loser1_rank']))}"
        texte += f") et {match['loser2_name']} ({match['loser2_ioc']}"
        if match['loser2_rank'] != '?':
                texte += f", rg : {str(int(match['loser2_rank']))}"
        texte += ").\n"

    elif type == 'qualificatif':
        texte = f"{match['round_label']} {match['winner_name']} "
        texte += f"({match['winner_ioc']}) "
        texte += f"contre {match['loser_name']} ({match['loser_ioc']}).\n"

    else :
        texte = f"{match['round_label']} {match['winner_name']} "
        texte += f"({match['winner_ioc']}"
        if match['winner_rank'] != '?':
            texte += f", rg : {str(int(match['winner_rank']))}"
        texte += f") contre {match['loser_name']} "
        texte += f"({match['loser_ioc']}"
        if match['loser_rank'] != '?':
            texte += f", rg : {str(int(match['loser_rank']))}"
        texte += ").\n"

    texte2 = f"Score final : {match['score']}"
    if match['minutes'] != '?':
        texte2 += f" en : {str(match['minutes'] // 60)}h et {str(match['minutes'] % 60)} min"
    texte2 += ".\n"
    if match['w_bpSaved'] != '?':
        texte2 += f"{str(int(match['w_bpSaved']))} balle(s) de break sauvée(s) sur "
        texte2 += f"{str(int(match['w_bpFaced']))}"

    return texte,texte2


def palmares():
    st.title("Palmares d'un joueur")

    # Création des onglets de choix
    tab1, tab2 ,tab3, tab4 = st.tabs(["Choix du joueur","Participation à un match",
                                       "Palamares de victoire","Evolution du rang"])

    with tab1:
        joueur = None
        nom_j = st.text_input("Entrez le nom du joueur (ex Nadal)")
        prenom_j = st.text_input("Entrez le prénom du joueur (ex Rafael)")

        # Vérification des entrées
        nom_valide = nom_j and nom_j.isalpha()
        prenom_valide = prenom_j and prenom_j.isalpha()

        if nom_j and not nom_j.isalpha():
            st.error("Le nom ne doit contenir que des lettres.")

        if prenom_j and not prenom_j.isalpha():
            st.error("Le prénom ne doit contenir que des lettres.")

        # Exécution uniquement si les deux champs sont remplis et valides
        if nom_valide and prenom_valide:
            joueur = creer_joueur(nom=nom_j, prenom=prenom_j)
            if joueur is None:
                st.write("Le joueur n'a pas été trouvé.")

            else:
                st.write(f"💳 Carte d'identité")
                st.write(f"""
                - **Nom :** {joueur.nom}, **prenom :** {joueur.prenom}
                - **Date de naissance :** {joueur.date_nais}
                - **Main dominante :** {joueur.main}
                - **Entrée dans le circuit professionnel :** {joueur.pre_match}
                - **Dernier match connu :** {joueur.der_match}
                """)

    with tab2:

        if joueur is not None:

            if not pd.isna(joueur.pre_match) and not pd.isna(joueur.der_match):

                annee_debut=pd.to_datetime(joueur.pre_match).year
                annee_fin=pd.to_datetime(joueur.der_match).year


                st.write(f"Dans notre base de données le premier match de {joueur.nom}"
                f" {joueur.prenom} à eu lieu le {joueur.pre_match}, le dernier match à"
                f" eu lieu le {joueur.der_match}")

                if annee_debut is None :
                    st.write("Aucun match n'est présent dans la base de donnée")

                else :
                    choix_annee = st.radio("Informations matchs:",
                                     ("Sur une année précise", "Carrière complete"))

                    if choix_annee == "Sur une année précise":
                        annee_m = st.number_input(
                            f"Saisir l'année désirée entre {annee_debut} et {annee_fin}",
                            min_value=annee_debut,
                            max_value=annee_fin,
                            step=1,
                            format="%d",  # pour forcer un affichage entier
                            key="annee_match"
                            )

                        data = joueur.chercher_matchs(annee_m)

                    else:
                        data = joueur.chercher_matchs()

                    data = data.sort_values(by='tourney_date', ascending=True)


                    # Ajout d'une colonne de sélection (si elle n'existe pas déjà)
                    # if "Sélectionner" not in data.columns:
                    #    data["Sélectionner"] = [False] * len(data)

                    if "Sélectionner" not in data.columns:
                        data["Sélectionner"] = False  # initialise avec False
                    else:
                        data["Sélectionner"] = data["Sélectionner"].fillna(0).astype(bool)

                    # Déplacer la colonne "Sélectionner" en première position
                    cols = ["Sélectionner"] + [col for col in data.columns if col != "Sélectionner"]
                    data = data[cols]

                    # Utiliser un data_editor pour afficher la sélection
                    edited_data = st.data_editor(
                        data,
                        use_container_width=True,
                        key="editor_tournoi",
                        column_config={
                            "Sélectionner": st.column_config.CheckboxColumn("Sélectionner", help="Cochez pour voir les détails du tournoi")
                            },
                        hide_index=True,
                        column_order=("Sélectionner", 'tourney_date', 'tourney_name', 'surface', 'type' ,
                              'resultat', 'round_label') # Optionnel: définir l'ordre des colonnes
                        )

                    # Trouver les lignes sélectionnées
                    selected = edited_data[edited_data["Sélectionner"] == True]


                    # Affichage des détails
                    if len(selected) == 1:
                        st.subheader("🎾 Détails du tournoi sélectionné")
                        match = selected.iloc[0]
                        id_tournoi = match['tourney_id']
                        type = match['type']
                        data_tournoi = joueur.chercher_parcours_tournois(id_tournoi,type)
                        for index, match in data_tournoi.iterrows():
                            texte, texte2 = afficher_match(match,type)
                            st.write(texte)
                            st.write(texte2)
                    elif len(selected) > 1:
                        st.warning("Merci de sélectionner un seul match à la fois.")
                    else:
                        st.info("Sélectionnez un match dans le tableau pour voir les détails.")

            else:
                st.write(f"Aucun match renseigné dans la base pour {joueur.nom} {joueur.prenom}")

    with tab3:

        if joueur is not None:

            if not pd.isna(joueur.pre_match) and not pd.isna(joueur.der_match):

                annee_debut=pd.to_datetime(joueur.pre_match).year
                annee_fin=pd.to_datetime(joueur.der_match).year

                st.write(f"Dans notre base de données le premier match de {joueur.nom}"
                f" {joueur.prenom} à eu lieu le {joueur.pre_match}, le dernier match à"
                f" eu lieu le {joueur.der_match}")

                if annee_debut is None :
                    st.write("Aucun match n'est présent dans la base de donnée")

                else :
                    choix_tournoi = st.radio("Informations tournois:",
                                     ("Sur une année précise", "Carrière complete"))

                    if choix_tournoi == "Sur une année précise":
                        annee_t = st.number_input(
                            f"Saisir l'année désirée entre {annee_debut} et {annee_fin}",
                            min_value=annee_debut,
                            max_value=annee_fin,
                            step=1,
                            format="%d",  # pour forcer un affichage entier
                            key="annee_tournoi"
                            )

                        data = joueur.chercher_tournois(annee_t)

                    else:
                        data = joueur.chercher_tournois()

                    data = data.sort_values(by='tourney_date', ascending=True)


                    # Ajout d'une colonne de sélection (si elle n'existe pas déjà)
                    # if "Sélectionner" not in data.columns:
                    #    data["Sélectionner"] = [False] * len(data)

                    if "Sélectionner" not in data.columns:
                        data["Sélectionner"] = False  # initialise avec False
                    else:
                        data["Sélectionner"] = data["Sélectionner"].fillna(0).astype(bool)

                    # Déplacer la colonne "Sélectionner" en première position
                    cols = ["Sélectionner"] + [col for col in data.columns if col != "Sélectionner"]
                    data = data[cols]

                    # Utiliser un data_editor pour afficher la sélection
                    edited_data = st.data_editor(
                        data,
                        use_container_width=True,
                        key="editor_tournoi_gagné",
                        column_config={
                            "Sélectionner": st.column_config.CheckboxColumn("Sélectionner", help="Cochez pour voir les détails du match")
                            },
                        hide_index=True,
                        column_order=("Sélectionner", 'tourney_date', 'tourney_name', 'surface', 'type' ,
                              'resultat', 'round_label') # Optionnel: définir l'ordre des colonnes
                        )

                    # Trouver les lignes sélectionnées
                    selected = edited_data[edited_data["Sélectionner"] == True]

                    # Affichage des détails
                    if len(selected) == 1:
                        st.subheader("🎾 Détails du tournoi sélectionné")
                        match = selected.iloc[0]
                        id_tournoi = match['tourney_id']
                        type = match['type']
                        data_tournoi = joueur.chercher_parcours_tournois(id_tournoi,type)
                        for index, match in data_tournoi.iterrows():
                            texte, texte2 = afficher_match(match,type)
                            st.write(texte)
                            st.write(texte2)


                    elif len(selected) > 1:
                        st.warning("Merci de sélectionner un seul tournoi à la fois.")
                    else:
                        st.info("Sélectionnez un tournoi dans le tableau pour voir les détails.")
            else:
                st.write(f"Aucun tournoi renseigné dans la base pour {joueur.nom} {joueur.prenom}")

    with tab4:

        if joueur is not None:

            data = joueur.chercher_rang()

            # Assurez-vous que les dates sont bien en datetime
            data['ranking_date'] = pd.to_datetime(data['ranking_date'].astype(str), format='%Y%m%d')

            # Trier par date
            data = data.sort_values('ranking_date')

            st.write("Évolution du classement au fil du temps")

            chart = alt.Chart(data).mark_line(point=True).encode(
                x=alt.X('ranking_date:T', title="Date"),
                y=alt.Y('rank:Q', title="Classement"),
                tooltip=['ranking_date:T', 'rank']
            ).properties(
                width=700,
                height=400,
                title="Évolution du rang du joueur"
            ).interactive()

            st.altair_chart(chart, use_container_width=True)

            st.write(data)

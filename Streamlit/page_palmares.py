import streamlit as st
import pandas as pd
import altair as alt
import os
import sys

# Utiliser le répertoire courant pour Streamlit
base_path = os.getcwd()
test_vacances_path = os.path.join(base_path, "Test_vacances")

# Ajouter au sys.path
if test_vacances_path not in sys.path:
    sys.path.append(test_vacances_path)

# Maintenant importer
from classe_joueur_v2 import Joueur, creer_joueur

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
                st.write(f"Visitez les onglet suivant pour avoir des informations sur {joueur.nom} {joueur.prenom}")

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

                    st.write(data)

            else:
                st.write(f"Aucun match renseigné dans la base pour {joueur.nom} {joueur.prenom}")

    with tab3:

        if joueur is not None:

            if not pd.isna(joueur.pre_match) and not pd.isna(joueur.der_match):

                annee_debut=pd.to_datetime(joueur.pre_match).year
                nnee_fin=pd.to_datetime(joueur.der_match).year

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

                        data = joueur.chercher_tournois(annee_m)

                    else:
                        data = joueur.chercher_tournois()

                    st.write(data)

            else:
                st.write(f"Aucun match renseigné dans la base pour {joueur.nom} {joueur.prenom}")

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

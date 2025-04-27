import streamlit as st
import pandas as pd
import altair as alt
import os
import sys
import math

# Récupère le chemin absolu du dossier où se trouve le script streamlit_app.py
current_dir = os.path.dirname(os.path.abspath(__file__))
code_path = os.path.abspath(os.path.join(current_dir, "..", "Code"))

# Ajout au sys.path
if code_path not in sys.path:
    sys.path.insert(0, code_path)  # Priorité plus haute

# Ensuite tu fais tes imports
from classe_joueur import Joueur
from creer_joueur import creer_joueur

def verifier_et_creer_joueur(nom_j, prenom_j):
    """ Créer un joueur/ joueuse """
    if nom_j and not nom_j.isalpha():
        st.error("Le nom ne doit contenir que des lettres.")
    if prenom_j and not prenom_j.isalpha():
        st.error("Le prénom ne doit contenir que des lettres.")

    if nom_j.isalpha() and prenom_j.isalpha():
        joueur = creer_joueur(nom=nom_j, prenom=prenom_j)
        if joueur:
            st.write(f"💳 Carte d'identité")
            st.write(f"""
            - **Nom :** {joueur.nom}, **prenom :** {joueur.prenom}
            - **Date de naissance :** {joueur.date_nais}
            - **Main dominante :** {joueur.main}
            - **Nombre de tournois joué :** {joueur.nb_tournois_joue}
            - **Nombre de tournois gagné :** {joueur.nb_tournois_gagne}
            - **Proportion de match gagné en ayant perdu le 1er set :** {joueur.prop_vic_set_1_perdu}
            - **Proportion de balle de break sauvée :** {joueur.prop_balle_break_sauvee}
            - **Nombre de semaine classé :** {joueur.nb_sem_classe}
            - **Nombre de semaine resté au top 10 :** {joueur.nb_sem_1_10}
            - **Nombre de semaine resté au top 50 :** {joueur.nb_sem_11_50}
            - **Nombre de semaine resté au top 100 :** {joueur.nb_sem_51_100}
            - **Entrée dans le circuit professionnel :** {joueur.pre_match}
            - **Dernier match connu :** {joueur.der_match}
            """)
        else:
            st.write("Le joueur n'a pas été trouvé.")
        return joueur
    return None

def texte_afficher_match(match):
    """ Affiche le détail d'un match  """

    # Remplacer les valeurs manquantes par des ?
    match = match.fillna('?')

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


def choix_parametre(joueur,data, cle):
    # Créer une liste pour stocker les valeurs sélectionnées
    param = [None, None, None]

    # Selection des années
    annee_debut = pd.to_datetime(joueur.pre_match).year
    annee_fin = pd.to_datetime(joueur.der_match).year

    # Créer une liste des années entre annee_debut et annee_fin
    annees = list(range(annee_debut, annee_fin + 1))

    # Utiliser un menu déroulant avec multiselect pour permettre à l'utilisateur de choisir plusieurs années
    annees_selectionnees = st.multiselect(
        "Sélectionner les années",
        options=annees,
        default=annees,  # Par défaut, toutes les années sont sélectionnées
        key="unique_key_annees" + cle
        )

    param[0] = annees_selectionnees

    # Selection des niveau de tournoi
    liste_level = data['tourney_level'].unique()

    # Utiliser un menu déroulant avec multiselect pour permettre à l'utilisateur de choisir plusieurs niveaux
    levels_selectionnes = st.multiselect(
        "Sélectionner les niveaux",
        options=liste_level,
        default=liste_level,  # Par défaut, tous les niveaux sont sélectionnés
        key="unique_key_levels" + cle
    )

    param[1] = levels_selectionnes

    # Selection surfaces
    liste_surface = data['surface'].unique()

    # Utiliser un menu déroulant avec multiselect pour permettre à l'utilisateur de choisir plusieurs niveaux
    surface_selectionnes = st.multiselect(
        "Sélectionner les niveaux",
        options=liste_surface,
        default=liste_surface,  # Par défaut, tous les niveaux sont sélectionnés
        key="unique_key_surfaces" + cle
    )

    param[2] = surface_selectionnes

    return param



# Fonction de sélection des données par année
def selection_tableau(joueur, fonction_cherche, cle):
    """ Choisir la modalité parcours/tournois année/carrière tournoi_level """

    data = fonction_cherche()

    # Demander à l'utilisateur s'il veut fixer des paramètres
    fix_parametres = st.radio(
        "Souhaitez-vous fixer des paramètres ?",
        ("Oui", "Non"),
        index=1, # Pour fixer a non
        key=f"fix_param_{cle}"
    )

    # Si l'utilisateur veut fixer des paramètres
    if fix_parametres == "Oui":
        # Appel à la fonction choisir_parametre pour récupérer les nouvelles années
        param = choix_parametre(joueur,data,cle)

        # Appel de la fonction de recherche avec les nouvelles années
        data = fonction_cherche(*param)

    return data.sort_values(by='tourney_date', ascending=True)



def afficher_tableau(joueur, data, key_suffix):
    """ Afficher tableau du parcours/ tournois """

    if "Sélectionner" not in data.columns:
        data["Sélectionner"] = False
    else:
        data["Sélectionner"] = data["Sélectionner"].fillna(0).astype(bool)

    data = data[["Sélectionner"] + [col for col in data.columns if col != "Sélectionner"]]

    edited_data = st.data_editor(
        data,
        use_container_width=True,
        key=f"editor_{key_suffix}",
        column_config={
            "Sélectionner": st.column_config.CheckboxColumn("Sélectionner", help="Cochez pour voir les détails")
        },
        hide_index=True,
    )

    selected = edited_data[edited_data["Sélectionner"] == True]

    if len(selected) == 1:
        st.subheader("🎾 Détails du tournoi sélectionné")
        match = selected.iloc[0]
        id_tournoi = match['tourney_id']
        type = match['type']
        data_tournoi = joueur.chercher_parcours_tournoi(id_tournoi, type)
        for _, match in data_tournoi.iterrows():
            texte, texte2 = texte_afficher_match(match)
            st.write(texte)
            st.write(texte2)
            st.markdown("<hr>", unsafe_allow_html=True)

    elif len(selected) > 1:
        st.warning("Merci de sélectionner un seul élément à la fois.")
    else:
        st.info("Sélectionnez un élément dans le tableau pour voir les détails.")

def appliquer_couleur_ligne(row):
    # Dictionnaire de correspondance couleur → pastel
    couleurs_pastel = {
        'black': '#d6d6d6',
        'green': '#d0f0c0',
        'blue': '#cce5ff',
        'orange': '#ffe5b4'
    }

    couleur = couleurs_pastel.get(row.get("couleur", ""), "#ffffff")  # blanc par défaut
    return [f"background-color: {couleur}"] * len(row)

def creer_graph_point(data):

    base = alt.Chart(data).mark_point(filled=True, size=50)

    # Si la colonne "couleur" existe, on l’utilise pour colorier les points
    if 'couleur' in data.columns:
        chart = base.encode(
            x=alt.X('ranking_date:T', title="Date"),
            y=alt.Y('rank:Q', title="Classement", scale=alt.Scale(reverse=True)),
            color=alt.Color('couleur:N', scale=None, legend=None),
            tooltip=['ranking_date:T', 'rank', 'couleur']
        )
    else:
        chart = base.encode(
            x=alt.X('ranking_date:T', title="Date"),
            y=alt.Y('rank:Q', title="Classement", scale=alt.Scale(reverse=True)),
            tooltip=['ranking_date:T', 'rank']
        )

    chart = chart.properties(
        width=700,
        height=400,
        title="Évolution du rang du joueur"
    ).interactive()

    return chart


def afficher_evolution_rang_generale(joueur):
    data = joueur.chercher_rang()
    # data['ranking_date'] = pd.to_datetime(data['ranking_date'].astype(str), format='%Y%m%d')
    data['ranking_date'] = pd.to_datetime(data['ranking_date'], errors='coerce').dt.date
    data = data.sort_values('ranking_date')

    # Créer une nouvelle colonne "segment_color" qui définit la couleur de chaque segment
    data['couleur'] = 'orange'  # Valeur par défaut
    data.loc[data['rank'] <= 10, 'couleur'] = 'black'  # Rangs entre 1 et 10 (noir)
    data.loc[(data['rank'] > 10) & (data['rank'] <= 50), 'couleur'] = 'green'  # Rangs entre 11 et 50 (bleu)
    data.loc[(data['rank'] > 50) & (data['rank'] <= 100), 'couleur'] = 'blue'  # Rangs entre 51 et 100 (vert)

    st.write("Évolution du classement au fil du temps")

    chart = creer_graph_point(data)

    # Affichage du graphique dans Streamlit
    st.altair_chart(chart, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Filtrer les rangs entre 1 et 100 (inclus)
    data_red = data[(data['rank'] >= 1) & (data['rank'] <= 100)]

    st.write("Évolution du classement dans le top 100 au fil du temps")

    color=alt.Color('couleur:N', scale=None, legend=None)
    chart_red = creer_graph_point(data_red)

    # Affichage du graphique dans Streamlit
    st.altair_chart(chart_red, use_container_width=True)

    # Applique la coloration ligne par ligne
    styled_df = data.style.apply(appliquer_couleur_ligne, axis=1)

    # Afficher le tableau avec les couleurs pastel
    st.dataframe(styled_df, use_container_width=True)







def palmares():
    st.title("Palmares d'un joueur")
    tab1, tab2, tab3, tab4 = st.tabs(["Choix du joueur", "Participation à un match", "Palmares de victoire", "Évolution du rang"])

    with tab1:
        nom_j = st.text_input("Entrez le nom du joueur (ex Nadal)")
        prenom_j = st.text_input("Entrez le prénom du joueur (ex Rafael)")
        joueur = verifier_et_creer_joueur(nom_j, prenom_j)

    if joueur:

        with tab2:
            st.write(f"Premier match : {joueur.pre_match}, dernier : {joueur.der_match}")

            data = selection_tableau(joueur,joueur.chercher_resultat, "match")
            afficher_tableau(joueur, data, "match")

        with tab3:
            st.write(f"Premier match : {joueur.pre_match}, dernier : {joueur.der_match}")

            data = selection_tableau(joueur,joueur.chercher_tournoi_gagne, "tournoi")
            afficher_tableau(joueur, data, "tournoi_gagne")

        with tab4:
            afficher_evolution_rang_generale(joueur)

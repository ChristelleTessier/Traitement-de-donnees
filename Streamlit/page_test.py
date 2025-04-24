import streamlit as st
import pandas as pd

def test():
    # Exemple de données
    data = pd.DataFrame({
        'tourney_date': ['1983-05-23', '1978-04-03', '1978-04-17'],
        'tourney_name': ['Roland Garros', 'Johannesburg', 'Nice'],
        'surface': ['Clay', 'Hard', 'Clay'],
        'type': ['simple', 'simple', 'simple'],
        'resultat': [1, 1, 0],
        'round_label': ['Finale', '16ème de finale', 'Finale']
    })

    # Ajouter une colonne de sélection
    data["Sélectionner"] = False

    # Éditeur interactif avec cases à cocher
    edited_data = st.data_editor(
        data,
        num_rows="dynamic",
        use_container_width=True,
        key="editor",
        column_config={
            "Sélectionner": st.column_config.CheckboxColumn("Sélectionner", help="Coche pour afficher les détails")
        },
        hide_index=False
)

    # Trouver les lignes sélectionnées
    selected_rows = edited_data[edited_data["Sélectionner"] == True]

    st.write(selected_rows)

    # Afficher les détails s’il y a une sélection
    if not selected_rows.empty:
        st.subheader("🎾 Détails du match sélectionné")
        for _, row in selected_rows.iterrows():
            st.write(row.drop("Sélectionner"))  # on n'affiche pas la colonne checkbox
    else:
        st.info("Sélectionne un match avec la case à cocher pour voir les détails.")

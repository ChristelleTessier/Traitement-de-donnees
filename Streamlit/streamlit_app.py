import streamlit as st

from page_intro import intro
from page_palmares import palmares


def main():
    # Sidebar
    pages = {
        "Introduction":intro,
        "Palmares d'un joueur": palmares
    }

    # Barre latérale avec des boutons radio pour chaque page
    selected_page = st.sidebar.radio("Choisis une page", list(pages.keys()))

    # Appeler la fonction correspondant à la page sélectionnée
    pages[selected_page]()

    st.sidebar.markdown("""
        Auteurs :
        * Valentin ROSE
        * Christelle TESSIER
        * Ivan TISSOT
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

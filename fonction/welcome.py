import streamlit as st


def welcome():
    st.title("Package NLP")
    st.header("Informations")
    st.markdown("Initié le : 02/03/2023")
    st.markdown("Interlocuteurs : Marine CERCLIER, Grégory GAUTHIER, Tangi LE TALLEC, Alan BIGNON, Islem EZZINE, Killian FARRELL")
    st.markdown("Dans le cadre du projet interne DataScience Package NLP")

    st.header("Présentation de la classe NLP")
    st.write("La classe NLP fournit un ensemble de méthodes pour le prétraitement du texte dans les langues française et anglaise. Voici une brève présentation de ses fonctionnalités principales:")
    st.write("- **cleanStopWord**: Cette méthode permet de nettoyer les mots d'arrêt dans le texte en fonction de la langue choisie et offre la possibilité d'ajouter ou de supprimer des mots d'arrêt spécifiques.")
    st.write("- **cleanText**: Cette méthode polyvalente nettoie un texte en supprimant tous les caractères spéciaux, avec des options pour garder les nombres et certains caractères exceptionnels.")
    st.write("- **lemmatisation**: Une méthode avancée qui applique la lemmatisation sur le texte, avec des options pour exclure certains mots ou types de mots et garder les nombres.")
    st.write("\nEnsemble, ces méthodes facilitent grandement le prétraitement du texte, ce qui est une étape cruciale dans de nombreux projets de traitement du langage naturel (NLP). La classe est conçue pour être facilement personnalisable et adaptable aux différents besoins et exigences des projets NLP.")
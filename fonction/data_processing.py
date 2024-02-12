import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import importlib.resources as resources

from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
from collections import Counter
from packagenlp.nlp import NLP


import streamlit as st
import pandas as pd
from io import StringIO


def process():
    dataframe = None
    language = None
    nlp = NLP()

    tab_titles = ['Import Data', 'Treatment Data', 'Visualization Data']
    tab1, tab2, tab3 = st.tabs(tab_titles)

    with tab1:
        st.header("📂 Import Data")
        st.divider()
        uploaded_file = st.file_uploader("Choose a file")

        if uploaded_file is not None:
            try:
                delimiter = st.text_input("Enter the delimiter:", ';')
                dataframe = pd.read_csv(uploaded_file, delimiter=delimiter)
                st.write("Data extract:")

                show_all_data = st.toggle("Show all data")
                if show_all_data:
                    st.write(dataframe)
                else:
                    st.write(dataframe.head())

                st.write(f"DataFrame Dimensions: {dataframe.shape}")

                language = st.radio("Select the language of your data",
                                ["**French**", "**English**"],
                                horizontal=True,
                                index=None)
                
                if language == "**French**":
                    language = "fr"
                elif language == "English":
                    language = "en"
    
            except Exception as e:
                st.error(f"Error parsing CSV file: {str(e)}")
        


    # Initialize session state
    if 'cleaned_data' not in st.session_state:
        st.session_state.cleaned_data = None


    with tab2:
        st.header("⚙️ Treatment Data")
        st.divider()

        

        if dataframe is not None:
            selected_column = st.selectbox("Select a column to apply the treatment", dataframe.columns)

            choices_treatment = st.multiselect('Select the treatments to apply to your column',
                                            ['Clean Text', 'StopWords', "Lemmatization"])

            st.divider()

            apply_stopwords = False
            apply_clean_text = False
            apply_lemmatization = False

            if 'Clean Text' in choices_treatment:
                st.subheader("Clean Text")

                st.caption("##### Paramètres")
                keep_numbers = st.checkbox("Keep the numbers", value=True)
                exception = st.text_input("Exceptions", "")
                remove_accent = st.checkbox("Remove accents", value=True)
                lowercase = st.checkbox("Lowercase text", value=True)

            if 'StopWords' in choices_treatment:
                st.subheader("StopWords Removal")
                add_stopwords = st.text_input("Add stopwords (separated by commas, press enter to apply)", "")
                remove_stopwords = st.text_input("Remove stopwords (separated by commas, press enter to apply)", "")
                
            if 'Lemmatization' in choices_treatment:
                st.subheader("Lemmatisation")
                lemma_exclu = st.text_input("Enter the lemma exclusions (separated by a comma) and their replacement form (separated by a colon). For example: `data:dater`, `hello:hi`", "")
                lemma_exclu_dict = {i.split(":")[0].strip(): (i.split(":")[1].strip() if len(i.split(":")) > 1 else None) for i in lemma_exclu.split(",") if i}
                keep_numbers = st.checkbox("Keep numbers", value=True)
                exlu_type_word_input = st.text_input("Enter the types of words to keep (separated by a comma). For example: `VER`, `NOM`", "")
                exlu_type_word = [i.strip() for i in exlu_type_word_input.split(",") if i]

            # Boutons Apply en dessous de tous les paramètres
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'Clean Text' in choices_treatment:
                    apply_clean_text = st.toggle("Apply Clean Text")
            with col2:
                if 'StopWords' in choices_treatment:
                    apply_stopwords = st.toggle("Apply StopWords Removal")
            with col3:
                if 'Lemmatization' in choices_treatment:
                    apply_lemmatization = st.toggle("Apply Lemmatization")

            if apply_clean_text:
                if selected_column is not None and selected_column in dataframe.columns and dataframe[selected_column].apply(lambda x: isinstance(x, str)).all():
                    with st.spinner("Clean Text in progress"):
                        cleaned_data = dataframe[selected_column].apply(lambda text: nlp.cleanText(text, keep_numbers, exception, remove_accent, lowercase))
                        st.session_state.cleaned_data = cleaned_data 
                    st.success('Clean Text Done!')
                else:
                    st.warning("La colonne sélectionnée ne contient pas de texte (chaînes de caractères). Veuillez sélectionner une colonne valide.")
            
            if apply_stopwords:
                if selected_column is not None and selected_column in dataframe.columns and dataframe[selected_column].apply(lambda x: isinstance(x, str)).all():
                    with st.spinner("StopWords Removal in progress"):
                        cleaned_data = dataframe[selected_column].apply(lambda text: nlp.cleanStopWord(text, language, add_stopwords.split(","), remove_stopwords.split(",")))
                        st.session_state.cleaned_data = cleaned_data 
                    st.success(' StopWords Done!')
                else:
                    st.warning("Selected column does not contain text (strings). Please select a valid column.")
            
            if apply_lemmatization:
                if selected_column is not None and selected_column in dataframe.columns and dataframe[selected_column].apply(lambda x: isinstance(x, str)).all():
                    with st.spinner("Lemmatization in progress"):
                        cleaned_data = dataframe[selected_column].apply(lambda text: nlp.lemmatisation(text, lemma_exclu_dict, language, keep_numbers, exlu_type_word))
                        st.session_state.cleaned_data = cleaned_data  
                    st.success('Lemmatization Done!')
                else:
                    st.warning("Selected column does not contain text (strings). Please select a valid column.")

            if st.session_state.cleaned_data is not None:
                st.write("Processed Data extract:")
                st.write(st.session_state.cleaned_data)  # Suppression de head() pour afficher toutes les données
            else:
                st.warning("Please apply one of the treatments to see the processed data.")

        else:
            st.warning("No DataFrame uploaded yet. Please upload a file in the 'Import Data' tab.")

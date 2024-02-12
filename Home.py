import streamlit as st
import importlib.resources as resources

from PIL import Image

from streamlit_option_menu import option_menu
from fonction import welcome, data_processing


st.set_page_config(
    page_title="Acceuil",
    page_icon="👋",
    layout = "wide"
)


logo =Image.open('resources/logo.png')
st.sidebar.image(logo)

with st.sidebar:
    selected = option_menu(
        menu_title="Package NLP",
        options=["Home", "Data Processing"],
        icons=['house', 'gear'],
        menu_icon="app-indicator", default_index=0,
        styles={
        "menu-title": {"color": "#FFFFFF"},
        "container": {"padding": "5!important", "background-color": "#000000"},
        "icon": {"color": "#FFFFFF", "font-size": "20px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#000000"},
        "nav-link-selected": {"background-color": "#DF6036"},
    }
    )

if selected == "Home":
    welcome.welcome()
if selected == "Data Processing":
    data_processing.process()

import streamlit as st
from pages.home import home_page
from pages.chat import chat_page
from pages.history import history_page
from pages.settings import settings_page
from components.login import login_page
from components.register import registration_page
from services.auth_service import authenticate


st.set_page_config(page_title="BankBot Assistant", page_icon="🏦", layout="wide")

def chatbot_page():
    if "language" not in st.session_state:
        st.session_state["language"] = "fr"
        
    menu_labels = {
        "🏠 Accueil": "Accueil", 
        "💬 Chat": "Chat",
        "🕓 Historique": "Historique",
        "⚙️ Paramètres": "Paramètres"
    }
    
    with st.sidebar:
        st.markdown("<div class='sidebar-title'>🔧 Navigation</div>", unsafe_allow_html=True)
        selection = st.radio("Aller à :", list(menu_labels.keys()), key="nav", label_visibility="collapsed")
        section = menu_labels[selection]
    
    if section == "Accueil":
        home_page()
    elif section == "Chat":
        chat_page()
    elif section == "Historique":
        history_page()
    elif section == "Paramètres":
        settings_page()
    else:
        st.error("Section inconnue")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    if "show_registration" in st.session_state and st.session_state.show_registration:
        registration_page()
    else:
        login_page()
else:
    chatbot_page()

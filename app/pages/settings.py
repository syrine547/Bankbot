import streamlit as st

def settings_page():
    st.title("⚙️ Paramètres")
    language = st.radio("Choisir la langue", ["Français", "English", "العربية التونسية"])
    st.session_state.language = 'fr' if language == "Français" else 'en' if language == "English" else 'ar'
    st.success(f"Langue changée à {language}")

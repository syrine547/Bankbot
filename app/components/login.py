import streamlit as st
from services.auth_service import authenticate

def login_page():
    st.image("app/assets/bankbot_logo.png", width=120)
    st.title("🔐 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Connexion réussie !")
            st.rerun()
        else:
            st.error("Identifiants invalides")
    if st.button("Pas de compte ? S'inscrire"):
        st.session_state.show_registration = True
        st.rerun()

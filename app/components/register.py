import streamlit as st
from services.auth_service import register

def registration_page():
    st.title("📝 Inscription")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    confirm_password = st.text_input("Confirmer le mot de passe", type="password")
    if st.button("S'inscrire"):
        if password != confirm_password:
            st.error("Les mots de passe ne correspondent pas.")
        elif register(username, password):
            st.success("Compte créé avec succès !")
            st.session_state.show_registration = False
            st.rerun()
        else:
            st.error("Ce nom d'utilisateur existe déjà.")

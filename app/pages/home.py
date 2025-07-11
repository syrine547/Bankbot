import streamlit as st
from services.chat_service import get_conversations
# from services.db_service import get_user_info  # à activer si tu ajoutes cette fonction

def home_page():
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Se déconnecter", key="logout_btn_home"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("Déconnexion réussie !")
        st.rerun()
    st.title("🏠 Accueil")
    st.markdown("Bienvenue dans **BankBot**, votre assistant bancaire intelligent.")

    if "username" not in st.session_state:
        st.warning("Veuillez vous connecter pour voir les informations de votre compte.")
        return

    username = st.session_state.username
    language = st.session_state.get("language", "fr")
    conversations = get_conversations(username)

    st.subheader("👤 Informations du compte")
    st.markdown(f"**Nom d'utilisateur :** {username}")
    st.markdown(f"**Langue préférée :** {language}")
    st.markdown(f"**Nombre de conversations enregistrées :** {len(conversations)}")

    # Si tu ajoutes une colonne 'created_at' dans la base de données :
    # user_info = get_user_info(username)
    # if user_info and 'created_at' in user_info:
    #     st.markdown(f"**Date d'inscription :** {user_info['created_at']}")

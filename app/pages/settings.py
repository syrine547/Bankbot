import streamlit as st

def settings_page():
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Se déconnecter", key="logout_btn_settings"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("Déconnexion réussie !")
        st.rerun()
    st.title("⚙️ Paramètres")
    language = st.radio("Choisir la langue", ["Français", "English", "العربية التونسية"], key="settings_language")
    st.session_state.language = 'fr' if language == "Français" else 'en' if language == "English" else 'ar'
    st.success(f"Langue changée à {language}")

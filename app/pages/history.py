import streamlit as st
import os
from services.chat_service import get_conversations

def history_page():
    st.title("🕓 Historique")
    st.write("Voici l'historique de vos conversations.")

    if "username" not in st.session_state:
        st.warning("Veuillez vous connecter pour voir votre historique.")
        return

    username = st.session_state.username
    conversations = get_conversations(username)

    if not conversations:
        st.info("Aucune conversation enregistrée pour le moment.")
    else:
        for filename in conversations:
            with st.expander(filename):
                filepath = os.path.join("data/historiques", filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    st.text_area("Contenu", content, height=300)

                if st.button(f"▶️ Poursuivre cette conversation", key=filename):
                    # Convertir le contenu en liste de tuples
                    lines = content.strip().split("\n")
                    chat_log = []
                    for i in range(0, len(lines), 2):
                        if i + 1 < len(lines):
                            question = lines[i].replace("User: ", "").replace("Utilisateur : ", "")
                            response = lines[i + 1].replace("Bot: ", "").replace("BankBot : ", "")
                            chat_log.append((question, response))
                    st.session_state.chat_log = chat_log
                    st.success("Conversation chargée. Redirection vers le chat...")
                    st.switch_page("pages/chat.py")

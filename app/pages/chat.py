import streamlit as st
from services.chat_service import save_conversation
import ollama

def chat_page():
    st.title("💬 Chat")

    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []

    def get_bot_response(prompt):
        try:
            response = ollama.chat(model="gemma:2b", messages=[
                {"role": "system", "content": "Tu es BankBot, un assistant bancaire intelligent."},
                *[
                    {"role": "user", "content": q} if i % 2 == 0 else {"role": "assistant", "content": r}
                    for i, (q, r) in enumerate(st.session_state.chat_log)
                ],
                {"role": "user", "content": prompt}
            ])
            return response['message']['content']
        except Exception as e:
            return f"Erreur : {e}"

    # Zone de conversation
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for question, response in st.session_state.chat_log:
        st.markdown(f"<div class='chat-bubble user'><strong>👤 Vous :</strong> {question}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bubble bot'><strong>🤖 BankBot :</strong> {response}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Zone de saisie
    with st.container():
        st.markdown("<div class='chat-input'>", unsafe_allow_html=True)
        user_input = st.text_input("Votre message", "", key="user_input", label_visibility="collapsed")
        if st.button("Envoyer") and user_input:
            bot_response = get_bot_response(user_input)
            st.session_state.chat_log.append((user_input, bot_response))

            # ✅ Sauvegarde automatique
            if "username" in st.session_state:
                save_conversation(st.session_state.username, st.session_state.chat_log)

            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

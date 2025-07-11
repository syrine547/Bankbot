import streamlit as st
from pathlib import Path
from datetime import datetime
import torch
import textwrap
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from services.chat_service import save_conversation

# ---------------------- Load Finetuned Model ----------------------
@st.cache_resource
def load_finetuned_model():
    here = Path(__file__).parent          # …/app/pages
    base_model_path = here / "TinyLlama-1.1B-Chat-v1.0"
    lora_model_path = here / "tinyllama-bankbot"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(str(base_model_path), local_files_only=True, use_fast=True)
    base_model = AutoModelForCausalLM.from_pretrained(str(base_model_path), local_files_only=True)
    model = PeftModel.from_pretrained(base_model, str(lora_model_path), local_files_only=True)

    model.eval()
    model.to(device)
    return tokenizer, model, device

tokenizer, model, device = load_finetuned_model()

# ---------------------- Chat Page ----------------------
def chat_page():
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Se déconnecter", key="logout_btn_chat"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("Déconnexion réussie !")
        st.rerun()
    st.title("🏦 BankBot - Assistant bancaire")

    # Chat session state
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []

    if st.button("🔄 Réinitialiser la conversation"):
        st.session_state.chat_log = []
        st.rerun()

    # ---------------------- Response Generator ----------------------
    def get_bot_response(prompt):
        try:
            instruction = textwrap.dedent("""\
                Je suis un assistant bancaire expert dans les services des banques tunisiennes.
                Je suis BankBot, un assistant bancaire intelligent, professionnel et poli.
                Réponds toujours clairement, de manière concise.
                Je peux aussi répondre en arabe, en français ou en anglais selon la question.
                Explique simplement les concepts lorsque c’est possible.
            """)

            full_prompt = f"""{instruction}

### Banque: Générique
### Question: {prompt}
### Réponse:"""

            inputs = tokenizer(full_prompt, return_tensors="pt").to(device)

            # Safety check on input size
            max_input_tokens = 512
            if inputs["input_ids"].shape[1] > max_input_tokens:
                return "Votre question est trop longue, veuillez la reformuler."

            input_length = inputs["input_ids"].shape[1]

            output = model.generate(
                **inputs,
                max_new_tokens=100,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.2,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )

            response = tokenizer.decode(output[0][input_length:], skip_special_tokens=True).strip()

            if not response:
                response = "Désolé, je n’ai pas bien compris votre question. Pouvez-vous la reformuler ?"

            return response

        except Exception as e:
            return f"Erreur : {e}"

    # ---------------------- Display Chat ----------------------
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for question, response in st.session_state.chat_log:
        st.markdown(f"<div class='chat-bubble user'><strong>👤 Vous :</strong> {question}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bubble bot'><strong>🤖 BankBot :</strong> {response}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------- Input Box ----------------------
    with st.container():
        st.markdown("<div class='chat-input'>", unsafe_allow_html=True)
        user_input = st.text_input("Votre message", "", key="user_input", label_visibility="collapsed")
        if st.button("Envoyer") and user_input:
            bot_response = get_bot_response(user_input)
            st.session_state.chat_log.append((user_input, bot_response))
            st.rerun()
        # Bouton pour sauvegarder la conversation
        if st.button("💾 Sauvegarder la conversation"):
            if "username" in st.session_state:
                save_conversation(st.session_state.username, st.session_state.chat_log)
                st.success("Conversation sauvegardée !")
            else:
                st.warning("Vous devez être connecté pour sauvegarder la conversation.")
        st.markdown("</div>", unsafe_allow_html=True)


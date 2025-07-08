import streamlit as st
from pathlib import Path
from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from services.chat_service import save_conversation
import ollama

@st.cache_resource
def load_finetuned_model():
    base_model_path = Path(__file__).parent / "../TinyLlama-1.1B-Chat-v1.0"
    lora_model_path = Path(__file__).parent / "../tinyllama-bankbot"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(str(base_model_path), local_files_only=True, use_fast=True)
    base_model = AutoModelForCausalLM.from_pretrained(str(base_model_path), local_files_only=True)
    model = PeftModel.from_pretrained(base_model, str(lora_model_path), local_files_only=True)

    model.eval()
    model.to(device)
    return tokenizer, model, device

tokenizer, model, device = load_finetuned_model()

def build_prompt_from_history(chat_log):
    messages = []
    for q, r in chat_log:
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": r})
    return messages

def chat_page():
    st.title("🏦 BankBot - Assistant bancaire")

    if "chat_log" not in st.session_state:
        st.session_state.chat_log = []

    #def get_bot_response(prompt):
    #    try:
    #        messages = build_prompt_from_history(st.session_state.chat_log)
    #        messages.append({"role": "user", "content": prompt})
    #        full_prompt = tokenizer.apply_chat_template(
    #            messages, 
    #            tokenize=False, 
    #            add_generation_prompt=True
    #        )
#
    #        inputs = tokenizer(full_prompt, return_tensors="pt").to(device)
    #        output = model.generate(
    #            **inputs,
    #            max_new_tokens=200,
    #            do_sample=True,
    #            top_p=0.9,
    #            temperature=0.7,
    #            pad_token_id=tokenizer.eos_token_id
    #        )
    #        decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    #        response = decoded.split(prompt)[-1].strip().split("</s>")[0].strip()
    #        return response
    #    except Exception as e:
    #        return f"Erreur : {e}"

    def get_bot_response(prompt):
        try:
            # Prompt système amélioré pour guider le modèle
            system_prompt = (
                "Tu es BankBot, un assistant bancaire intelligent, professionnel et poli. "
                "Réponds toujours clairement, de manière concise, en français correct, "
                "en expliquant simplement les concepts lorsque c’est possible."
            )

            messages = [
                {"role": "system", "content": system_prompt},
                *[
                    {"role": "user", "content": q} if i % 2 == 0 else {"role": "assistant", "content": r}
                    for i, (q, r) in enumerate(st.session_state.chat_log)
                ],
                {"role": "user", "content": prompt}
            ]

            response = ollama.chat(model="gemma:2b", messages=messages)
            return response['message']['content'].strip()

        except Exception as e:
            return f"Erreur : {e}"

    # Affichage du chat
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for question, response in st.session_state.chat_log:
        st.markdown(f"<div class='chat-bubble user'><strong>👤 Vous :</strong> {question}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bubble bot'><strong>🤖 BankBot :</strong> {response}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='chat-input'>", unsafe_allow_html=True)
        user_input = st.text_input("Votre message", "", key="user_input", label_visibility="collapsed")
        if st.button("Envoyer") and user_input:
            bot_response = get_bot_response(user_input)
            st.session_state.chat_log.append((user_input, bot_response))

            if "username" in st.session_state:
                save_conversation(st.session_state.username, st.session_state.chat_log)

            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

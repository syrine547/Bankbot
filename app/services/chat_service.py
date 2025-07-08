import os
from datetime import datetime
import re
import streamlit as st

CHATS_DIR = 'data/historiques'
os.makedirs(CHATS_DIR, exist_ok=True)

def extract_keywords(chat_log):
    text = " ".join(q + " " + r for q, r in chat_log).lower()
    words = re.findall(r"\\b\\w+\\b", text)
    stopwords = {"le", "la", "les", "de", "des", "et", "à", "un", "une", "en", "du", "pour", "avec", "sur", "dans"}
    keywords = [w for w in words if w not in stopwords]
    return keywords[:3] if keywords else ["conversation"]

def save_conversation(username, chat_log):
    user_dir = os.path.join("data/historiques", username)
    os.makedirs(user_dir, exist_ok=True)

    # Vérifie si un fichier est déjà en cours
    if "current_conversation_file" in st.session_state:
        filename = st.session_state.current_conversation_file
    else:
        # Génère un nom de fichier basé sur le thème
        keywords = extract_keywords(chat_log)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{'_'.join(keywords)}_{timestamp}.txt"
        st.session_state.current_conversation_file = filename

    filepath = os.path.join(user_dir, filename)

    # Sauvegarde la conversation complète (écrase à chaque fois)
    with open(filepath, "w", encoding="utf-8") as f:
        for question, response in chat_log:
            f.write(f"User: {question}\n")
            f.write(f"Bot: {response}\n")

def get_conversations(username):
    if not os.path.exists(CHATS_DIR):
        return []
    files = [f for f in os.listdir(CHATS_DIR) if f.startswith(username)]
    return sorted(files, reverse=True)

def generate_title_from_content(content):
    content_lower = content.lower()
    mots_cles = {
        "solde": "Demande de solde",
        "transaction": "Historique de transactions",
        "prêt": "Information sur les prêts",
        "carte": "Information sur les cartes",
        "sécurité": "Alertes de sécurité",
        "rdv": "Prise de rendez-vous",
        "banque": "Discussion bancaire",
        "paiement": "Information sur les paiements",
        "compte": "Information sur le compte",
        "crédit": "Information sur le crédit",
        "taux": "Information sur les taux"
    }
    for mot, titre in mots_cles.items():
        if mot in content_lower:
            return titre
    lignes = content.splitlines()
    return lignes[1][:60] + "..." if len(lignes) > 1 else "Conversation sans titre"

def is_valid_chat_filename(filename):
    return re.fullmatch(r"[\\w\\-]+\\.txt", filename) is not None

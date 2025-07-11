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

    # Sauvegarde dans la base de données MySQL
    from services.db_service import init_db
    conn = init_db()
    if conn is not None:
        cursor = conn.cursor()
        # Récupérer l'id utilisateur
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_row = cursor.fetchone()
        if user_row:
            user_id = user_row[0]
            # Insérer chaque message dans chat_history
            for question, response in chat_log:
                cursor.execute(
                    "INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (%s, %s, %s)",
                    (user_id, question, response)
                )
            conn.commit()
        conn.close()

def get_conversations(username):
    if not os.path.exists(CHATS_DIR):
        return []
    user_dir = os.path.join(CHATS_DIR, username)
    conversations = []
    # Fichiers à la racine
    for f in os.listdir(CHATS_DIR):
        if f.startswith(username) and f.endswith('.txt'):
            conversations.append(f)
    # Fichiers dans le dossier utilisateur
    if os.path.isdir(user_dir):
        for f in os.listdir(user_dir):
            if f.endswith('.txt'):
                conversations.append(os.path.join(username, f))
    return sorted(conversations, reverse=True)

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

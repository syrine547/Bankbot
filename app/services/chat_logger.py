from data.db_connect import get_connection

def create_user(username, email=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email) VALUES (%s, %s)",
        (username, email)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def log_chat(user_id, user_message, bot_response):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (%s, %s, %s)",
        (user_id, user_message, bot_response)
    )
    conn.commit()
    conn.close()

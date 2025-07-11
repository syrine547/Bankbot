import mysql.connector

# Connect to DB
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2807",  
        database="bankbot_db"
    )
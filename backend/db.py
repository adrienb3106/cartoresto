import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # charge .env automatiquement

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", "default_user"),
        password=os.getenv("DB_PASSWORD", "default_password"),
        database=os.getenv("DB_NAME", "cartoresto"),
        port=int(os.getenv("DB_PORT", 3306))
    )

import os
from dotenv import load_dotenv
import mysql.connector

# ===== Charger le .env =====
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", ""),
        port=int(os.getenv("DB_PORT", 3306 )),
        user=os.getenv("DB_USER", "default_user"),
        password=os.getenv("DB_PASSWORD", "default_password"),
        database=os.getenv("DB_NAME", "cartoresto")
    )

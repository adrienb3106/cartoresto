import sys
import os

# Ajouter backend/ au PYTHONPATH pour pouvoir importer db.py
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from db import get_connection

def test_connection():
    print("Connexion à la base...")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM restaurants;")
    count = cursor.fetchone()[0]
    print(f"Nombre de restaurants dans la table : {count}")
    
    cursor.execute("SELECT * FROM restaurants;")
    for row in cursor.fetchall():
        print(row)
    
    conn.close()


if __name__ == "__main__":
    test_connection()

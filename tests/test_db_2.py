import sys
import os

# Ajouter backend/ au PYTHONPATH pour que db.py soit trouvable
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from db import get_connection

def test_connection():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1;")
    print(cursor.fetchone())
    conn.close()

if __name__ == "__main__":
    test_connection()

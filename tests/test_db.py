import sys
import os

# Ajouter backend/ au PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from db import get_connection

def test_connection():
    print("Connexion à la base...")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # pour récupérer les colonnes par nom

    # Vérifier le nombre de restaurants
    cursor.execute("SELECT COUNT(*) AS count FROM restaurants;")
    count = cursor.fetchone()["count"]
    print(f"Nombre de restaurants dans la table : {count}")

    # Sélectionner les restaurants avec localisation et informations
    cursor.execute("""
        SELECT r.id, r.nom, r.adresse,
               l.ville, l.code_postal, l.pays, l.latitude, l.longitude,
               i.category, i.note, i.description, i.review
        FROM restaurants r
        JOIN localisation l ON r.localisation_id = l.id
        JOIN informations i ON r.informations_id = i.id
    """)
    rows = cursor.fetchall()
    if not rows:
        print("Aucun restaurant trouvé.")
    else:
        for row in rows:
            print(row)

    conn.close()


if __name__ == "__main__":
    test_connection()

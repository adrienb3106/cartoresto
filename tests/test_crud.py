import sys
import os

# Ajouter backend/ au PYTHONPATH pour importer db.py
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))
from db import get_connection

def test_crud():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # ===== 1Ajouter un nouveau restaurant =====
    cursor.execute("""
        INSERT INTO localisation (ville, code_postal, pays, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
    """, ("Toulouse", "31000", "France", 43.6045, 1.444))
    localisation_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO informations (category, note, description, review)
        VALUES (%s, %s, %s, %s)
    """, ("Français", 7, "Restaurant test unique", "Bon accueil"))
    informations_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO restaurants (nom, adresse, localisation_id, informations_id)
        VALUES (%s, %s, %s, %s)
    """, ("Le Test Resto", "5 Rue Exemple", localisation_id, informations_id))
    
    restaurant_id = cursor.lastrowid
    conn.commit()
    print(f"Restaurant ajouté avec id={restaurant_id}")

    # ===== 2Modifier la note et le pays =====
    cursor.execute("UPDATE informations SET note=%s WHERE id=%s", (9, informations_id))
    cursor.execute("UPDATE localisation SET pays=%s WHERE id=%s", ("Espagne", localisation_id))
    conn.commit()
    print("Note et pays modifiés.")

    # ===== Afficher le restaurant =====
    cursor.execute("""
        SELECT r.id, r.nom, r.adresse,
               i.category, i.note, i.description, i.review,
               l.ville, l.code_postal, l.pays, l.latitude, l.longitude
        FROM restaurants r
        JOIN informations i ON r.informations_id = i.id
        JOIN localisation l ON r.localisation_id = l.id
        WHERE r.id=%s
    """, (restaurant_id,))
    
    resto = cursor.fetchone()
    print("Restaurant après update:")
    print(resto)

    # ===== Supprimer le restaurant =====
    cursor.execute("DELETE FROM restaurants WHERE id=%s", (restaurant_id,))
    cursor.execute("DELETE FROM localisation WHERE id=%s", (localisation_id,))
    cursor.execute("DELETE FROM informations WHERE id=%s", (informations_id,))
    conn.commit()
    print(f"Restaurant id={restaurant_id} supprimé.")

    conn.close()

# Lancer le test
if __name__ == "__main__":
    test_crud()

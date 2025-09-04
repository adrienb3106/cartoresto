import sys
import os

# Ajouter backend/ au PYTHONPATH pour importer db.py
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))
from db import get_connection

# =========================
# CRUD pour les restaurants
# =========================

def create_restaurant(nom, adresse, ville, code_postal, pays, latitude, longitude, category, note, description, review):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ajouter localisation
    cursor.execute("""
        INSERT INTO localisation (ville, code_postal, pays, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
    """, (ville, code_postal, pays, latitude, longitude))
    localisation_id = cursor.lastrowid
    
    # Ajouter informations
    cursor.execute("""
        INSERT INTO informations (category, note, description, review)
        VALUES (%s, %s, %s, %s)
    """, (category, note, description, review))
    informations_id = cursor.lastrowid
    
    # Ajouter restaurant
    cursor.execute("""
        INSERT INTO restaurants (nom, adresse, localisation_id, informations_id)
        VALUES (%s, %s, %s, %s)
    """, (nom, adresse, localisation_id, informations_id))
    
    conn.commit()
    conn.close()
    print(f"Restaurant '{nom}' créé avec succès.")

def read_restaurants():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT r.id, r.nom, r.adresse,
               i.category, i.note, i.description, i.review,
               l.ville, l.code_postal, l.pays, l.latitude, l.longitude
        FROM restaurants r
        JOIN informations i ON r.informations_id = i.id
        JOIN localisation l ON r.localisation_id = l.id
    """)
    
    results = cursor.fetchall()
    conn.close()
    return results

def update_restaurant(restaurant_id, nom=None, adresse=None, note=None, description=None, review=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Mettre à jour le restaurant
    if nom or adresse:
        fields = []
        values = []
        if nom:
            fields.append("nom=%s")
            values.append(nom)
        if adresse:
            fields.append("adresse=%s")
            values.append(adresse)
        values.append(restaurant_id)
        cursor.execute(f"""
            UPDATE restaurants SET {', '.join(fields)} WHERE id=%s
        """, tuple(values))
    
    # Mettre à jour les informations
    if note is not None or description or review:
        # récupérer informations_id
        cursor.execute("SELECT informations_id FROM restaurants WHERE id=%s", (restaurant_id,))
        informations_id = cursor.fetchone()[0]
        fields = []
        values = []
        if note is not None:
            fields.append("note=%s")
            values.append(note)
        if description:
            fields.append("description=%s")
            values.append(description)
        if review:
            fields.append("review=%s")
            values.append(review)
        values.append(informations_id)
        if fields:
            cursor.execute(f"""
                UPDATE informations SET {', '.join(fields)} WHERE id=%s
            """, tuple(values))
    
    conn.commit()
    conn.close()
    print(f"Restaurant id={restaurant_id} mis à jour.")

def delete_restaurant(restaurant_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Récupérer les ids liés
    cursor.execute("SELECT localisation_id, informations_id FROM restaurants WHERE id=%s", (restaurant_id,))
    row = cursor.fetchone()
    if row:
        localisation_id, informations_id = row
        
        # Supprimer restaurant
        cursor.execute("DELETE FROM restaurants WHERE id=%s", (restaurant_id,))
        # Supprimer localisation et informations
        cursor.execute("DELETE FROM localisation WHERE id=%s", (localisation_id,))
        cursor.execute("DELETE FROM informations WHERE id=%s", (informations_id,))
        conn.commit()
        print(f"Restaurant id={restaurant_id} supprimé.")
    else:
        print(f"Restaurant id={restaurant_id} introuvable.")
    
    conn.close()

# =========================
# Test rapide CRUD
# =========================
if __name__ == "__main__":
    # Création
    create_restaurant(
        "Test Resto", "123 Rue Test", "Paris", "75001", "France", 48.8566, 2.3522,
        "Français", 8, "Restaurant test pour dev", "Review test"
    )
    
    # Lecture
    restos = read_restaurants()
    print("Restaurants en BDD:")
    for r in restos:
        print(r)
    
    # Mise à jour
    update_restaurant(restos[0]["id"], nom="Test Resto Modifié", note=9)
    
    # Lecture après update
    restos = read_restaurants()
    print("Après update:")
    for r in restos:
        print(r)
    
    # Suppression
    delete_restaurant(restos[0]["id"])
    
    # Lecture finale
    restos = read_restaurants()
    print("Après suppression:")
    for r in restos:
        print(r)

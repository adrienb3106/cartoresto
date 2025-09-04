import sys
import os
from datetime import datetime

# Ajouter backend/ au PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from db import get_connection


def insert_restaurant(nom, adresse, ville, note, description):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO restaurants (nom, adresse, ville, note, description)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (nom, adresse, ville, note, description))
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id


def get_restaurant(resto_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM restaurants WHERE id = %s", (resto_id,))
    resto = cursor.fetchone()
    conn.close()
    return resto


def update_restaurant(resto_id, new_note):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE restaurants SET note = %s WHERE id = %s"
    cursor.execute(sql, (new_note, resto_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected


def delete_restaurant(resto_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM restaurants WHERE id = %s", (resto_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected


def test_crud():
    print("Test INSERT")
    resto_id = insert_restaurant(
        "Test Resto",
        "123 Rue de Python",
        "Toulouse",
        7,
        "Restaurant inséré pour test CRUD"
    )
    print(f"Restaurant inséré avec id={resto_id}")

    print("\nTest UPDATE")
    update_restaurant(resto_id, 9)
    resto_updated = get_restaurant(resto_id)
    print(f"Après mise à jour : note={resto_updated['note']}")
    
    print("\nTest SELECT")
    resto = get_restaurant(resto_id)
    print(f"Récupéré : {resto}")

    print("\nTest DELETE")
    delete_restaurant(resto_id)
    resto_deleted = get_restaurant(resto_id)
    print(f"Après suppression, SELECT renvoie : {resto_deleted}")


if __name__ == "__main__":
    test_crud()

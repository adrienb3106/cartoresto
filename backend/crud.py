from db import get_connection
from models import Restaurant

def get_restaurants():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM restaurants")
    restos = cursor.fetchall()
    conn.close()
    return restos

def get_restaurant(resto_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM restaurants WHERE id = %s", (resto_id,))
    resto = cursor.fetchone()
    conn.close()
    return resto

def add_restaurant(resto: Restaurant):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO restaurants (nom, adresse, ville, note, description) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (resto.nom, resto.adresse, resto.ville, resto.note, resto.description))
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def update_restaurant(resto_id: int, new_note: int):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE restaurants SET note = %s WHERE id = %s"
    cursor.execute(sql, (new_note, resto_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

def delete_restaurant(resto_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM restaurants WHERE id = %s", (resto_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

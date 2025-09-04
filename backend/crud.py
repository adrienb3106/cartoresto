from db import get_connection

# ==========================
# Fonctions CRUD
# ==========================

# --- CREATE ---
def add_restaurant(nom, adresse, localisation, informations):
    """
    localisation : dict avec ville, code_postal, pays, latitude, longitude
    informations : dict avec category, note, description, review
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Ajouter localisation
    cursor.execute("""
        INSERT INTO localisation (ville, code_postal, pays, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
    """, (localisation['ville'], localisation.get('code_postal'),
          localisation.get('pays'), localisation.get('latitude'),
          localisation.get('longitude')))
    localisation_id = cursor.lastrowid

    # Ajouter informations
    cursor.execute("""
        INSERT INTO informations (category, note, description, review)
        VALUES (%s, %s, %s, %s)
    """, (informations.get('category'), informations.get('note'),
          informations.get('description'), informations.get('review')))
    informations_id = cursor.lastrowid

    # Ajouter restaurant
    cursor.execute("""
        INSERT INTO restaurants (nom, adresse, localisation_id, informations_id)
        VALUES (%s, %s, %s, %s)
    """, (nom, adresse, localisation_id, informations_id))
    restaurant_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return restaurant_id

# --- READ ---
def get_restaurants():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.nom, r.adresse,
               i.note, i.category, i.description, i.review,
               l.ville, l.code_postal, l.pays, l.latitude, l.longitude
        FROM restaurants r
        JOIN localisation l ON r.localisation_id = l.id
        JOIN informations i ON r.informations_id = i.id
    """)
    rows = cursor.fetchall()
    conn.close()

    # Reformatage pour le client
    result = []
    for r in rows:
        result.append({
            "id": r["id"],
            "nom": r["nom"],
            "adresse": r["adresse"],
            "localisation": {
                "ville": r["ville"],
                "code_postal": r["code_postal"],
                "pays": r["pays"],
                "latitude": r["latitude"],
                "longitude": r["longitude"]
            },
            "informations": {
                "note": r["note"],
                "category": r["category"],
                "description": r["description"],
                "review": r["review"]
            }
        })
    return result

def get_restaurant(restaurant_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, r.nom, r.adresse,
               i.note, i.category, i.description, i.review,
               l.ville, l.code_postal, l.pays, l.latitude, l.longitude
        FROM restaurants r
        JOIN localisation l ON r.localisation_id = l.id
        JOIN informations i ON r.informations_id = i.id
        WHERE r.id = %s
    """, (restaurant_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    # Reformater pour le client
    result = {
        "id": row["id"],
        "nom": row["nom"],
        "adresse": row["adresse"],
        "localisation": {
            "ville": row["ville"],
            "code_postal": row["code_postal"],
            "pays": row["pays"],
            "latitude": row["latitude"],
            "longitude": row["longitude"]
        },
        "informations": {
            "note": row["note"],
            "category": row["category"],
            "description": row["description"],
            "review": row["review"]
        }
    }
    return result

# --- UPDATE ---
def update_restaurant(resto_id, fields: dict):
    """
    Met à jour un restaurant avec les champs fournis.
    fields peut contenir des clés pour 'informations', 'localisation', ou des champs directs de 'restaurants'.
    Exemple :
    fields = {
        "nom": "Nouveau nom",
        "adresse": "Nouvelle adresse",
        "informations": {"note": 9, "category": "Fastfood"},
        "localisation": {"pays": "France", "ville": "Paris"}
    }
    """
    conn = get_connection()
    cursor = conn.cursor()

    # --- Table restaurants ---
    restaurant_fields = {k: v for k, v in fields.items() if k not in ["informations", "localisation"]}
    if restaurant_fields:
        set_clause = ", ".join([f"{k} = %s" for k in restaurant_fields])
        values = list(restaurant_fields.values()) + [resto_id]
        cursor.execute(f"UPDATE restaurants SET {set_clause} WHERE id = %s", values)

    # --- Table informations ---
    info_fields = fields.get("informations")
    if info_fields:
        set_clause = ", ".join([f"{k} = %s" for k in info_fields])
        values = list(info_fields.values()) + [resto_id]
        cursor.execute(f"""
            UPDATE informations
            SET {set_clause}
            WHERE id = (SELECT informations_id FROM restaurants WHERE id = %s)
        """, values)

    # --- Table localisation ---
    loc_fields = fields.get("localisation")
    if loc_fields:
        set_clause = ", ".join([f"{k} = %s" for k in loc_fields])
        values = list(loc_fields.values()) + [resto_id]
        cursor.execute(f"""
            UPDATE localisation
            SET {set_clause}
            WHERE id = (SELECT localisation_id FROM restaurants WHERE id = %s)
        """, values)

    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

# --- DELETE ---
def delete_restaurant(restaurant_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Récupérer les ids liés
    cursor.execute("SELECT localisation_id, informations_id FROM restaurants WHERE id=%s", (restaurant_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return 0
    localisation_id, informations_id = row

    # Supprimer le restaurant
    cursor.execute("DELETE FROM restaurants WHERE id=%s", (restaurant_id,))
    # Supprimer localisation et informations associées
    cursor.execute("DELETE FROM localisation WHERE id=%s", (localisation_id,))
    cursor.execute("DELETE FROM informations WHERE id=%s", (informations_id,))

    conn.commit()
    conn.close()
    return 1

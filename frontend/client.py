import requests

BASE_URL = "http://127.0.0.1:8000/restaurants"

def list_restaurants():
    resp = requests.get(BASE_URL)
    if resp.ok:
        print("\n--- Liste des restaurants ---")
        for r in resp.json():
            info = r.get("informations", {})
            loc = r.get("localisation", {})
            print(f"{r.get('id', '-')}: {r.get('nom', '-')}"
                  f" - {r.get('adresse', '-')}"
                  f" - Note: {info.get('note', '-')}"
                  f", Pays: {loc.get('pays', '-')}")
    else:
        print("Erreur:", resp.status_code, resp.text)
        
def read_restaurant(resto_id):
    resp = requests.get(f"{BASE_URL}/{resto_id}")
    if resp.ok:
        print("\n--- Information restaurant ---")
        r = resp.json()
        info = r.get("informations", {})
        loc = r.get("localisation", {})
        print(f"{r.get('nom', '-')}\n"
        f"{r.get('adresse', '-')}"
        f",{loc.get('ville', '-')}\n"
        f"- Note: {info.get('note', '-')}\n"
        f"- Description: {info.get('description', '-')}"
        )
    else:
        print("Erreur:", resp.status_code, resp.text)


def add_restaurant():
    nom = input("Nom: ")
    adresse = input("Adresse: ")
    ville = input("Ville: ")
    code_postal = input("Code postal: ")
    pays = input("Pays: ")
    category = input("Catégorie: ")
    note = int(input("Note (0-10): "))
    description = input("Description: ")

    resto = {
        "nom": nom,
        "adresse": adresse,
        "localisation": {
            "ville": ville,
            "code_postal": code_postal,
            "pays": pays,
            "latitude": 0.0,
            "longitude": 0.0
        },
        "informations": {
            "category": category,
            "note": note,
            "description": description,
            "review": None
        }
    }

    resp = requests.post(BASE_URL, json=resto)
    print(resp.json())

def update_restaurant():
    resto_id = input("ID du restaurant à modifier: ")

    print("Laissez vide pour ne pas modifier un champ.")
    nom = input("Nouveau nom: ")
    adresse = input("Nouvelle adresse: ")
    ville = input("Nouvelle ville: ")
    code_postal = input("Nouveau code postal: ")
    pays = input("Nouveau pays: ")
    note_input = input("Nouvelle note (0-10): ")
    category = input("Nouvelle catégorie: ")
    description = input("Nouvelle description: ")
    review = input("Nouvelle review: ")

    fields = {}

    # Champs de restaurants
    if nom: fields["nom"] = nom
    if adresse: fields["adresse"] = adresse

    # Champs localisation
    loc = {}
    if ville: loc["ville"] = ville
    if code_postal: loc["code_postal"] = code_postal
    if pays: loc["pays"] = pays
    if loc: fields["localisation"] = loc

    # Champs informations
    info = {}
    if note_input: info["note"] = int(note_input)
    if category: info["category"] = category
    if description: info["description"] = description
    if review: info["review"] = review
    if info: fields["informations"] = info

    if not fields:
        print("Aucun champ à mettre à jour.")
        return

    resp = requests.put(f"{BASE_URL}/{resto_id}", json=fields)
    if resp.ok:
        print("Restaurant mis à jour avec succès !")
    else:
        print("Erreur:", resp.status_code, resp.text)



def delete_restaurant():
    resto_id = int(input("ID du restaurant à supprimer: "))
    resp = requests.delete(f"{BASE_URL}/{resto_id}")
    print(resp.json())

def main():
    while True:
        print("\n--- Menu ---")
        print("1. Lister les restaurants")
        print("2. Ajouter un restaurant")
        print("3. Mettre à jour un restaurant")
        print("4. Supprimer un restaurant")
        print("5. Quitter")
        print("DEV : 6. Voir restaurant specifique.")

        choix = input("Choix: ")

        if choix == "1":
            list_restaurants()
        elif choix == "2":
            add_restaurant()
        elif choix == "3":
            update_restaurant()
        elif choix == "4":
            delete_restaurant()
        elif choix == "5":
            break
        elif choix == "6":
            choix_id = input("resto id : ")
            read_restaurant(choix_id)
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()

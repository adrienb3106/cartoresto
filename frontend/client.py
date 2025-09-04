import requests

BASE_URL = "http://127.0.0.1:8000"  # adresse de ton API FastAPI

def lister_restaurants():
    response = requests.get(f"{BASE_URL}/restaurants")
    if response.status_code == 200:
        restos = response.json()
        if not restos:
            print("Aucun restaurant trouvé.")
        else:
            for r in restos:
                print(f"{r['id']}: {r['nom']} ({r['ville']}) - Note: {r['note']}")
    else:
        print("Erreur :", response.status_code)

def ajouter_restaurant():
    nom = input("Nom du restaurant : ")
    adresse = input("Adresse : ")
    ville = input("Ville : ")
    note = int(input("Note (1-10) : "))
    description = input("Description : ")

    data = {
        "nom": nom,
        "adresse": adresse,
        "ville": ville,
        "note": note,
        "description": description
    }

    response = requests.post(f"{BASE_URL}/restaurants", json=data)
    if response.status_code == 200:
        print("Restaurant ajouté :", response.json())
    else:
        print("Erreur :", response.status_code, response.text)

def modifier_note():
    resto_id = int(input("ID du restaurant à modifier : "))
    note = int(input("Nouvelle note (1-10) : "))
    response = requests.put(f"{BASE_URL}/restaurants/{resto_id}", params={"note": note})
    if response.status_code == 200:
        print(response.json())
    else:
        print("Erreur :", response.status_code, response.text)

def supprimer_restaurant():
    resto_id = int(input("ID du restaurant à supprimer : "))
    response = requests.delete(f"{BASE_URL}/restaurants/{resto_id}")
    if response.status_code == 200:
        print(response.json())
    else:
        print("Erreur :", response.status_code, response.text)

def menu():
    while True:
        print("\n--- Menu Client CartoResto ---")
        print("1. Lister les restaurants")
        print("2. Ajouter un restaurant")
        print("3. Modifier la note d'un restaurant")
        print("4. Supprimer un restaurant")
        print("0. Quitter")

        choix = input("Choix : ")
        if choix == "1":
            lister_restaurants()
        elif choix == "2":
            ajouter_restaurant()
        elif choix == "3":
            modifier_note()
        elif choix == "4":
            supprimer_restaurant()
        elif choix == "0":
            break
        else:
            print("Choix invalide")

if __name__ == "__main__":
    menu()
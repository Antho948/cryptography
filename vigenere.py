import re

# Fonction pour répéter la clé à la longueur du texte
def generate_key(text, key):
    key = key.upper()
    repeated_key = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            repeated_key += key[key_index % len(key)]
            key_index += 1
        else:
            repeated_key += char
    return repeated_key

# Fonction de chiffrement Vigenère
def message_encrypt(text, key):
    encrypted = ""
    text = text.upper()
    key = generate_key(text, key)

    for i in range(len(text)):
        if text[i].isalpha():
            shift = (ord(text[i]) - ord('A') + ord(key[i]) - ord('A')) % 26
            encrypted += chr(shift + ord('A'))
        else:
            encrypted += text[i]
    return encrypted

# Fonction de déchiffrement Vigenère
def message_decrypt(text, key):
    decrypted = ""
    text = text.upper()
    key = generate_key(text, key)

    for i in range(len(text)):
        if text[i].isalpha():
            shift = (ord(text[i]) - ord(key[i]) + 26) % 26
            decrypted += chr(shift + ord('A'))
        else:
            decrypted += text[i]
    return decrypted

# Vérifie que le texte contient seulement des lettres
def get_valid_input(prompt):
    while True:
        user_input = input(prompt)
        if re.fullmatch(r"[A-Za-z]+", user_input):
            return user_input
        else:
            print("Veuillez entrer uniquement des lettres.")

# Programme principal
def main():
    boucle = True
    while boucle:
        print("\n--- Menu ---")
        print("1 - Chiffrer un message")
        print("2 - Déchiffrer un message")
        print("0 - Quitter")

        try:
            choice = int(input("Choix : "))
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            continue

        if choice == 1:
            message = get_valid_input("Message à chiffrer : ")
            key = get_valid_input("Clé : ")
            result = message_encrypt(message, key)
            print("Message chiffré :", result)

        elif choice == 2:
            message = get_valid_input("Message à déchiffrer : ")
            key = get_valid_input("Clé : ")
            result = message_decrypt(message, key)
            print("Message déchiffré :", result)

        elif choice == 0:
            print("Fin du programme.")
            boucle = False
        else:
            print("Choix invalide.")

# Exécution
main()


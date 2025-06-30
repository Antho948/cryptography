import math
from collections import Counter
import numpy as np
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


# Entropie
def calc_entropie(txt):
    total = len(txt)
    freq = Counter(txt)
    return -sum((f/total) * math.log2(f/total) for f in freq.values())

def calc_redondance(txt):
    h = calc_entropie(txt)
    hmax = math.log2(26)  # alphabet A-Z
    return 1 - (h / hmax)

def indice_coincidence(txt):
    n = len(txt)
    if n <= 1:
        return 0
    freq = Counter(txt)
    return sum(f*(f-1) for f in freq.values()) / (n*(n-1))


# Chiffrement de Hill
def hill(txt, cle):
    txt = txt.upper().replace(" ", "")
    n = cle.shape[0]
    while len(txt) % n != 0:
        txt += 'X'  # on complète

    res = ''
    for i in range(0, len(txt), n):
        bloc = txt[i:i+n]
        vect = np.array([[ord(c) - ord('A')] for c in bloc])
        chiffré = np.dot(cle, vect) % 26
        res += ''.join(chr(int(x[0]) + ord('A')) for x in chiffré)
    return res


# Chiffrement affine
def affine(txt, a, b):
    if math.gcd(a, 26) != 1:
        raise ValueError("a pas inversible mod 26")

    txt = txt.upper().replace(" ", "")
    out = ''
    for c in txt:
        if c.isalpha():
            x = ord(c) - ord('A')
            y = (a * x + b) % 26
            out += chr(y + ord('A'))
        else:
            out += c
    return out


# AES & RSA
# AES
def aes_enc(msg, key):
    c = AES.new(key, AES.MODE_CBC)
    ct = c.encrypt(pad(msg.encode(), AES.block_size))
    return base64.b64encode(c.iv + ct).decode()

def aes_dec(enc, key):
    d = base64.b64decode(enc)
    iv, ct = d[:16], d[16:]
    c = AES.new(key, AES.MODE_CBC, iv)
    return unpad(c.decrypt(ct), AES.block_size).decode()

# RSA
def gen_rsa():
    k = RSA.generate(2048)
    return k.export_key(), k.publickey().export_key()

def rsa_enc(msg, pub):
    k = RSA.import_key(pub)
    c = PKCS1_OAEP.new(k)
    return base64.b64encode(c.encrypt(msg.encode())).decode()

def rsa_dec(enc, priv):
    k = RSA.import_key(priv)
    c = PKCS1_OAEP.new(k)
    return c.decrypt(base64.b64decode(enc)).decode()

def stats(titre, texte):
    print(f"\n--- {titre} ---")
    print("Texte :", texte)
    print("Entropie :", round(calc_entropie(texte), 4))
    print("Redondance :", round(calc_redondance(texte), 4))
    print("Indice de coïncidence :", round(indice_coincidence(texte), 4))

def menu():
    print("\n==== Menu Chiffrement ====")
    print("1. Hill")
    print("2. Affine")
    print("3. AES")
    print("4. RSA")
    print("5. Quitter")
    choix = input("Choix (1-5) : ")
    return choix


def boucle_principale():
    cle_hill = np.array([[3, 3], [2, 5]])
    a_affine, b_affine = 5, 8
    k_aes = get_random_bytes(16)
    priv_rsa, pub_rsa = gen_rsa()

    while True:
        choix = menu()
        if choix == "5":
            print("Fin du programme.")
            break

        texte = input("Texte à chiffrer : ").replace(" ", "").upper()
        stats("Texte clair", texte)

        if choix == "1":
            try:
                chiffré = hill(texte, cle_hill)
                print("\nMéthode : Hill")
            except Exception as e:
                print("Erreur Hill :", e)
                continue

        elif choix == "2":
            try:
                chiffré = affine(texte, a_affine, b_affine)
                print("\nMéthode : Affine")
            except Exception as e:
                print("Erreur Affine :", e)
                continue

        elif choix == "3":
            try:
                chiffré = aes_enc(texte, k_aes)
                print("\nMéthode : AES")
                print("AES déchiffré :", aes_dec(chiffré, k_aes))
            except Exception as e:
                print("Erreur AES :", e)
                continue

        elif choix == "4":
            try:
                chiffré = rsa_enc(texte, pub_rsa)
                print("\nMéthode : RSA")
                print("RSA déchiffré :", rsa_dec(chiffré, priv_rsa))
            except Exception as e:
                print("Erreur RSA :", e)
                continue

        else:
            print("Choix invalide.")
            continue

        stats("Texte chiffré", chiffré)


# main

if __name__ == "__main__":
    boucle_principale()
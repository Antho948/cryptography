import re

# Variables
key = 0 #décalage
chiffre = []
text_chiffre=""
tab_chiffre=[]
text_chiffre=""
boucle = True
choice1 =0
first = True

def choice():
    global first, boucle
    choice2 = 0
    continuer = 2
    if first == False and boucle == True:
        print("choice2 different de 0 et boucle = True")
        while continuer !=0 and continuer != 1:
            continuer = int(input("Voulez-vous continuer ? (0=NON & 1=OUI) : "))
        if continuer == 0:
            boucle=False
            exit()
    while choice2 != 1 and choice2 != 2:
        choice2 = int(input("1 pour chiffrer et 2 pour déchiffrer : "))
    first=False
    return choice2

def entree():
    if choice1 == 1 :
        non_chiffre = input("Veuillez écrire un mot : ")
        while not re.fullmatch(r"[A-Za-z]+", non_chiffre):
            non_chiffre = input("Veuillez écrire un mot : ")
        return non_chiffre
    if choice1 == 2:
        chiffre = input("Veuillez écrire le mot chiffré : ")
        while not re.fullmatch(r"[A-Za-z]+", chiffre):
            chiffre = input("Veuillez écrire le mot chiffré : ")
            print(chiffre)
        return chiffre

def text2ascii(text):
    ascii = [ord(char) for char in text]
    return ascii

def decalage(text):
    if choice1 == 1:
        tab1_chiffre =[]
        for i in text:
            if 97 <= i <= 122:
                i = (i - 97 + key) % 26 + 97 # lettre minuscule
            
            elif 65 <= i <= 90:
                i = (i - 65 + key) % 26 + 65 # lettre majuscule

            else:
                i+=key
            tab1_chiffre.append(chr(i))
        return tab1_chiffre
    if choice1 == 2:
        tab1_dechiffre = []
        for i in text:
            if 97 <= i <= 122:  # lettre minuscule
                i = (i - 97 - key) % 26 + 97
            elif 65 <= i <= 90:  # lettre majuscule
                i = (i - 65 - key) % 26 + 65
            else:
                i -= key
            tab1_dechiffre.append(chr(i))
        return tab1_dechiffre

def tab2str(text):
    text_chiffre=""
    for i in text :
        text_chiffre += i
    return text_chiffre

def chiffrement(text):
    ascii_non_chiffre = text2ascii(text)
    tab_chiffre = decalage(ascii_non_chiffre)
    text_chiffre = tab2str(tab_chiffre)
    return text_chiffre
    
def dechiffrement(text):
    ascii_chiffre = text2ascii(text)
    tab_non_chiffre = decalage(ascii_chiffre)
    text_non_chiffre = tab2str(tab_non_chiffre)
    return text_non_chiffre

# main
while boucle == True:
    choice1 = choice()
    if choice1 == 1:
        non_chiffre = entree()
        key = int(input("Veuillez écrire votre clé de chiffrement : "))
        text_chiffre = chiffrement(non_chiffre)
        print("Voici le message chiffré : {0}".format(text_chiffre))

    if choice1 == 2:
        chiffre = entree()
        key = int(input("Veuillez écrire la clé que vous avez utilisez pour chiffrer : "))
        text_dechiffre = dechiffrement(chiffre)
        print("Voici le message déchiffré avec la clé de {0} : {1}".format(key, text_dechiffre)) 




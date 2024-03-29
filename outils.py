# Fichier fait par Francois Dufour Martel (2330346)

import random
import os
import time
from util import lire_historique_utilisateur, enregistrer_partie, lire_dictionnaires_mots

def choisirNom():
    while True:
        nom_entre = input("Veuillez entrer votre nom d'utilisateur: ")
        effacerConsole()
    
        if len(nom_entre) > 3 and nom_entre.isalpha():
            print(f"Bienvenue, {nom_entre}!\n\n")
            return nom_entre
        else:
            print("Votre nom est invalide!")
            continue

def choisirMot(mots):
    index = random.randrange(len(mots)-1)
    print(mots[index])
    return mots[index]

def effacerConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficherMot(lettres_trouvees, mot):
    txt = []
    for i in range(len(mot)):
        txt.append("_")

    for i in range(len(lettres_trouvees)):
        for j in range(len(mot)):
            if mot[j] == lettres_trouvees[i]:
                txt[j] = lettres_trouvees[i]
    
    print("Mot: " + " ".join(txt))


def afficherJeu(lettres_ratees, lettres_trouvees, mot):
    effacerConsole()
    afficherMot(lettres_trouvees, mot)
    print("Lettres trouvees: " + " ".join(lettres_trouvees))
    print("Lettres ratees: " + " ".join(lettres_ratees)+"\n") 

    parties_jouees = [
    ["   0   |", "       |", "       |"],
    ["   0   |", "   |   |", "       |"],
    ["   0   |", "  /|   |", "       |"],
    ["   0   |", "  /|\  |", "       |"],
    ["   0   |", "  /|\  |", "  /    |"],
    ["   0   |", "  /|\  |", "  / \  |"]
    ]

    partie_a_afficher = parties_jouees[len(lettres_ratees)-1] if len(lettres_ratees) > 0 else ["       |", "       |", "       |"]

    print("   +---+")
    print("   |   |")
    print("\n".join(partie_a_afficher))
    print("       |")
    print("==========")
    
def validerLettre(lettres_ratees, lettres_trouvees, mot):

    lettre = input("Entrez une lettre: ")

    if len(lettre) == 1 and lettre.isalpha():

        lettre = lettre.lower()

        if (lettre in lettres_ratees) or (lettre in lettres_trouvees):
            print("Cette lettre a déjà été essayée.")
        elif mot.find(lettre) == -1:
            lettres_ratees.append(lettre)
            afficherJeu(lettres_ratees, lettres_trouvees, mot)
        else:
            lettres_trouvees.append(lettre)
            afficherJeu(lettres_ratees, lettres_trouvees, mot)
    else:
        print("Vous devez entrer une lettre.")
    

def etatDeLaPartie(lettres_ratees, lettres_trouvees, mot, nom, temps_debut):
    temps = round(time.time()-temps_debut)

    partie_terminee = False

    if len(lettres_ratees) == 6:
        print(f"Dommage ! Le mot était {mot}.")
        partie_terminee = True
        
    elif len(lettres_trouvees) == len(set(mot)):
        print(f"Félicitations {nom} ! Vous avez deviné le mot {mot} en {temps} secondes et {len(lettres_ratees)} tentatives échouées.")
        partie_terminee = True
    
    if partie_terminee:
        input("Appuyez sur entrer pour continuer...")
        enregistrer_partie(nom, mot, len(lettres_trouvees) == len(set(mot)), temps)
        effacerConsole()

    return partie_terminee
    

def game(choix,nom):

    lettres_trouvees = []
    lettres_ratees = []
    fin_de_partie = False
    mot = choisirMot(lire_dictionnaires_mots()[["facile", "intermediaire", "difficile"][int(choix)-1]])

    afficherJeu(lettres_ratees, lettres_trouvees, mot)
    start = time.time()
    while not fin_de_partie:
        print(mot)
        validerLettre(lettres_ratees, lettres_trouvees, mot)
        fin_de_partie = etatDeLaPartie(lettres_ratees, lettres_trouvees, mot, nom, start)
        

def afficherHistorique(nom):
    effacerConsole()
    parties_jouees = lire_historique_utilisateur(nom)

    print("Historique des parties_jouees:")

    for i in range(len(parties_jouees)):
        victoire = "gagné" if parties_jouees[i]["resultat"] == True else "perdu"
        print("\t"+ parties_jouees[i]["mot"] + f" - {victoire} - " + str(parties_jouees[i]["duree"]) + " secondes")

    input("Appuyez pour continuer...")
    effacerConsole()
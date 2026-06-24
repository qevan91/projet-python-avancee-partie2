import collections
import matplotlib.pyplot as plt

author_trouve = False
title_trouve = False
chapter_trouve = False
compteur_chapitre = 0

paragraphes_mots = []
paragraphe_actuel = []

try:
    with open("data/Moby_Dick_Or_The_Whale_by_Herman_Melville.txt", "r", encoding="utf-8") as fichier:
        for ligne in fichier:

            # Extraction de l'Auteur
            if ligne.startswith("Author:") and not author_trouve:
                author = ligne.split("Author:")[1]
                author_trouve = True
                print("L'auteur est :", author)

            # Extraction du Titre
            if ligne.startswith("Title:") and not title_trouve:
                title = ligne.split("Title:")[1]
                title_trouve = True
                print("Le titre est :", title)

            # Détection du "CHAPTER 1."
            if ligne.startswith("CHAPTER 1."):
                if not chapter_trouve:
                    chapter = ligne.split("CHAPTER 1.")[1]
                    chapter_trouve = True
                    print("Le premier chapitre est :", chapter)

                # On incrémente le compteur
                compteur_chapitre += 1
                continue  # Passer à la ligne suivante

            # Détection de la fin du chapitre 1
            if compteur_chapitre == 2 and ligne.startswith("CHAPTER 2."):
                break

            # Traitement du corps du texte du chapitre 1
            if compteur_chapitre == 2:
                if ligne.strip() == "":
                    if paragraphe_actuel:
                        # On rassemble les lignes et on sépare les mots
                        texte_para = " ".join(paragraphe_actuel)
                        mots = texte_para.split()
                        if mots:
                            paragraphes_mots.append(len(mots))
                        paragraphe_actuel = []
                else:
                    # On accumule la ligne dans le paragraphe en cours
                    paragraphe_actuel.append(ligne.strip())

    # Gestion du dernier paragraphe si le fichier ne se termine pas par une ligne vide
    if paragraphe_actuel:
        texte_para = " ".join(paragraphe_actuel)
        mots = texte_para.split()
        if mots:
            paragraphes_mots.append(len(mots))

    # Arrondir le nombre de mots à la dizaine inférieure
    longueurs_arrondies = [(n // 10) * 10 for n in paragraphes_mots]

    # Compter le nombre de paragraphes ayant la même longueur et trier du plus court au plus long
    frequences = collections.Counter(longueurs_arrondies)
    frequences_triees = sorted(frequences.items())

    # Affichage des résultats textuels
    print("\nDistribution des longueurs de paragraphes")
    for longueur, nb_paragraphes in frequences_triees:
        print(f"Paragraphes d'environ {longueur} mots : {nb_paragraphes}")

    # Création du graphique de distribution
    categories = [str(item[0]) for item in frequences_triees]
    valeurs = [item[1] for item in frequences_triees]

    plt.bar(categories, valeurs, color='skyblue', edgecolor='black', alpha=0.8)
    plt.xlabel('Nombre de mots (arrondi à la dizaine)')
    plt.ylabel('Nombre de paragraphes')
    plt.title('Distribution de la longueur des paragraphes (Chapitre 1)')
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Sauvegarde et affichage du graphique
    plt.tight_layout()
    plt.savefig('distribution_paragraphes.png')
    print("\nLe graphique a été généré et sauvegardé avec succès sous le nom 'distribution_paragraphes.png'.")

except FileNotFoundError:
    print("Erreur : Le fichier spécifié est introuvable. Vérifiez le chemin d'accès.")
except PermissionError:
    print("Erreur : Droits insuffisants pour lire ce fichier.")
except Exception as e:
    print(f"Une erreur imprévue est survenue lors de la lecture : {e}")
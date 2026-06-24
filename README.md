# Analyse Documentaire et Traitement d'Images - Moby Dick

Ce projet industriel implémente un pipeline d'ingestion, d'analyse statistique et de traitement graphique basé sur le roman *Moby Dick* d'Herman Melville. L'objectif principal est d'extraire des métriques textuelles ciblées, de manipuler des ressources visuelles dynamiques et de compiler ces indicateurs au sein d'un livrable d'ingénierie automatisé au format Word (`.docx`).

L'ensemble de l'architecture logicielle respecte les paradigmes de programmation défensive, les standards de style PEP 8, de documentation PEP 257 (format Google) et applique le principe de responsabilité unique (SRP).

---

## Architecture des Fichiers

L'organisation des modules et des ressources sur le disque est structurée de la manière suivante :

```text
.
├── data/
│   ├── Moby_Dick_Or_The_Whale_by_Herman_Melville.txt
│   ├── logo.png
│   └── image_finale.jpg
├── src/
│   ├── extract.py
│   ├── image_processing.py
│   ├── docs.py
│   └── main.py
├── tests/
│   └── test_image_processing.py
├── distribution_paragraphes.png
├── requirements.txt
└── Rapport_Livre.docx
```

---

## Description des Modules

### 1. Extraction et Analyse Statistique (`src/extract.py`)
Ce module est responsable de la lecture et du parsing du fichier texte brut.
* **Extraction des Métadonnées** : Isole de façon programmatique l'auteur et le titre de l'œuvre.
* **Segmentation et Filtrage** : Localise le premier chapitre (*Loomings*) pour compter les mots et évaluer la structure morphologique des paragraphes.
* **Visualisation** : Génère un graphique de distribution des longueurs de paragraphes (arrondies à la dizaine la plus proche) à l'aide de Matplotlib sous le nom `distribution_paragraphes.png`.

### 2. Traitement Numérique d'Images (`src/image_processing.py`)
Ce module encapsule l'ensemble de la logique de traitement graphique via la bibliothèque Pillow.
* **Téléchargement Asynchrone** : Récupère une illustration depuis les serveurs Wikimedia avec une gestion stricte des timeouts et des agents utilisateurs.
* **Transformation Géométrique** : Effectue un recadrage (crop) de 10% sur les bordures périphériques puis applique un redimensionnement (resize) normalisé en 800x600 pixels.
* **Composition Graphique** : Convertit le logo de l'entreprise en niveaux de gris, lui applique une rotation de 45° et réalise un masquage alpha pour l'incruster de manière transparente sur l'image finale (`data/image_finale.jpg`).

### 3. Automatisation Documentaire (`src/docs.py`)
Ce sous-système gère la création du livrable professionnel final à l'aide de `python-docx`.
* **Page de Garde Professionnelle** : Agence harmonieusement le titre de l'œuvre, l'illustration traitée, le nom de l'auteur original ainsi que l'identité du contributeur.
* **Mise en Page Typographique** : Utilise des variations d'en-têtes enrichis (gras, italique) et insère des sauts de page stricts pour isoler les sections.
* **Reporting Analytique** : Intègre le graphique de distribution et compile les statistiques clés (volume global, étendue des paragraphes, moyenne pondérée) au sein d'une synthèse technique descriptive.

### 4. Orchestrateur Central (`src/main.py`)
Point d'entrée névralgique de l'application. Il pilote l'exécution du pipeline de bout en bout sous forme de sous-processus isolés, intercepte les codes de retour non nuls et centralise la journalisation des erreurs pour garantir l'intégrité des traitements.

---

## Directives d'Installation

1. Assurez-vous de disposer d'un interpréteur Python (version 3.8 ou supérieure).

2. Clonez le dépôt et créez un environnement virtuel isolé afin d'éviter tout conflit de paquets :

```bash
python -m venv .venv
```

Activer l'environnement virtuel sur Linux :
```Bash
source .venv/bin/activate  
```

Activer l'environnement virtuel sur Windows
````bash
.venv\Scripts\activate
````

3. Installez l'ensemble des dépendances figées du projet via le fichier de description des prérequis :

```bash
pip install -r requirements.txt
```

---

## Manuel d'Utilisation

### Exécution du Pipeline Complet
Pour déclencher l'ensemble de la chaîne de traitement (extraction, imagerie et compilation Word), exécutez la commande suivante depuis la racine du projet :

```bash
python src/main.py
```

L'orchestrateur affichera les logs d'exécution de chaque étape en temps réel. Une fois l'exécution terminée, le fichier final `Rapport_Livre.docx` sera généré à la racine.

### Exécution Intermédiaire (Mode Unitaire)
Chaque module étant autonome, vous pouvez tester unitairement un comportement particulier si nécessaire :

```bash
python src/extract.py
python src/image_processing.py
python src/docs.py
```

---

## Validation et Robustesse du Code

Le projet intègre une suite de tests unitaires automatiques validant la logique métier sans dépendance externe (isolation complète via simulacres ou *mocks*). Les requêtes HTTP et l'accès au disque y sont simulés pour garantir la reproductibilité des validations.

Pour lancer la suite de tests unitaires, utilisez la commande suivante :

```bash
python -m unittest discover -s tests
```
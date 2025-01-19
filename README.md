# Tableau de bord en Python

## Description
Ce projet est un tableau de bord interactif conçu en Python, permettant de visualiser et d'analyser des données de manière intuitive et efficace. Il est construit à l'aide de bibliothèques puissantes comme Dash, Plotly et Pandas.

## Fonctionnalités
- Une Carte du monde interactive : Visualisation des données sur la carte du monde avec les données sur les médailles gagnés de chaque pays, ainsi que leur classement.
- Un Histogramme qui représente la répartition des athlètes en fonction de leurs âge dans la discipline sélectionnée.

## Prérequis
- Python 3.12.6 ou une version ultérieure
- Bibliothèques Python suivantes :
  - dash
  - dash_bootstrap_components
  - kaggle
  - plotly
  - pandas
  - folium

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/gregoirelefevre/data_project
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Kaggle :
   ```bash
   Faire bien attention à mettre le fichier kaggle.json avec vos identifiants dans .kaggle sur votre machine. 
   Puis appuyer sur la touche 'y' pour lancer le programme. 
   La touche 'n' permet normalement de créer le fichier kaggle.json avec vos identifiants mais il est préférable que le fichier soit déjà présent. 
   Le programme prend de toute façon le jeu de données en mode local par défaut si le requête API ne marche pas. 
   
   voir (https://www.kaggle.com/docs/api) pour plus d'information.
   ```

## Utilisation
1. Lancez l'application :
   ```bash
   python main.py
   ```
2. Cela ouvre normalement votre navigateur automatiquement à l'adresse suivante :
   ```
   http://127.0.0.1:8050/
   ```

## Structure du projet
**.**
- **assets/**                  # Contient le style.css de notre site
- **data/**                    # Données 
  - **local/**                 # Données locales 
  - **raw/**                   # Données brutes d'entrée
  - **countries.geojson**      # Fichier GeoJSON utilisé pour les cartes
- **src/**                     # Code source principal
  - **__pycache__/**           # Cache Python
  - **dashboard.py**           # Script pour le tableau de bord
  - **cleandata.py**           # Nettoyage des données
  - **utils/**                 # Scripts utilitaires
    - **get_dataset.py**       # Récupération des données
- **.gitignore**               # Fichiers à ignorer par Git
- **folium_map.html**          # Carte générée avec Folium
- **main.py**                  # Script principal du projet
- **README.md**                # Documentation du projet
- **requirements.txt**         # Dépendances nécessaires
- **video.mp4**                # Vidéo explicative du projet

## Fichier GeoJSON
Ce fichier contient des coordonnées qui nous permet de tracer les frontières sur notre carte du monde. 

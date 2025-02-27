# Scraper d'Images Google

Ce projet permet d'automatiser la recherche et le téléchargement d'images depuis Google Images en se basant sur des mots-clés spécifiques. Il identifie également les correspondances texte/image et visite les sites sources pour extraire des images contenant des attributs alt spécifiés.

## Fonctionnalités

- 🔍 Recherche automatique sur Google Images
- 📸 Capture d'écran des résultats avec mise en évidence des paires image/texte
- 🌐 Visite des sites sources des images
- 📥 Téléchargement des images avec attributs alt spécifiques
- 📊 Génération de rapports CSV

## Prérequis

- Python 3.6+
- Firefox (navigateur)
- Geckodriver (pilote pour Selenium)

## Installation

1. **Clonez ou téléchargez ce dépôt**

2. **Installez les dépendances Python**

   ```bash
   pip install -r requirements.txt
   ```

3. **Téléchargez Geckodriver**
   
   - Rendez-vous sur [la page de téléchargement de Geckodriver](https://github.com/mozilla/geckodriver/releases)
   - Téléchargez la version compatible avec votre système
   - Décompressez l'exécutable et placez-le dans webdriver (ou modifiez le chemin dans `config.py`)

4. **Créez la structure de dossiers**

   Le programme créera automatiquement les dossiers nécessaires, mais vous devez vous assurer que le dossier data existe avec un fichier `search_queries.csv` à l'intérieur.

## Configuration

1. **Ouvrez le fichier `config.py`** pour ajuster les chemins si nécessaire

2. **Préparez votre fichier de requêtes CSV**

   Créez un fichier `search_queries.csv` dans le dossier data avec la structure suivante :
   ```
   query,alt_attribute
   chaussures de sport,chaussure
   montres connectées,montre
   ```

## Utilisation

1. **Lancez le script principal**

   ```bash
   python src/main.py
   ```

2. **Résultats générés**

   - **Images** : Les captures d'écran des résultats Google et les images téléchargées se trouvent dans le dossier images
   - **Rapports** : Les fichiers CSV contenant les données extraites sont dans le dossier reports

## Structure des fichiers CSV

Pour chaque requête de recherche, vous devez fournir :
- **query** : Le terme de recherche pour Google Images
- **alt_attribute** : Le mot-clé à rechercher dans l'attribut alt des images sur les sites visités

## Dépannage

- **Erreur de pilote** : Vérifiez que le chemin vers `geckodriver.exe` est correct dans `config.py`
- **Erreurs de navigation** : Ajustez les délais (`time.sleep()`) si nécessaire pour les sites plus lents
- **Aucun résultat** : Vérifiez le format de votre fichier CSV et les termes de recherche

## Remarques

- Respectez les conditions d'utilisation de Google et des sites visités
- Le scraping intensif peut entraîner une limitation temporaire de votre accès à Google
- Certains sites peuvent bloquer l'accès automatisé via Selenium

---

*Note: Ce script est fourni à des fins éducatives uniquement. L'utilisation de scrapers doit respecter les conditions d'utilisation des sites concernés.*
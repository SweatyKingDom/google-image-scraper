import os

# Chemins d'accès aux fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../data')
OUTPUT_DIR = os.path.join(BASE_DIR, '../output')
SEARCH_QUERIES_FILE = os.path.join(DATA_DIR, 'search_queries.csv')
IMAGES_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'images')
SCREENSHOTS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'screenshots')
REPORTS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'reports')

# Configuration du navigateur
WEBDRIVER_PATH = r'C:\\webdriver\\geckodriver.exe'
FIREFOX_OPTIONS = {
    "user_agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)"
}

# Configuration des images
MIN_IMAGE_SIZE_BYTES = 10000  # Taille minimale en octets (10 Ko par défaut)
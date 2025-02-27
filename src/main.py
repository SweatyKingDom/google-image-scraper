import os
import time
import csv
import random
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from utils.browser import initialize_browser
from utils.image_utils import read_search_queries, download_image
# Importer la configuration
from config import WEBDRIVER_PATH, IMAGES_OUTPUT_DIR, REPORTS_OUTPUT_DIR, SEARCH_QUERIES_FILE

# Utiliser le chemin absolu de la configuration
path = WEBDRIVER_PATH

# Utiliser les dossiers depuis la configuration
img_dir = IMAGES_OUTPUT_DIR
files_dir = REPORTS_OUTPUT_DIR
img_inside_dir = IMAGES_OUTPUT_DIR

# Créer les dossiers nécessaires s'ils n'existent pas
for directory in [img_dir, files_dir, img_inside_dir]:
    os.makedirs(directory, exist_ok=True)
    print(f"Dossier vérifié : {directory}")

service = Service(executable_path=path)
firefox_options = Options()
firefox_options.set_preference("general.useragent.override", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)")

driver = initialize_browser(service, firefox_options)

data_for_csv = []
processed_texts = set()
sites_to_visit = []

# Utiliser le chemin absolu pour le CSV
print(f"Tentative de lecture du CSV depuis : {SEARCH_QUERIES_FILE}")
search_queries = read_search_queries(SEARCH_QUERIES_FILE)

# Si search_queries est vide, afficher un message d'erreur
if not search_queries:
    print(f"ERREUR: Aucune requête n'a été trouvée dans le fichier {SEARCH_QUERIES_FILE}")
    driver.quit()
    exit(1)
    
def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"rgb({r}, {g}, {b})"

# Fonction principale pour traiter une requête
def process_search_query(query_data):
    global data_for_csv, processed_texts, sites_to_visit
    
    # Réinitialiser les listes pour chaque nouvelle requête
    data_for_csv = []
    processed_texts = set()
    sites_to_visit = []
    
    query_term = query_data['query']
    alt_keyword = query_data.get('alt_attribute', '')
    
    print(f"\n\n==== Traitement de la requête : {query_term} (alt: {alt_keyword}) ====\n")
    
    try:
        # Construire l'URL de recherche Google
        search_url = f"https://www.google.com/search?q={query_term.replace(' ', '+')}"
        driver.get(search_url)
        print(f"Page de recherche Google ouverte pour: {query_term}")
        
        # Cliquer sur l'onglet Images
        wait = WebDriverWait(driver, 10)
        images_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='IMAGES']"))
        )
        print("Bouton IMAGES trouvé")
        images_link.click()
        print("Clic sur le bouton IMAGES effectué")
        
        time.sleep(3)
        
        # Traiter les éléments de la page
        divs_with_spans = driver.find_elements(By.XPATH, "//div[.//span]")
        print(f"Nombre de divs avec spans trouvées : {len(divs_with_spans)}")
        
        for i, div in enumerate(divs_with_spans):
            try:
                span = div.find_element(By.TAG_NAME, "span")
                
                if span.is_displayed():
                    span_text = span.text.strip()
                    if not span_text:
                        continue
                    
                    if span_text in processed_texts:
                        print(f"Texte déjà traité, ignoré: {span_text}")
                        continue
                    
                    processed_texts.add(span_text)
                        
                    try:
                        tr_parent = driver.execute_script("return arguments[0].closest('tr')", span)
                        if tr_parent:
                            prev_tr = driver.execute_script("return arguments[0].previousElementSibling", tr_parent)
                            if prev_tr:
                                img = prev_tr.find_element(By.TAG_NAME, "img")
                                
                                parent_link = driver.execute_script("return arguments[0].closest('a')", img)
                                if parent_link:
                                    site_url = parent_link.get_attribute("href")
                                    if site_url and len(sites_to_visit) < 4:  
                                        sites_to_visit.append({
                                            "url": site_url,
                                            "text": span_text,
                                            "index": i,
                                            "query": query_term,
                                            "alt_keyword": alt_keyword
                                        })
                                
                                color = generate_random_color()
                                
                                driver.execute_script(f"""
                                    arguments[0].style.border = '2px solid {color}';
                                    arguments[0].style.padding = '1px';
                                    arguments[0].style.backgroundColor = 'rgba({color.replace("rgb(", "").replace(")", "")}, 0.3)';
                                """, span)
                                
                                driver.execute_script(f"""
                                    arguments[0].style.border = '2px solid {color}';
                                    arguments[0].style.padding = '1px';
                                """, img)
                                
                                print(f"Paire {i+1} encadrée avec la couleur {color}")
                                
                                data_for_csv.append({
                                    'index': i,
                                    'span_text': span_text
                                })
                        
                    except Exception as e:
                        print(f"Erreur lors de la recherche de l'image pour le span {i}: {e}")
                    
            except Exception as e:
                print(f"Impossible de traiter la div {i}: {e}")
        
        time.sleep(1)
        
        # Prendre une capture d'écran
        query_slug = query_term.lower().replace(' ', '_')
        screenshot_path = os.path.join(img_dir, f"{query_slug}_paires_encadrees_{int(time.time())}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Capture d'écran avec paires encadrées enregistrée : {screenshot_path}")
        
        # Sauvegarder les données dans un fichier CSV
        csv_path = os.path.join(files_dir, f"{query_slug}_span_data_{int(time.time())}.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['index', 'span_text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data_for_csv:
                writer.writerow(row)
        print(f"Données sauvegardées dans : {csv_path}")
        print(f"Nombre d'éléments uniques trouvés : {len(data_for_csv)}")
        
        # Visiter les sites trouvés
        print(f"\nVisite des {len(sites_to_visit)} premiers sites pour la requête {query_term}:")
        
        for site_info in sites_to_visit:
            try:
                url = site_info['url']
                alt_keyword = site_info['alt_keyword']
                print(f"\nNavigation vers : {url}")
                
                driver.get(url)
                time.sleep(3)  

                site_screenshot = os.path.join(img_dir, f"{query_slug}_site_{site_info['index']}_{int(time.time())}.png")
                driver.save_screenshot(site_screenshot)
                print(f"Capture d'écran du site enregistrée : {site_screenshot}")
                
                xpath_query = f"//img[contains(translate(@alt, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{alt_keyword.lower()}')]"
                target_images = driver.find_elements(By.XPATH, xpath_query)
                print(f"Nombre d'images avec '{alt_keyword}' dans l'attribut alt : {len(target_images)}")
                
                for j, target_img in enumerate(target_images):
                    try:
                        img_src = target_img.get_attribute("src")
                        img_alt = target_img.get_attribute("alt") or "sans_alt"
                        
                        img_path = download_image(
                            img_src, 
                            img_inside_dir, 
                            f"{query_slug}_site_{site_info['index']}_{alt_keyword}_{j}"
                        )
                        
                        if img_path:
                            print(f"Image {alt_keyword} téléchargée : {img_path}, Alt: {img_alt}")
                            
                    except Exception as e:
                        print(f"Erreur lors du traitement de l'image {alt_keyword} {j} : {e}")
                
            except Exception as e:
                print(f"Erreur lors de la visite du site {site_info['url']} : {e}")
        
        return True
    except Exception as e:
        print(f"Erreur lors du traitement de la requête {query_term} : {e}")
        return False

try:
    for query_data in search_queries:
        process_search_query(query_data)
        time.sleep(2) 
    
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
    
finally:
    time.sleep(5)
    driver.quit()
    print("Navigateur fermé")
import os
import csv
import random
import time
import requests
from config import MIN_IMAGE_SIZE_BYTES

def read_search_queries(csv_file):
    queries = []
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                queries.append({
                    'query': row['query'],
                    'alt_attribute': row['alt_text']  
                })
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
    return queries

def write_results_to_csv(results, output_file):
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['index', 'span_text', 'image_path']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier CSV : {e}")


def download_image(url, folder, prefix):
    """
    Télécharge une image à partir d'une URL et la sauvegarde dans le dossier spécifié
    si sa taille est supérieure à la taille minimale configurée.
    
    Args:
        url (str): L'URL de l'image à télécharger
        folder (str): Le chemin du dossier où sauvegarder l'image
        prefix (str): Préfixe pour le nom de fichier
        
    Returns:
        str: Le chemin du fichier sauvegardé ou None en cas d'erreur ou si l'image est trop petite
    """
    try:
        if not url or not url.startswith('http'):
            print(f"URL invalide: {url}")
            return None
        
        head_response = requests.head(url, timeout=5)
        
        content_length = head_response.headers.get('Content-Length')
        
        if content_length is not None:
            image_size = int(content_length)
            print(f"Taille de l'image: {image_size} octets")
            
            if image_size < MIN_IMAGE_SIZE_BYTES:
                print(f"Image ignorée car trop petite ({image_size} octets < {MIN_IMAGE_SIZE_BYTES} octets)")
                return None
        else:
            print("Impossible de déterminer la taille de l'image à l'avance")
        
        img_name = f"{prefix}_{int(time.time())}_{random.randint(1000, 9999)}.jpg"
        img_path = os.path.join(folder, img_name)
        
        response = requests.get(url, stream=True, timeout=5)
        if response.status_code == 200:
            if content_length is None:
                image_data = response.content
                image_size = len(image_data)
                
                if image_size < MIN_IMAGE_SIZE_BYTES:
                    print(f"Image ignorée car trop petite ({image_size} octets < {MIN_IMAGE_SIZE_BYTES} octets)")
                    return None
                
                with open(img_path, 'wb') as f:
                    f.write(image_data)
            else:
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                    
            print(f"Image sauvegardée : {img_path} ({image_size} octets)")
            return img_path
        else:
            print(f"Échec du téléchargement : {response.status_code}")
            return None
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")
        return None
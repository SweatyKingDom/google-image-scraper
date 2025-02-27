from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time

def initialize_browser(service, options):
    """
    Initialise et renvoie une instance du navigateur Firefox
    
    Args:
        service: Instance Service pour Firefox
        options: Options de configuration du navigateur
        
    Returns:
        WebDriver: Instance du navigateur Firefox
    """
    try:
        driver = webdriver.Firefox(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Erreur lors de l'initialisation du navigateur: {e}")
        raise

# def accept_cookies(driver):
#     """
#     Tente d'accepter les cookies sur la page actuelle
    
#     Args:
#         driver: L'instance WebDriver active
        
#     Returns:
#         bool: True si les cookies ont été acceptés, False sinon
#     """
#     cookie_button_selectors = [
#         "button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
#         "button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accepter')]",
#         "button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cookies')]",
#         "a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
#         "a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accepter')]",
        
#         "//*[@id='accept-cookies']",
#         "//*[@id='cookie-accept']",
#         "//*[@id='cookie-consent-accept']",
#         "//*[@class='cookie-accept']",
#         "//*[@class='accept-cookies']",
        
#         "//button[contains(@class, 'cookie')]",
#         "//a[contains(@class, 'cookie')]"
#     ]
    
#     for selector in cookie_button_selectors:
#         try:
#             cookie_button = WebDriverWait(driver, 3).until(
#                 EC.element_to_be_clickable((By.XPATH, selector))
#             )
#             cookie_button.click()
#             print("Bouton de cookies accepté")
#             time.sleep(1)  # Petit délai après avoir cliqué
#             return True
#         except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
#             continue
    
#     print("Aucun bouton de cookies trouvé ou cliquable")
#     return False
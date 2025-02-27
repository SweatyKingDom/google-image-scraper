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
# Importations des modules
import csv
import datetime
import re
import time
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                       StaleElementReferenceException,
                                       TimeoutException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def wait_for_element(driver, by, value, timeout=20, retries=3):
    for attempt in range(retries):
        try:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.visibility_of_element_located((by, value)))
            return element
        except (StaleElementReferenceException, TimeoutException):
            print(f"Tentative {attempt + 1}/{retries} échouée pour localiser l'élément {value}")
            if attempt == retries - 1:
                raise
            time.sleep(1)

# Récupération des inputs utilisateur avec valeurs par défaut
specialite_input = input("Spécialité médicale (défaut: médecin généraliste) : ") or "médecin généraliste"
localisation_input = input("Localisation (défaut: 75013) : ") or "75013"
nombre_max_input = input("Nombre maximum de résultats (défaut: 3) : ") or "3"
nombre_max = int(nombre_max_input)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.doctolib.fr")

try:
    refuse_button = wait_for_element(driver, By.ID, "didomi-notice-disagree-button")
    refuse_button.click()
    print("Bouton de refus des cookies cliqué")
except (TimeoutException, StaleElementReferenceException):
    print("Le bouton de refus des cookies n'a pas été trouvé.")
time.sleep(2)

try:
    specialite_field = wait_for_element(driver, By.CSS_SELECTOR, "input.searchbar-input.searchbar-query-input")
    specialite_field.clear()
    specialite_field.send_keys(specialite_input)
    print(f"Spécialité médicale saisie : {specialite_input}")
    
    first_specialite_suggestion = wait_for_element(driver, By.CSS_SELECTOR, "ul#search-query-input-results-container li:first-child button.searchbar-result")
    first_specialite_suggestion.click()
    print("Première suggestion de spécialité sélectionnée")
    
except (TimeoutException, StaleElementReferenceException):
    print("Erreur lors de la saisie ou sélection de la spécialité")
    driver.quit()
    exit()

try:
    place_field = wait_for_element(driver, By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input")
    place_field.clear()
    place_field.send_keys(localisation_input)
    time.sleep(1)
    
    # Sélection de la deuxième suggestion de localisation car la premiere est "Autour de moi"
    second_place_suggestion = wait_for_element(driver, By.CSS_SELECTOR, "ul#search-place-input-results-container li:nth-child(2) button.searchbar-result")
    second_place_suggestion.click()
    print(f"Deuxième suggestion de localisation sélectionnée : {localisation_input}")
    
except (TimeoutException, StaleElementReferenceException):
    print("Erreur lors de la saisie ou sélection de la localisation")
    driver.quit()
    exit()

try:
    search_button = wait_for_element(driver, By.CSS_SELECTOR, "button.searchbar-submit-button")
    search_button.click()
    print("Recherche soumise")
except (TimeoutException, StaleElementReferenceException):
    print("Le bouton de recherche n'a pas été trouvé.")
    driver.quit()
    exit()

print("Attente des résultats de recherche...")
time.sleep(5)

# Vérification de la page de résultats
place_value = driver.find_element(By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input").get_attribute("value")
if ("search" in driver.current_url or place_value in driver.current_url) and place_value in driver.current_url:
    result_url = driver.current_url
    print(f"Page de résultats chargée avec succès. URL sauvegardée : {result_url}")
else:
    print("La page de résultats ne semble pas s'être chargée correctement")
    print(driver.current_url)
    driver.quit()
    exit()

# Récupération des cartes de praticiens
try:
    cards = driver.find_elements(By.CSS_SELECTOR, "div.dl-search-result")
    print(f"Nombre total de cartes trouvées : {len(cards)}")
    
    # Limiter le nombre de cartes selon l'input utilisateur
    if len(cards) > nombre_max:
        cards = cards[:nombre_max]
        print(f"Limitation à {nombre_max} cartes comme demandé")
    
    # Récupération des liens et navigation sur chaque page de praticien
    for index, card in enumerate(cards):
        try:
            # Récupérer le lien du praticien
            link = card.find_element(By.CSS_SELECTOR, "a.dl-search-result-name").get_attribute("href")
            print(f"Navigation vers le praticien {index+1}/{len(cards)} : {link}")
            
            # Ouvrir la page du praticien
            driver.get(link)
            time.sleep(3)  # Attendre le chargement de la page
            
            # Faire quelque chose sur la page du praticien (à compléter)
            print(f"Page du praticien {index+1} chargée")
            
            # Retour à la page de résultats sauf pour le dernier praticien
            if index < len(cards) - 1:
                print("Retour à la page de résultats...")
                driver.get(result_url)
                time.sleep(3)  # Attendre le rechargement de la page de résultats
        
        except NoSuchElementException:
            print(f"Impossible de récupérer le lien pour le praticien {index+1}")
            continue
            
except NoSuchElementException:
    print("Aucune carte de praticien trouvée sur la page")
finally:
    driver.quit()
    print("Navigateur fermé")
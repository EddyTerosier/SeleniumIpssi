from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://doctolib.fr/")

wait = WebDriverWait(driver, 10)

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input")))

place_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input")))

place_input.clear()
place_input.send_keys("75013")

wait.until(EC.text_to_be_present_in_element_value((By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input"), "75013"))

place_input.send_keys(Keys.ENTER)

time.sleep(10)

total_results = driver.find_element(By.CSS_SELECTOR, "div[data-test='total-number-of-results']")

driver.quit()
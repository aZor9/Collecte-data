from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.centre-commercial.fr/carrefour-st-jean/boutiques/"
output_dir = Path(__file__).resolve().parent / "resultat"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "h2_titles.txt"

driver = webdriver.Chrome()
try:
    driver.get(url)

    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.boutique-card h2.custom-h2"))
    )

    h2_elements = driver.find_elements(By.CSS_SELECTOR, "a.boutique-card h2.custom-h2")
    titles = [element.text.strip() for element in h2_elements if element.text.strip()]

    with open(output_file, "w", encoding="utf-8") as file:
        for title in titles:
            file.write(f"{title}\n")

    print(f"{len(titles)} titres H2 enregistres dans: {output_file}")
finally:
    driver.quit()

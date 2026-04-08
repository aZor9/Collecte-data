from datetime import datetime
from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"


def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument(f"--user-agent={USER_AGENT}")
    return webdriver.Chrome(options=options)

url = "https://www.centre-commercial.fr/carrefour-st-jean/boutiques/"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = Path(__file__).resolve().parent / "resultat" / "script_h2"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"h2_titles_{timestamp}.txt"

driver = build_driver()
try:
    driver.get(url)
    time.sleep(3)

    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.boutique-card h2.custom-h2"))
    )

    h2_elements = driver.find_elements(By.CSS_SELECTOR, "a.boutique-card h2.custom-h2")
    titles = [element.text.strip() for element in h2_elements if element.text.strip()]

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Collecte des titres boutiques\n")
        file.write(f"Source: {url}\n")
        file.write(f"Date: {timestamp}\n")
        file.write(f"Nombre de titres: {len(titles)}\n\n")
        for title in titles:
            file.write(f"{title}\n")

    print(f"{len(titles)} titres H2 enregistres dans: {output_file}")
finally:
    driver.quit()

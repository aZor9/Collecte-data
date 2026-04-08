from datetime import datetime
from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"


def build_driver() -> webdriver.Chrome:
	options = Options()
	options.add_argument(f"--user-agent={USER_AGENT}")
	return webdriver.Chrome(options=options)

driver = build_driver()
driver.get("https://www.centre-commercial.fr/carrefour-st-jean/boutiques/")
time.sleep(3)

title = driver.title
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = Path(__file__).resolve().parent / "resultat" / "script_title"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"title_{timestamp}.txt"

with open(output_file, "w", encoding="utf-8") as file:
	file.write(f"Titre de la page: {title}\n")

print(f"Titre récupéré: {title}")
print(f"Résultat enregistré dans: {output_file}")

driver.quit()
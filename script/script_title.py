from selenium import webdriver
from pathlib import Path

driver = webdriver.Chrome()
driver.get("https://www.centre-commercial.fr/carrefour-st-jean/boutiques/")

title = driver.title
output_dir = Path(__file__).resolve().parent / "resultat"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "title.txt"

with open(output_file, "w", encoding="utf-8") as file:
	file.write(f"Titre de la page: {title}\n")

print(f"Titre récupéré: {title}")
print(f"Résultat enregistré dans: {output_file}")

driver.quit()
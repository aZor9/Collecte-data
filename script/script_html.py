from pathlib import Path

from selenium import webdriver

url = "https://www.centre-commercial.fr/carrefour-st-jean/boutiques/"
output_dir = Path(__file__).resolve().parent / "resultat"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "html.html"

driver = webdriver.Chrome()
try:
    driver.get(url)
    html_content = driver.page_source

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"HTML enregistré dans: {output_file}")
finally:
    driver.quit()
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

url = "https://www.centre-commercial.fr/carrefour-st-jean/boutiques/"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = Path(__file__).resolve().parent / "resultat" / "script_html"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"html_{timestamp}.html"

driver = build_driver()
try:
    driver.get(url)
    time.sleep(3)
    html_content = driver.page_source

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"HTML enregistré dans: {output_file}")
finally:
    driver.quit()
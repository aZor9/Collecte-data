from datetime import datetime
from pathlib import Path
import random
import re
import time
from typing import List, Set
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import (
    InvalidSessionIdException,
    NoSuchWindowException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

HOME_URL = "https://www.centre-commercial.fr/"
COOKIE_ACCEPT_SELECTOR = "#onetrust-accept-btn-handler"
COOKIE_REJECT_SELECTOR = "#onetrust-reject-all-handler"
SEE_MORE_SELECTOR = "button.see-more-centers"
CENTER_LINKS_SELECTOR = "div.centers-list div.center a[href]"
H2_SELECTOR = "a.boutique-card h2.custom-h2"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"


def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument(f"--user-agent={USER_AGENT}")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(45)
    return driver


def human_pause(min_seconds: float = 2.0, max_seconds: float = 4.0) -> None:
    time.sleep(random.uniform(min_seconds, max_seconds))


def safe_slug(url: str, fallback: str) -> str:
    parsed = urlparse(url)
    slug = parsed.path.strip("/").replace("/", "-")
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug).strip("-")
    return slug or fallback


def close_cookie_banner(driver: webdriver.Chrome) -> None:
    for selector in (COOKIE_ACCEPT_SELECTOR, COOKIE_REJECT_SELECTOR):
        try:
            button = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            button.click()
            return
        except TimeoutException:
            continue
        except Exception:
            continue


def expand_centers_list(driver: webdriver.Chrome) -> None:
    try:
        button = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, SEE_MORE_SELECTOR))
        )
        if "voir plus" in button.text.strip().lower():
            driver.execute_script("arguments[0].click();", button)
    except TimeoutException:
        return


def collect_center_urls(driver: webdriver.Chrome) -> List[str]:
    driver.get(HOME_URL)
    human_pause(2.5, 4.5)
    close_cookie_banner(driver)
    expand_centers_list(driver)

    WebDriverWait(driver, 12).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, CENTER_LINKS_SELECTOR))
    )
    anchors = driver.find_elements(By.CSS_SELECTOR, CENTER_LINKS_SELECTOR)

    unique_urls: List[str] = []
    seen: Set[str] = set()
    for anchor in anchors:
        href = (anchor.get_attribute("href") or "").strip()
        if not href.startswith("http"):
            continue
        center_url = href.rstrip("/")
        boutiques_url = f"{center_url}/boutiques/"
        if boutiques_url in seen:
            continue
        seen.add(boutiques_url)
        unique_urls.append(boutiques_url)

    return unique_urls


def scrape_h2_titles(driver: webdriver.Chrome, url: str) -> List[str]:
    driver.get(url)
    human_pause(2.5, 5.0)
    close_cookie_banner(driver)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, H2_SELECTOR))
        )
    except TimeoutException:
        return []

    h2_elements = driver.find_elements(By.CSS_SELECTOR, H2_SELECTOR)
    return [element.text.strip() for element in h2_elements if element.text.strip()]


def scrape_h2_titles_with_retry(url: str, retries: int = 2) -> List[str]:
    last_exception = None
    for attempt in range(1, retries + 1):
        driver = build_driver()
        try:
            return scrape_h2_titles(driver, url)
        except (InvalidSessionIdException, NoSuchWindowException, WebDriverException) as exc:
            last_exception = exc
            print(f"[WARN] Session Chrome perdue ({attempt}/{retries}) sur: {url}")
            human_pause(2.0, 4.0)
        except Exception as exc:
            last_exception = exc
            print(f"[WARN] Erreur scraping ({attempt}/{retries}) sur: {url} -> {exc}")
            human_pause(2.0, 4.0)
        finally:
            try:
                driver.quit()
            except Exception:
                pass

    print(f"[ERROR] Echec final sur: {url} -> {last_exception}")
    return []


def main() -> None:
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_output_dir = Path(__file__).resolve().parent / "resultat" / "script_collect_all_h2" / f"run_{run_timestamp}"
    urls_output_dir = base_output_dir / "centers_urls"
    h2_output_dir = base_output_dir / "boutiques_h2"
    urls_output_dir.mkdir(parents=True, exist_ok=True)
    h2_output_dir.mkdir(parents=True, exist_ok=True)

    driver = build_driver()
    try:
        boutiques_urls = collect_center_urls(driver)
    finally:
        try:
            driver.quit()
        except Exception:
            pass

    urls_file = urls_output_dir / f"boutiques_urls_{run_timestamp}.txt"
    with open(urls_file, "w", encoding="utf-8") as file:
        for url in boutiques_urls:
            file.write(f"{url}\n")

    summary_file = base_output_dir / f"run_summary_{run_timestamp}.txt"
    with open(summary_file, "w", encoding="utf-8") as summary:
        summary.write("Collecte nationale des boutiques Carrefour\n")
        summary.write(f"Date: {run_timestamp}\n")
        summary.write(f"Nombre de centres detectes: {len(boutiques_urls)}\n\n")

        for index, boutiques_url in enumerate(boutiques_urls, start=1):
            titles = scrape_h2_titles_with_retry(boutiques_url, retries=3)
            center_slug = safe_slug(boutiques_url, f"center_{index:03d}")
            center_file = h2_output_dir / f"{index:03d}_{center_slug}_h2_{run_timestamp}.txt"

            with open(center_file, "w", encoding="utf-8") as file:
                file.write("Collecte des titres boutiques\n")
                file.write(f"Source: {boutiques_url}\n")
                file.write(f"Date: {run_timestamp}\n")
                file.write(f"Nombre de titres: {len(titles)}\n\n")
                for i, title in enumerate(titles, start=1):
                    file.write(f"{i:03d}. {title}\n")

            status = "OK" if titles else "VIDE/ERREUR"
            summary.write(
                f"{index:03d} | {center_slug} | {len(titles)} titres | {status} | {boutiques_url}\n"
            )
            human_pause(1.5, 3.5)

    print(f"Collecte terminee: {len(boutiques_urls)} centres traites")
    print(f"Resultats: {base_output_dir}")


if __name__ == "__main__":
    main()

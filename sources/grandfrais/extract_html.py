"""Extraction HTML specifique Grand Frais."""

from __future__ import annotations

from pathlib import Path
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import FAST_NAVIGATION, SCRAPING_SOURCES
from scraper.driver import get_driver
from scraper.navigator import click_element, close_cookie_banner, load_page
from sources.common import save_html
from utils.helpers import normalize_text, safe_slug
from utils.logger import get_logger

logger = get_logger()
SOURCE_KEY = "grandfrais"


def _collect_store_links(driver) -> List[str]:
    config = SCRAPING_SOURCES[SOURCE_KEY]
    load_page(driver, config["home_url"], timeout=FAST_NAVIGATION["page_ready_timeout"], scroll=False)
    close_cookie_banner(driver, config["cookie_accept_selector"], config["cookie_reject_selector"], timeout=2)

    WebDriverWait(driver, 6).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, config["center_links_selector"]))
    )

    links = []
    for anchor in driver.find_elements(By.CSS_SELECTOR, config["center_links_selector"]):
        href = (anchor.get_attribute("href") or "").strip()
        if not href:
            continue
        if href.startswith("/"):
            href = urljoin(config["home_url"], href)
        if "/magasins" in href and href.rstrip("/") != config["home_url"].rstrip("/"):
            links.append(href)

    return list(dict.fromkeys(links))


def _click_optional_detail_toggles(driver) -> None:
    for selector in ["button", "summary", "[role='button']"]:
        try:
            for element in driver.find_elements(By.CSS_SELECTOR, selector)[:6]:
                text = normalize_text(element.text or "")
                if text and any(token in text.lower() for token in ["horaire", "hour", "plus", "détail", "detail"]):
                    driver.execute_script("arguments[0].click();", element)
        except Exception:
            continue


def extract_html(output_dir: Path | None = None) -> List[Path]:
    config = SCRAPING_SOURCES[SOURCE_KEY]
    saved_files: List[Path] = []
    driver_manager = get_driver()
    driver = driver_manager.create()

    try:
        store_links = _collect_store_links(driver)
        logger.info(f"Grand Frais: {len(store_links)} magasins detectes")

        for store_url in store_links:
            load_page(driver, store_url, timeout=FAST_NAVIGATION["page_ready_timeout"], scroll=False)
            close_cookie_banner(driver, config["cookie_accept_selector"], config["cookie_reject_selector"], timeout=1)
            _click_optional_detail_toggles(driver)

            html = driver.page_source
            saved = save_html(html, store_url, SOURCE_KEY)
            saved_files.append(saved)

        return saved_files
    finally:
        driver_manager.quit()

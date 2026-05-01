"""Extraction HTML specifique Carrefour."""

from __future__ import annotations

from pathlib import Path
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import FAST_NAVIGATION, SCRAPING_SOURCES
from scraper.driver import get_driver
from scraper.navigator import click_element, close_cookie_banner, load_page
from sources.common import save_html
from utils.helpers import normalize_text, safe_slug
from utils.exceptions import SiteBlockedError
from utils.logger import get_logger

logger = get_logger()
SOURCE_KEY = "carrefour"


def _raise_if_blocked(driver, context_url: str) -> None:
    page_text = (driver.page_source or "").lower()
    blocked_markers = [
        "sorry, you have been blocked",
        "you are unable to access",
        "unable to access centre-commercial.fr",
        "cloudflare",
        "attention required",
    ]
    if any(marker in page_text for marker in blocked_markers):
        raise SiteBlockedError(
            f"Blocage detecte sur Carrefour ({context_url}). "
            "Le site a refuse l'acces au navigateur automatise."
        )


def _collect_center_urls(driver) -> List[str]:
    config = SCRAPING_SOURCES[SOURCE_KEY]
    load_page(driver, config["home_url"], timeout=FAST_NAVIGATION["page_ready_timeout"], scroll=False)
    _raise_if_blocked(driver, config["home_url"])
    close_cookie_banner(driver, config["cookie_accept_selector"], config["cookie_reject_selector"], timeout=2)

    see_more_selector = config.get("see_more_selector")
    if see_more_selector:
        try:
            click_element(driver, see_more_selector)
        except Exception:
            pass

    WebDriverWait(driver, 6).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, config["center_links_selector"]))
    )
    links = []
    for anchor in driver.find_elements(By.CSS_SELECTOR, config["center_links_selector"]):
        href = (anchor.get_attribute("href") or "").strip()
        if href.startswith("http"):
            links.append(href)
    return list(dict.fromkeys(links))


def _collect_store_links(driver, center_url: str) -> List[str]:
    config = SCRAPING_SOURCES[SOURCE_KEY]
    load_page(driver, center_url, timeout=FAST_NAVIGATION["page_ready_timeout"], scroll=False)
    _raise_if_blocked(driver, center_url)
    close_cookie_banner(driver, config["cookie_accept_selector"], config["cookie_reject_selector"], timeout=2)
    WebDriverWait(driver, 6).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, config["store_card_selector"]))
    )

    links = []
    for card in driver.find_elements(By.CSS_SELECTOR, config["store_card_selector"]):
        href = (card.get_attribute("href") or "").strip()
        if not href:
            try:
                href = (card.find_element(By.CSS_SELECTOR, config["store_detail_link_selector"]).get_attribute("href") or "").strip()
            except Exception:
                href = ""
        if href.startswith("/"):
            href = urljoin(center_url, href)
        if href.startswith("http"):
            links.append(href)

    return list(dict.fromkeys(links))


def _click_optional_detail_toggles(driver) -> None:
    for selector in ["button", "summary", "[role='button']"]:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements[:6]:
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
        centers = _collect_center_urls(driver)
        logger.info(f"Carrefour: {len(centers)} centres detectes")

        for center_url in centers:
            store_links = _collect_store_links(driver, center_url)
            logger.info(f"Carrefour: {len(store_links)} commerces dans {safe_slug(center_url)}")

            for store_url in store_links:
                load_page(driver, store_url, timeout=FAST_NAVIGATION["page_ready_timeout"], scroll=False)
                _raise_if_blocked(driver, store_url)
                close_cookie_banner(driver, config["cookie_accept_selector"], config["cookie_reject_selector"], timeout=1)
                _click_optional_detail_toggles(driver)

                html = driver.page_source
                saved = save_html(html, store_url, SOURCE_KEY)
                saved_files.append(saved)

        return saved_files
    finally:
        driver_manager.quit()

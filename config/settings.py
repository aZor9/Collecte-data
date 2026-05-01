"""Configuration centrale du projet.

La logique est maintenant organisée par source et par étape.
"""

from pathlib import Path
from typing import Dict, List

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
LOGS_DIR = BASE_DIR / "logs"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
]

SELENIUM_OPTIONS = {
    "disable_notifications": True,
    "disable_popup_blocking": True,
    "disable_automation": True,
    "disable_logging": True,
    "start_maximized": False,
    "headless": False,
    "page_load_timeout": 18,
}

FAST_NAVIGATION = {
    "page_ready_timeout": 8,
    "page_pause_min": 0.4,
    "page_pause_max": 1.0,
    "click_pause_min": 0.2,
    "click_pause_max": 0.8,
    "scroll_pause_min": 0.2,
    "scroll_pause_max": 0.6,
}

SCRAPING_SOURCES: Dict[str, Dict] = {
    "carrefour": {
        "name": "Carrefour Galerie Marchande",
        "home_url": "https://www.centre-commercial.fr/",
        "list_container_selector": "div.centers-list",
        "center_links_selector": "div.centers-list div.center a[href]",
        "cookie_accept_selector": "#onetrust-accept-btn-handler",
        "cookie_reject_selector": "#onetrust-reject-all-handler",
        "see_more_selector": "button.see-more-centers",
        "store_card_selector": "a.boutique-card",
        "store_name_selector": "h2.custom-h2",
        "store_detail_link_selector": "a",
        "store_detail_name_selector": "h1, h2",
        "store_detail_hours_selector": "[class*='hour'], [class*='horaire'], [class*='schedule']",
        "store_detail_description_selector": "[class*='description'], p",
        "max_retries": 2,
    },
    "grandfrais": {
        "name": "Grand Frais",
        "home_url": "https://www.grandfrais.com/magasins",
        "list_container_selector": "body",
        "center_links_selector": "a[href*='/magasins/']",
        "cookie_accept_selector": "button#onetrust-accept-btn-handler, #onetrust-accept-btn-handler",
        "cookie_reject_selector": "button#onetrust-reject-all-handler, #onetrust-reject-btn-handler",
        "see_more_selector": None,
        "store_card_selector": "a[href*='/magasins/']",
        "store_name_selector": "h2, h3, [class*='title']",
        "store_detail_link_selector": "a",
        "store_detail_name_selector": "h1, h2",
        "store_detail_hours_selector": "[class*='hour'], [class*='horaire'], [class*='schedule']",
        "store_detail_description_selector": "[class*='description'], p",
        "max_retries": 2,
    },
}

CATEGORY_MAPPING = {
    "mode": "mode",
    "fashion": "mode",
    "Mode": "mode",
    "Fashion": "mode",
    "FASHION": "mode",
    "MODE": "mode",
    "Vêtements": "mode",
    "vêtements": "mode",
    "restauration": "restauration",
    "Restauration": "restauration",
    "restaurant": "restauration",
    "Restaurant": "restauration",
    "café": "restauration",
    "Café": "restauration",
    "food": "restauration",
    "beauté": "beauté",
    "Beauté": "beauté",
    "beauty": "beauté",
    "Beauty": "beauté",
}

EXTRACT_FIELDS = [
    "name",
    "category",
    "size",
    "open_date",
    "close_date",
    "owner",
    "description",
    "hours",
]

CSV_COLUMNS = [
    "name",
    "category",
    "size",
    "open_date",
    "close_date",
    "owner",
    "description",
    "hours",
    "source",
    "scrape_date",
]

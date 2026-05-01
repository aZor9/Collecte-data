"""
config/settings.py

Configuration centrale pour le scraping et le pipeline.
"""

from pathlib import Path
from typing import Dict, List

# ============================================================================
# CHEMINS
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

# Logs
LOGS_DIR = BASE_DIR / "logs"

# ============================================================================
# SELENIUM CONFIG
# ============================================================================

# User-Agents rotatif
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
]

# Options Selenium
SELENIUM_OPTIONS = {
    "disable_notifications": True,
    "disable_popup_blocking": True,
    "disable_automation": True,
    "disable_logging": True,
    "start_maximized": True,
    "headless": False,  # Mettre à True pour prod
    "page_load_timeout": 45,
}

# Delais humains (secondes)
HUMAN_DELAYS = {
    "min_pause": 2.0,
    "max_pause": 4.0,
    "min_scroll": 1.0,
    "max_scroll": 3.0,
}

# ============================================================================
# SOURCES DE SCRAPING
# ============================================================================

SCRAPING_SOURCES: Dict[str, Dict] = {
    "centre-commercial.fr": {
        "name": "Centre Commercial France",
        "home_url": "https://www.centre-commercial.fr/",
        "cookie_accept_selector": "#onetrust-accept-btn-handler",
        "cookie_reject_selector": "#onetrust-reject-all-handler",
        "see_more_selector": "button.see-more-centers",
        "center_links_selector": "div.centers-list div.center a[href]",
        "boutique_selector": "a.boutique-card h2.custom-h2",
        "boutique_url_pattern": "/boutiques/",
        "max_retries": 3,
    },
    # Exemple pour une future 2ème source
    # "source2.com": {
    #     "name": "Source 2",
    #     "home_url": "https://...",
    #     ...
    # },
}

# ============================================================================
# CATEGORIES MAPPING (normalisation)
# ============================================================================

CATEGORY_MAPPING = {
    # Mode/Fashion
    "mode": "mode",
    "fashion": "mode",
    "Mode": "mode",
    "Fashion": "mode",
    "FASHION": "mode",
    "MODE": "mode",
    "Vêtements": "mode",
    "vêtements": "mode",
    
    # Restauration
    "restauration": "restauration",
    "Restauration": "restauration",
    "restaurant": "restauration",
    "Restaurant": "restauration",
    "café": "restauration",
    "Café": "restauration",
    "food": "restauration",
    
    # Autres
    "beauté": "beauté",
    "Beauté": "beauté",
    "beauty": "beauté",
    "Beauty": "beauté",
}

# ============================================================================
# EXTRACTION CONFIG (quels champs extraire)
# ============================================================================

EXTRACT_FIELDS = [
    "name",
    "category",
    "size",
    "open_date",
    "close_date",
    "owner",
    "description",
]

# ============================================================================
# CSV OUTPUT COLUMNS
# ============================================================================

CSV_COLUMNS = [
    "name",
    "category",
    "size",
    "open_date",
    "close_date",
    "owner",
    "description",
    "source",
    "scrape_date",
]

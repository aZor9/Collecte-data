"""
scraper/collector.py

Orchestration du scraping par source.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd
from datetime import datetime

from config.settings import (
    SCRAPING_SOURCES,
    RAW_DIR,
    INTERIM_DIR,
)
from scraper.driver import get_driver
from scraper.navigator import load_page, close_cookie_banner
from scraper.saver import save_html, save_raw_data
from parsers.html_parser import parse_html
from utils.logger import get_logger
from utils.retry import retry

logger = get_logger()


class SourceCollector:
    """Collecteur pour une source spécifique."""
    
    def __init__(self, source_key: str):
        self.source_key = source_key
        self.config = SCRAPING_SOURCES[source_key]
        self.name = self.config["name"]
    
    @retry(max_attempts=3)
    def collect_center_urls(self) -> List[str]:
        """
        Récupérer la liste des URLs des centres commerciaux.
        
        Implémentation spécifique pour centre-commercial.fr
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.common.exceptions import TimeoutException
        
        driver_manager = get_driver()
        driver = driver_manager.create()
        
        try:
            # Charger la home
            load_page(driver, self.config["home_url"], scroll=False)
            
            # Fermer les cookies
            close_cookie_banner(
                driver,
                self.config["cookie_accept_selector"],
                self.config["cookie_reject_selector"]
            )
            
            # Cliquer sur "voir plus" si présent
            try:
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.config["see_more_selector"]))
                )
                driver.execute_script("arguments[0].click();", button)
                logger.debug("✓ Bouton 'voir plus' cliqué")
            except TimeoutException:
                logger.debug("⚠ Bouton 'voir plus' non trouvé")
            
            # Récupérer les URLs
            anchors = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, self.config["center_links_selector"])
                )
            )
            
            urls = []
            for anchor in anchors:
                href = anchor.get_attribute("href")
                if href and href.startswith("http"):
                    urls.append(href)
            
            # Dédupliquer
            urls = list(dict.fromkeys(urls))
            
            logger.info(f"✓ {len(urls)} centres trouvés pour {self.name}")
            return urls
        
        finally:
            driver_manager.quit()
    
    @retry(max_attempts=2)
    def scrape_center(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scraper un centre commercial spécifique.
        """
        driver_manager = get_driver()
        driver = driver_manager.create()
        
        try:
            # Charger la page
            load_page(driver, url)
            
            # Fermer les cookies
            close_cookie_banner(
                driver,
                self.config["cookie_accept_selector"],
                self.config["cookie_reject_selector"]
            )
            
            # Récupérer le HTML
            html = driver.page_source
            
            # Sauvegarder le HTML brut
            raw_subdir = RAW_DIR / self.source_key / datetime.now().strftime("%Y%m%d")
            save_html(html, url, raw_subdir)
            
            # Parser
            data = parse_html(html, self.source_key, url)
            
            # Sauvegarder les données brutes
            data_subdir = INTERIM_DIR / self.source_key / datetime.now().strftime("%Y%m%d")
            save_raw_data(data, url, data_subdir)
            
            return data
        
        except Exception as e:
            logger.error(f"✗ Erreur scraping {url}: {e}")
            raise
        
        finally:
            driver_manager.quit()
    
    def collect_all(self, skip_urls: List[str] = None) -> List[Dict[str, Any]]:
        """
        Récupérer tous les centres et scraper leurs données.
        """
        if skip_urls is None:
            skip_urls = []
        
        logger.info(f"\n{'='*60}")
        logger.info(f"COLLECTION: {self.name}")
        logger.info(f"{'='*60}")
        
        # Récupérer les URLs
        urls = self.collect_center_urls()
        urls = [u for u in urls if u not in skip_urls]
        
        logger.info(f"→ Scraping {len(urls)} centres...")
        
        all_data = []
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls, 1):
            logger.info(f"\n[{i}/{len(urls)}] {url}")
            
            try:
                data = self.scrape_center(url)
                if data and data.get("boutiques"):
                    all_data.append(data)
                    successful += 1
            except Exception as e:
                logger.error(f"  ✗ Erreur: {str(e)[:100]}")
                failed += 1
        
        logger.info(f"\n✓ Collection terminée: {successful} OK, {failed} erreurs")
        
        return all_data


def collect_from_all_sources() -> pd.DataFrame:
    """
    Scraper toutes les sources configurées.
    """
    all_records = []
    
    for source_key in SCRAPING_SOURCES.keys():
        try:
            collector = SourceCollector(source_key)
            data_list = collector.collect_all()
            
            # Convertir en records
            for data in data_list:
                for boutique in data.get("boutiques", []):
                    record = boutique.copy()
                    record["source"] = source_key
                    record["scrape_date"] = datetime.now().strftime("%Y-%m-%d")
                    all_records.append(record)
        
        except Exception as e:
            logger.error(f"✗ Erreur source {source_key}: {e}")
            continue
    
    logger.info(f"\n✓ Total records collectés: {len(all_records)}")
    
    return pd.DataFrame(all_records)

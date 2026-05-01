"""
scraper/driver.py

Setup et gestion du driver Selenium.
"""

import random
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config.settings import SELENIUM_OPTIONS, USER_AGENTS
from utils.logger import get_logger

logger = get_logger()


class SeleniumDriver:
    """Gestionnaire du driver Selenium."""
    
    def __init__(self):
        self.driver: Optional[webdriver.Chrome] = None
    
    def create(self) -> webdriver.Chrome:
        """Créer et configurer un driver Chrome."""
        
        options = Options()
        
        # User-agent aléatoire
        user_agent = random.choice(USER_AGENTS)
        options.add_argument(f"--user-agent={user_agent}")
        logger.debug(f"User-agent: {user_agent[:50]}...")
        
        # Options de désactivation
        if SELENIUM_OPTIONS.get("disable_automation"):
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        if SELENIUM_OPTIONS.get("disable_notifications"):
            options.add_argument("--disable-notifications")
        
        if SELENIUM_OPTIONS.get("disable_popup_blocking"):
            options.add_argument("--disable-popup-blocking")
        
        if SELENIUM_OPTIONS.get("disable_logging"):
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        if SELENIUM_OPTIONS.get("start_maximized"):
            options.add_argument("--start-maximized")
        
        if SELENIUM_OPTIONS.get("headless"):
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        
        # Performance
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-sync")
        
        # Créer le driver
        try:
            self.driver = webdriver.Chrome(options=options)
            
            # Timeouts
            page_load_timeout = SELENIUM_OPTIONS.get("page_load_timeout", 45)
            self.driver.set_page_load_timeout(page_load_timeout)
            
            logger.info(f"✓ Driver Selenium créé (timeout: {page_load_timeout}s)")
            return self.driver
        
        except Exception as e:
            logger.error(f"✗ Erreur lors de la création du driver: {e}")
            raise
    
    def quit(self):
        """Fermer le driver proprement."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✓ Driver Selenium fermé")
            except Exception as e:
                logger.warning(f"Erreur lors de la fermeture du driver: {e}")
            finally:
                self.driver = None
    
    def __enter__(self):
        """Context manager entry."""
        self.create()
        return self.driver
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.quit()


def get_driver() -> SeleniumDriver:
    """Retourner une instance du gestionnaire de driver."""
    return SeleniumDriver()

"""
scraper/navigator.py

Navigation et simulation de comportement humain.
"""

import random
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import FAST_NAVIGATION
from utils.logger import get_logger

logger = get_logger()


def human_scroll(driver: webdriver.Chrome, pause_min: float = 0.2, pause_max: float = 0.6):
    """
    Scroll humain:
    - Scroll au milieu de la page
    - Pause
    - Scroll à la fin
    """
    try:
        # Scroll au milieu
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(random.uniform(pause_min, pause_max))
        
        # Scroll à la fin
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(pause_min, pause_max))
        
        # Retour au top
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.1, 0.4))
        
        logger.debug("✓ Scroll humain complété")
    
    except Exception as e:
        logger.warning(f"Erreur lors du scroll: {e}")


def human_hover(driver: webdriver.Chrome, selector: str, by: By = By.CSS_SELECTOR):
    """
    Hover sur un élément (souris humaine).
    """
    try:
        element = driver.find_element(by, selector)
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(random.uniform(0.5, 1.5))
        logger.debug(f"✓ Hover sur {selector}")
    except Exception as e:
        logger.debug(f"Erreur hover: {e}")


def load_page(
    driver: webdriver.Chrome,
    url: str,
    timeout: int = 8,
    scroll: bool = True
):
    """
    Charger une page avec comportement humain.
    
    Args:
        driver: Selenium driver
        url: URL à charger
        timeout: Timeout en secondes
        scroll: Faire un scroll humain après chargement
    """
    try:
        logger.info(f"→ Chargement: {url}")
        
        driver.get(url)
        
        # Attendre le chargement
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # Pause avant interaction
        time.sleep(random.uniform(
            FAST_NAVIGATION["page_pause_min"],
            FAST_NAVIGATION["page_pause_max"]
        ))
        
        # Scroll humain
        if scroll:
            human_scroll(
                driver,
                FAST_NAVIGATION["scroll_pause_min"],
                FAST_NAVIGATION["scroll_pause_max"]
            )
        
        logger.info(f"✓ Page chargée: {url}")
    
    except TimeoutException:
        logger.error(f"✗ Timeout lors du chargement de {url}")
        raise
    except Exception as e:
        logger.error(f"✗ Erreur lors du chargement de {url}: {e}")
        raise


def close_cookie_banner(
    driver: webdriver.Chrome,
    accept_selector: str,
    reject_selector: str,
    timeout: int = 3
):
    """
    Fermer la banneau de cookies.
    
    Try accept d'abord, sinon reject.
    """
    for selector in (accept_selector, reject_selector):
        try:
            button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            driver.execute_script("arguments[0].click();", button)
            logger.debug(f"✓ Cookie banner fermée ({selector})")
            return True
        except TimeoutException:
            continue
        except Exception as e:
            logger.debug(f"Erreur cookie banner: {e}")
            continue
    
    logger.debug("⚠ Pas de cookie banner trouvée")
    return False


def wait_for_element(
    driver: webdriver.Chrome,
    selector: str,
    by: By = By.CSS_SELECTOR,
    timeout: int = 6
):
    """
    Attendre qu'un élément soit présent et visible.
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        return element
    except TimeoutException:
        logger.warning(f"Timeout en attendant: {selector}")
        return None


def click_element(driver: webdriver.Chrome, selector: str, by: By = By.CSS_SELECTOR):
    """
    Cliquer sur un élément avec scroll si nécessaire.
    """
    try:
        element = driver.find_element(by, selector)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(random.uniform(0.1, 0.3))
        driver.execute_script("arguments[0].click();", element)
        logger.debug(f"✓ Click sur {selector}")
    except Exception as e:
        logger.error(f"Erreur click: {e}")
        raise

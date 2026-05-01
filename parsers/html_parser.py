"""
parsers/html_parser.py

Parsing du HTML en donnees structurees.
"""

from typing import Optional, Dict, List, Any
from bs4 import BeautifulSoup

from utils.logger import get_logger
from utils.helpers import normalize_text

logger = get_logger()


class HTMLParser:
    """Parser HTML generique."""

    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")

    def extract_by_selector(self, selector: str, attr: Optional[str] = None) -> List[str]:
        """Extraire les elements par selecteur CSS."""
        elements = self.soup.select(selector)
        results = []

        for el in elements:
            value = el.get(attr, "") if attr else el.get_text(strip=True)
            value = normalize_text(value)
            if value:
                results.append(value)

        return results

    def extract_single(self, selector: str, attr: Optional[str] = None) -> Optional[str]:
        """Extraire un seul element."""
        results = self.extract_by_selector(selector, attr)
        return results[0] if results else None


class CentreCommercialParser:
    """Parser specialise pour centre-commercial.fr"""

    def __init__(self, html: str, url: str):
        self.html = html
        self.url = url
        self.parser = HTMLParser(html)

    def extract_boutique_info(self) -> Dict[str, Any]:
        boutiques = []

        elements = self.parser.soup.select("a.boutique-card")

        for el in elements:
            boutique = {
                "name": normalize_text(el.select_one("h2.custom-h2").get_text()) if el.select_one("h2.custom-h2") else None,
                "description": normalize_text(el.select_one("p.description").get_text()) if el.select_one("p.description") else None,
                "category": normalize_text(el.select_one(".category").get_text()) if el.select_one(".category") else None,
            }

            boutique = {k: v for k, v in boutique.items() if v is not None}

            if "name" in boutique:
                boutiques.append(boutique)

        logger.info(f"✓ {len(boutiques)} boutiques extraites de {self.url}")

        return {
            "url": self.url,
            "boutiques": boutiques,
            "total": len(boutiques),
        }


def parse_html(html: str, source: str = "centre-commercial.fr", url: str = "") -> Dict[str, Any]:
    """Parser HTML selon la source."""
    if source == "centre-commercial.fr":
        return CentreCommercialParser(html, url).extract_boutique_info()

    logger.warning(f"Source inconnue: {source}")
    return {"boutiques": [], "total": 0}

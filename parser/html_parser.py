"""
parser/html_parser.py

Parsing du HTML en données structurées.
"""

from typing import Optional, Dict, List, Any
from bs4 import BeautifulSoup

from utils.logger import get_logger
from utils.helpers import normalize_text

logger = get_logger()


class HTMLParser:
    """Parser HTML générique."""
    
    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")
    
    def extract_by_selector(self, selector: str, attr: Optional[str] = None) -> List[str]:
        """
        Extraire les éléments par sélecteur CSS.
        
        Args:
            selector: Sélecteur CSS
            attr: Attribut à extraire (ex: 'href'), sinon texte
        
        Returns:
            List de valeurs
        """
        elements = self.soup.select(selector)
        results = []
        
        for el in elements:
            if attr:
                value = el.get(attr, "")
            else:
                value = el.get_text(strip=True)
            
            value = normalize_text(value)
            if value:
                results.append(value)
        
        return results
    
    def extract_single(self, selector: str, attr: Optional[str] = None) -> Optional[str]:
        """Extraire un seul élément."""
        results = self.extract_by_selector(selector, attr)
        return results[0] if results else None
    
    def extract_text_by_selector(self, selector: str) -> Optional[str]:
        """Extraire le texte d'un élément."""
        return self.extract_single(selector)
    
    def extract_attr_by_selector(self, selector: str, attr: str) -> Optional[str]:
        """Extraire un attribut d'un élément."""
        return self.extract_single(selector, attr)


class CentreCommercialParser:
    """Parser spécialisé pour centre-commercial.fr"""
    
    def __init__(self, html: str, url: str):
        self.html = html
        self.url = url
        self.parser = HTMLParser(html)
    
    def extract_boutique_names(self) -> List[str]:
        """Extraire les noms des boutiques."""
        return self.parser.extract_by_selector("a.boutique-card h2.custom-h2")
    
    def extract_boutique_info(self) -> Dict[str, Any]:
        """
        Extraire les informations des boutiques.
        
        Returns:
            {
                "boutiques": [
                    {"name": "...", "category": "...", ...},
                    ...
                ]
            }
        """
        boutiques = []
        
        # Chercher tous les éléments boutique
        elements = self.parser.soup.select("a.boutique-card")
        
        for el in elements:
            boutique = {
                "name": normalize_text(el.select_one("h2.custom-h2").get_text()) if el.select_one("h2.custom-h2") else None,
                "description": normalize_text(el.select_one("p.description").get_text()) if el.select_one("p.description") else None,
                "category": normalize_text(el.select_one(".category").get_text()) if el.select_one(".category") else None,
            }
            
            # Filtrer les None
            boutique = {k: v for k, v in boutique.items() if v is not None}
            
            if "name" in boutique:  # Au moins le nom doit être présent
                boutiques.append(boutique)
        
        logger.info(f"✓ {len(boutiques)} boutiques extraites de {self.url}")
        
        return {
            "url": self.url,
            "boutiques": boutiques,
            "total": len(boutiques),
        }


def parse_html(html: str, source: str = "centre-commercial.fr", url: str = "") -> Dict[str, Any]:
    """
    Parser HTML selon la source.
    
    Args:
        html: Contenu HTML
        source: Source (ex: "centre-commercial.fr")
        url: URL source pour contexte
    
    Returns:
        Dictionnaire de données extraites
    """
    if source == "centre-commercial.fr":
        parser = CentreCommercialParser(html, url)
        return parser.extract_boutique_info()
    else:
        logger.warning(f"Source inconnue: {source}")
        return {"boutiques": [], "total": 0}

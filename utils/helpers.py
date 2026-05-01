"""
utils/helpers.py

Fonctions utilitaires générales.
"""

import random
import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
from datetime import datetime


def human_pause(min_seconds: float = 2.0, max_seconds: float = 4.0) -> None:
    """Pause aléatoire pour simuler un comportement humain."""
    import time
    time.sleep(random.uniform(min_seconds, max_seconds))


def random_user_agent(user_agents: list) -> str:
    """Retourner un user-agent aléatoire."""
    return random.choice(user_agents)


def safe_slug(url: str, fallback: str = "unknown") -> str:
    """
    Générer un slug sûr à partir d'une URL.
    
    Ex: https://example.com/carrefour-paris/boutiques/ → carrefour-paris-boutiques
    """
    parsed = urlparse(url)
    slug = parsed.path.strip("/").replace("/", "-")
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug).strip("-")
    return slug or fallback


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Nettoyer un nom de fichier.
    
    Supprime les caractères invalides et tronque si nécessaire.
    """
    # Remplacer les caractères invalides
    invalid_chars = r'[<>:"/\\|?*]'
    safe_name = re.sub(invalid_chars, "_", filename)
    
    # Tronquer si trop long
    if len(safe_name) > max_length:
        safe_name = safe_name[:max_length]
    
    return safe_name


def get_timestamp() -> str:
    """Retourner timestamp au format YYYYMMDD_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(path: Path) -> Path:
    """Créer le répertoire s'il n'existe pas."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def is_valid_url(url: str) -> bool:
    """Vérifier si une URL est valide."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def normalize_text(text: Optional[str]) -> Optional[str]:
    """
    Normaliser un texte:
    - Trim whitespace
    - Remplacer les whitespaces multiples par 1
    - Retourner None si vide
    """
    if not text:
        return None
    
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    
    return text if text else None


def parse_date(date_str: Optional[str], format_str: str = "%Y-%m-%d") -> Optional[str]:
    """
    Parser une date et la retourner au format standard (YYYY-MM-DD).
    
    Si le parsing échoue, retourner None.
    """
    if not date_str:
        return None
    
    try:
        parsed = datetime.strptime(date_str.strip(), format_str)
        return parsed.strftime("%Y-%m-%d")
    except Exception:
        return None


def parse_size(size_str: Optional[str]) -> Optional[int]:
    """
    Parser une taille (m², ha, etc.) et retourner en entier (m²).
    
    Ex: "5000 m²" → 5000
    Ex: "0.5 ha" → 5000 (1 ha = 10000 m²)
    """
    if not size_str:
        return None
    
    try:
        # Extraire le nombre et l'unité
        match = re.match(r'([0-9.,]+)\s*([a-zA-Z²³⁰¹²³]*)', size_str.strip())
        if not match:
            return None
        
        number_str, unit = match.groups()
        
        # Remplacer virgule par point
        number_str = number_str.replace(',', '.')
        number = float(number_str)
        
        # Convertir selon l'unité
        unit = unit.lower().strip()
        if 'ha' in unit or 'hectare' in unit:
            number = number * 10000  # 1 ha = 10000 m²
        
        return int(number)
    except Exception:
        return None

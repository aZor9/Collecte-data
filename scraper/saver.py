"""
scraper/saver.py

Sauvegarde du contenu HTML et données brutes.
"""

from pathlib import Path
from datetime import datetime

from utils.logger import get_logger
from utils.helpers import safe_slug, sanitize_filename

logger = get_logger()


def save_html(html: str, url: str, output_dir: Path) -> Path:
    """
    Sauvegarder le HTML d'une page.
    
    Returns:
        Path: Chemin du fichier sauvegardé
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Générer le nom du fichier
    slug = safe_slug(url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{slug}_{timestamp}.html"
    filename = sanitize_filename(filename)
    
    file_path = output_dir / filename
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        logger.info(f"✓ HTML sauvegardé: {file_path.name}")
        return file_path
    
    except Exception as e:
        logger.error(f"✗ Erreur sauvegarde HTML: {e}")
        raise


def save_raw_data(data: dict, url: str, output_dir: Path) -> Path:
    """
    Sauvegarder les données brutes extraites (JSON).
    """
    import json
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    slug = safe_slug(url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{slug}_{timestamp}.json"
    filename = sanitize_filename(filename)
    
    file_path = output_dir / filename
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✓ Données brutes sauvegardées: {file_path.name}")
        return file_path
    
    except Exception as e:
        logger.error(f"✗ Erreur sauvegarde données: {e}")
        raise

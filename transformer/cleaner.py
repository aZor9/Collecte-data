"""
transformer/cleaner.py

Nettoyage des données brutes.
"""

from typing import Optional, Dict, Any, List
import pandas as pd

from config.settings import CATEGORY_MAPPING
from utils.logger import get_logger
from utils.helpers import normalize_text, parse_date, parse_size

logger = get_logger()


def clean_text_field(value: Optional[str]) -> Optional[str]:
    """Nettoyer un champ texte."""
    return normalize_text(value)


def clean_category(value: Optional[str]) -> Optional[str]:
    """
    Nettoyer et normaliser une catégorie.
    
    Ex: "Mode" → "mode"
    """
    if not value:
        return None
    
    value = normalize_text(value)
    
    # Chercher dans le mapping
    if value in CATEGORY_MAPPING:
        return CATEGORY_MAPPING[value]
    
    # Sinon retourner la valeur normalisée en minuscule
    return value.lower() if value else None


def clean_size(value: Optional[str]) -> Optional[int]:
    """
    Nettoyer la taille.
    
    Ex: "5000 m²" → 5000
    """
    return parse_size(value)


def clean_date(value: Optional[str]) -> Optional[str]:
    """
    Nettoyer une date.
    
    Retourner au format YYYY-MM-DD
    """
    if not value:
        return None
    
    # Essayer différents formats
    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d.%m.%Y",
    ]
    
    for fmt in formats:
        result = parse_date(value, fmt)
        if result:
            return result
    
    return None


def clean_boutique_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nettoyer un enregistrement boutique.
    """
    cleaned = {
        "name": clean_text_field(record.get("name")),
        "category": clean_category(record.get("category")),
        "size": clean_size(record.get("size")),
        "open_date": clean_date(record.get("open_date")),
        "close_date": clean_date(record.get("close_date")),
        "owner": clean_text_field(record.get("owner")),
        "description": clean_text_field(record.get("description")),
    }
    
    # Filtrer les champs à None
    return {k: v for k, v in cleaned.items() if v is not None}


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoyer un DataFrame complet.
    """
    df_clean = df.copy()
    
    # Appliquer le nettoyage
    for col in ["name", "owner", "description"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].apply(clean_text_field)
    
    if "category" in df_clean.columns:
        df_clean["category"] = df_clean["category"].apply(clean_category)
    
    if "size" in df_clean.columns:
        df_clean["size"] = df_clean["size"].apply(clean_size)
    
    if "open_date" in df_clean.columns:
        df_clean["open_date"] = df_clean["open_date"].apply(clean_date)
    
    if "close_date" in df_clean.columns:
        df_clean["close_date"] = df_clean["close_date"].apply(clean_date)
    
    # Supprimer les lignes complètement vides
    df_clean = df_clean.dropna(how='all')
    
    logger.info(f"✓ Nettoyage: {len(df_clean)} lignes restantes")
    
    return df_clean

"""
transformer/normalizer.py

Normalisation et standardisation des données.
"""

from typing import Optional
import pandas as pd

from utils.logger import get_logger

logger = get_logger()


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliser les colonnes du DataFrame.
    
    - Standardiser les noms de colonnes
    - Uniformiser les types
    - Ajouter les colonnes manquantes
    """
    df_norm = df.copy()
    
    # Colonnes attendues
    expected_cols = [
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
    
    # Ajouter les colonnes manquantes
    for col in expected_cols:
        if col not in df_norm.columns:
            df_norm[col] = None
    
    # Réordonner les colonnes
    df_norm = df_norm[expected_cols]
    
    # Standardiser les types
    df_norm["name"] = df_norm["name"].astype("string", errors="ignore")
    df_norm["category"] = df_norm["category"].astype("string", errors="ignore")
    df_norm["owner"] = df_norm["owner"].astype("string", errors="ignore")
    df_norm["description"] = df_norm["description"].astype("string", errors="ignore")
    df_norm["source"] = df_norm["source"].astype("string", errors="ignore")
    df_norm["size"] = pd.to_numeric(df_norm["size"], errors="coerce")
    
    logger.info(f"✓ Normalisation: {len(df_norm)} lignes")
    
    return df_norm


def remove_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    """
    Supprimer les doublons.
    
    Par défaut, comparer sur 'name' et 'source'
    """
    if subset is None:
        subset = ["name", "source"]
    
    df_dedup = df.drop_duplicates(subset=subset, keep="first")
    
    removed = len(df) - len(df_dedup)
    if removed > 0:
        logger.info(f"✓ Doublons supprimés: {removed}")
    
    return df_dedup


def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Supprimer les lignes invalides.
    
    - Au minimum: name + (category OR owner)
    """
    df_valid = df[
        df["name"].notna() & 
        ((df["category"].notna()) | (df["owner"].notna()))
    ].copy()
    
    removed = len(df) - len(df_valid)
    if removed > 0:
        logger.info(f"✓ Lignes invalides supprimées: {removed}")
    
    return df_valid

"""
transformer/enricher.py

Enrichissement des données avec du contexte métier.
"""

from typing import Dict, Any
from datetime import datetime
import pandas as pd

from utils.logger import get_logger

logger = get_logger()


def add_scrape_metadata(df: pd.DataFrame, source: str, scrape_date: str = None) -> pd.DataFrame:
    """
    Ajouter les métadonnées de scraping.
    """
    df_enriched = df.copy()
    
    if scrape_date is None:
        scrape_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    df_enriched["source"] = source
    df_enriched["scrape_date"] = scrape_date
    
    logger.info(f"✓ Métadonnées ajoutées: source={source}, date={scrape_date}")
    
    return df_enriched


def compute_business_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculer les métriques métier.
    """
    metrics = {}
    
    # Par catégorie
    if "category" in df.columns and "size" in df.columns:
        metrics["avg_size_by_category"] = df.groupby("category")["size"].agg([
            ("count", "count"),
            ("mean", "mean"),
            ("min", "min"),
            ("max", "max"),
        ]).to_dict()
    
    # Par propriétaire
    if "owner" in df.columns:
        metrics["stores_per_owner"] = df["owner"].value_counts().to_dict()
    
    # Statistiques globales
    metrics["total_stores"] = len(df)
    metrics["total_by_source"] = df["source"].value_counts().to_dict() if "source" in df.columns else {}
    
    logger.info(f"✓ Métriques calculées: {metrics['total_stores']} magasins")
    
    return metrics


def add_business_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajouter des champs calculés utiles.
    """
    df_enriched = df.copy()
    
    # Flag: magasin ouvert (close_date null ou dans le futur)
    if "close_date" in df_enriched.columns:
        today = datetime.now().strftime("%Y-%m-%d")
        df_enriched["is_open"] = (df_enriched["close_date"].isna()) | (df_enriched["close_date"] > today)
    
    # Flag: magasin récent (ouvert dans les 6 derniers mois)
    if "open_date" in df_enriched.columns:
        six_months_ago = pd.Timestamp.now() - pd.Timedelta(days=180)
        df_enriched["is_recent"] = pd.to_datetime(df_enriched["open_date"], errors="coerce") > six_months_ago
    
    return df_enriched


def save_metrics(metrics: Dict[str, Any], output_path: str):
    """
    Sauvegarder les métriques en JSON.
    """
    import json
    from pathlib import Path
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2, default=str)
    
    logger.info(f"✓ Métriques sauvegardées: {output_path}")

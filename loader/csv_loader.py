"""
loader/csv_loader.py

Chargement et sauvegarde de fichiers CSV.
"""

from pathlib import Path
from typing import Optional
import pandas as pd

from config.settings import CSV_COLUMNS
from utils.logger import get_logger

logger = get_logger()


def load_csv(file_path: Path) -> Optional[pd.DataFrame]:
    """
    Charger un fichier CSV.
    """
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        logger.info(f"✓ CSV chargé: {file_path.name} ({len(df)} lignes)")
        return df
    except Exception as e:
        logger.error(f"✗ Erreur chargement CSV: {e}")
        return None


def save_csv(df: pd.DataFrame, file_path: Path, include_index: bool = False) -> bool:
    """
    Sauvegarder un DataFrame en CSV.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Sélectionner les colonnes disponibles
        cols = [c for c in CSV_COLUMNS if c in df.columns]
        df_export = df[cols]
        
        df_export.to_csv(
            file_path,
            encoding="utf-8",
            index=include_index,
            quotechar='"',
            quoting=1,  # QUOTE_ALL
        )
        
        logger.info(f"✓ CSV sauvegardé: {file_path.name} ({len(df_export)} lignes)")
        return True
    
    except Exception as e:
        logger.error(f"✗ Erreur sauvegarde CSV: {e}")
        return False


def append_csv(df_new: pd.DataFrame, file_path: Path) -> bool:
    """
    Ajouter des lignes à un CSV existant.
    """
    try:
        if file_path.exists():
            df_existing = load_csv(file_path)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new
        
        return save_csv(df_combined, file_path)
    
    except Exception as e:
        logger.error(f"✗ Erreur append CSV: {e}")
        return False


def export_summary(df: pd.DataFrame, file_path: Path) -> bool:
    """
    Exporter un résumé des données en texte.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("RÉSUMÉ DES DONNÉES\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Total lignes: {len(df)}\n\n")
            
            f.write("Colonnes:\n")
            for col in df.columns:
                non_null = df[col].notna().sum()
                f.write(f"  - {col}: {non_null}/{len(df)} valeurs\n")
            
            f.write("\nPour catégorie:\n")
            if "category" in df.columns:
                for cat, count in df["category"].value_counts().items():
                    f.write(f"  - {cat}: {count}\n")
            
            f.write("\nPour source:\n")
            if "source" in df.columns:
                for src, count in df["source"].value_counts().items():
                    f.write(f"  - {src}: {count}\n")
        
        logger.info(f"✓ Résumé exporté: {file_path.name}")
        return True
    
    except Exception as e:
        logger.error(f"✗ Erreur export résumé: {e}")
        return False

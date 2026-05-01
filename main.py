"""
main.py

Point d'entree principal du projet.

Commandes:
- `python main.py` ou `python main.py pipeline`
- `python main.py compare-files A B`
- `python main.py compare-runs --auto`
"""

from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

from loader.csv_loader import export_summary, save_csv
from scraper.collector import collect_from_all_sources
from tools.compare_lists import compare_files
from tools.compare_runs import compare_runs, get_latest_runs
from transformer.cleaner import clean_dataframe
from transformer.enricher import add_business_fields, compute_business_metrics, save_metrics
from transformer.normalizer import normalize_dataframe, remove_duplicates, remove_invalid_rows
from utils.helpers import get_timestamp
from utils.logger import get_logger

logger = get_logger()


def run_pipeline():
    """
    Exécuter le pipeline complet.
    
    [SELENIUM SCRAPER] → [HTML SAVE] → [PARSE → CSV] → [TRANSFORM] → [DATASET FINAL]
    """
    
    logger.info("\n" + "="*80)
    logger.info("🚀 DÉMARRAGE DU PIPELINE DE SCRAPING")
    logger.info("="*80 + "\n")
    
    start_time = datetime.now()
    
    try:
        # =====================================================================
        # 1. SCRAPING SELENIUM
        # =====================================================================
        logger.info("\n[1/5] SCRAPING SELENIUM")
        logger.info("-" * 80)
        
        df_raw = collect_from_all_sources()
        
        if df_raw.empty:
            logger.error("✗ Aucune donnée collectée!")
            return False
        
        logger.info(f"✓ {len(df_raw)} records collectés")
        
        # =====================================================================
        # 2. NETTOYAGE
        # =====================================================================
        logger.info("\n[2/5] NETTOYAGE DES DONNÉES")
        logger.info("-" * 80)
        
        df_clean = clean_dataframe(df_raw)
        logger.info(f"✓ Nettoyage: {len(df_clean)} lignes valides")
        
        # =====================================================================
        # 3. NORMALISATION & DÉDUPLICATION
        # =====================================================================
        logger.info("\n[3/5] NORMALISATION")
        logger.info("-" * 80)
        
        df_norm = normalize_dataframe(df_clean)
        df_dedup = remove_duplicates(df_norm)
        df_valid = remove_invalid_rows(df_dedup)
        
        logger.info(f"✓ Normalisation: {len(df_valid)} lignes finales")
        
        # =====================================================================
        # 4. ENRICHISSEMENT
        # =====================================================================
        logger.info("\n[4/5] ENRICHISSEMENT")
        logger.info("-" * 80)
        
        df_enriched = add_business_fields(df_valid)
        metrics = compute_business_metrics(df_enriched)
        
        logger.info(f"✓ Enrichissement avec métriques métier")
        
        # =====================================================================
        # 5. EXPORT & SAUVEGARDE
        # =====================================================================
        logger.info("\n[5/5] EXPORT & SAUVEGARDE")
        logger.info("-" * 80)
        
        timestamp = get_timestamp()
        
        # CSV final
        csv_file = PROCESSED_DIR / f"final_dataset_{timestamp}.csv"
        save_csv(df_enriched, csv_file)
        
        # Résumé texte
        summary_file = PROCESSED_DIR / f"summary_{timestamp}.txt"
        export_summary(df_enriched, summary_file)
        
        # Métriques JSON
        metrics_file = PROCESSED_DIR / f"metrics_{timestamp}.json"
        save_metrics(metrics, metrics_file)
        
        # =====================================================================
        # RÉSUMÉ FINAL
        # =====================================================================
        elapsed = datetime.now() - start_time
        
        logger.info("\n" + "="*80)
        logger.info("✅ PIPELINE TERMINÉ AVEC SUCCÈS")
        logger.info("="*80)
        logger.info(f"Durée: {elapsed}")
        logger.info(f"Records: {len(df_enriched)}")
        logger.info(f"Sources: {df_enriched['source'].nunique() if 'source' in df_enriched.columns else 0}")
        logger.info(f"Catégories: {df_enriched['category'].nunique() if 'category' in df_enriched.columns else 0}")
        logger.info(f"\nFichiers générés:")
        logger.info(f"  - {csv_file}")
        logger.info(f"  - {summary_file}")
        logger.info(f"  - {metrics_file}")
        logger.info("="*80 + "\n")
        
        return True
    
    except Exception as e:
        logger.critical(f"\n✗ ERREUR PIPELINE: {e}\n", exc_info=True)
        return False


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Pipeline principal du projet de scraping")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("pipeline", help="Lancer le pipeline Selenium complet")

    compare_files_parser = subparsers.add_parser("compare-files", help="Comparer deux fichiers liste")
    compare_files_parser.add_argument("file_a", help="Premier fichier")
    compare_files_parser.add_argument("file_b", help="Second fichier")
    compare_files_parser.add_argument("--out", help="Dossier de sortie optionnel")

    compare_runs_parser = subparsers.add_parser("compare-runs", help="Comparer deux runs complets")
    compare_runs_parser.add_argument("run_a", nargs="?", help="Premier run")
    compare_runs_parser.add_argument("run_b", nargs="?", help="Second run")
    compare_runs_parser.add_argument("--auto", action="store_true", help="Auto-detecter les deux derniers runs")
    compare_runs_parser.add_argument("--out", help="Dossier de sortie optionnel")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command in (None, "pipeline"):
        return 0 if run_pipeline() else 1

    if args.command == "compare-files":
        out = compare_files(args.file_a, args.file_b, args.out)
        print(f"Résultats écrits dans: {out}")
        return 0

    if args.command == "compare-runs":
        if args.auto:
            base_dir = Path.cwd() / "results" / "compare_runs"
            latest = get_latest_runs(base_dir, count=2)
            if len(latest) < 2:
                raise ValueError(f"Impossible de trouver 2 runs dans {base_dir}")
            run_a, run_b = latest
        else:
            if not args.run_a or not args.run_b:
                parser.error("Fournir deux chemins de run ou utiliser --auto")
            run_a, run_b = args.run_a, args.run_b

        out = compare_runs(run_a, run_b, args.out)
        print(f"Résultats écrits dans: {out}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
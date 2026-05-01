"""Point d'entree principal du projet.

Stages disponibles:
- extract: extraction HTML specifique a la source
- transform: transformation HTML -> CSV specifique a la source
- compare: comparaison des CSV finaux
- all: extraction + transformation
"""

from __future__ import annotations

from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

from config.settings import PROCESSED_DIR
from sources.carrefour.extract_html import extract_html as extract_carrefour_html
from sources.carrefour.transform_csv import transform_csv as transform_carrefour_csv
from sources.grandfrais.extract_html import extract_html as extract_grandfrais_html
from sources.grandfrais.transform_csv import transform_csv as transform_grandfrais_csv
from tools.compare_results import compare_final_csvs
from utils.exceptions import SiteBlockedError
from utils.logger import get_logger

logger = get_logger()

DEFAULT_SOURCE = "carrefour"
DEFAULT_STAGE = "all"
RUN_EXTRACTION_BY_DEFAULT = True
RUN_TRANSFORMATION_BY_DEFAULT = True
RUN_COMPARISON_BY_DEFAULT = False
ALLOW_TRANSFORM_IF_BLOCKED = True


def run_extraction(source: str) -> list[Path]:
    logger.info(f"Extraction HTML: {source}")
    if source == "carrefour":
        return extract_carrefour_html()
    if source == "grandfrais":
        return extract_grandfrais_html()
    raise ValueError(f"Source inconnue: {source}")


def run_transformation(source: str) -> Path:
    logger.info(f"Transformation CSV: {source}")
    if source == "carrefour":
        return transform_carrefour_csv()
    if source == "grandfrais":
        return transform_grandfrais_csv()
    raise ValueError(f"Source inconnue: {source}")


def latest_source_csv(source: str) -> Path:
    folder = PROCESSED_DIR / source
    candidates = sorted(folder.glob("*.csv"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError(f"Aucun CSV final trouve pour {source} dans {folder}")
    return candidates[0]


def run_comparison() -> Path:
    carrefour_csv = latest_source_csv("carrefour")
    grandfrais_csv = latest_source_csv("grandfrais")
    logger.info("Comparaison des resultats finaux entre Carrefour et Grand Frais")
    return compare_final_csvs(carrefour_csv, grandfrais_csv)


def run_pipeline(source: str, stage: str) -> int:
    start = datetime.now()

    if stage in ("extract", "all"):
        try:
            run_extraction(source)
        except SiteBlockedError as exc:
            logger.error(str(exc))
            if stage == "extract":
                return 2
            if stage == "all" and ALLOW_TRANSFORM_IF_BLOCKED:
                logger.warning(
                    "Extraction bloquee. Passage en mode fallback: "
                    "transformation depuis les HTML deja collectes."
                )
            else:
                return 2

    if stage in ("transform", "all"):
        run_transformation(source)

    if stage == "compare":
        run_comparison()

    elapsed = datetime.now() - start
    logger.info(f"Pipeline termine en {elapsed}")
    return 0


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Pipeline principal de scraping Carrefour / Grand Frais")
    parser.add_argument("--source", choices=["carrefour", "grandfrais"], default=DEFAULT_SOURCE)
    parser.add_argument("--stage", choices=["extract", "transform", "compare", "all"], default=DEFAULT_STAGE)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not RUN_EXTRACTION_BY_DEFAULT and args.stage in ("extract", "all"):
        logger.info("Extraction desactivee par configuration")
        return 0
    if not RUN_TRANSFORMATION_BY_DEFAULT and args.stage in ("transform", "all"):
        logger.info("Transformation desactivee par configuration")
        return 0
    if RUN_COMPARISON_BY_DEFAULT and args.stage == "compare":
        return run_pipeline(args.source, args.stage)

    return run_pipeline(args.source, args.stage)


if __name__ == "__main__":
    raise SystemExit(main())

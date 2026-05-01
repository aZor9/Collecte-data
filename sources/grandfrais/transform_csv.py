"""Transformation CSV specifique Grand Frais depuis les HTML bruts."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd
from bs4 import BeautifulSoup

from config.settings import PROCESSED_DIR
from loader.csv_loader import save_csv
from sources.common import (
    extract_description_text,
    extract_horaires_text,
    name_key,
    normalize_store_name,
    latest_source_raw_dir,
)
from utils.helpers import normalize_text
from utils.logger import get_logger

logger = get_logger()
SOURCE_KEY = "grandfrais"


def _extract_record_from_html(html: str, url_hint: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    title = None
    for selector in ["h1", "h2", "[class*='title']"]:
        node = soup.select_one(selector)
        if node:
            title = normalize_text(node.get_text(" ", strip=True))
            if title:
                break

    record = {
        "name": normalize_store_name(title),
        "name_key": name_key(title),
        "category": None,
        "size": None,
        "open_date": None,
        "close_date": None,
        "owner": None,
        "description": extract_description_text(soup),
        "hours": extract_horaires_text(soup),
        "source": SOURCE_KEY,
        "url": url_hint,
        "scrape_date": datetime.now().strftime("%Y-%m-%d"),
    }

    text = soup.get_text(" ", strip=True)
    size_match = re.search(r"(\d[\d\s.,]*)\s*m²", text, re.I)
    if size_match:
        record["size"] = int(float(size_match.group(1).replace(" ", "").replace(",", ".")))

    return record


def transform_csv(raw_dir: Path | None = None) -> Path:
    raw_root = raw_dir or latest_source_raw_dir(SOURCE_KEY)
    html_files = sorted(raw_root.rglob("*.html"))
    records: List[dict] = []

    for html_file in html_files:
        html = html_file.read_text(encoding="utf-8", errors="ignore")
        records.append(_extract_record_from_html(html, html_file.stem))

    df = pd.DataFrame(records)
    if df.empty:
        logger.warning("Grand Frais: aucune donnée HTML à transformer")
        return PROCESSED_DIR / "grandfrais_empty.csv"

    df = df[df["name"].notna()].copy()
    df["name_key"] = df["name"].fillna("").str.casefold()
    df = df.drop_duplicates(subset=["name_key", "url"], keep="first")
    df = df.sort_values(by=["name_key", "url"])

    output_dir = PROCESSED_DIR / SOURCE_KEY
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"grandfrais_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    save_csv(df, output_file)
    return output_file

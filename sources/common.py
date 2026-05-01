"""Outils partages pour les extracteurs et transformateurs par source."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

from bs4 import BeautifulSoup

from config.settings import INTERIM_DIR, RAW_DIR
from utils.helpers import normalize_text, safe_slug, sanitize_filename


def source_raw_dir(source: str, day: Optional[str] = None) -> Path:
    day = day or datetime.now().strftime("%Y%m%d")
    path = RAW_DIR / source / day
    path.mkdir(parents=True, exist_ok=True)
    return path


def latest_source_raw_dir(source: str) -> Path:
    root = RAW_DIR / source
    candidates = [path for path in root.glob("*") if path.is_dir()]
    if not candidates:
        return source_raw_dir(source)
    return sorted(candidates, key=lambda path: path.name, reverse=True)[0]


def source_interim_dir(source: str, day: Optional[str] = None) -> Path:
    day = day or datetime.now().strftime("%Y%m%d")
    path = INTERIM_DIR / source / day
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_html(html: str, url: str, source: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = sanitize_filename(f"{safe_slug(url)}_{timestamp}.html")
    path = source_raw_dir(source) / filename
    path.write_text(html, encoding="utf-8")
    return path


def soup_texts(soup: BeautifulSoup, selectors: Iterable[str]) -> list[str]:
    values: list[str] = []
    for selector in selectors:
        for element in soup.select(selector):
            text = normalize_text(element.get_text(" ", strip=True))
            if text:
                values.append(text)
    return values


def normalize_store_name(name: Optional[str]) -> Optional[str]:
    text = normalize_text(name)
    if not text:
        return None
    words = []
    for word in text.split():
        if word.isupper() and len(word) <= 4:
            words.append(word)
        else:
            words.append(word[:1].upper() + word[1:].lower())
    return " ".join(words)


def name_key(name: Optional[str]) -> Optional[str]:
    text = normalize_text(name)
    return text.casefold() if text else None


def extract_horaires_text(soup: BeautifulSoup) -> Optional[str]:
    for selector in ["[class*='hour']", "[class*='horaire']", "[class*='schedule']", "table", "ul", "p"]:
        candidates = soup.select(selector)
        for candidate in candidates:
            text = normalize_text(candidate.get_text(" ", strip=True))
            if not text:
                continue
            if re.search(r"\b(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|horaire|hours)\b", text, re.I):
                return text
    return None


def extract_description_text(soup: BeautifulSoup) -> Optional[str]:
    for selector in ["[class*='description']", "article p", "main p", "p"]:
        for candidate in soup.select(selector):
            text = normalize_text(candidate.get_text(" ", strip=True))
            if text and len(text) > 30:
                return text
    return None

"""Comparaison des resultats finaux entre deux sources ou deux runs."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from utils.logger import get_logger

logger = get_logger()


def _load_final_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "name_key" not in df.columns and "name" in df.columns:
        df["name_key"] = df["name"].fillna("").astype(str).str.casefold()
    return df


def compare_final_csvs(file_a: str | Path, file_b: str | Path, out_dir: str | Path | None = None) -> Path:
    df_a = _load_final_csv(file_a)
    df_b = _load_final_csv(file_b)

    name_col = "name_key"
    set_a = set(df_a[name_col].dropna())
    set_b = set(df_b[name_col].dropna())

    common = sorted(set_a & set_b)
    only_a = sorted(set_a - set_b)
    only_b = sorted(set_b - set_a)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path(out_dir) if out_dir else Path.cwd() / "results" / "compare_results" / f"run_{ts}"
    out_path.mkdir(parents=True, exist_ok=True)

    summary = out_path / f"summary_{ts}.txt"
    common_file = out_path / "common.txt"
    only_a_file = out_path / "only_in_a.txt"
    only_b_file = out_path / "only_in_b.txt"

    common_file.write_text("\n".join(common), encoding="utf-8")
    only_a_file.write_text("\n".join(only_a), encoding="utf-8")
    only_b_file.write_text("\n".join(only_b), encoding="utf-8")

    with summary.open("w", encoding="utf-8") as handle:
        handle.write(f"Compare resultats: {ts}\n")
        handle.write(f"A: {Path(file_a).resolve()}\n")
        handle.write(f"B: {Path(file_b).resolve()}\n")
        handle.write(f"Commun: {len(common)}\n")
        handle.write(f"Seulement dans A: {len(only_a)}\n")
        handle.write(f"Seulement dans B: {len(only_b)}\n")

    logger.info(f"✓ Comparaison terminee: {out_path}")
    return out_path

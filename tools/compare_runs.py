#!/usr/bin/env python
"""
Compare deux runs complets (dossiers run_YYYYMMDD_HHMMSS).
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from tools.compare_lists import compare_files


def find_h2_files(run_dir: Path) -> Dict[str, Path]:
    h2_dir = run_dir / "boutiques_h2"
    if not h2_dir.exists():
        return {}

    files: Dict[str, Path] = {}
    for f in h2_dir.glob("*.txt"):
        match = re.match(r"(\d+)_(.+?)_h2_", f.name)
        if match:
            key = f"{match.group(1)}_{match.group(2)}"
            files[key] = f
    return files


def get_latest_runs(base_dir: Path, count: int = 2) -> List[Path]:
    runs = sorted([d for d in base_dir.glob("run_*") if d.is_dir()], key=lambda x: x.name, reverse=True)[:count]
    return sorted(runs)


def compare_runs(run_a: Path, run_b: Path, out_base: Path | None = None) -> Path:
    run_a = Path(run_a).resolve()
    run_b = Path(run_b).resolve()

    if not run_a.exists() or not run_b.exists():
        raise ValueError(f"L'un des runs n'existe pas: {run_a} ou {run_b}")

    files_a = find_h2_files(run_a)
    files_b = find_h2_files(run_b)

    if not files_a or not files_b:
        raise ValueError("Aucun fichier H2 trouvé dans l'un des runs")

    keys_common = set(files_a) & set(files_b)
    keys_only_a = set(files_a) - set(files_b)
    keys_only_b = set(files_b) - set(files_a)

    if not keys_common:
        raise ValueError("Aucun fichier H2 commun entre les deux runs")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(out_base) / f"compare_runs_{ts}" if out_base else Path.cwd() / "results" / "compare_runs" / f"run_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    global_summary = out_dir / f"global_summary_{ts}.txt"
    with global_summary.open("w", encoding="utf-8") as gs:
        gs.write(f"Compare Runs: {ts}\n")
        gs.write(f"Run A: {run_a}\n")
        gs.write(f"Run B: {run_b}\n")
        gs.write(f"\n--- Fichiers traités ---\n")
        gs.write(f"Communs (appairés): {len(keys_common)}\n")
        gs.write(f"Seulement dans A: {len(keys_only_a)}\n")
        gs.write(f"Seulement dans B: {len(keys_only_b)}\n")
        gs.write(f"\n--- Détails des comparaisons ---\n")

        for idx, key in enumerate(sorted(keys_common), start=1):
            file_a = files_a[key]
            file_b = files_b[key]
            center_dir = out_dir / key
            center_dir.mkdir(parents=True, exist_ok=True)

            compare_files(str(file_a), str(file_b), str(center_dir))

            gs.write(f"{idx:03d}. {key}\n")
            gs.write(f"    A: {file_a.name}\n")
            gs.write(f"    B: {file_b.name}\n")
            gs.write(f"    Résultat: {center_dir}\n")

        if keys_only_a:
            gs.write(f"\n--- Fichiers uniquement dans A ---\n")
            for key in sorted(keys_only_a):
                gs.write(f"  - {key}\n")

        if keys_only_b:
            gs.write(f"\n--- Fichiers uniquement dans B ---\n")
            for key in sorted(keys_only_b):
                gs.write(f"  - {key}\n")

    print(f"Résultats écrits dans: {out_dir}")
    return out_dir

#!/usr/bin/env python
"""
compare_runs.py

Compare deux runs complets (dossiers `run_YYYYMMDD_HHMMSS`).
Boucle automatiquement sur tous les fichiers H2 appairés et compare chaque paire.

Usage (CLI):
    python compare_runs.py path/to/run_A path/to/run_B

Ou (auto-detect les deux derniers runs):
    python compare_runs.py --auto

Exemple:
    python compare_runs.py script/resultat/script_collect_all_h2/run_20260427_100000 script/resultat/script_collect_all_h2/run_20260427_110000
"""
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from compare_lists import compare_files


def find_h2_files(run_dir: Path) -> Dict[str, Path]:
    """
    Trouve tous les fichiers H2 dans un run (boutiques_h2).
    Retourne {center_name: file_path}.
    """
    h2_dir = run_dir / "boutiques_h2"
    if not h2_dir.exists():
        return {}

    files = {}
    for f in h2_dir.glob("*.txt"):
        # Format: NNN_center_name_h2_timestamp.txt
        match = re.match(r"(\d+)_(.+?)_h2_", f.name)
        if match:
            idx = match.group(1)
            name = match.group(2)
            key = f"{idx}_{name}"
            files[key] = f

    return files


def get_latest_runs(base_dir: Path, count: int = 2) -> List[Path]:
    """
    Trouve les `count` runs les plus récents dans base_dir.
    Retourne la liste triée (plus ancien en premier).
    """
    runs = sorted(
        [d for d in base_dir.glob("run_*") if d.is_dir()],
        key=lambda x: x.name,
        reverse=True,
    )[:count]
    return sorted(runs)


def compare_runs(run_a: Path, run_b: Path, out_base: Path | None = None) -> Path:
    """
    Compare deux runs entiers.
    Boucle sur tous les fichiers H2 appairés et génère un résumé global.
    """
    run_a = Path(run_a).resolve()
    run_b = Path(run_b).resolve()

    if not run_a.exists() or not run_b.exists():
        raise ValueError(f"L'un des runs n'existe pas: {run_a} ou {run_b}")

    files_a = find_h2_files(run_a)
    files_b = find_h2_files(run_b)

    if not files_a or not files_b:
        raise ValueError("Aucun fichier H2 trouvé dans l'un des runs")

    # Appairage: cherche les clés communes
    keys_common = set(files_a.keys()) & set(files_b.keys())
    keys_only_a = set(files_a.keys()) - set(files_b.keys())
    keys_only_b = set(files_b.keys()) - set(files_a.keys())

    if not keys_common:
        raise ValueError("Aucun fichier H2 commun entre les deux runs")

    # Créer le dossier de sortie
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = (
        Path(out_base) / f"compare_runs_{ts}"
        if out_base
        else Path.cwd() / "results" / "compare_runs" / f"run_{ts}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    # Résumé global
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

        # Boucle sur tous les fichiers appairés
        for idx, key in enumerate(sorted(keys_common), start=1):
            file_a = files_a[key]
            file_b = files_b[key]

            # Créer un sous-dossier pour chaque centre
            center_dir = out_dir / key
            center_dir.mkdir(parents=True, exist_ok=True)

            # Comparer la paire
            compare_files(str(file_a), str(file_b), str(center_dir))

            # Écrire ligne dans le résumé
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


def main():
    parser = argparse.ArgumentParser(
        description="Comparer deux runs complets (boucle automatique sur tous les fichiers H2)."
    )
    parser.add_argument(
        "run_a", nargs="?", help="Chemin vers le premier run (ou --auto)"
    )
    parser.add_argument("run_b", nargs="?", help="Chemin vers le second run")
    parser.add_argument(
        "--auto", action="store_true", help="Auto-détecter les deux derniers runs"
    )
    parser.add_argument("--out", help="Dossier de sortie (optionnel)")
    args = parser.parse_args()

    if args.auto or (args.run_a == "--auto"):
        base_dir = (
            Path.cwd() / "script" / "resultat" / "script_collect_all_h2"
        )
        latest = get_latest_runs(base_dir, count=2)
        if len(latest) < 2:
            raise ValueError(
                f"Impossible de trouver 2 runs dans {base_dir}"
            )
        run_a, run_b = latest
        print(f"Auto-détecté: {run_a.name} vs {run_b.name}")
    else:
        run_a = args.run_a
        run_b = args.run_b
        if not run_a or not run_b:
            parser.print_help()
            raise ValueError("Fournir deux chemins de run ou utiliser --auto")

    compare_runs(run_a, run_b, args.out)


if __name__ == "__main__":
    main()

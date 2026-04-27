#!/usr/bin/env python
"""
compare_lists.py

Compare deux fichiers texte contenant des listes (une valeur par ligne).
Génère un répertoire daté dans `results/compare/` contenant:
 - compare_summary_TIMESTAMP.txt
 - only_in_a.txt
 - only_in_b.txt
 - common.txt

Usage (CLI):
    python compare_lists.py path/to/a.txt path/to/b.txt

Exporte aussi une fonction `compare_files(a,b, out_dir=None)` pour réutilisation.
"""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Set, Tuple


def read_list_file(path: Path) -> List[str]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]
    # Filter empty lines
    return [l for l in lines if l]


def compare_items(a_items: List[str], b_items: List[str]) -> Tuple[Set[str], Set[str], Set[str]]:
    set_a = set(a_items)
    set_b = set(b_items)
    common = set_a & set_b
    only_a = set_a - set_b
    only_b = set_b - set_a
    return only_a, only_b, common


def ensure_out_dir(base: Path) -> Path:
    base.mkdir(parents=True, exist_ok=True)
    return base


def write_list(path: Path, items: List[str]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(f"{item}\n")


def compare_files(path_a: str, path_b: str, out_dir: str | None = None) -> Path:
    p_a = Path(path_a)
    p_b = Path(path_b)

    a_items = read_list_file(p_a)
    b_items = read_list_file(p_b)

    only_a, only_b, common = compare_items(a_items, b_items)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_out = Path(out_dir) if out_dir else Path.cwd() / "results" / "compare" / f"run_{ts}"
    base_out = ensure_out_dir(base_out)

    summary_path = base_out / f"compare_summary_{ts}.txt"
    only_a_path = base_out / "only_in_a.txt"
    only_b_path = base_out / "only_in_b.txt"
    common_path = base_out / "common.txt"

    # Write detailed files
    write_list(only_a_path, sorted(only_a))
    write_list(only_b_path, sorted(only_b))
    write_list(common_path, sorted(common))

    # Summary
    with summary_path.open("w", encoding="utf-8") as s:
        s.write(f"Compare run: {ts}\n")
        s.write(f"File A: {p_a.resolve()}\n")
        s.write(f"File B: {p_b.resolve()}\n")
        s.write(f"Total A (non-empty lines): {len(a_items)}\n")
        s.write(f"Total B (non-empty lines): {len(b_items)}\n")
        s.write(f"Common: {len(common)}\n")
        s.write(f"Only in A: {len(only_a)}\n")
        s.write(f"Only in B: {len(only_b)}\n")
        s.write("\nFiles:\n")
        s.write(f" - {only_a_path}\n")
        s.write(f" - {only_b_path}\n")
        s.write(f" - {common_path}\n")

    return base_out


def main():
    parser = argparse.ArgumentParser(description="Comparer deux fichiers liste et générer résultat daté.")
    parser.add_argument("a", help="Chemin vers le premier fichier (A)")
    parser.add_argument("b", help="Chemin vers le second fichier (B)")
    parser.add_argument("--out", help="Dossier de sortie (optionnel)")
    args = parser.parse_args()

    out = compare_files(args.a, args.b, args.out)
    print(f"Résultats écrits dans: {out}")


if __name__ == "__main__":
    main()

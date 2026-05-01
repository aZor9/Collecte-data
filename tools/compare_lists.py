#!/usr/bin/env python
"""
Compare deux fichiers texte contenant des listes (une valeur par ligne).
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List, Set, Tuple


def read_list_file(path: Path) -> List[str]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]
    return [line for line in lines if line]


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

    write_list(only_a_path, sorted(only_a))
    write_list(only_b_path, sorted(only_b))
    write_list(common_path, sorted(common))

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

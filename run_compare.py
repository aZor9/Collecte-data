#!/usr/bin/env python
"""Compatibilité: exemples de comparaison, désormais pilotés par main.py."""

from pathlib import Path

from tools.compare_lists import compare_files
from tools.compare_runs import compare_runs, get_latest_runs


def mode_boutiques():
    # Exemple: comparer la liste de titres d'une boutique à deux dates
    # Remplace ces chemins par les fichiers que tu veux comparer
    a = Path("script/resultat/script_h2/h2_titles_20260408_160000.txt")
    b = Path("script/resultat/script_h2/h2_titles_20260409_160000.txt")
    out = compare_files(str(a), str(b))
    print(f"Résultat: {out}")


def mode_centres():
    # Option alternative: comparer deux fichiers contenant des listes de centres
    # (décommente si besoin et commente `mode_boutiques()` ci-dessus)
    a = Path("script/resultat/script_collect_all_h2/run_20260408_120000/centers_urls/boutiques_urls_20260408_120000.txt")
    b = Path("script/resultat/script_collect_all_h2/run_20260409_120000/centers_urls/boutiques_urls_20260409_120000.txt")
    out = compare_files(str(a), str(b))
    print(f"Résultat: {out}")


def mode_compare_runs():
    # Comparer deux runs entiers: auto-détecte les deux derniers runs
    base_dir = Path("results") / "compare_runs"
    runs = get_latest_runs(base_dir, count=2)
    if len(runs) < 2:
        print(f"Erreur: impossible de trouver 2 runs dans {base_dir}")
        return
    out = compare_runs(runs[0], runs[1])
    print(f"Résultat: {out}")


if __name__ == "__main__":
    # Par défaut on lance `mode_boutiques`. Pour changer, commente et décommente l'autre.
    mode_boutiques()
    # mode_centres()
    # mode_compare_runs()

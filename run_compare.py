#!/usr/bin/env python
"""
run_compare.py

Script helper qui appelle `compare_lists.compare_files`.
Contient deux modes d'usage (décommenter l'un et commenter l'autre pour basculer):
 - comparer deux fichiers boutique à deux dates différentes
 - (option commentée) comparer deux listes de centres

Usage:
    python run_compare.py
"""
from pathlib import Path
from compare_lists import compare_files


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


if __name__ == "__main__":
    # Par défaut on lance `mode_boutiques`. Pour changer, commente et décommente `mode_centres()`.
    mode_boutiques()
    # mode_centres()

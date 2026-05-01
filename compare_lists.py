#!/usr/bin/env python
"""Compatibilité: redirige vers tools.compare_lists."""

from tools.compare_lists import compare_files


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Comparer deux fichiers liste et générer résultat daté.")
    parser.add_argument("a", help="Chemin vers le premier fichier (A)")
    parser.add_argument("b", help="Chemin vers le second fichier (B)")
    parser.add_argument("--out", help="Dossier de sortie (optionnel)")
    args = parser.parse_args()

    out = compare_files(args.a, args.b, args.out)
    print(f"Résultats écrits dans: {out}")

#!/usr/bin/env python
"""Compatibilité: redirige vers tools.compare_runs."""

from tools.compare_runs import compare_runs, get_latest_runs


def main():
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="Comparer deux runs complets (boucle automatique sur tous les fichiers H2)."
    )
    parser.add_argument("run_a", nargs="?", help="Chemin vers le premier run (ou --auto)")
    parser.add_argument("run_b", nargs="?", help="Chemin vers le second run")
    parser.add_argument("--auto", action="store_true", help="Auto-détecter les deux derniers runs")
    parser.add_argument("--out", help="Dossier de sortie (optionnel)")
    args = parser.parse_args()

    if args.auto or (args.run_a == "--auto"):
        base_dir = Path.cwd() / "results" / "compare_runs"
        latest = get_latest_runs(base_dir, count=2)
        if len(latest) < 2:
            raise ValueError(f"Impossible de trouver 2 runs dans {base_dir}")
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

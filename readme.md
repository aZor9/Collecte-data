# Projet scolaire - Collecte de donnees

Objectif:
Comparer des centres commerciaux concurrents en recuperant des informations depuis leurs pages boutiques.

Technologie utilisee:
- Python
- Selenium

## Sites cibles
- https://www.centre-commercial.fr/labege2/boutiques/
- https://www.centre-commercial.fr/carrefour-st-jean/boutiques/

## Structure actuelle
- `main.py` : lance les scripts dans l'ordre
- `script/script_title.py` : recupere le titre de la page
- `script/script_html.py` : recupere tout le HTML de la page
- `script/script_h2.py` : recupere les titres `h2.custom-h2` d'une page boutiques
- `script/script_collect_all_h2.py` : collecte toutes les URLs centres depuis la home, ajoute `/boutiques/`, puis scrape les titres H2 pour chaque centre
- `script/resultat/` : dossier des fichiers generes

## Installation (Windows / PowerShell)
1. Creer le venv:
	`python -m venv .venv`
2. Activer le venv:
	`.\.venv\Scripts\Activate.ps1`
3. Installer Selenium:
	`pip install selenium`

Si PowerShell bloque l'activation, executer une fois:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Execution
Lancer toute la chaine:
`python .\main.py`

## Arret du venv
`deactivate`

## Fichiers générés
- `script/resultat/script_title/title_YYYYMMDD_HHMMSS.txt`
- `script/resultat/script_html/html_YYYYMMDD_HHMMSS.html`
- `script/resultat/script_h2/h2_titles_YYYYMMDD_HHMMSS.txt`
- `script/resultat/script_collect_all_h2/run_YYYYMMDD_HHMMSS/`

## Comparer des listes (nouveau)
Tu peux comparer deux fichiers texte (une valeur par ligne) avec le script `compare_lists.py`.

Exemples :

- Comparer deux fichiers manuellement :
```bash
python compare_lists.py path/to/a.txt path/to/b.txt
```

- Utiliser le helper `run_compare.py` (exemples prêts à modifier) :
```bash
python run_compare.py
```

Résultats :
- Les résultats sont écrits dans `results/compare/run_YYYYMMDD_HHMMSS/` (summary + `only_in_a.txt`, `only_in_b.txt`, `common.txt`).

Remarque : modifie les chemins d'exemple dans `run_compare.py` pour pointer vers tes fichiers réels. Le helper contient deux modes (boutiques vs listes de centres) ; commente/décommente pour changer de mode.

## Comparer deux runs complets (collecte à deux dates différentes)
Utilise `compare_runs.py` pour comparer automatiquement deux exécutions complètes du script de collecte.
Le script boucle sur tous les fichiers H2 appairés et génère un résumé global.

### Auto-détect (deux derniers runs) :
```bash
python compare_runs.py --auto
```

### Manuel (chemins spécifiques) :
```bash
python compare_runs.py script/resultat/script_collect_all_h2/run_20260427_100000 script/resultat/script_collect_all_h2/run_20260427_110000
```

### Via le helper `run_compare.py` :
Décommente la fonction `mode_compare_runs()` dans `run_compare.py` et exécute :
```bash
python run_compare.py
```

Résultats :
- Chaque centre comparé a son sous-dossier dans `results/compare_runs/run_YYYYMMDD_HHMMSS/`
- Résumé global dans `global_summary_YYYYMMDD_HHMMSS.txt`
- Fichiers absents d'un run sont listés séparément

## Option Selenium headless
Tu peux exécuter les scripts Selenium en mode headless (sans interface graphique) en définissant la variable d'environnement `SELENIUM_HEADLESS` à `1` ou `true`.

PowerShell (temporaire pour la session) :
```powershell
$env:SELENIUM_HEADLESS=1
python .\main.py
```

Commande Windows (cmd.exe) :
```cmd
set SELENIUM_HEADLESS=1
python .\main.py
```

Pour revenir en mode normal, ferme le terminal ou réinitialise la variable (PowerShell) :
```powershell
Remove-Item Env:\SELENIUM_HEADLESS
```
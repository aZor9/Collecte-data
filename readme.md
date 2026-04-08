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
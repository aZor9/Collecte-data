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
- `script/resultat/title.txt`
- `script/resultat/html.html`
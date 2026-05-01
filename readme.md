# Projet de collecte de données

Pipeline de scraping modulaire pour deux sources:
- Carrefour
- Grand Frais

## Vision

```text
[1. EXTRACTION HTML] → [2. TRANSFORMATION CSV] → [3. COMPARAISON]
```

Chaque source a ses deux premières étapes dédiées:
- Carrefour: extraction HTML + transformation CSV
- Grand Frais: extraction HTML + transformation CSV

La comparaison est une étape séparée, branchée sur les CSV finaux.
Elle compare les deux derniers CSV finaux d'une meme source.

## Arborescence utile

- `main.py` : orchestrateur principal
- `sources/carrefour/` : extraction + transformation Carrefour
- `sources/grandfrais/` : extraction + transformation Grand Frais
- `tools/compare_results.py` : comparaison finale des CSV
- `launchers/` : scripts de lancement dédiés
- `config/settings.py` : URLs, timeouts, user-agent, sources
- `scraper/` : driver Selenium et navigation rapide
- `loader/` et `utils/` : export CSV, logs, helpers

## Installation (Windows / PowerShell)

- Creer le venv: `python -m venv .venv`
- Activer le venv: `.\.venv\Scripts\Activate.ps1`
- Installer Selenium: `pip install selenium`

Si PowerShell bloque l'activation, executer une fois:
- `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Note:
- Pour executer tout le pipeline (extraction + transformation + comparaison), installer aussi les dependances du projet avec `pip install -r requirements.txt`.

## Execution

- Lancer toute la chaine: `python .\main.py`

Comportement actuel de cette commande:
- Elle lance le pipeline par defaut sur Carrefour avec les etapes extraction + transformation.
- La comparaison se lance ensuite via `python .\launchers\run_compare_results.py` ou `python .\main.py --stage compare`.

## Arret du venv

- `deactivate`

## Lancer le projet

### Carrefour
- Extraction HTML seule: `python .\launchers\run_carrefour_extract_html.py`
- Transformation CSV seule: `python .\launchers\run_carrefour_transform_csv.py`
- Extraction + transformation: `python .\launchers\run_carrefour_pipeline.py`

### Grand Frais
- Extraction HTML seule: `python .\launchers\run_grandfrais_extract_html.py`
- Transformation CSV seule: `python .\launchers\run_grandfrais_transform_csv.py`
- Extraction + transformation: `python .\launchers\run_grandfrais_pipeline.py`

### Comparaison
- Comparaison des CSV finaux: `python .\launchers\run_compare_results.py`

### Point d'entrée principal
- `python .\main.py --source carrefour --stage all`
- `python .\main.py --source grandfrais --stage all`
- `python .\main.py --stage compare`

Note:
- `--stage compare` utilise la source passee avec `--source` et compare ses deux derniers CSV finaux.
- Exemple: `python .\main.py --source grandfrais --stage compare`

## Données extraites

Champs visés:
- nom
- horaires
- description
- catégorie
- taille / superficie quand disponible
- propriétaire quand disponible
- URL source
- date de scraping

## Notes techniques

- User-agent activé côté Selenium.
- Navigation raccourcie pour passer moins de temps sur les pages.
- Les noms sont normalisés pour gérer les variantes majuscules / minuscules.
- Le pipeline est séparé par source et par étape pour rester lisible et testable.
- Si Carrefour renvoie une page de blocage (`Sorry, you have been blocked`), le pipeline:
	- arrête proprement l'extraction,
	- loggue clairement le blocage,
	- et peut continuer sur la transformation en utilisant les HTML déjà présents (fallback configurable dans `main.py`, variable `ALLOW_TRANSFORM_IF_BLOCKED`).

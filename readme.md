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

## Arborescence utile

- `main.py` : orchestrateur principal
- `sources/carrefour/` : extraction + transformation Carrefour
- `sources/grandfrais/` : extraction + transformation Grand Frais
- `tools/compare_results.py` : comparaison finale des CSV
- `launchers/` : scripts de lancement dédiés
- `config/settings.py` : URLs, timeouts, user-agent, sources
- `scraper/` : driver Selenium et navigation rapide
- `loader/` et `utils/` : export CSV, logs, helpers

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

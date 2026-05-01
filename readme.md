# Projet scolaire - Collecte de donnees

Objectif: construire un pipeline de scraping modulaire, robuste et extensible, avec plusieurs sources de collecte.

Technologies utilisees:
- Python
- Selenium
- Pandas
- BeautifulSoup

## Vision du pipeline

```text
[SELENIUM SCRAPER] → [HTML SAVE] → [PARSE → CSV] → [TRANSFORM] → [DATASET FINAL]
```

L'objectif est de separer clairement chaque etape:
- scraping Selenium avec comportement humain
- sauvegarde du HTML brut
- parsing HTML vers donnees structurees
- nettoyage et normalisation
- enrichissement metier et export final

## Structure du projet

- `config/settings.py` : URLs, options Selenium, mapping de categories, sources
- `scraper/driver.py` : creation du driver Chrome
- `scraper/navigator.py` : navigation, scroll, hover, cookies
- `scraper/saver.py` : sauvegarde HTML et JSON bruts
- `scraper/collector.py` : orchestration du scraping par source
- `parser/html_parser.py` : parsing HTML generic et specialise
- `transformer/cleaner.py` : nettoyage des champs
- `transformer/normalizer.py` : normalisation, validation, deduplication
- `transformer/enricher.py` : metriques metier et champs calcules
- `loader/csv_loader.py` : export et lecture CSV
- `utils/` : logger, retry, helpers
- `main.py` : pipeline complet

## Installation (Windows / PowerShell)

1. Creer le venv:
	`python -m venv .venv`
2. Activer le venv:
	`\.\.venv\Scripts\Activate.ps1`
3. Installer les dependances:
	`pip install -r requirements.txt`

Si PowerShell bloque l'activation, executer une fois:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Execution

Lancer tout le pipeline:

```bash
python main.py
```

## Sorties

Les resultats sont ecrits dans:
- `data/raw/` : HTML brut par source
- `data/interim/` : donnees extraites en JSON
- `data/processed/` : CSV final, resume texte, metriques JSON
- `logs/` : logs d'execution

## Donnees ciblees

Champs vises dans le dataset final:
- nom
- categorie normalisee
- taille / superficie
- date d'ouverture
- date de fermeture
- description
- groupe proprietaire
- source
- date de scraping

## Ajouter une nouvelle source

1. Ajouter sa configuration dans `config/settings.py`
2. Brancher son parser dans `parser/html_parser.py`
3. Lancer `python main.py`

## Notes

- Le projet est pense pour supporter plusieurs sources de scraping.
- La categorie `fashion` est normalisee en `mode`.
- La logique de retry et de logs est centralisee dans `utils/`.

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
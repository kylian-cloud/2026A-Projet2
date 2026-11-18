# Prédire la note NBA 2K d'un joueur à partir de ses vraies stats

Projet 2 INF1007 (A2026) — Kylian Amani (2445524) et Aziz Boly (2465875)

## Description
<!-- TODO (A) : 3-4 phrases. Que fait l'application ? Pour qui ? -->

## Jeu de données
- **Source** : <!-- TODO : lien du dépôt GitHub d'où vient le CSV -->
- **Postes des joueurs** : ajoutés à partir de Basketball-Reference (tableaux de stats par match, saisons 2014-15 à 2019-20)
- **Licence** : aucune licence explicite trouvée. <!-- TODO : à préciser après la validation B -->
- **Taille** : 2 412 lignes (un joueur pour une saison), saisons 2014-15 à 2019-20

## Installation
```bash
git clone <lien du dépôt>
cd 2026A-Projet2
pip install -r requirements.txt
```

## Lancement
```bash
python -m src.main entrainer   # entraîne et sauvegarde le modèle (une fois)
python -m src.main             # lance l'interface Streamlit
pytest                      # lance les tests
coverage run -m pytest && coverage report   # mesure la couverture
```

## Structure du code
```
src/
├── donnees.py      # (A) lecture, nettoyage, classes de variables, JeuDeDonnees
├── exceptions.py   # (A) exceptions personnalisées
├── modele.py       # (B) entraînement, évaluation, sauvegarde, prédiction
├── historique.py   # (B) historique des prédictions
├── interface.py    # (A + B) interface graphique (Streamlit)
└── main.py         # (B) point d'entrée
```
<!-- TODO : schéma des classes (héritage, composition) -->

## Résultats du modèle
Les deux scores sont des RMSE calculées sur le même ensemble de test. La référence
prédit la moyenne des notes d'entraînement; la forêt aléatoire encode `POS` dans
un pipeline scikit-learn. Les valeurs exactes sont affichées par la commande
d'entraînement et enregistrées dans `modeles/metadonnees.json`.

| Modèle | Métrique | Valeur |
|---|---|---|
| Référence (moyenne) | RMSE | `metrique.reference` dans le JSON |
| Forêt aléatoire | RMSE | `metrique.modele` dans le JSON |

## Couverture des tests
<!-- TODO : résultat de `coverage report` -->

## Outil du chapitre 7
Le décorateur `@chronometrer` mesure et affiche la durée de l'entraînement du modèle.

## Documentation consultée
<!-- Au moins 3 pages : pandas, scikit-learn, technologie d'interface -->
- 
- 
- 

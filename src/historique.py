"""Historique des prédictions (personne B).

Chaque prédiction est ajoutée à un fichier et peut être relue depuis l'interface.
"""

import csv
import os

DOSSIER_RACINE = os.path.dirname(os.path.dirname(__file__))
FICHIER_HISTORIQUE = os.path.join(DOSSIER_RACINE, "historique.csv")


def ajouter_prediction(entrees: dict, note_predite: float, chemin: str = FICHIER_HISTORIQUE) -> None:
    """Ajoute une ligne à l'historique (crée le fichier avec l'en-tête s'il n'existe pas).

    Args:
        entrees: valeurs saisies par l'utilisateur.
        note_predite: résultat du modèle.
        chemin: fichier de l'historique.
    """
    ligne = dict(entrees)
    ligne["note_predite"] = float(note_predite)

    fichier_existant = os.path.exists(chemin) and os.path.getsize(chemin) > 0
    if fichier_existant:
        with open(chemin, "r", newline="", encoding="utf-8") as fichier:
            colonnes = next(csv.reader(fichier), None)
        if not colonnes:
            fichier_existant = False
            colonnes = [*entrees.keys(), "note_predite"]
    else:
        colonnes = [*entrees.keys(), "note_predite"]

    with open(chemin, "a", newline="", encoding="utf-8") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=colonnes, extrasaction="ignore")
        if not fichier_existant:
            ecrivain.writeheader()
        ecrivain.writerow(ligne)


def lire_historique(chemin: str = FICHIER_HISTORIQUE) -> list[dict]:
    """Retourne toutes les prédictions enregistrées (liste vide si le fichier n'existe pas)."""
    if not os.path.exists(chemin) or os.path.getsize(chemin) == 0:
        return []

    with open(chemin, "r", newline="", encoding="utf-8") as fichier:
        return list(csv.DictReader(fichier))

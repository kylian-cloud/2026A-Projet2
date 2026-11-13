"""Historique des prédictions (personne B).

Chaque prédiction est ajoutée à un fichier et peut être relue depuis l'interface.
"""

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
    # TODO (B) : os.path.exists, with open(..., "a")
    raise NotImplementedError


def lire_historique(chemin: str = FICHIER_HISTORIQUE) -> list[dict]:
    """Retourne toutes les prédictions enregistrées (liste vide si le fichier n'existe pas)."""
    # TODO (B)
    raise NotImplementedError

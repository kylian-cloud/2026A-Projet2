"""Entraînement, évaluation, sauvegarde et prédiction (personne B).

Contient la classe Modele et le décorateur chronometrer (outil du chapitre 7).
Le modèle exact et la métrique seront fixés à la validation C.
"""

import os
import time
from functools import wraps

import numpy as np
import pandas as pd

DOSSIER_MODELES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "modeles")
FICHIER_MODELE = os.path.join(DOSSIER_MODELES, "modele.joblib")
FICHIER_METADONNEES = os.path.join(DOSSIER_MODELES, "metadonnees.json")
GRAINE = 42


def chronometrer(fonction):
    """Décorateur (chapitre 7) : affiche la durée d'exécution de la fonction décorée."""
    # TODO (B) : définir une fonction interne `enveloppe` (avec @wraps(fonction))
    #            qui mesure time.perf_counter() avant et après l'appel.
    #            En attendant, le décorateur retourne la fonction telle quelle
    #            pour que le module reste importable.
    return fonction


def rmse_numpy(y_vrai: np.ndarray, y_predit: np.ndarray) -> float:
    """Calcule la métrique avec NumPy, sans boucle Python (exigence du chapitre 12).

    À comparer dans un test avec la valeur de scikit-learn (pytest.approx).
    Remplacer par la métrique choisie à la validation C si ce n'est pas la RMSE.

    Raises:
        ValueError: si les deux tableaux n'ont pas la même taille ou sont vides.
    """
    # TODO (B)
    raise NotImplementedError


class Modele:
    """Encapsule le modèle scikit-learn, sa référence et ses résultats."""

    def __init__(self) -> None:
        # TODO (B) : attributs protégés (_modele, _reference, _scores…)
        raise NotImplementedError

    def separer(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Sépare entraînement / test avec train_test_split et random_state=GRAINE."""
        # TODO (B)
        raise NotImplementedError

    def entrainer_reference(self) -> float:
        """Entraîne le modèle trivial (prédit la moyenne) et retourne son score sur le test."""
        # TODO (B)
        raise NotImplementedError

    @chronometrer
    def entrainer(self) -> float:
        """Entraîne le modèle choisi et retourne son score sur l'ensemble de test."""
        # TODO (B) : penser à encoder POS (ex. OneHotEncoder dans un Pipeline)
        raise NotImplementedError

    def predire(self, entrees: dict) -> float:
        """Prédit la note 2K pour un joueur.

        Args:
            entrees: {"POS": "PG", "AGE": 25.0, ...} — valeurs déjà validées par l'interface.

        Returns:
            La note prédite.
        """
        # TODO (B)
        raise NotImplementedError

    def sauvegarder(self, variables: list[dict]) -> None:
        """Enregistre le modèle (joblib) et le JSON de métadonnées (format : voir document d'Aziz).

        Args:
            variables: descriptions des variables (Variable.vers_dict() pour chacune).
        """
        # TODO (B) : os.path, with open(...)
        raise NotImplementedError

    @classmethod
    def charger(cls) -> "Modele":
        """Recharge un modèle sauvegardé (l'interface ne ré-entraîne jamais).

        Raises:
            ModeleIntrouvableError: si un des fichiers n'existe pas.
        """
        # TODO (B)
        raise NotImplementedError

    # TODO (B) : __str__ (ex. « Forêt aléatoire — RMSE 3,1 (référence 5,8) »)


def lire_metadonnees(chemin: str = FICHIER_METADONNEES) -> dict:
    """Lit le JSON de métadonnées.

    Raises:
        ModeleIntrouvableError: si le fichier n'existe pas.
    """
    # TODO (B)
    raise NotImplementedError

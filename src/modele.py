"""Entraînement, évaluation, sauvegarde et prédiction (personne B).

Contient la classe Modele et le décorateur chronometrer (outil du chapitre 7).
La forêt aléatoire est évaluée avec la RMSE et comparée à une référence moyenne.
"""

import json
import os
import time
from functools import wraps

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.exceptions import ModeleIntrouvableError

DOSSIER_MODELES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "modeles")
FICHIER_MODELE = os.path.join(DOSSIER_MODELES, "modele.joblib")
FICHIER_METADONNEES = os.path.join(DOSSIER_MODELES, "metadonnees.json")
GRAINE = 42
NOM_MODELE = "Forêt aléatoire"
CIBLE = "rankings"


def chronometrer(fonction):
    """Décorateur (chapitre 7) : affiche la durée d'exécution de la fonction décorée."""
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        debut = time.perf_counter()
        resultat = fonction(*args, **kwargs)
        print("Durée :", round(time.perf_counter() - debut, 1), "s")
        return resultat
    return enveloppe


def rmse_numpy(y_vrai: np.ndarray, y_predit: np.ndarray) -> float:
    """Calcule la métrique avec NumPy, sans boucle Python (exigence du chapitre 12).

    À comparer dans un test avec la valeur de scikit-learn (pytest.approx).
    La RMSE est exprimée dans la même unité que la cible (points de note).

    Raises:
        ValueError: si les deux tableaux n'ont pas la même taille ou sont vides.
    """

    y_vrai = np.asarray(y_vrai)
    y_predit = np.asarray(y_predit)
    if y_vrai.shape != y_predit.shape or y_vrai.size == 0:
        raise ValueError("Les tableaux doivent avoir la même taille et ne pas être vides.")
    erreurs = y_vrai - y_predit
    return float(np.sqrt(np.mean(erreurs ** 2)))


class Modele:
    """Encapsule le modèle scikit-learn, sa référence et ses résultats."""

    def __init__(self) -> None:
        self._modele = None
        self._reference = None
        self._scores = None
        self._X_train = None
        self._X_test = None
        self._y_train = None
        self._y_test = None

    @property
    def modele(self):
        return self._modele

    @property
    def reference(self):
        return self._reference

    @property
    def scores(self):
        return self._scores


    def separer(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Sépare entraînement / test de façon reproductible avec GRAINE."""
        self._X_train, self._X_test, self._y_train, self._y_test = train_test_split(
            X, y, random_state=GRAINE
        )


    def entrainer_reference(self) -> float:
        """Entraîne le modèle trivial (prédit la moyenne) et retourne son score sur le test."""
        if self._X_train is None or self._X_test is None:
            raise RuntimeError("Appelez separer() avant d'entraîner la référence.")

        self._reference = DummyRegressor(strategy="mean")
        self._reference.fit(self._X_train, self._y_train)
        predictions = self._reference.predict(self._X_test)
        score = rmse_numpy(self._y_test, predictions)
        self._scores = {"reference": score}
        return score

    @chronometrer
    def entrainer(self) -> float:
        """Entraîne le modèle choisi et retourne son score sur l'ensemble de test."""
        if self._X_train is None or self._X_test is None:
            raise RuntimeError("Appelez separer() avant d'entraîner le modèle.")

        preparation = ColumnTransformer(
            transformers=[
                ("poste", OneHotEncoder(handle_unknown="ignore"), ["POS"]),
            ],
            remainder="passthrough",
        )
        self._modele = Pipeline(
            steps=[
                ("preparation", preparation),
                (
                    "regression",
                    RandomForestRegressor(n_estimators=300, random_state=GRAINE, n_jobs=-1),
                ),
            ]
        )
        self._modele.fit(self._X_train, self._y_train)
        score_modele = rmse_numpy(self._y_test, self._modele.predict(self._X_test))

        if self._reference is None:
            score_reference = self.entrainer_reference()
        else:
            score_reference = rmse_numpy(
                self._y_test, self._reference.predict(self._X_test)
            )
        self._scores = {"modele": score_modele, "reference": score_reference}
        return score_modele

    def predire(self, entrees: dict) -> float:
        """Prédit la note 2K pour un joueur.

        Args:
            entrees: {"POS": "PG", "AGE": 25.0, ...} — valeurs déjà validées par l'interface.

        Returns:
            La note prédite.
        """
        if self._modele is None:
            raise ModeleIntrouvableError("Aucun modèle n'est chargé ou entraîné.")

        colonnes = getattr(self._modele, "feature_names_in_", list(entrees))
        ligne = pd.DataFrame([entrees], columns=colonnes)
        return float(self._modele.predict(ligne)[0])

    def sauvegarder(self, variables: list[dict]) -> None:
        """Enregistre le modèle (joblib) et le JSON de métadonnées (format : voir document d'Aziz).

        Args:
            variables: descriptions des variables (Variable.vers_dict() pour chacune).
        """
        if self._modele is None or self._scores is None:
            raise RuntimeError("Le modèle doit être entraîné avant d'être sauvegardé.")

        os.makedirs(os.path.dirname(os.path.abspath(FICHIER_MODELE)), exist_ok=True)
        os.makedirs(os.path.dirname(os.path.abspath(FICHIER_METADONNEES)), exist_ok=True)
        joblib.dump(self._modele, FICHIER_MODELE)

        metadonnees = {
            "variables": variables,
            "cible": CIBLE,
            "modele": NOM_MODELE,
            "metrique": {
                "nom": "RMSE",
                "modele": self._scores.get("modele"),
                "reference": self._scores.get("reference"),
            },
        }
        with open(FICHIER_METADONNEES, "w", encoding="utf-8") as fichier:
            json.dump(metadonnees, fichier, ensure_ascii=False, indent=2)

    @classmethod
    def charger(cls) -> "Modele":
        """Recharge un modèle sauvegardé (l'interface ne ré-entraîne jamais).

        Raises:
            ModeleIntrouvableError: si un des fichiers n'existe pas.
        """
        if not os.path.exists(FICHIER_MODELE) or not os.path.exists(FICHIER_METADONNEES):
            raise ModeleIntrouvableError(
                "Modèle introuvable. Lancez d'abord `python -m src.main entrainer`."
            )

        instance = cls()
        instance._modele = joblib.load(FICHIER_MODELE)
        metadonnees = lire_metadonnees(FICHIER_METADONNEES)
        resultats = metadonnees.get("metrique", {})
        if isinstance(resultats, dict):
            instance._scores = {
                "modele": resultats.get("modele"),
                "reference": resultats.get("reference"),
            }
        return instance

    def __str__(self) -> str:
        """Résume le modèle et ses performances sur l'ensemble de test."""
        if not self._scores or self._scores.get("modele") is None:
            return f"{NOM_MODELE} — non entraîné"

        score = f"{self._scores['modele']:.1f}".replace(".", ",")
        texte = f"{NOM_MODELE} — RMSE {score}"
        reference = self._scores.get("reference")
        if reference is not None:
            score_reference = f"{reference:.1f}".replace(".", ",")
            texte += f" (référence {score_reference})"
        return texte


def lire_metadonnees(chemin: str = FICHIER_METADONNEES) -> dict:
    """Lit le JSON de métadonnées.

    Raises:
        ModeleIntrouvableError: si le fichier n'existe pas.
    """
    if not os.path.exists(chemin):
        raise ModeleIntrouvableError(f"Métadonnées introuvables : {chemin}")

    with open(chemin, "r", encoding="utf-8") as fichier:
        return json.load(fichier)

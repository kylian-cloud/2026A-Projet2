"""Lecture, nettoyage et description des données (personne A).

Contient :
- les fonctions de chargement et de nettoyage du CSV ;
- la hiérarchie Variable → VariableNumerique / VariableCategorielle (héritage + polymorphisme) ;
- la classe JeuDeDonnees (composition : elle contient une liste de Variable).
"""

import os
from abc import ABC, abstractmethod

import pandas as pd

# --- Constantes -----------------------------------------------------------

DOSSIER_DONNEES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "donnees")
FICHIER_CSV = os.path.join(DOSSIER_DONNEES, "nba2k_stats_positions.csv")

VARIABLES_NUMERIQUES = ["AGE", "GP", "MIN", "PTS", "REB", "AST", "STL", "BLK", "FG%"]
VARIABLES_CATEGORIELLES = ["POS"]
CIBLE = "rankings"

ETIQUETTES = {
    "POS": "Poste",
    "AGE": "Âge",
    "GP": "Matchs joués",
    "MIN": "Minutes par match",
    "PTS": "Points par match",
    "REB": "Rebonds par match",
    "AST": "Passes décisives par match",
    "STL": "Interceptions par match",
    "BLK": "Contres par match",
    "FG%": "% de tirs réussis",
}


# --- Fonctions ------------------------------------------------------------

def charger_csv(chemin: str = FICHIER_CSV) -> pd.DataFrame:
    """Charge le CSV brut.

    Args:
        chemin: chemin du fichier CSV.

    Returns:
        Le DataFrame brut, sans modification.

    Raises:
        FileNotFoundError: si le fichier n'existe pas (vérifier avec os.path.exists).
        DonneeInvalideError: si une colonne attendue manque.
    """
    # TODO (A)
    raise NotImplementedError


def nettoyer(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie le DataFrame brut.

    Étapes décidées (voir DECISIONS.md) :
    1. retirer la colonne d'index sans nom et PLAYER ;
    2. garder seulement VARIABLES_NUMERIQUES + VARIABLES_CATEGORIELLES + CIBLE ;
    3. retirer les 4 lignes où FG% = 0 sans aucun tir tenté (FGA == 0) ;
    4. vérifier : aucune valeur manquante, aucun doublon.

    Args:
        df: DataFrame brut retourné par charger_csv.

    Returns:
        Un nouveau DataFrame propre (le DataFrame d'origine n'est pas modifié).

    Raises:
        DonneeInvalideError: si une vérification échoue.
    """
    # TODO (A) — format de retour à confirmer (voir le document d'Aziz)
    raise NotImplementedError


def tracer_exploration(df: pd.DataFrame, chemin_image: str) -> None:
    """Trace le graphique d'exploration (PTS vs note 2K, coloré par poste) et l'enregistre avec savefig.

    Args:
        df: DataFrame propre.
        chemin_image: chemin du fichier PNG à créer.
    """
    # TODO (A)
    raise NotImplementedError


# --- Classes de variables (héritage + polymorphisme) --------------------

class Variable(ABC):
    """Variable d'entrée du modèle (classe abstraite)."""

    def __init__(self, nom: str, etiquette: str) -> None:
        # TODO (A) : attributs protégés _nom et _etiquette
        raise NotImplementedError

    @abstractmethod
    def valider(self, saisie: str):
        """Vérifie et convertit une saisie de l'utilisateur.

        Args:
            saisie: le texte entré dans l'interface.

        Returns:
            La valeur convertie (float ou str).

        Raises:
            SaisieInvalideError: si la saisie est invalide.
        """

    @abstractmethod
    def vers_dict(self) -> dict:
        """Retourne la description de la variable pour le JSON de métadonnées."""

    # TODO (A) : __repr__ (méthode spéciale exigée au chapitre 9-11)


class VariableNumerique(Variable):
    """Variable numérique avec un intervalle autorisé [minimum, maximum]."""

    def __init__(self, nom: str, etiquette: str, minimum: float, maximum: float) -> None:
        # TODO (A)
        raise NotImplementedError

    def valider(self, saisie: str) -> float:
        # TODO (A) : vide ? non numérique ? hors intervalle ? → SaisieInvalideError
        raise NotImplementedError

    def vers_dict(self) -> dict:
        # TODO (A) : {"nom", "type": "numerique", "etiquette", "min", "max"}
        raise NotImplementedError


class VariableCategorielle(Variable):
    """Variable catégorielle avec une liste de valeurs possibles."""

    def __init__(self, nom: str, etiquette: str, valeurs: list[str]) -> None:
        # TODO (A)
        raise NotImplementedError

    def valider(self, saisie: str) -> str:
        # TODO (A) : la saisie doit être dans self._valeurs
        raise NotImplementedError

    def vers_dict(self) -> dict:
        # TODO (A) : {"nom", "type": "categorielle", "etiquette", "valeurs"}
        raise NotImplementedError


def variable_depuis_dict(description: dict) -> Variable:
    """Recrée une Variable à partir de sa description JSON (utilisé par l'interface).

    Raises:
        DonneeInvalideError: si le type est inconnu.
    """
    # TODO (A)
    raise NotImplementedError


# --- Jeu de données (composition) ---------------------------------------

class JeuDeDonnees:
    """Regroupe le DataFrame propre et la liste des Variable qui le décrivent."""

    def __init__(self, df_propre: pd.DataFrame) -> None:
        # TODO (A) : self._df et self._variables (construites à partir du DataFrame :
        #            min/max pour les numériques, valeurs uniques pour les catégorielles)
        raise NotImplementedError

    @property
    def variables(self) -> list[Variable]:
        # TODO (A)
        raise NotImplementedError

    def entrees(self) -> pd.DataFrame:
        """Retourne X : les colonnes d'entrée."""
        # TODO (A)
        raise NotImplementedError

    def cible(self) -> pd.Series:
        """Retourne y : la colonne rankings."""
        # TODO (A)
        raise NotImplementedError

    # TODO (A) : __len__ (nombre de lignes)

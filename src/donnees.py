"""Lecture, nettoyage et description des données (personne A).

Contient :
- les fonctions de chargement et de nettoyage du CSV ;
- la hiérarchie Variable → VariableNumerique / VariableCategorielle (héritage + polymorphisme) ;
- la classe JeuDeDonnees (composition : elle contient une liste de Variable).
"""

import os
from abc import ABC, abstractmethod


import pandas as pd
import matplotlib.pyplot as plt 
from src.exceptions import DonneeInvalideError,SaisieInvalideError

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

    if not os.path.exists(chemin):
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    df = pd.read_csv(chemin, index_col=0)

    for colonne in VARIABLES_CATEGORIELLES + VARIABLES_NUMERIQUES + [CIBLE]:
        if colonne not in df.columns:
            raise DonneeInvalideError(f"Colonne manquante dans le fichier : {colonne}")
    return df



   
      
    


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
    dfc = df.copy()
    dfc = dfc[dfc["FGA"]> 0]
    dfc = dfc[VARIABLES_CATEGORIELLES+VARIABLES_NUMERIQUES+[CIBLE]]
    manque = dfc.isna().sum().sum()
    if manque > 0:
        raise DonneeInvalideError(f"Le fichier contient {manque} valeur(s) manquante(s)")
    dfc = dfc.reset_index(drop=True)
    return dfc
  


def tracer_exploration(df: pd.DataFrame, chemin_image: str) -> None:
    """Trace le graphique d'exploration (PTS vs note 2K, coloré par poste) et l'enregistre avec savefig.

    Args:
        df: DataFrame propre.
        chemin_image: chemin du fichier PNG à créer.
    """
    fig, ax = plt.subplots()
    for poste in sorted(df["POS"].unique()):
        dfc = df[df["POS"] == poste]
        ax.scatter(dfc["PTS"], dfc["rankings"], label=poste, alpha=0.5, s=10)

    ax.set_title("Note 2K selon les points par match")
    ax.set_xlabel("Points par match")
    ax.set_ylabel("Note 2K")
    ax.legend(title="Poste")
    fig.savefig(chemin_image)
    plt.close(fig)
    


# --- Classes de variables (héritage + polymorphisme) --------------------

class Variable(ABC):
    """Variable d'entrée du modèle (classe abstraite)."""

    def __init__(self, nom: str, etiquette: str) -> None:
         self._nom = nom
         self._etiquette = etiquette
    
    @property
    def nom(self) -> str:
        return self._nom

    @property
    def etiquette(self) -> str:
        return self._etiquette
        

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

    
    def __repr__(self) -> str:
        return f"{type(self).__name__}(nom ={self.nom!r}, etiquette ={self.etiquette!r})"
        


class VariableNumerique(Variable):
    """Variable numérique avec un intervalle autorisé [minimum, maximum]."""

    def __init__(self, nom: str, etiquette: str, minimum: float, maximum: float) -> None:
        super().__init__(nom,etiquette)
        if minimum > maximum:
                    raise ValueError(f"le minimum est plus grand que le maximum ({minimum} > {maximum})")
        self._minimum = minimum
        self._maximum = maximum

    @property
    def minimum(self) -> float:
        return self._minimum

    @property
    def maximum(self) -> float:
            return self._maximum

        
        

    def valider(self, saisie: str) -> float:
        temp = ""
        for lettre in saisie:
            if lettre == " ":
                continue
            if lettre == ",":
                temp+= "."
                continue
            temp += lettre

        saisie = temp
        if len(saisie) == 0:
            raise SaisieInvalideError(f"{self.etiquette} est vide")
        try:
            fsaisie =float(saisie)
        except ValueError:
            raise SaisieInvalideError(f"{self.etiquette} n'est pas un nombre")
        if fsaisie < self.minimum:
            raise SaisieInvalideError(f"{self.etiquette} est trop petit, {self.etiquette} doit etre entre {self.minimum} et {self.maximum}")
        if fsaisie > self.maximum:
            raise SaisieInvalideError(f"{self.etiquette} est trop grand, {self.etiquette} doit etre entre {self.minimum} et {self.maximum}")
        return fsaisie
    

    def vers_dict(self) -> dict:
        vnum_dict = {"nom":self.nom,"type":"numerique","etiquette":self.etiquette,"min":self.minimum,"max":self.maximum}
        return vnum_dict
        


class VariableCategorielle(Variable):
    """Variable catégorielle avec une liste de valeurs possibles."""

    def __init__(self, nom: str, etiquette: str, valeurs: list[str]) -> None:
        # TODO (A)
        super().__init__(nom,etiquette)
        self._valeurs = valeurs

    @property
    def valeurs(self) -> list:
        return self._valeurs

    def valider(self, saisie: str) -> str:
        saisie = saisie.strip().upper()
        if not saisie in self.valeurs:
            raise SaisieInvalideError (f"{self.etiquette} doit etre parmis {','.join(self.valeurs)}")
        return saisie
        
       

    def vers_dict(self) -> dict:
        vcat_dict = {"nom":self.nom,"type":"categorielle","etiquette":self.etiquette,"valeurs":self.valeurs}
        return vcat_dict
        


def variable_depuis_dict(description: dict) -> Variable:
    """Recrée une Variable à partir de sa description JSON (utilisé par l'interface).

    Raises:
        DonneeInvalideError: si le type est inconnu.
    """
    if description["type"] == "numerique":
        return VariableNumerique(description["nom"],description["etiquette"],description["min"],description["max"])
    elif description["type"] == "categorielle":
        return VariableCategorielle(description["nom"],description["etiquette"],description["valeurs"])
    else:
        raise DonneeInvalideError(f"{description['type']} n'est pas un type de variable reconnu")
    


# --- Jeu de données (composition) ---------------------------------------

class JeuDeDonnees:
    """Regroupe le DataFrame propre et la liste des Variable qui le décrivent."""

    def __init__(self, df_propre: pd.DataFrame) -> None:
        self._df = df_propre
        self._variables = []
        for colonne in VARIABLES_CATEGORIELLES:
            valeurs = sorted(df_propre[colonne].unique())
            self._variables.append(VariableCategorielle(colonne,ETIQUETTES[colonne],valeurs))
        for colonne in VARIABLES_NUMERIQUES:
            self._variables.append(VariableNumerique(colonne,ETIQUETTES[colonne],float(df_propre[colonne].min()),float(df_propre[colonne].max())))


    
  


    @property
    def variables(self) -> list[Variable]:
        return self._variables
        

    def entrees(self) -> pd.DataFrame:
        """Retourne X : les colonnes d'entrée."""
        return self._df[VARIABLES_CATEGORIELLES+VARIABLES_NUMERIQUES]

    def cible(self) -> pd.Series:
        """Retourne y : la colonne rankings."""
        return self._df[CIBLE]

   
    def __len__(self) -> int:
        return len(self._df)
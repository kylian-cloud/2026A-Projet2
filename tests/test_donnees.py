"""Tests de src/donnees.py (personne A). Cas usuels, cas limites et cas d'erreur."""

import pandas as pd
import pytest

from src.donnees import (
    CIBLE,
    VARIABLES_CATEGORIELLES,
    VARIABLES_NUMERIQUES,
    JeuDeDonnees,
    Variable,
    VariableCategorielle,
    VariableNumerique,
    charger_csv,
    nettoyer,
    variable_depuis_dict,
)
from src.exceptions import DonneeInvalideError, SaisieInvalideError


@pytest.fixture
def age():
    """Variable numérique utilisée dans plusieurs tests."""
    return VariableNumerique("AGE", "Âge", 19, 41)


@pytest.fixture
def poste():
    """Variable catégorielle utilisée dans plusieurs tests."""
    return VariableCategorielle("POS", "Poste", ["C", "PF", "PG", "SF", "SG"])


# --- VariableNumerique ------------------------------------------------------

def test_valider_numerique_valeur_normale(age):
    assert age.valider("25") == 25.0


def test_valider_numerique_accepte_virgule_et_espaces(age):
    assert age.valider(" 30,5 ") == 30.5


@pytest.mark.parametrize("saisie, attendu", [("19", 19.0), ("41", 41.0)])
def test_valider_numerique_bornes_incluses(age, saisie, attendu):
    assert age.valider(saisie) == attendu


@pytest.mark.parametrize("saisie", ["", "   ", "abc", "18.9", "41.1"])
def test_valider_numerique_refuse_saisie_invalide(age, saisie):
    with pytest.raises(SaisieInvalideError):
        age.valider(saisie)


def test_variable_numerique_refuse_minimum_plus_grand_que_maximum():
    with pytest.raises(ValueError):
        VariableNumerique("AGE", "Âge", 41, 19)


# --- VariableCategorielle ---------------------------------------------------

def test_valider_categorielle_normalise_la_saisie(poste):
    assert poste.valider(" pg ") == "PG"


def test_valider_categorielle_refuse_valeur_inconnue(poste):
    with pytest.raises(SaisieInvalideError):
        poste.valider("XY")


# --- Classe abstraite et aller-retour JSON ----------------------------------

def test_variable_est_abstraite():
    with pytest.raises(TypeError):
        Variable("AGE", "Âge")


@pytest.mark.parametrize("fabrique", ["age", "poste"])
def test_variable_depuis_dict_recree_une_variable_equivalente(fabrique, request):
    variable = request.getfixturevalue(fabrique)
    copie = variable_depuis_dict(variable.vers_dict())
    assert type(copie) is type(variable)
    assert copie.vers_dict() == variable.vers_dict()


def test_variable_depuis_dict_refuse_type_inconnu():
    with pytest.raises(DonneeInvalideError):
        variable_depuis_dict({"nom": "X", "type": "inconnu", "etiquette": "X"})


# --- Chargement et nettoyage ------------------------------------------------

def test_charger_csv_fichier_absent(tmp_path):
    with pytest.raises(FileNotFoundError):
        charger_csv(str(tmp_path / "absent.csv"))


def test_charger_csv_colonne_manquante(tmp_path):
    chemin = tmp_path / "incomplet.csv"
    pd.DataFrame({"index": [0], "AGE": [25]}).to_csv(chemin, index=False)
    with pytest.raises(DonneeInvalideError):
        charger_csv(str(chemin))


def test_nettoyer_garde_les_bonnes_colonnes_et_lignes():
    propre = nettoyer(charger_csv())
    attendues = VARIABLES_CATEGORIELLES + VARIABLES_NUMERIQUES + [CIBLE]
    assert sorted(propre.columns) == sorted(attendues)
    assert len(propre) == 2408
    assert propre.isna().sum().sum() == 0


def test_nettoyer_ne_modifie_pas_le_dataframe_d_origine():
    brut = charger_csv()
    forme_avant = brut.shape
    nettoyer(brut)
    assert brut.shape == forme_avant


# --- JeuDeDonnees -----------------------------------------------------------

def test_jeu_de_donnees_entrees_cible_et_variables():
    jeu = JeuDeDonnees(nettoyer(charger_csv()))
    assert len(jeu) == 2408
    assert jeu.entrees().shape == (2408, 10)
    assert CIBLE not in jeu.entrees().columns
    assert jeu.cible().name == CIBLE
    assert [v.nom for v in jeu.variables][0] == "POS"
    assert len(jeu.variables) == 10

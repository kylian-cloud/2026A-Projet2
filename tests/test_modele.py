"""Tests de src/modele.py et src/historique.py (personne B).

Idées de tests :
- rmse_numpy == mean_squared_error de scikit-learn (racine) → pytest.approx
- rmse_numpy de deux tableaux identiques == 0
- rmse_numpy de tableaux de tailles différentes → pytest.raises(ValueError)
- la référence prédit bien la moyenne de y_train
- même graine → même séparation (reproductibilité)
- predire() retourne une note dans un intervalle plausible (ex. 40 à 99)
- charger() sans fichier → pytest.raises(ModeleIntrouvableError)
- ajouter_prediction puis lire_historique (dans un dossier temporaire : fixture tmp_path)
"""

import json

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import mean_squared_error

from src import historique, modele
from src.exceptions import ModeleIntrouvableError


def _donnees_test():
    entrees = pd.DataFrame(
        {
            "POS": ["PG", "SG", "SF", "PF", "C"] * 6,
            "AGE": [19 + index % 15 for index in range(30)],
            "GP": [30 + index % 53 for index in range(30)],
            "MIN": [10.0 + index % 27 for index in range(30)],
            "PTS": [5.0 + index * 0.8 for index in range(30)],
            "REB": [2.0 + index % 10 for index in range(30)],
            "AST": [1.0 + index % 9 for index in range(30)],
            "STL": [0.2 + (index % 8) / 10 for index in range(30)],
            "BLK": [0.1 + (index % 7) / 10 for index in range(30)],
            "FG%": [35.0 + index % 30 for index in range(30)],
        }
    )
    cible = pd.Series(
        [55.0 + index * 0.9 for index in range(30)], name="rankings"
    )
    return entrees, cible


def test_rmse_numpy_correspond_a_scikit_learn():
    vrai = np.array([60.0, 70.0, 80.0])
    predit = np.array([62.0, 68.0, 77.0])

    assert modele.rmse_numpy(vrai, predit) == pytest.approx(
        mean_squared_error(vrai, predit) ** 0.5
    )


def test_rmse_numpy_de_tableaux_identiques_est_nulle():
    valeurs = np.array([60.0, 70.0, 80.0])

    assert modele.rmse_numpy(valeurs, valeurs) == 0.0


@pytest.mark.parametrize(
    "vrai,predit",
    [(np.array([]), np.array([])), (np.array([1, 2]), np.array([1]))],
)
def test_rmse_numpy_refuse_des_tailles_invalides(vrai, predit):
    with pytest.raises(ValueError):
        modele.rmse_numpy(vrai, predit)


def test_separation_est_reproductible():
    entrees, cible = _donnees_test()
    premier = modele.Modele()
    second = modele.Modele()

    premier.separer(entrees, cible)
    second.separer(entrees, cible)

    pd.testing.assert_frame_equal(premier._X_train, second._X_train)
    pd.testing.assert_frame_equal(premier._X_test, second._X_test)
    pd.testing.assert_series_equal(premier._y_train, second._y_train)
    pd.testing.assert_series_equal(premier._y_test, second._y_test)


def test_reference_prevoit_la_moyenne_de_y_train():
    entrees, cible = _donnees_test()
    instance = modele.Modele()
    instance.separer(entrees, cible)
    instance.entrainer_reference()

    predictions = instance.reference.predict(instance._X_test)
    assert predictions == pytest.approx(instance._y_train.mean())


def test_modele_entraine_et_predire_retourne_un_float_plausible():
    entrees, cible = _donnees_test()
    instance = modele.Modele()
    instance.separer(entrees, cible)
    instance.entrainer()

    note = instance.predire(entrees.iloc[0].to_dict())
    assert isinstance(note, float)
    assert 40 <= note <= 99


def test_sauvegarder_et_charger_restituent_modele_et_metadonnees(
    tmp_path, monkeypatch
):
    entrees, cible = _donnees_test()
    instance = modele.Modele()
    instance.separer(entrees, cible)
    instance.entrainer()
    fichier_modele = tmp_path / "modele.joblib"
    fichier_metadonnees = tmp_path / "metadonnees.json"
    monkeypatch.setattr(modele, "FICHIER_MODELE", str(fichier_modele))
    monkeypatch.setattr(modele, "FICHIER_METADONNEES", str(fichier_metadonnees))

    instance.sauvegarder([{"nom": "POS", "type": "categorielle"}])
    recharge = modele.Modele.charger()

    assert recharge.predire(entrees.iloc[0].to_dict()) == pytest.approx(
        instance.predire(entrees.iloc[0].to_dict())
    )
    contenu = json.loads(fichier_metadonnees.read_text(encoding="utf-8"))
    assert contenu["variables"] == [{"nom": "POS", "type": "categorielle"}]
    assert contenu["cible"] == "rankings"
    assert contenu["metrique"]["nom"] == "RMSE"


def test_charger_sans_fichier_leve_modele_introuvable(tmp_path, monkeypatch):
    monkeypatch.setattr(modele, "FICHIER_MODELE", str(tmp_path / "absent.joblib"))
    monkeypatch.setattr(
        modele, "FICHIER_METADONNEES", str(tmp_path / "absent.json")
    )

    with pytest.raises(ModeleIntrouvableError):
        modele.Modele.charger()


def test_lire_metadonnees_absentes_leve_modele_introuvable(tmp_path):
    with pytest.raises(ModeleIntrouvableError):
        modele.lire_metadonnees(str(tmp_path / "absent.json"))


def test_historique_ajoute_et_relit_les_predictions(tmp_path):
    chemin = tmp_path / "historique.csv"
    premiere = {"POS": "PG", "AGE": 25.0}
    seconde = {"POS": "C", "AGE": 31.0}

    historique.ajouter_prediction(premiere, 82.5, str(chemin))
    historique.ajouter_prediction(seconde, 76.0, str(chemin))

    lignes = historique.lire_historique(str(chemin))
    assert len(lignes) == 2
    assert lignes[0] == {"POS": "PG", "AGE": "25.0", "note_predite": "82.5"}
    assert lignes[1] == {"POS": "C", "AGE": "31.0", "note_predite": "76.0"}


def test_historique_absent_est_vide(tmp_path):
    assert historique.lire_historique(str(tmp_path / "absent.csv")) == []

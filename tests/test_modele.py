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

# TODO (B)

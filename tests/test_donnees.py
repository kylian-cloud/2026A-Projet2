"""Tests de src/donnees.py (personne A). Cas usuels, cas limites et cas d'erreur.

Idées de tests :
- nettoyer() garde seulement les 10 colonnes + la cible
- nettoyer() retire les lignes avec FGA == 0
- nettoyer() ne modifie pas le DataFrame d'origine
- VariableNumerique.valider("25") → 25.0
- VariableNumerique.valider("") → pytest.raises(SaisieInvalideError)
- VariableNumerique.valider("abc") → pytest.raises(SaisieInvalideError)
- VariableNumerique.valider(valeur hors intervalle) → pytest.raises(SaisieInvalideError)
- VariableNumerique.valider(exactement le minimum) → accepté (cas limite)
- VariableCategorielle.valider("XX") → pytest.raises(SaisieInvalideError)
- variable_depuis_dict(v.vers_dict()) redonne une variable équivalente
"""

# TODO (A)

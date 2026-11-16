"""Exceptions personnalisées du projet (personne A).

Exigence du chapitre 8 : au moins une exception personnalisée, levée avec `raise`.
"""

class DonneeInvalideError(Exception):
    """Levée quand le CSV est mal formé (colonne manquante, fichier vide…)"""

class SaisieInvalideError(Exception):
    """Levée quand une saisie de l'utilisateur est vide, non numérique ou hors intervalle."""


# TODO (B) : ModeleIntrouvableError — hérite de Exception.
#            Levée quand le fichier du modèle ou des métadonnées n'existe pas.

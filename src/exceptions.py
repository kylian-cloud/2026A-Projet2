"""Exceptions personnalisées du projet (personne A).

Exigence du chapitre 8 : au moins une exception personnalisée, levée avec `raise`.
"""


# TODO (A) : DonneeInvalideError — hérite de Exception.
#            Levée quand le CSV est mal formé (colonne manquante, fichier vide…).


# TODO (A) : SaisieInvalideError — hérite de Exception.
#            Levée quand une saisie de l'utilisateur est vide, non numérique ou hors intervalle.
#            Le message doit être compréhensible par un non-informaticien.


class ModeleIntrouvableError(Exception):
    """Le modèle ou ses métadonnées ne sont pas disponibles sur le disque."""

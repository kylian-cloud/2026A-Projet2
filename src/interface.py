"""Interface graphique Streamlit (personnes A et B).

Lancement (depuis la racine du projet) :
    python -m streamlit run src/interface.py
ou :
    python -m src.main

Règle du chapitre 8 : l'interface APPELLE la logique (donnees, modele, historique),
elle ne la contient pas. Aucun calcul ici.

Rappel Streamlit : tout le script est ré-exécuté à chaque clic.
- @st.cache_resource : pour ne charger le modèle qu'une seule fois.
- st.session_state : pour garder une valeur d'un clic à l'autre (ex. dernière prédiction).
"""

import streamlit as st

from src import donnees, historique, modele


class Application:
    """Regroupe le modèle et la liste des Variable (composition)."""

    def __init__(self) -> None:
        # TODO (B) : self._modele = modele.Modele.charger()
        #            self._metadonnees = modele.lire_metadonnees()
        # TODO (A) : self._variables = [donnees.variable_depuis_dict(v) for v in ...]
        raise NotImplementedError

    # --- Partie A : saisie et validation ---------------------------------

    def afficher_champs(self) -> dict:
        """Affiche un champ par variable et retourne les saisies brutes.

        - VariableNumerique → st.text_input (ou st.number_input avec min/max)
        - VariableCategorielle → st.selectbox(valeurs)
        Idée : une méthode `afficher_champ()` dans chaque classe Variable (polymorphisme).
        """
        # TODO (A)
        raise NotImplementedError

    def valider_saisies(self, saisies: dict) -> dict:
        """Valide chaque saisie avec Variable.valider.

        Raises:
            SaisieInvalideError: au premier champ invalide.
        """
        # TODO (A)
        raise NotImplementedError

    def afficher_avertissement(self) -> None:
        """Rappelle que l'outil est un exercice pédagogique (st.info)."""
        # TODO (A)
        raise NotImplementedError

    # --- Partie B : prédiction, graphique, historique --------------------

    def predire(self, saisies: dict) -> None:
        """Bouton « Prédire » : valider_saisies → modele.predire → affichage → historique.

        try / except SaisieInvalideError → st.error(message clair), jamais de traceback.
        """
        # TODO (B)
        raise NotImplementedError

    def afficher_resultat(self, note: float) -> None:
        """Affiche la note en langage clair (ex. st.metric « Note 2K estimée : 78 / 99 »)."""
        # TODO (B)
        raise NotImplementedError

    def afficher_graphique(self, note: float | None = None) -> None:
        """Graphique Matplotlib avec st.pyplot (titre, axes étiquetés, légende si utile)."""
        # TODO (B)
        raise NotImplementedError

    def afficher_historique(self) -> None:
        """Affiche les prédictions passées (st.dataframe(historique.lire_historique()))."""
        # TODO (B)
        raise NotImplementedError


@st.cache_resource
def obtenir_application() -> Application:
    """Crée l'Application une seule fois (le modèle n'est pas rechargé à chaque clic)."""
    return Application()


def page() -> None:
    """Construit la page : titre, avertissement, champs, bouton, résultat, graphique, historique."""
    # TODO (A + B) — gérer ModeleIntrouvableError ici : st.error("Lancez d'abord l'entraînement…")
    raise NotImplementedError


page()

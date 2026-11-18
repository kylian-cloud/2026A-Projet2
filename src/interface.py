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
import matplotlib.pyplot as plt

from src import donnees, historique, modele
from src.exceptions import ModeleIntrouvableError


class Application:
    """Regroupe le modèle et la liste des Variable (composition)."""

    def __init__(self) -> None:
        self._modele = modele.Modele.charger()
        self._metadonnees = modele.lire_metadonnees()
        self._variables = [
            donnees.variable_depuis_dict(description)
            for description in self._metadonnees["variables"]
        ]

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
        from src.exceptions import SaisieInvalideError

        try:
            entrees = self.valider_saisies(saisies)
            note = self._modele.predire(entrees)
        except SaisieInvalideError as erreur:
            st.session_state.pop("derniere_note", None)
            st.error(str(erreur))
            return

        st.session_state["derniere_note"] = note
        self.afficher_resultat(note)
        historique.ajouter_prediction(entrees, note)

    def afficher_resultat(self, note: float) -> None:
        """Affiche la note en langage clair (ex. st.metric « Note 2K estimée : 78 / 99 »)."""
        st.metric("Note 2K estimée", f"{note:.1f} / 99")

    def afficher_graphique(self, note: float | None = None) -> None:
        """Graphique Matplotlib avec st.pyplot (titre, axes étiquetés, légende si utile)."""
        if note is None:
            st.info("Effectuez une prédiction pour afficher le graphique.")
            return

        figure, axes = plt.subplots(figsize=(7, 1.8))
        axes.barh(["Joueur"], [note], color="#4b8bbe")
        axes.set_xlim(0, 99)
        axes.set_xlabel("Note estimée (sur 99)")
        axes.set_title("Estimation de la note NBA 2K")
        axes.grid(axis="x", linestyle=":", alpha=0.5)
        figure.tight_layout()
        st.pyplot(figure)
        plt.close(figure)

    def afficher_historique(self) -> None:
        """Affiche les prédictions passées (st.dataframe(historique.lire_historique()))."""
        predictions = historique.lire_historique()
        st.subheader("Historique des prédictions")
        if predictions:
            st.dataframe(predictions, use_container_width=True, hide_index=True)
        else:
            st.caption("Aucune prédiction enregistrée pour le moment.")


@st.cache_resource
def obtenir_application() -> Application:
    """Crée l'Application une seule fois (le modèle n'est pas rechargé à chaque clic)."""
    return Application()


def page() -> None:
    """Construit la page : titre, avertissement, champs, bouton, résultat, graphique, historique."""
    st.title("Prédire une note NBA 2K")
    try:
        application = obtenir_application()
    except ModeleIntrouvableError:
        st.error(
            "Aucun modèle sauvegardé. Lancez d'abord `python -m src.main entrainer`."
        )
        return

    application.afficher_avertissement()
    saisies = application.afficher_champs()
    prediction_demandee = st.button("Prédire", type="primary")
    if prediction_demandee:
        application.predire(saisies)
    elif st.session_state.get("derniere_note") is not None:
        application.afficher_resultat(st.session_state["derniere_note"])

    application.afficher_graphique(st.session_state.get("derniere_note"))
    application.afficher_historique()


page()

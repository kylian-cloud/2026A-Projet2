"""Point d'entrée de l'application (personne B).

Usage (depuis la racine du projet) :
    python -m src.main entrainer  # entraîne et sauvegarde le modèle (une seule fois)
    python -m src.main            # lance l'interface Streamlit
"""

import os
import subprocess
import sys

from src import donnees
from src.modele import Modele

FICHIER_INTERFACE = os.path.join(os.path.dirname(__file__), "interface.py")


def entrainer_et_sauvegarder() -> None:
    """charger_csv → nettoyer → JeuDeDonnees → Modele (séparer, référence, entraîner) → sauvegarder."""
    dataframe = donnees.nettoyer(donnees.charger_csv())
    jeu = donnees.JeuDeDonnees(dataframe)

    modele = Modele()
    modele.separer(jeu.entrees(), jeu.cible())
    modele.entrainer_reference()
    modele.entrainer()
    modele.sauvegarder([variable.vers_dict() for variable in jeu.variables])
    print(modele)


def lancer_interface() -> None:
    """Lance Streamlit sur src/interface.py."""
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", FICHIER_INTERFACE],
        check=True,
        cwd=os.path.dirname(os.path.dirname(__file__)),
    )


def main() -> None:
    """Lance l'entraînement ou l'interface selon l'argument de la ligne de commande."""
    arguments = sys.argv[1:]
    if arguments == ["entrainer"]:
        entrainer_et_sauvegarder()
    elif not arguments:
        lancer_interface()
    else:
        raise SystemExit(
            "Usage : python -m src.main [entrainer]"
        )


if __name__ == "__main__":
    main()

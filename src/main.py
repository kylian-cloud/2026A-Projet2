"""Point d'entrée de l'application (personne B).

Usage (depuis la racine du projet) :
    python -m src.main entrainer  # entraîne et sauvegarde le modèle (une seule fois)
    python -m src.main            # lance l'interface Streamlit
"""

import os
import subprocess
import sys

FICHIER_INTERFACE = os.path.join(os.path.dirname(__file__), "interface.py")


def entrainer_et_sauvegarder() -> None:
    """charger_csv → nettoyer → JeuDeDonnees → Modele (séparer, référence, entraîner) → sauvegarder."""
    # TODO (B)
    raise NotImplementedError


def lancer_interface() -> None:
    """Lance Streamlit sur src/interface.py."""
    # TODO (B) : subprocess.run([sys.executable, "-m", "streamlit", "run", FICHIER_INTERFACE])
    raise NotImplementedError


def main() -> None:
    """Lance l'entraînement ou l'interface selon l'argument de la ligne de commande."""
    # TODO (B) : sys.argv
    raise NotImplementedError


if __name__ == "__main__":
    main()

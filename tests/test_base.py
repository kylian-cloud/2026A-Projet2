"""Premier test (étape 0) : il passe dès le départ pour que la CI soit verte."""

import os

from src import donnees


def test_csv_present():
    assert os.path.exists(donnees.FICHIER_CSV)

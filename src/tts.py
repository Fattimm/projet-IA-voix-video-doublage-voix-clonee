"""Étape ⑤ : lire chaque phrase anglaise avec la voix clonée.
Responsable : Alassane
"""


def synthetiser(texte_en, chemin_voix_reference, duree_cible, chemin_sortie, nb_essais=3):
    """Lit texte_en avec la voix de la personne (XTTS-v2).

    chemin_voix_reference : 10 à 15 secondes de sa voix (issues de l'étape ②).
    Génère nb_essais versions et garde celle dont la durée est la plus proche de duree_cible.

    Renvoie : le chemin du fichier .wav gardé.
    """
    raise NotImplementedError("À faire par Alassane")
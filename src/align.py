"""Étape ⑥ : recaler la durée de chaque phrase anglaise sur la phrase française.
Responsable : Khadidiatou
"""


def recaler(chemin_wav_en, duree_cible, chemin_sortie):
    """Ajuste la durée d'une phrase anglaise pour qu'elle tienne dans duree_cible (en secondes).

    Plus courte : on complète avec du silence.
    Jusqu'à 25 % plus longue : on accélère légèrement, sans changer la hauteur de la voix.
    Au-delà : on signale qu'il faut régénérer la phrase.

    Renvoie : le chemin du fichier .wav recalé.
    """
    raise NotImplementedError("À faire par Khadidiatou")
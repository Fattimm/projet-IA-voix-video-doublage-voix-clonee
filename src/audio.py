"""Étapes ① et ② : extraire le son de la vidéo, puis séparer la voix du fond.
Responsable : Fatoumata
"""


def extraire_audio(chemin_video, chemin_wav):
    """Extrait la bande son de la vidéo dans un fichier .wav (avec ffmpeg).

    Renvoie : le chemin du fichier .wav créé.
    """
    raise NotImplementedError("À faire par Fatoumata")


def separer_voix_fond(chemin_wav, dossier_sortie):
    """Sépare la voix et le fond musical (avec Demucs).

    Renvoie : (chemin_voix, chemin_fond), deux fichiers .wav.
    """
    raise NotImplementedError("À faire par Fatoumata")
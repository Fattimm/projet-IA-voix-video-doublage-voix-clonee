"""Étapes ① et ② : extraire le son de la vidéo, puis séparer la voix du fond.
Responsable : Fatoumata
"""
import os
import subprocess


def extraire_audio(chemin_video, chemin_wav):
    """Extrait la bande son de la vidéo dans un fichier .wav (avec ffmpeg).

    Renvoie : le chemin du fichier .wav créé.
    """
    commande = ["ffmpeg", "-y", "-i", chemin_video, "-vn", "-ac", "1", "-ar", "24000", chemin_wav]
    subprocess.run(commande, check=True)
    return chemin_wav


def separer_voix_fond(chemin_wav, dossier_sortie):
    """Sépare la voix et le fond musical (avec Demucs).

    Renvoie : (chemin_voix, chemin_fond), deux fichiers .wav.
    """
    commande = ["python", "-m", "demucs", "--two-stems=vocals", "-o", dossier_sortie, chemin_wav]
    subprocess.run(commande, check=True)
    nom = os.path.splitext(os.path.basename(chemin_wav))[0]
    dossier = os.path.join(dossier_sortie, "htdemucs", nom)
    return os.path.join(dossier, "vocals.wav"), os.path.join(dossier, "no_vocals.wav")


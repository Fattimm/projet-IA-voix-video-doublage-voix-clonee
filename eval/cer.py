"""Mesure : CER (taux d'erreur par caractère) de la voix anglaise.
Responsable : Fatoumata
"""

import re

import jiwer
from faster_whisper import WhisperModel



def normaliser(texte):
    """Met en minuscules et enlève la ponctuation, pour ne compter que les vraies erreurs."""
    texte = texte.lower()
    texte = re.sub(r"[^\w\s]", "", texte)
    return " ".join(texte.split())


def calculer_cer(segments):
    """Retranscrit chaque phrase anglaise avec Whisper et la compare au texte attendu (jiwer).

    Renvoie : le CER moyen (0 = parfait).
    """
    modele = WhisperModel("large-v3", device="cuda", compute_type="float16")
    scores = []
    for s in segments:
        resultats, info = modele.transcribe(s["wav_en"], language="en")
        entendu = " ".join(r.text for r in resultats)
        scores.append(jiwer.cer(normaliser(s["texte_en"]), normaliser(entendu)))
    return sum(scores) / len(scores)

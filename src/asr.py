"""Étape ③ : transcrire la voix française, phrase par phrase.
Responsable : Fatoumata
"""


def transcrire(chemin_voix):
    """Transcrit la voix en français (faster-whisper large-v3 + VAD).

    Renvoie : une liste de segments (des phrases de 2 à 10 secondes), par exemple :
        [{"id": 0, "debut": 1.20, "fin": 4.85, "texte_fr": "Bonjour à tous", "texte_en": ""}, ...]
    """
    raise NotImplementedError("À faire par Fatoumata")
"""Étape ③ : transcrire la voix française, phrase par phrase.
Responsable : Fatoumata
"""
from faster_whisper import WhisperModel


def transcrire(chemin_voix):
    """Transcrit la voix en français (faster-whisper large-v3 + VAD).

    Renvoie : une liste de segments (des phrases de 2 à 10 secondes), par exemple :
        [{"id": 0, "debut": 1.20, "fin": 4.85, "texte_fr": "Bonjour à tous", "texte_en": "", "wav_en": ""}, ...]
    """
    modele = WhisperModel("large-v3", device="cuda", compute_type="float16")
    resultats, info = modele.transcribe(chemin_voix, language="fr", vad_filter=True)
    segments = []
    for i, r in enumerate(resultats):
        segments.append({
            "id": i,
            "debut": round(r.start, 2),
            "fin": round(r.end, 2),
            "texte_fr": r.text.strip(),
            "texte_en": "",
            "wav_en": "",
        })
    return segments
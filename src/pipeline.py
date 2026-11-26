"""Relie toutes les étapes, de la vidéo française à la vidéo doublée.
Chronomètre chaque étape et enregistre les segments dans segments.json.
Responsable : Khadidiatou
"""
import json
import os
import subprocess
import time


def _chrono(temps, nom, debut):
    """Note le temps écoulé depuis 'debut' pour l'étape 'nom'."""
    temps[nom] = round(time.perf_counter() - debut, 2)


def _extraire_reference(chemin_voix, chemin_ref, debut=0.0, duree=12):
    """Découpe 12 secondes de voix propre : c'est l'échantillon à cloner."""
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(debut),
         "-t", str(duree), "-i", chemin_voix, chemin_ref],
        check=True,
    )
    return chemin_ref


def _synthese_factice(texte_en, chemin_voix_reference, duree_cible,
                      chemin_sortie, nb_essais=3):
    """Faux TTS : un bip un peu plus long que la fenêtre.
    Sert à tester le pipeline avant que tts.py d'Alassane soit prêt."""
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
         f"sine=frequency=440:duration={duree_cible * 1.2:.2f}", chemin_sortie],
        check=True,
    )
    return chemin_sortie


def doubler_video(chemin_video, dossier_sortie, consentement=False, factice=False):
    """Lance tout le pipeline sur une vidéo.

    consentement : si False, on n'utilise pas la voix clonée mais une voix neutre.
    factice : si True, le TTS est remplacé par un bip (test uniquement).
    Renvoie : le chemin de la vidéo doublée.
    """
    # Imports ici pour pouvoir importer ce fichier sans GPU ni Whisper installé
    from src.audio import extraire_audio, separer_voix_fond
    from src.asr import transcrire
    from src.translate import traduire_segments
    from src.align import aligner_segments
    from src.assemble import assembler
    if factice:
        synthetiser = _synthese_factice
    else:
        from src.tts import synthetiser

    os.makedirs(dossier_sortie, exist_ok=True)
    dossier_segments = os.path.join(dossier_sortie, "segments")
    os.makedirs(dossier_segments, exist_ok=True)
    temps = {}

    # ① Extraction du son
    t = time.perf_counter()
    chemin_wav = os.path.join(dossier_sortie, "audio.wav")
    extraire_audio(chemin_video, chemin_wav)
    _chrono(temps, "1_extraction", t)

    # ② Séparation voix / fond
    t = time.perf_counter()
    voix, fond = separer_voix_fond(chemin_wav, os.path.join(dossier_sortie, "demucs"))
    _chrono(temps, "2_separation", t)

    # ③ Transcription
    t = time.perf_counter()
    segments = transcrire(voix)
    _chrono(temps, "3_transcription", t)
    if not segments:
        raise ValueError("Aucune parole détectée dans la vidéo.")

    # ④ Traduction
    t = time.perf_counter()
    segments = traduire_segments(segments)
    _chrono(temps, "4_traduction", t)

    # Voix de référence : seulement si la personne a donné son consentement
    if consentement:
        reference = _extraire_reference(
            voix, os.path.join(dossier_sortie, "reference.wav"),
            debut=segments[0]["debut"])
    else:
        reference = None  # voix neutre (à convenir avec Alassane)

    # ⑤ Synthèse de chaque segment
    t = time.perf_counter()
    for seg in segments:
        duree_cible = seg["fin"] - seg["debut"]
        sortie = os.path.join(dossier_segments, f"seg_{seg['id']:03d}.wav")
        seg["wav_en"] = synthetiser(seg["texte_en"], reference, duree_cible, sortie)
    _chrono(temps, "5_synthese", t)

    # ⑥ Recalage des durées
    t = time.perf_counter()
    segments, rapport = aligner_segments(
        segments,
        dossier_sortie=os.path.join(dossier_sortie, "alignes"),
        fichier_rapport=os.path.join(dossier_sortie, "rapport_durees.json"),
    )
    _chrono(temps, "6_recalage", t)

    # Sauvegarde avant l'assemblage : utile même si l'étape 7 plante
    with open(os.path.join(dossier_sortie, "segments.json"), "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    # ⑦ Assemblage
    t = time.perf_counter()
    video_doublee = assembler(
        chemin_video, segments, fond,
        os.path.join(dossier_sortie, "video_doublee.mp4"))
    _chrono(temps, "7_assemblage", t)

    with open(os.path.join(dossier_sortie, "temps.json"), "w", encoding="utf-8") as f:
        json.dump(temps, f, indent=2)
    return video_doublee
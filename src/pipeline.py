"""Relie toutes les étapes, de la vidéo française à la vidéo doublée.
Chronomètre chaque étape et enregistre les segments dans segments.json.
Responsable : Khadidiatou
"""


def doubler_video(chemin_video, dossier_sortie, consentement=False):
    """Lance tout le pipeline sur une vidéo.

    consentement : si False, on n'utilise pas la voix clonée mais une voix neutre.
    Renvoie : le chemin de la vidéo doublée.
    """
    # ① extraire_audio          (audio.py)
    # ② separer_voix_fond       (audio.py)
    # ③ transcrire              (asr.py)      -> crée les segments
    # ④ traduire                (translate.py) -> remplit "texte_en"
    # ⑤ synthetiser             (tts.py)      -> pour chaque segment
    # ⑥ recaler                 (align.py)    -> pour chaque segment, remplit "wav_en"
    # ⑦ assembler               (assemble.py)
    raise NotImplementedError("À faire par Khadidiatou")
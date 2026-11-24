"""Étape ⑧ : interface de démonstration Gradio.
Pas de voix clonée si la case de consentement n'est pas cochée.
Responsable : Fatoumata
"""

import json
import os

import gradio as gr

from src.pipeline import doubler_video

DOSSIER_SORTIE = "sorties"


def traiter(chemin_video, consentement):
    """Double la vidéo, puis renvoie la vidéo doublée et le tableau des phrases."""
    chemin_double = doubler_video(chemin_video, DOSSIER_SORTIE, consentement)
    with open(os.path.join(DOSSIER_SORTIE, "segments.json"), encoding="utf-8") as f:
        segments = json.load(f)
    tableau = [[s["debut"], s["fin"], s["texte_fr"], s["texte_en"]] for s in segments]
    return chemin_double, tableau


def lancer_interface():
    """Crée la page web : déposer une vidéo, cocher le consentement,
    récupérer la vidéo doublée et le tableau des phrases.
    """
    page = gr.Interface(
        fn=traiter,
        inputs=[
            gr.Video(label="Vidéo en français"),
            gr.Checkbox(label="La personne filmée a signé son consentement pour le clonage de sa voix"),
        ],
        outputs=[
            gr.Video(label="Vidéo doublée en anglais (voix générée par IA)"),
            gr.Dataframe(headers=["Début (s)", "Fin (s)", "Français", "Anglais"], label="Phrases"),
        ],
        title="Doublage FR → EN avec voix clonée",
        description="Sans consentement coché, une voix neutre est utilisée à la place de la voix clonée.",
    )
    page.launch(share=True)


if __name__ == "__main__":
    lancer_interface()
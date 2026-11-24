# Doublage avec voix clonée (FR → EN)

Projet P4 · Groupe 1 · École du Code Sonatel Academy (ODC) · Module IA Voix et Vidéo

On prend une vidéo de 2 minutes où une personne parle **français**, et on produit la même vidéo **doublée en anglais avec sa propre voix** (voix clonée), synchronisée phrase par phrase, avec la musique de fond conservée et la mention « Voix générée par IA ».

## Le pipeline

| Étape | Outil | Fichier |
|---|---|---|
| ① Extraction du son | ffmpeg | `src/audio.py` |
| ② Séparation voix / fond | Demucs | `src/audio.py` |
| ③ Transcription | faster-whisper large-v3 + VAD | `src/asr.py` |
| ④ Traduction | MarianMT opus-mt-fr-en | `src/translate.py` |
| ⑤ Voix clonée (meilleur de 3) | XTTS-v2 | `src/tts.py` |
| ⑥ Recalage des durées | | `src/align.py` |
| ⑦ Assemblage + mention IA | ffmpeg | `src/assemble.py` |
| ⑧ Interface de démo | Gradio | `app.py` |

`src/pipeline.py` lance les étapes dans l'ordre.

## Qui fait quoi

**Fatoumata**
- Étapes ① ② ③ : `src/audio.py`, `src/asr.py`
- Interface Gradio : `app.py`
- Mesure CER et temps de calcul : `eval/cer.py`
- `README.md`

**Khadidiatou**
- Étapes ④ ⑥ : `src/translate.py`, `src/align.py`
- Enchaînement des étapes : `src/pipeline.py`
- Mesure de l'écart de durée : `eval/durations.py`
- Documents : `docs/`

**Alassane**
- Étapes ⑤ ⑦ : `src/tts.py`, `src/assemble.py`
- Notebook de démo : `notebooks/demo_colab.ipynb`
- Test d'écoute : `eval/test_ecoute/`
- Dépendances : `requirements.txt`

**Chacun modifie uniquement ses fichiers.** C'est ce qui évite les conflits Git.

## Pour commencer (à faire une seule fois)

1. Accepter l'invitation GitHub (reçue par e-mail).
2. Faire les réglages Git du **Guide technique**.
3. Copier le projet sur son ordinateur :
   ```bash
   git clone https://github.com/Fattimm/projet-IA-voix-video-doublage-voix-clonee.git
   cd projet-IA-voix-video-doublage-voix-clonee
   ```

## Pour chaque tâche (toujours les mêmes étapes)

1. Récupérer la dernière version :
   ```bash
   git switch main
   git pull
   ```
2. Créer sa branche : `git switch -c prenom/tache` (exemple : `khadidiatou/traduction`).
3. Écrire le code **uniquement dans ses fichiers**.
4. Sauvegarder :
   ```bash
   git add nom_du_fichier.py
   git commit -m "ce que j'ai fait"
   ```
5. Envoyer sa branche sur GitHub : `git push -u origin prenom/tache`
6. Sur GitHub, ouvrir une **Pull Request** et demander une relecture à un autre membre.
7. Quand elle est approuvée et fusionnée, revenir à l'étape 1 pour la tâche suivante.

## Première tâche de chacun

- **Fatoumata** : branche `fatoumata/audio`, puis remplir `src/audio.py` (ffmpeg + Demucs).
- **Khadidiatou** : branche `khadidiatou/traduction`, puis remplir `src/translate.py`. Préparer aussi les formulaires de consentement.
- **Alassane** : branche `alassane/installation`, puis tester l'installation sur Colab (XTTS, Whisper, Demucs) et remplir `requirements.txt`.

Toutes les tâches, jour par jour, sont dans [TACHES.md](TACHES.md). Chacune a aussi son Issue sur GitHub.

## Le format des segments (à ne pas changer seul)

Toutes les étapes se passent une liste de segments (une phrase = un segment) :

```python
{"id": 0, "debut": 1.20, "fin": 4.85, "texte_fr": "Bonjour", "texte_en": "Hello", "wav_en": "sorties/seg_000.wav"}
```

`debut` et `fin` sont en secondes. Si vous avez besoin d'une nouvelle clé, on en parle d'abord au groupe.

## Règles Git de l'équipe

1. Jamais de travail directement sur `main`.
2. Une branche par tâche : `git switch -c nom-de-la-tache`.
3. Une Pull Request pour chaque tâche, relue et approuvée par un autre membre avant la fusion.
4. Avant de commencer à travailler : `git switch main` puis `git pull`.
5. **Jamais de vidéos, de sons ni de mots de passe sur GitHub** (ils vont sur le Drive).
6. Dans Colab, on fait seulement `git pull`, jamais de modification.

## Lancer le projet sur Colab

*À compléter après le test d'installation.*

## Éthique

- On ne clone que la voix d'une personne qui a **signé son consentement**.
- Toutes les vidéos produites portent la mention **« Voix générée par IA »**.
- XTTS-v2 est sous licence CPML : **usage non commercial uniquement**.
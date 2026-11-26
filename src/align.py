"""Étape ⑥ : recalage des durées des segments synthétisés."""
import json
import subprocess
from pathlib import Path

ACCEL_MAX = 1.3  # au-delà, la voix devient peu naturelle


def duree_audio(chemin):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(chemin)],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip())


def _ajuster(src, dst, facteur, duree_cible, remplir):
    filtres = []
    if facteur > 1.0:
        filtres.append(f"atempo={facteur:.4f}")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src)]
    if remplir:
        filtres.append("apad")  # silence jusqu'à la durée cible
    if filtres:
        cmd += ["-af", ",".join(filtres)]
    if remplir:
        cmd += ["-t", f"{duree_cible:.3f}"]
    cmd.append(str(dst))
    subprocess.run(cmd, check=True)


def aligner_segments(segments, dossier_sortie="sorties/alignes",
                     fichier_rapport="sorties/rapport_durees.json"):
    """Recale chaque segment sur sa fenêtre [debut, fin].
    Retourne (segments, rapport). 'wav_en' pointe vers le fichier recalé."""
    Path(dossier_sortie).mkdir(parents=True, exist_ok=True)
    rapport = []

    for seg in segments:
        cible = seg["fin"] - seg["debut"]
        cible = max(cible, 0.1)
        cible = max(cible, 0.1)  # évite une division par zéro
        d_avant = duree_audio(seg["wav_en"])
        facteur = 1.0
        if d_avant > cible:
            facteur = min(d_avant / cible, ACCEL_MAX)
        d_apres = d_avant / facteur
        depasse = d_apres > cible + 0.05  # tolérance de 50 ms

        dst = Path(dossier_sortie) / f"seg_{seg['id']:03d}_align.wav"
        _ajuster(seg["wav_en"], dst, facteur, cible, remplir=not depasse)

        rapport.append({
            "id": seg["id"],
            "duree_cible": round(cible, 3),
            "duree_avant": round(d_avant, 3),
            "duree_apres": round(d_apres, 3),
            "facteur": round(facteur, 3),
            "depasse": depasse,  # True => retraduire plus court
        })
        seg["wav_en"] = str(dst)

    Path(fichier_rapport).parent.mkdir(parents=True, exist_ok=True)
    with open(fichier_rapport, "w", encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=2)
    return segments, rapport
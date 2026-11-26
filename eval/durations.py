"""Mesure de l'écart de durée par segment (avant et après recalage).
Responsable : Khadidiatou
Lit sorties/rapport_durees.json, produit sorties/ecarts_durees.csv.
"""
import csv
import json
import statistics
import sys


def mesurer(chemin_rapport="sorties/rapport_durees.json",
            chemin_csv="sorties/ecarts_durees.csv"):
    with open(chemin_rapport, encoding="utf-8") as f:
        rapport = json.load(f)

    for r in rapport:
        r["ecart_avant"] = round(r["duree_avant"] - r["duree_cible"], 3)
        r["ecart_apres"] = round(r["duree_apres"] - r["duree_cible"], 3)

    avant = [abs(r["ecart_avant"]) for r in rapport]
    apres = [max(r["ecart_apres"], 0) for r in rapport]  # dépassement seulement
    n = len(rapport)
    ok = sum(1 for r in rapport if not r["depasse"])

    print(f"Segments : {n}")
    print(f"Écart absolu moyen AVANT recalage : {statistics.mean(avant):.2f} s")
    print(f"Dépassement moyen APRÈS recalage  : {statistics.mean(apres):.2f} s")
    print(f"Segments qui tiennent dans leur fenêtre : {ok}/{n} ({100 * ok / n:.0f} %)")

    with open(chemin_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rapport[0].keys())
        w.writeheader()
        w.writerows(rapport)
    print(f"Détail écrit dans {chemin_csv}")


if __name__ == "__main__":
    mesurer(*sys.argv[1:3])
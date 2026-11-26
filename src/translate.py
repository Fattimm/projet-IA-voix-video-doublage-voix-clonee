"""Étape ④ : traduction FR -> EN avec MarianMT (opus-mt-fr-en)."""
import torch
from transformers import MarianMTModel, MarianTokenizer

NOM_MODELE = "Helsinki-NLP/opus-mt-fr-en"
_tokenizer = None
_model = None


def _charger():
    global _tokenizer, _model
    if _model is None:
        _tokenizer = MarianTokenizer.from_pretrained(NOM_MODELE)
        _model = MarianMTModel.from_pretrained(NOM_MODELE)
        _model.to("cuda" if torch.cuda.is_available() else "cpu")
        _model.eval()
    return _tokenizer, _model


def traduire_textes(textes, taille_lot=8, num_beams=4):
    """Traduit une liste de phrases françaises en anglais."""
    tok, model = _charger()
    resultats = []
    for i in range(0, len(textes), taille_lot):
        lot = textes[i:i + taille_lot]
        entrees = tok(lot, return_tensors="pt", padding=True, truncation=True)
        entrees = {k: v.to(model.device) for k, v in entrees.items()}
        with torch.no_grad():
            sorties = model.generate(**entrees, num_beams=num_beams, max_new_tokens=256)
        resultats += tok.batch_decode(sorties, skip_special_tokens=True)
    return resultats


def traduire_segments(segments):
    """Remplit la clé 'texte_en' de chaque segment (format du README inchangé)."""
    textes = [s["texte_fr"].strip() for s in segments]
    traductions = traduire_textes(textes)
    for seg, trad in zip(segments, traductions):
        seg["texte_en"] = trad
    return segments


def traduire_court(texte_fr, n_candidats=5):
    """Renvoie la traduction la plus courte parmi n candidates
    (utile quand la phrase anglaise est trop longue pour le segment)."""
    tok, model = _charger()
    entrees = tok([texte_fr], return_tensors="pt", truncation=True)
    entrees = {k: v.to(model.device) for k, v in entrees.items()}
    with torch.no_grad():
        sorties = model.generate(
            **entrees, num_beams=n_candidats + 2,
            num_return_sequences=n_candidats, max_new_tokens=256,
        )
    candidats = tok.batch_decode(sorties, skip_special_tokens=True)
    return min(candidats, key=len)


if __name__ == "__main__":
    test = [
        {"id": 0, "debut": 1.20, "fin": 4.85, "texte_fr": "Bonjour à tous, bienvenue à l'UCAD."},
        {"id": 1, "debut": 5.00, "fin": 8.00, "texte_fr": "L'inscription coûte 10 000 F CFA."},
    ]
    for s in traduire_segments(test):
        print(s["id"], s["texte_fr"], "->", s["texte_en"])
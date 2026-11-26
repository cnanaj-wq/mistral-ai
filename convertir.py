"""Demande à Mistral de convertir les expressions Spotfire de cas.json en expressions Qlik Sense.

Usage : python convertir.py
La clé se lit dans le fichier .env (ignoré par Git, voir .env.example), sinon dans la variable
d'environnement MISTRAL_API_KEY. Elle n'est jamais affichée. Le modèle se choisit avec la
variable d'environnement MISTRAL_MODELE.
Résultat : conversions.json
"""

import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

DOSSIER = pathlib.Path(__file__).parent
ADRESSE = "https://api.mistral.ai/v1/chat/completions"
MODELE = os.environ.get("MISTRAL_MODELE", "mistral-medium-latest")

CONSIGNE = """Tu convertis une expression Spotfire en expression Qlik Sense.

{modele}

Règles
- L'expression Qlik doit donner le même nombre que l'expression Spotfire avec sa limitation.
- La limitation Spotfire entre dans l'expression Qlik par analyse d'ensembles.
- N'utilise que les champs décrits ci-dessus.
- Réponds par un objet JSON avec deux clés : "expression" (l'expression Qlik, sur une ligne,
  sans signe égal au début) et "explication" (une phrase en français)."""

QUESTION = """Table Spotfire : {table_spotfire}
Limitation de données : {limitation_spotfire}
Expression : {expression_spotfire}"""


def demander(cle, consigne, question):
    corps = {
        "model": MODELE,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": consigne},
            {"role": "user", "content": question},
        ],
    }
    requete = urllib.request.Request(
        ADRESSE,
        data=json.dumps(corps).encode("utf-8"),
        headers={"Authorization": "Bearer " + cle, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(requete, timeout=60) as reponse:
        contenu = json.load(reponse)
    return json.loads(contenu["choices"][0]["message"]["content"]), contenu.get("model", MODELE)


def lire_cle():
    """La clé du fichier .env, sinon celle de la variable d'environnement."""
    fichier = DOSSIER / ".env"
    if fichier.exists():
        for ligne in fichier.read_text(encoding="utf-8-sig").splitlines():
            nom, _, valeur = ligne.partition("=")
            if nom.strip() == "MISTRAL_API_KEY" and valeur.strip():
                return valeur.strip().strip("\"'")
    return os.environ.get("MISTRAL_API_KEY", "")


def main():
    cle = lire_cle()
    if not cle or not cle.isascii() or " " in cle:
        sys.exit("Clé MISTRAL_API_KEY absente ou invalide dans .env : rien n'a été envoyé.")
    consigne = CONSIGNE.format(modele=(DOSSIER / "modele_qlik.md").read_text(encoding="utf-8"))
    cas = json.loads((DOSSIER / "cas.json").read_text(encoding="utf-8"))
    conversions = []
    for un_cas in cas:
        try:
            reponse, modele = demander(cle, consigne, QUESTION.format(**un_cas))
        except urllib.error.HTTPError as erreur:
            sys.exit("Mistral a refusé la demande : %s %s" % (erreur.code, erreur.reason))
        conversions.append(
            {
                "id": un_cas["id"],
                "modele": modele,
                "expression": str(reponse.get("expression", "")).strip(),
                "explication": str(reponse.get("explication", "")).strip(),
            }
        )
        print("%-16s %s" % (un_cas["id"], conversions[-1]["expression"]))
    (DOSSIER / "conversions.json").write_text(
        json.dumps(conversions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()

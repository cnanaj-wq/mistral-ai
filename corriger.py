"""Second essai : renvoie à Mistral ce que Qlik Sense a constaté, et lui demande de se corriger.

Usage : python corriger.py <identifiant de l'application Qlik>
Part de conversions.json. Chaque expression est exécutée dans Qlik Sense ; si elle n'est pas
conforme, Mistral reçoit sa propre réponse et le constat de Qlik, sans la valeur attendue ni
indication sur la cause. Deux corrections au plus par cas. Résultat : corrections.json
"""

import json
import sys
import urllib.error

from controler import evaluer
from convertir import CONSIGNE, DOSSIER, QUESTION, demander, lire_cle

CORRECTIONS_MAX = 2


def constat(valeur, erreur):
    """Ce que Qlik Sense a répondu, dit à Mistral tel quel."""
    if valeur is None:
        observe = "Qlik Sense répond : %s." % erreur
    else:
        observe = "elle renvoie %s, ce qui n'est pas le nombre que donne Spotfire." % valeur
    return (
        "J'ai exécuté ton expression dans Qlik Sense : %s "
        "Corrige l'expression et réponds dans le même format JSON." % observe
    )


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    application = sys.argv[1]
    cle = lire_cle()
    if not cle or not cle.isascii() or " " in cle:
        sys.exit("Clé MISTRAL_API_KEY absente ou invalide dans .env : rien n'a été envoyé.")
    consigne = CONSIGNE.format(modele=(DOSSIER / "modele_qlik.md").read_text(encoding="utf-8"))
    cas = {c["id"]: c for c in json.loads((DOSSIER / "cas.json").read_text(encoding="utf-8"))}
    conversions = json.loads((DOSSIER / "conversions.json").read_text(encoding="utf-8"))
    corrections = []
    for conversion in conversions:
        un_cas = cas[conversion["id"]]
        expression, demandes, essais = conversion["expression"], 1, [conversion["expression"]]
        messages = [
            {"role": "system", "content": consigne},
            {"role": "user", "content": QUESTION.format(**un_cas)},
        ]
        while True:
            valeur, erreur = evaluer(application, expression)
            conforme = (
                valeur is not None
                and abs(valeur - un_cas["valeur_attendue"]) <= un_cas["tolerance"]
            )
            if conforme or demandes > CORRECTIONS_MAX:
                break
            messages += [
                {"role": "assistant", "content": json.dumps({"expression": expression})},
                {"role": "user", "content": constat(valeur, erreur)},
            ]
            try:
                reponse, _ = demander(cle, messages)
            except urllib.error.HTTPError as echec:
                sys.exit("Mistral a refusé la demande : %s %s" % (echec.code, echec.reason))
            expression = str(reponse.get("expression", "")).strip()
            essais.append(expression)
            demandes += 1
        corrections.append(
            {
                "id": un_cas["id"],
                "modele": conversion["modele"],
                "expression": expression,
                "demandes": demandes,
                "conforme": conforme,
                "essais": essais,
            }
        )
        print(
            "%-16s %d demande(s) %-13s %s"
            % (un_cas["id"], demandes, "conforme" if conforme else "non conforme", expression)
        )
    (DOSSIER / "corrections.json").write_text(
        json.dumps(corrections, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()

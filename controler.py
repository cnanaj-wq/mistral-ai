"""Exécute chaque expression Qlik dans l'application et compare son résultat à la valeur attendue.

Usage : python controler.py <identifiant de l'application Qlik>
Demande l'outil en ligne de commande « qlik », déjà connecté au tenant.
Contrôle jusqu'à trois séries : la migration manuelle (cas.json), le résultat de convertir.py
(conversions.json) et celui de corriger.py (corrections.json), s'ils existent. Résultat : resultats.md
"""

import json
import pathlib
import subprocess
import sys

DOSSIER = pathlib.Path(__file__).parent


def evaluer(application, expression):
    """Valeur de l'expression dans l'application, ou le message d'erreur de Qlik."""
    sortie = subprocess.run(
        ["qlik", "app", "eval", expression, "--app", application],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=90,
    )
    lignes = [ligne for ligne in sortie.stdout.splitlines() if ligne.strip()]
    if sortie.returncode != 0 or len(lignes) < 2:
        return None, (sortie.stderr or sortie.stdout).strip()[:200]
    texte = lignes[-1].strip()
    if texte == "-":
        return None, "Qlik ne renvoie aucune valeur (expression invalide)"
    try:
        # Qlik affiche les nombres à la française : espace des milliers, virgule décimale
        return float(texte.replace("\u00a0", "").replace(" ", "").replace(",", ".")), ""
    except ValueError:
        return None, texte[:200]


def controler(application, cas, expressions):
    lignes = []
    for un_cas in cas:
        expression = expressions.get(un_cas["id"], "")
        valeur, erreur = evaluer(application, expression) if expression else (None, "absente")
        conforme = (
            valeur is not None and abs(valeur - un_cas["valeur_attendue"]) <= un_cas["tolerance"]
        )
        lignes.append((un_cas, expression, valeur, erreur, conforme))
    return lignes


def tableau(titre, lignes):
    conformes = sum(1 for ligne in lignes if ligne[4])
    texte = ["## %s : %d conformes sur %d" % (titre, conformes, len(lignes)), ""]
    texte += ["| Cas | Expression Qlik | Attendu | Obtenu | Conforme |", "|---|---|---|---|---|"]
    for un_cas, expression, valeur, erreur, conforme in lignes:
        obtenu = ("%.4f" % valeur) if valeur is not None else "erreur : " + erreur
        texte.append(
            "| %s | `%s` | %.4f | %s | %s |"
            % (
                un_cas["libelle"],
                expression.replace("|", "\\|"),
                un_cas["valeur_attendue"],
                obtenu.replace("|", "\\|").replace("\n", " "),
                "oui" if conforme else "non",
            )
        )
    return texte + [""]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    application = sys.argv[1]
    cas = json.loads((DOSSIER / "cas.json").read_text(encoding="utf-8"))
    texte = ["# Résultats du contrôle", ""]
    manuelle = {un_cas["id"]: un_cas["qlik_migration_manuelle"] for un_cas in cas}
    texte += tableau("Migration manuelle", controler(application, cas, manuelle))
    fichier = DOSSIER / "conversions.json"
    if fichier.exists():
        conversions = json.loads(fichier.read_text(encoding="utf-8"))
        mistral = {c["id"]: c["expression"] for c in conversions}
        modele = conversions[0]["modele"] if conversions else "?"
        texte += tableau(
            "Conversion par Mistral (%s)" % modele, controler(application, cas, mistral)
        )
    fichier = DOSSIER / "corrections.json"
    if fichier.exists():
        corrections = json.loads(fichier.read_text(encoding="utf-8"))
        corrige = {c["id"]: c["expression"] for c in corrections}
        texte += tableau(
            "Conversion par Mistral après retour de Qlik Sense",
            controler(application, cas, corrige),
        )
        texte += ["Demandes envoyées à Mistral par cas, première conversion comprise :", ""]
        texte += ["- %s : %d" % (c["id"], c["demandes"]) for c in corrections] + [""]
    (DOSSIER / "resultats.md").write_text("\n".join(texte), encoding="utf-8")
    print("\n".join(texte))


if __name__ == "__main__":
    main()

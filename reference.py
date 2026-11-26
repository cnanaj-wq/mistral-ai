"""Recalcule depuis data/ la valeur attendue de chaque cas et la compare à cas.json.

Usage : python reference.py
C'est le témoin du POC : il ne dépend ni de Mistral ni de Qlik Sense. Chaque calcul applique
la limitation Spotfire puis l'expression Spotfire, en Python.
"""

import csv
import json
import pathlib
import sys

DOSSIER = pathlib.Path(__file__).parent


def lignes(table):
    with open(DOSSIER / "data" / (table + ".csv"), encoding="utf-8-sig", newline="") as fichier:
        return list(csv.DictReader(fichier))


def somme(table, colonne):
    return sum(float(ligne[colonne]) for ligne in table)


def clos_2026(ligne):
    return ligne["Exercice"] == "2026" and int(ligne["Mois"]) <= 10


def calculer():
    ventes = [ligne for ligne in lignes("ventes") if clos_2026(ligne)]
    resultat = [
        ligne
        for ligne in lignes("compte_resultat")
        if clos_2026(ligne) and int(ligne["Ordre"]) <= 7
    ]
    effets = [
        ligne
        for ligne in lignes("ecarts_marge")
        if ligne["Exercice"] == "2026" and ligne["Type"] == "Effet"
    ]
    return {
        "ca_cumule": somme(ventes, "CA Réel"),
        "taux_marge": 100 * somme(ventes, "Marge brute Réel") / somme(ventes, "CA Réel"),
        "ecart_ca_budget": 100 * (somme(ventes, "CA Réel") / somme(ventes, "CA Budget") - 1),
        "ebitda": somme(resultat, "Réel"),
        "effets_marge": somme(effets, "Montant") / 1000,
    }


def main():
    cas = json.loads((DOSSIER / "cas.json").read_text(encoding="utf-8"))
    calcule = calculer()
    ecarts = 0
    for un_cas in cas:
        valeur = calcule[un_cas["id"]]
        conforme = abs(valeur - un_cas["valeur_attendue"]) <= un_cas["tolerance"]
        ecarts += not conforme
        print(
            "%-4s %-16s attendu %16.4f  recalculé %16.4f"
            % ("OK" if conforme else "ÉCART", un_cas["id"], un_cas["valeur_attendue"], valeur)
        )
    if ecarts:
        sys.exit("%d valeur(s) attendue(s) ne correspondent pas aux données." % ecarts)
    print("Les %d valeurs attendues se retrouvent dans data/." % len(cas))


if __name__ == "__main__":
    main()

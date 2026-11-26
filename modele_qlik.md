Modèle de données de l'application Qlik Sense cible.

Dans Spotfire, chaque fichier est une table indépendante : ventes, compte_resultat,
ecarts_marge. Un visuel porte une expression et une limitation de données (clause where).

Dans Qlik Sense, toutes ces lignes sont dans une seule table de faits. Il n'y a pas de clause
where : la limitation doit entrer dans l'expression, par analyse d'ensembles.

Champs communs
- Exercice : année, numérique (2024, 2025, 2026). Vient du calendrier.
- Mois : numéro du mois, de 1 à 12. Vient du calendrier.
- [Mois clos] : 1 si le mois est inférieur ou égal à 10, sinon 0.
- BU, Région, Canal, Produit : mêmes noms que dans Spotfire.

Table Spotfire « ventes » : mêmes noms de champs dans Qlik
- [CA Réel], [CA Budget], [CA N-1]
- [Marge brute Réel], [Marge brute Budget], [Marge brute N-1]

Table Spotfire « compte_resultat » : champs renommés dans Qlik
- [Réel] devient [CR Réel]
- [Budget] devient [CR Budget]
- [N-1] devient [CR N-1]
- [Ordre] devient [Ordre rubrique]
- [Rubrique] garde son nom

Table Spotfire « ecarts_marge » : champs renommés dans Qlik
- [Montant] devient [Écart de marge]
- [Ordre] devient [Ordre poste]
- [Type] devient [Type de poste]
- [Poste] garde son nom

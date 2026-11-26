# Résultats du contrôle

## Migration manuelle : 5 conformes sur 5

| Cas | Expression Qlik | Attendu | Obtenu | Conforme |
|---|---|---|---|---|
| Chiffre d'affaires réel, cumul 2026 sur les mois clôturés | `Sum({<Exercice={2026}, [Mois clos]={1}>} [CA Réel])` | 74215646.7100 | 74215646.7100 | oui |
| Taux de marge brute en %, cumul 2026 sur les mois clôturés | `100 * Sum({<Exercice={2026}, [Mois clos]={1}>} [Marge brute Réel]) / Sum({<Exercice={2026}, [Mois clos]={1}>} [CA Réel])` | 29.4514 | 29.4514 | oui |
| Écart de chiffre d'affaires au budget en %, cumul 2026 sur les mois clôturés | `100 * (Sum({<Exercice={2026}, [Mois clos]={1}>} [CA Réel]) / Sum({<Exercice={2026}, [Mois clos]={1}>} [CA Budget]) - 1)` | 1.0753 | 1.0753 | oui |
| EBITDA réel, cumul 2026 sur les mois clôturés | `Sum({<Exercice={2026}, [Mois clos]={1}, [Ordre rubrique]={"<=7"}>} [CR Réel])` | 5311850.5900 | 5311850.5900 | oui |
| Somme des effets volume, prix et coûts d'achat en k€, exercice 2026 | `Sum({<Exercice={2026}, [Type de poste]={'Effet'}>} [Écart de marge]) / 1000` | -1072.4964 | -1072.4964 | oui |

## Conversion par Mistral (mistral-medium-latest) : 1 conformes sur 5

| Cas | Expression Qlik | Attendu | Obtenu | Conforme |
|---|---|---|---|---|
| Chiffre d'affaires réel, cumul 2026 sur les mois clôturés | `Sum({<[Exercice]={2026}, [Mois]={<=10}>} [CA Réel])` | 74215646.7100 | erreur : Qlik ne renvoie aucune valeur (expression invalide) | non |
| Taux de marge brute en %, cumul 2026 sur les mois clôturés | `100 * Sum({<[Exercice]={2026}, [Mois]={<=10}>} [Marge brute Réel]) / Sum({<[Exercice]={2026}, [Mois]={<=10}>} [CA Réel])` | 29.4514 | erreur : Qlik ne renvoie aucune valeur (expression invalide) | non |
| Écart de chiffre d'affaires au budget en %, cumul 2026 sur les mois clôturés | `100 * (Sum({<[Exercice]={2026}, [Mois]={<=10}>} [CA Réel]) / Sum({<[Exercice]={2026}, [Mois]={<=10}>} [CA Budget]) - 1)` | 1.0753 | erreur : Qlik ne renvoie aucune valeur (expression invalide) | non |
| EBITDA réel, cumul 2026 sur les mois clôturés | `Sum({<[Exercice]={2026}, [Mois]={<=10}, [Ordre rubrique]={<=7}>} [CR Réel])` | 5311850.5900 | erreur : Qlik ne renvoie aucune valeur (expression invalide) | non |
| Somme des effets volume, prix et coûts d'achat en k€, exercice 2026 | `Sum({<[Exercice]={2026}, [Type de poste]={'Effet'}>} [Écart de marge]) / 1000` | -1072.4964 | -1072.4964 | oui |

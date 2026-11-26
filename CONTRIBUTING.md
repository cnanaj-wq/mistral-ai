# Contribuer

Les corrections et les idées sont les bienvenues.

## Signaler une anomalie ou proposer une idée

Ouvre une issue avec le modèle proposé. Indique ce que tu as lancé, ce que tu attendais et ce que tu as obtenu.

## Proposer une modification

1. Crée une branche à partir de `main`.
2. Lance les contrôles avant de pousser :

   ```powershell
   pip install -r requirements.txt
   ruff check .
   ruff format --check .
   python reference.py
   ```

3. Si tu ajoutes un cas dans `cas.json`, ajoute son calcul dans `reference.py` : la valeur attendue doit se retrouver depuis `data/`.
4. Ouvre une pull request qui explique le pourquoi du changement.

## Règles

- Aucune clé d'API, aucun secret, aucune donnée personnelle.
- Les données restent fictives : aucun nom d'entreprise ou de client réel.
- Un résultat de conversion se publie tel qu'il est sorti, échecs compris.

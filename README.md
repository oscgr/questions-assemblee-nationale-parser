# questions-assemblee-nationale-parser

## Présentation
Parse le JSON fourni par l'Assemblée Nationale (http://data.assemblee-nationale.fr/travaux-parlementaires/questions/questions-au-gouvernement) qui présente la liste des questions posées au Gouvernement ainsi que les réponses de ce dernier lors des séances publiques dédiées les mardis et mercredis depuis le début de la quatorzième législature (juin 2012).

## Output
Le parser compte l'occurence des mots prononcés plus de X fois (1000 par défaut, environ 130 mots différents) et les trie par date puis par parti politique, avec leur occurence correspondante.

## Comment ça marche ?
 - Téléchargez le fichier JSON (voir au dessus)
 - Renommez le en `data.json` et mettez le à la racine
  - Certaines bibliothèques sont requises :
    - `ijson`
 - Lancez le projet (`python main.py`)
 - le script génère un fichier `output.json` à la racine

## Modèle
 - "ALL" (l'occurrence globale et non triée des mots)
    - mot : occurrence (int)
 - mois (format "ANNEE-MOIS")
    - trigramme parti politique
        - mot : occurrence (int)

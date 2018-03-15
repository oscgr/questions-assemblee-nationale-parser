# questions-assemblee-nationale-parser

## Présentation
Parse le [JSON fourni par l'Assemblée Nationale](http://data.assemblee-nationale.fr/travaux-parlementaires/questions/questions-au-gouvernement) qui présente la liste des questions posées au Gouvernement ainsi que les réponses de ce dernier lors des séances publiques dédiées les mardis et mercredis depuis le début de la quatorzième législature (juin 2012).

## Output
Le parser compte l'occurence des mots prononcés plus de 100 fois et les trie par date puis par parti politique, avec leur occurence correspondante.

## Comment ça marche ?
 - Téléchargez le fichier JSON (voir au dessus)
 - Renommez le en `data.json` et mettez le à la racine
  - Certaines bibliothèques sont requises :
    - `ijson`
 - Lancez le projet (`python main.py`)
 - le script génère un fichier `CSV.txt` à la racine

## Modèle
|mois|parti|mot|occurrence|
|---|---|---|---|
| 2012-01 | UMP | avoir | 20 |

## Et après ?

Le fichier peut être traité via un autre projet :
https://github.com/OGrainger/questions-assemblee-nationale-visualisation
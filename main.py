import ijson
import json
from helpers import *

# --- PARAMS ---


limit_word_occurence = 1000

# --------------


data = {"ALL": {}}
FRENCH_BASIC_DICTIONARY = open("dictionary.txt").read().split('\n')
parser = ijson.parse(open('data.json'))
output = open('output.json', 'w')

print("00 - CAPTURING WORDS...")

for prefix, event, value in parser:

    if prefix == 'questionsGvt.question.item.textesReponse.texteReponse.texte':
        text = unicode_normalize(value)
        data = data_handler_ALL(data, text)

print("01 - PARSED DATA")
print("10 - LIMITING WORDS BY OCCURENCE AND COMMON USE...")

data = remove_words_with_less_than_x_occurrences(data, limit_word_occurence, FRENCH_BASIC_DICTIONARY)

print("11 - LIMITED WORDS TO " + str(limit_word_occurence) + " OCCURRENCES")
print("20 - POPULATING DATA PER DATE AND PARTY...")

parser.close()
parser = ijson.parse(open('data.json'))

group = "null"
date = "null"
text = "null"

for prefix, event, value in parser:

    if prefix == 'questionsGvt.question.item.auteur.groupe.abrege':
        group = unicode_normalize(value)

    if prefix == 'questionsGvt.question.item.textesReponse.texteReponse.infoJO.dateJO':
        date = unicode_normalize(value)

    if prefix == 'questionsGvt.question.item.textesReponse.texteReponse.texte':
        text = unicode_normalize(value)
        data = data_handler(data, date, group, text)

print("21 - POPULATED DATA")
print("30 - WRITING TO FILE...")

output.write(json.dumps(data))
output.close()

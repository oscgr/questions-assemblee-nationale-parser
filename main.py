import ijson
import json
from helpers import *

# --- PARAMS ---


limit_word_occurence = 800

# --------------


data = {"ALL": {}, "FILTERED": {}}
FRENCH_BASIC_DICTIONARY = open("dictionary.txt").read().split('\n')
parser = ijson.parse(open('data.json'))
output_json = open('JSON_output.json', 'w')
output_CSV_filtered = open('CSV.txt', 'w')

print("00 - CAPTURING WORDS...")

for prefix, event, value in parser:

    if prefix == 'questionsGvt.question.item.textesReponse.texteReponse.texte':
        text = unicode_normalize(value)
        data = data_parser_ALL(data, text)

print("01 - PARSED DATA")
print("10 - LIMITING WORDS BY OCCURENCE AND COMMON USE...")

data = remove_words(data, limit_word_occurence, FRENCH_BASIC_DICTIONARY)

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
        data = data_parser_FILTERED(data, date, group, text)

print("21 - POPULATED DATA")
print("30 - GENERATING CSV...")

csv_filtered = csv_generator_filtered(data)

print("31 - GENERATED CSV")
print("40 - WRITING TO FILE...")

output_json.write(json.dumps(data))
output_json.close()

output_CSV_filtered.write(csv_filtered)
output_CSV_filtered.close()

import ijson
import json
import unicodedata
import re


data = {"ALL": {}}

limit_word_occurence = 1000

FRENCH_BASIC_DICTIONARY = open("dictionary.txt").read().split('\n')

ignore_word_regex_1 = re.compile('[=<>]')
ignore_word_regex_2 = re.compile('[0-9]')
remove_html_tag_regex = re.compile('<[^>]*>')
remove_special_char_regex = re.compile('[-(.),;:\']')


def unicode_normalize(t):
    return unicodedata.normalize('NFKD', t).encode('ascii', 'ignore')


def ignore_word(word):
    if len(word) <= 2:
        return True
    if re.match(ignore_word_regex_1, word):
        return True
    if re.match(ignore_word_regex_2, word):
        return True
    return False


def data_handler_ALL(h_text):
    h_text = h_text.lower()
    h_text = re.sub(remove_special_char_regex, ' ', h_text)
    h_text = re.sub(remove_html_tag_regex, ' ', h_text)

    words = h_text.split(' ')

    for word in words:
        if not ignore_word(word):
            try:
                data["ALL"][word] += 1
            except:
                data["ALL"][word] = 1


def data_handler(h_date, h_group, h_text):

    h_text = h_text.lower()
    h_text = re.sub(remove_special_char_regex, ' ', h_text)
    h_text = re.sub(remove_html_tag_regex, ' ', h_text)
    words = h_text.split(' ')
    h_date = h_date.split('-')[0] + '-' + h_date.split('-')[1]

    try:
        data[h_date]
    except:
        data[h_date] = {}
    try:
        data[h_date][h_group]
    except:
        data[h_date][h_group] = {}

    for word in words:
        if word in data["ALL"] and not ignore_word(word):
            try:
                data[h_date][h_group][word] += 1
            except:
                data[h_date][h_group][word] = 1


# ----------------------------------------------------------------------------

parser = ijson.parse(open('data.json'))

output = open('output.json', 'w')

print("00 - CAPTURING WORDS...")

for prefix, event, value in parser:

    if prefix == 'questionsGvt.question.item.textesReponse.texteReponse.texte':
        text = unicode_normalize(value)
        data_handler_ALL(text)

print("01 - PARSED DATA")

print("10 - LIMITING WORDS BY OCCURENCE AND COMMON USE...")

for key, value in data["ALL"].items():
    if value < limit_word_occurence:
        data["ALL"].pop(key)
    elif key in FRENCH_BASIC_DICTIONARY:
        data["ALL"].pop(key)

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
        data_handler(date, group, text)

print("21 - POPULATED DATA")

print("30 - WRITING TO FILE...")

output.write(json.dumps(data))
output.close()

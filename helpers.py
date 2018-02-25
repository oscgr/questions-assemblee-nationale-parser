import unicodedata
import re

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


def data_parser_ALL(d, h_text):
    h_text = h_text.lower()
    h_text = re.sub(remove_special_char_regex, ' ', h_text)
    h_text = re.sub(remove_html_tag_regex, ' ', h_text)

    words = h_text.split(' ')

    for word in words:
        if not ignore_word(word):
            try:
                d["ALL"][word] += 1
            except:
                d["ALL"][word] = 1
    return d


def data_parser_FILTERED(d, h_date, h_group, h_text):
    h_text = h_text.lower()
    h_text = re.sub(remove_special_char_regex, ' ', h_text)
    h_text = re.sub(remove_html_tag_regex, ' ', h_text)
    words = h_text.split(' ')
    h_date = h_date.split('-')[0] + '-' + h_date.split('-')[1]

    try:
        d["FILTERED"][h_date]
    except:
        d["FILTERED"][h_date] = {}
    try:
        d["FILTERED"][h_date][h_group]
    except:
        d["FILTERED"][h_date][h_group] = {}

    for word in words:
        if word in d["ALL"] and not ignore_word(word):
            try:
                d["FILTERED"][h_date][h_group][word] += 1
            except:
                d["FILTERED"][h_date][h_group][word] = 1
    return d


def remove_words(data, limit, banned_words):

    for key, value in data["ALL"].items():

        if value < limit:
            data["ALL"].pop(key)
        elif key in banned_words:
            data["ALL"].pop(key)
    return data


def csv_generator_all(d):
    output = ""
    for k, v in d["ALL"].items():
        output += k + "," + str(v) + "\n"
    return output


def csv_generator_filtered(d):
    output = ""
    for date, partis in d["FILTERED"].items():
        for parti, words in partis.items():
            for word, occurrence in words.items():
                output += date + "," + parti + "," + word + "," + str(occurrence) + "\n"
    return output

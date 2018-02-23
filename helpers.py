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


def data_handler_ALL(d, h_text):
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


def data_handler(d, h_date, h_group, h_text):
    h_text = h_text.lower()
    h_text = re.sub(remove_special_char_regex, ' ', h_text)
    h_text = re.sub(remove_html_tag_regex, ' ', h_text)
    words = h_text.split(' ')
    h_date = h_date.split('-')[0] + '-' + h_date.split('-')[1]

    try:
        d[h_date]
    except:
        d[h_date] = {}
    try:
        d[h_date][h_group]
    except:
        d[h_date][h_group] = {}

    for word in words:
        if word in d["ALL"] and not ignore_word(word):
            try:
                d[h_date][h_group][word] += 1
            except:
                d[h_date][h_group][word] = 1
    return d


def remove_words_with_less_than_x_occurrences(data, limit, banned_words):
    for key, value in data["ALL"].items():
        if value < limit:
            data["ALL"].pop(key)
        elif key in banned_words:
            data["ALL"].pop(key)
    return data

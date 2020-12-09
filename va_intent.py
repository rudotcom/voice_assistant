"""
Здесь происходит распознввание интентов по совпадению с фразой конфига, по наличию императива
TODO: переделать - name теперь получается не в этих функциях, а в экземпляре класса Action
"""
from va_assistant import assistant, context
from fuzzywuzzy import process
from va_config import CONFIG


def intent_by_latent(phrase):
    """ есть ли в фразе скрытый интент """
    latent_where = words_in_phrase(CONFIG['intents']['find_out_where']['requests'], phrase)
    latent_wiki = words_in_phrase(CONFIG['intents']['find_out_wiki']['requests'], phrase)
    if latent_where:
        context.subject = context.text.partition(latent_where)[2]
        print('>>intent_by_latent = find_out_where')
        assistant.intent = 'find_out_where'
        return True
    elif latent_wiki:
        print('>>intent_by_latent = find_out_wiki')
        context.subject = context.text.partition(latent_wiki)[2]
        assistant.intent = 'find_out_wiki'
        return True
    else:
        return False


def intent_by_levenshtein(phrase, levenshtein=90):
    """ поиск интента по сходству с фразой пользователя. Расстояние Левенштейна """
    for intent, intent_data in CONFIG['intents'].items():
        levenshtein_distance = process.extractOne(phrase, intent_data['requests'])
        if levenshtein_distance[1] > levenshtein:
            levenshtein = levenshtein_distance[1]  # степень совпадения
            print('>>intent_by_levenshtein = ', intent)
            assistant.intent = intent
            word = levenshtein_distance[0].strip()
            context.text = phrase.replace(word, '')  # удаляем из фразы само совпадение
            return True
    return False  # если интент не найден


def intent_by_imperative():
    """ имеющиеся в CONFIG имеративы ? """
    for intent in CONFIG['intents'].keys():
        if context.imperative in CONFIG['intents'][intent]['requests']:
            assistant.intent = intent
            print('>>intent_by_imperative = ', intent)
            return True
    return False


def intent_in_phrase(phrase):
    for intent, intent_data in CONFIG['intents'].items():
        for conf in intent_data['requests']:
            if conf in phrase:
                print('>>intent_by_imperative = ', intent)
                assistant.intent = intent
                return True
    return False


def words_in_phrase(tuple1, phrase):
    for word in tuple(tuple1):
        if word in phrase:
            return word



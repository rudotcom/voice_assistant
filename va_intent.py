"""
Здесь происходит распознввание интентов по совпадению с фразой конфига, по наличию императива
"""
from va_assistant import context
from fuzzywuzzy import process
from va_config import CONFIG


def intent_by_latent(phrase: str) -> bool:
    """ есть ли в фразе скрытый интент """
    latent_where = words_in_phrase(CONFIG['intents']['find_out_where']['requests'], phrase)
    latent_wiki = words_in_phrase(CONFIG['intents']['find_out_wiki']['requests'], phrase)
    if latent_where:
        context.subject = context.text.partition(latent_where)[2]
        print('🛎 intent by latent: find_out_where')
        context.intent = 'find_out_where'
        context.target_value = 'https://yandex.ru/maps/?text='
        return True
    elif latent_wiki:
        print('📽 intent by latent: find_out_wiki')
        context.subject = context.text.partition(latent_wiki)[2]
        context.intent = 'find_out_wiki'
        return True
    else:
        return False


def intent_by_levenshtein(phrase: str, levenshtein: int = 90) -> bool:
    """ поиск интента по сходству с фразой пользователя. Расстояние Левенштейна """
    for intent, intent_data in CONFIG['intents'].items():
        levenshtein_distance = process.extractOne(phrase, intent_data['requests'])
        if levenshtein_distance[1] > levenshtein:
            levenshtein = levenshtein_distance[1]  # степень совпадения
            print('🎚 intent by levenshtein:', intent)
            context.intent = intent
            word = levenshtein_distance[0].strip()
            context.text = phrase.replace(word, '')  # удаляем из фразы само совпадение
            return True
    return False  # если интент не найден


def intent_by_imperative() -> bool:
    """ имеющиеся в CONFIG имеративы ? """
    for intent in CONFIG['intents'].keys():
        if context.imperative in CONFIG['intents'][intent]['requests']:
            context.intent = intent
            print('✂ intent by imperative:', intent)
            return True
    return False


def intent_in_phrase(phrase: str) -> bool:
    for intent, intent_data in CONFIG['intents'].items():
        for conf in intent_data['requests']:
            if conf in phrase:
                print('⚗ intent by imperative:', intent)
                context.intent = intent
                return True
    return False


def words_in_phrase(tuple1: tuple, phrase: str) -> str:
    for word in tuple(tuple1):
        if word in phrase:
            return word

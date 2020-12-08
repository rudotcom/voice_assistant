"""
Здесь происходит распознввание интентов по совпадению с фразой конфига, по наличию императива
"""
from va_assistant import assistant, context, new_context
import random
from fuzzywuzzy import process
from va_config import CONFIG


def inquire_subject(intent):
    """ запрос недостающего субъекта интента """
    assistant.speak(random.choice(CONFIG['intents'][intent]['spec']))


def subject_not_exist(subject):
    """ ответ пользователю, что такой субъект помощнику неизвестен """
    assistant.speak(' '.join([subject, random.choice(CONFIG['intents']['turn_on']['not_exists'])]))


def get_action_by_find():
    # значит намерение искать с помощью поискового инструмента
    if not context.source:
        context.source = 'в яндексе'
    context.subject = context.text.replace(context.source, '')
    if not context.subject:
        inquire_subject('find')
        return True
    context.action = CONFIG['intents']['find']['targets'][context.source]
    return True


def get_action_by_turn_on():
    context.action = 'turn_on'
    if not context.subject:
        inquire_subject('turn_on')
        return True
    else:
        if context.subject not in CONFIG['intents']['turn_on']['targets'].keys():
            subject_not_exist(context.subject)
            context.action = None
            return True
        else:
            context.subject = CONFIG['intents']['turn_on']['targets'][context.subject]
            return True


def get_action_by_intent_now(intent_now):
    # print('get action by intent now', intent_now)
    """ если у интента есть экшены """
    intent_data = CONFIG['intents'][intent_now]
    if 'action' in intent_data.keys():
        context.action = intent_data['action']
        return True
    return False


def get_action_by_imperative():
    intent_now = None
    """ имеющиеся в CONFIG имеративы ? """
    for intent_key in CONFIG['intents'].keys():
        if context.imperative in CONFIG['intents'][intent_key]['requests']:
            intent_now = intent_key

    if intent_now == 'find':
        return get_action_by_find()
    elif intent_now == 'turn_on':
        return get_action_by_turn_on()
    elif intent_now:
        """ все остальные императивы """
        return get_action_by_intent_now(intent_now)
    else:
        """ интенты не найдены """
        return False


def intent_by_levenshtein(phrase, levenshtein=90):
    """ поиск интента по сходству с фразой пользователя. Расстояние Левенштейна """
    intent_now = ''
    for intent, intent_data in CONFIG['intents'].items():
        levenshtein_distance = process.extractOne(phrase, intent_data['requests'])
        if levenshtein_distance[1] > levenshtein:
            levenshtein = levenshtein_distance[1]  # оценка совпадения
            intent_now = intent
            intent_words = levenshtein_distance[0].strip()  # само совпадение
            # print(phrase, '<-', intent_words, '=', levenshtein, '%')

    if intent_now:
        context.intent = intent_now
        print('intent <-', intent_now)
        context.text = phrase.replace(intent_words, '')

        get_action_by_intent_now(intent_now)
        return True

    return False  # если интент не найден


def reply_by_intent():
    if context.intent and 'replies' in CONFIG['intents'][context.intent].keys():
        return random.choice(CONFIG['intents'][context.intent]['replies'])


def has_latent(phrase):
    """ есть ли в фразе скрытый интент """
    latent_where = words_in_phrase(CONFIG['intents']['find_out_where']['requests'], phrase)
    latent_wiki = words_in_phrase(CONFIG['intents']['find_out_wiki']['requests'], phrase)
    if latent_where:
        context.subject = context.text.partition(latent_where)[2]
        context.intent = 'find_out_where'
        context.action = 'yandex_maps'
        return True
    elif latent_wiki:
        context.subject = context.text.partition(latent_wiki)[2]
        context.action = 'wikipedia'
        return True
    else:
        return False


def words_in_phrase(tuple1, phrase):
    for word in tuple(tuple1):
        if word in phrase:
            return word


def intent_in_phrase(phrase):
    for intent, intent_data in CONFIG['intents'].items():
        for conf in intent_data['requests']:
            if conf in phrase:
                get_action_by_intent_now(intent)
                return True
    return False

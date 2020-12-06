"""
Здесь происходит распознввание интентов по совпадению с фразой конфига, по наличию императива
"""
from va_assistant import assistant, context, new_context
import random
from fuzzywuzzy import process
from va_config import CONFIG


def inquire_subject(intent):
    assistant.speak(random.choice(CONFIG['intents'][intent]['spec']))


def subject_not_exist(subject):
    assistant.speak(' '.join([subject, random.choice(CONFIG['intents']['turn_on']['not_exists'])]))


def get_action_by_find():
    print('ищем с помощью инструмента')
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
    print('включаем музыку')
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
    print('get action by intent now', intent_now)
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
            print('intent found:', intent_now)

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
    intent_now = ''
    for intent, intent_data in CONFIG['intents'].items():
        levenshtein_distance = process.extractOne(phrase, intent_data['requests'])
        if levenshtein_distance[1] > levenshtein:
            levenshtein = levenshtein_distance[1]  # оценка совпадения
            intent_now = intent
            intent_words = levenshtein_distance[0].strip()  # само совпадение
            print(phrase, '<-', intent_words, '=', levenshtein, '%')

    if intent_now:
        context.intent = intent_now
        print('intent:', intent_now)
        context.text = phrase.replace(intent_words, '')

        get_action_by_intent_now(intent_now)
        return True

    return False  # если интент не найден


# def action_by_intent(intent_now):
#     intent_data = CONFIG['intents'][intent_now]
#     for choice in intent_data.keys():
#         if choice == 'actions':
#             for actions in intent_data['actions'].keys():
#                 context.action = intent_data['actions'][actions]
#         elif choice == 'action':
#             context.action = intent_data['action']
#         elif choice == 'sources':
#             context.subject = context.text.replace('найди', '').replace(context.source, '')
#             if context.source:
#                 context.action = intent_data['sources'][context.source]
#             else:
#                 inquire_subject('find')
#
#
def reply_by_intent():
    if context.intent and 'replies' in CONFIG['intents'][context.intent].keys():
        return random.choice(CONFIG['intents'][context.intent]['replies'])


# def turn_on():
#     """ проверяем, есть ли радио или музыка в контексте"""
#     for sound in CONFIG['intents']['music']['requests']:
#         if sound in context.subject:
#             """ если есть, находим action """
#             for action in CONFIG['intents']['music']['requests']:
#                 """ если action есть, включаем плеер"""
#                 if context.subject in CONFIG['intents']['music']['actions']:
#                     aimp(CONFIG['intents']['music']['actions'][context.subject])
#                     return
#                 else:
#                     # если такого радио или музыки нет
#                     # assistant.speak(context.target + ' ' + random.choice(CONFIG['intents']['music']['not_exists']))
#                     return
#             break
#         else:
#             please_specify('что включить:', 'target')
#             break
#
#


def please_specify(where, what):
    if what == 'target':
        assistant.speak('уточни, ' + where)
    if what == 'source':
        print('где именно?')
    # assistant.speak(random.choice(CONFIG['intents']['music']['spec']))
    pass


# def find_source_action():
#     levenshtein = 80
#     source_now = reply = action = None
#     sources = CONFIG['intents']['find_out']['sources'].keys()
#     if context.text.startswith(CONFIG['intents']['find_out']['requests']):
#         for source, source_data in sources.items():
#             levenshtein_distance = process.extractOne(context.text, source_data['requests'])
#             if levenshtein_distance[1] >= levenshtein:
#                 levenshtein = levenshtein_distance[1]
#                 source_now = source
#
#         if source_now:
#             source = sources[source_now]
#             if 'replies' in source.keys():
#                 reply = random.choice(source['replies'])
#             if 'action' in source.keys():
#                 action = source['action']
#             return reply, action
#     else:
#         return None, None
#
#
def has_latent(phrase):
    latent_where = words_in_phrase(CONFIG['intents']['find_out_where']['requests'], phrase)
    latent_wiki = words_in_phrase(CONFIG['intents']['find_out_wiki']['requests'], phrase)
    if latent_where:
        print('latent where')
        context.subject = context.text.partition(latent_where)[2]
        context.intent = 'find_out_where'
        context.action = 'yandex_maps'
        return True
    elif latent_wiki:
        print('latent wiki')
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

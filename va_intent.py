from va_assistant import assistant, context
import random
from fuzzywuzzy import process
from va_config import CONFIG


def inquire_subject(intent):
    assistant.speak(random.choice(CONFIG['intents'][intent]['spec']))


def subject_not_exist(subject):
    assistant.speak(' '.join([subject, random.choice(CONFIG['intents']['turn_on']['not_exists'])]))


def get_action_by_imperative():
    """ известные конфигу имеративы ? """
    if context.imperative in CONFIG['intents']['find']['requests']:
        print('ищем с помощью инструмента')
        # значит намерение искать с помощью поискового инструмента
        if not context.source:
            context.source = 'в яндексе'
        context.subject = context.text.replace(context.source, '')
        if not context.subject:
            inquire_subject('find')
            return True
        context.action = CONFIG['intents']['find']['sources'][context.source]
        return True

    if context.imperative in CONFIG['intents']['turn_on']['requests']:
        print('включаем музыку')
        context.action = 'turn_on'
        if not context.subject:
            inquire_subject('turn_on')
            return True
        else:
            if context.subject not in CONFIG['intents']['turn_on']['sources'].keys():
                subject_not_exist(context.subject)
                context.action = None
                return True
            else:
                context.subject = CONFIG['intents']['turn_on']['sources'][context.subject]
                return True

    else:
        for intent, intent_data in CONFIG['intents'].items():
            if context.imperative in intent_data['requests']:
                print('imperative in intents:', context.imperative)
                for choice in intent_data.keys():
                    if choice == 'replies':
                        context.reply = random.choice(intent_data['replies'])
                    elif choice == 'actions':
                        for word in tuple(intent_data['actions']):
                            if word in context.text:
                                context.action = intent_data['actions'][word]
                    elif choice == 'action':
                        context.action = intent_data['action']

                return True
    return False


def action_by_intent(levenshtein=90):
    phrase = context.text
    intent_now = ''
    for intent, intent_data in CONFIG['intents'].items():
        levenshtein_distance = process.extractOne(phrase, intent_data['requests'])
        if levenshtein_distance[1] > levenshtein:
            levenshtein = levenshtein_distance[1]  # оценка совпадения
            intent_now = intent
            intent_words = levenshtein_distance[0].strip()  # само совпадение
            print(intent_words, levenshtein, '%')

    if intent_now:
        print(intent_now)
        context.text = phrase.replace(intent_words, '')
        intent = CONFIG['intents'][intent_now]
        for choice in intent.keys():
            if choice == 'actions':
                for actions in intent['actions'].keys():
                    context.action = intent['actions'][actions]
            elif choice == 'action':
                context.action = intent['action']
            elif choice == 'sources':
                context.subject = context.text.replace('найди', '').replace(context.source, '')
                if not context.source:
                    inquire_subject('find')
                    return True
                context.action = intent['sources'][context.source]

        if 'replies' in intent.keys():
            context.reply = random.choice(intent['replies'])
        return True
    return False  # если интент не найден


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


def get_intent_action(imperative):
    """Получение интента (intents) из текста (сравнение с перечнем интентов в CONFIG)"""
    if imperative:
        intent, action, response = action_by_intent(70)

        if intent:
            return action, response
        else:
            assistant.fail()
            return '', ''


def please_specify(where, what):
    if what == 'target':
        assistant.speak('уточни, ' + where)
    if what == 'source':
        print('где именно?')
    # assistant.speak(random.choice(CONFIG['intents']['music']['spec']))
    pass


def find_source_action():
    levenshtein = 80
    source_now = reply = action = None
    sources = CONFIG['intents']['find_out']['sources'].keys()
    if context.text.startswith(CONFIG['intents']['find_out']['requests']):
        for source, source_data in sources.items():
            levenshtein_distance = process.extractOne(context.text, source_data['requests'])
            if levenshtein_distance[1] >= levenshtein:
                levenshtein = levenshtein_distance[1]
                source_now = source

        if source_now:
            source = sources[source_now]
            if 'replies' in source.keys():
                reply = random.choice(source['replies'])
            if 'action' in source.keys():
                action = source['action']
            return reply, action
    else:
        return None, None


def has_latent():
    phrase = context.phrase
    latent_where = words_in_phrase(CONFIG['intents']['find_out_where']['requests'], phrase)
    latent_wiki = words_in_phrase(CONFIG['intents']['find_out_wiki']['requests'], phrase)
    if latent_where:
        print('latent where')
        context.subject = context.text.partition(latent_where)[2]
        context.reply = random.choice(CONFIG['intents']['find_out_where']['replies'])
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


def intent_in_phrase():
    return False

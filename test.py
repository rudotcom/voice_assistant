from va_assistant import CONFIG, context
import random
import pymorphy2


""" если имератив контекста "искать, поискать", то берем where, а остальное без изменения
    если другой императив, полный морфологический расклад
    """

phrases = [
    'что такое глубокое обучение',
    'ну ладно скажи ксюше в москве завтра какая погода если что ',
    'найди генератор в маркете',
    'включи музыку 2020 like fm',
    'включи пожалуйста если можно радио chill никите',
    'скажи какая послезавтра погода?',
    'какая температура в москве?',
    'поищи в гугле выставка в москве',
    'скажи дяде как тебя зовут',
    'как тебя зовут',
    'сколько тебе лет',
    'где находится тепловозная 31',
    'включи',
    'радио чилаут',
    'открой',
    'телеграм',
    'поищи в ютубе как пить водку',
]

for phrase in phrases:
    context.context_by_phrase(phrase)

    print('_________________\n', phrase)
    print('imperative:', context.imperative)
    print('tool:', context.tool)
    print('target:', context.target)
    print('adverb:', context.adverb)
    print('addressee:', context.addressee)
    # print('text:', context.text)

from va_misc import normal_phrase
import random

phrase = 'найди генератор в маркете'
phrase = 'включи музыку 2020 like fm Завтра'
phrase = 'включи радио chill Дяде'
phrase = 'ну ладно скажи ксюше в москве завтра какая температура то если что '

LISTEN = ['слушай', 'слушай сюда', '', '', 'послушай', 'тебе говорю', '']
dic = normal_phrase(phrase)
phrase = ' '.join([dic['address'], random.choice(LISTEN), dic['imperative'], dic['target'], dic['location'], dic['adverb']])
print(phrase)


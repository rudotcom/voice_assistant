"""
Различные вспомогательные функции
"""
import os
import requests
import pymorphy2
import time
import threading

from fuzzywuzzy import process
from number_parser import parse_number
from va_assistant import assistant
from va_config import CONFIG

morph = pymorphy2.MorphAnalyzer()


def timedelta_to_dhms(duration):
    # преобразование в дни, часы, минуты и секунды
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds


def request_yandex_fast(request):
    response = requests.request('post', 'https://yandex.ru/search/?text=' + request)
    html = response.text
    html = html.partition('<div class="fact-answer')[2]
    html = html.partition('>')[2]
    html = html.partition('</div>')[0]
    html = html.replace('<b>', '')
    html = html.replace('</b>', '')
    return html


def integer_from_phrase(phrase):
    for word in phrase.split():
        if 'NUMB' in morph.parse(word)[0].tag:
            return int(word)
        if 'NUMR' in morph.parse(word)[0].tag:
            number = parse_number(word, language='ru')
            return int(number)
    return ''


class TimerThread(threading.Thread):
    def __init__(self, minutes, reminder=''):
        threading.Thread.__init__(self)
        self.daemon = True
        self.minutes = minutes
        self.reminder = reminder

    def run(self):
        seconds = self.minutes * 60
        time.sleep(seconds)
        assistant.play_wav('slow-spring-board-longer-tail-571')

        # Показываем текст напоминания
        if self.reminder:
            self.reminder = 'Ты просил напомнить, ' + self.reminder
        else:
            self.reminder = str(self.minutes) + ' минута прошло. Ты просил напомнить'
        # надо ли усыплять помощника, чтобы не слушал свое напоминание, или он уже спит?
        was_alert = assistant.is_alert()
        assistant.sleep()
        assistant.say(self.reminder)
        if was_alert:
            assistant.alert()


def initial_form(word):
    return morph.parse(word)[0][2]


def cls():
    print('\n' * 2)
    # os.system('cls' if os.name == 'nt' else 'clear')


def is_color_in_text(text):
    """ Найти во фразе слово, обозначающее цвет и вернуть его hex """
    levenshtein = []
    for c in text.split(' '):
        levi = process.extractOne(c, CONFIG['colors'].keys())
        if levi[1] > 70:
            levenshtein.append(levi)

    if len(levenshtein):
        color = max(levenshtein, key=lambda x: x[1])[0]
        assistant.say(color + '.')
        return CONFIG['colors'][color]
    else:
        return '516766'  # default "dark gray" color

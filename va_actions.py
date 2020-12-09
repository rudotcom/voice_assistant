"""
Здесь инициируются все действия, распознанные по интентам, императиам и т.п.
Действия, которые способен выполнять помощник:
- только сказать что прописано в интенте
- получить инфу из функции или от assistant и произнести полученный текст
    ctime, age, repeat, repeat_after_me, usd, btc, my_mood, mood_up, mood_down, die, weather, app_close, whois,
    wikipedia, translate, anecdote, quotation
- открыть определенную страницу браузера с запросом
    youtube, browse google, yandex, maps
- Запустить (остановить) процесс Windows
    turn_on, application, app_close
- сделать request в web
    telegram_bot, email
- повесить hook на телеграм, чтобы получать ответы
Для каждого действия необходим ограниченный набор параметров (source, target...)
Если действие назначено интентом, но параметров не хватает, необхоимо запросить отдельно
"""
import subprocess as sp
from va_assistant import assistant, context, new_context
from va_config import CONFIG
import psutil
import random
from datetime import datetime
import webbrowser  # работа с использованием браузера по умолчанию
import requests

from va_misc import num_unit, timedelta_to_dhms, request_yandex_fast, TimerThread, integer_from_phrase
import wikipediaapi  # поиск определений в Wikipedia
from translate import Translator

from va_sand_box import context_landscape
from va_weather import open_weather
from pycbrf.toolbox import ExchangeRates


class Action:
    """ Экземпляр action ассоциируется с интентом из контекста
    экземпляры класса получают параметры от функций определения интента и из контекста """

    def __init__(self, context_now):
        self.intent = assistant.intent
        self.subject = context_now.subject
        self.target = context_now.target
        self.text = context_now.text
        self.location = context_now.location
        if self.intent:
            self.name = self._get_action()
        else:
            return
        print(context_landscape())
        print('action:', self.name)
        if not self._missing_parameters():
            self.make_action()

    def _get_action(self):
        if 'action' in CONFIG['intents'][self.intent].keys():
            return CONFIG['intents'][self.intent]['action']

    def _missing_parameters(self):
        intent_param = CONFIG['intents'][self.intent]
        """ если параметра target нет, но в конфиге есть запрос параметра, запросить """
        if not self.target and 'target_missing' in intent_param:
            assistant.speak(random.choice(intent_param['target_missing']))
            return True
        elif not self.subject and 'subject_missing' in intent_param:
            assistant.speak(random.choice(intent_param['subject_missing']))
            return True
        elif 'not_exists' in intent_param and self.subject not in intent_param['subject'].keys():
            assistant.speak(random.choice((intent_param['not_exists'])))
            return True
        elif not self.text and 'text_missing' in intent_param:
            assistant.speak(random.choice(intent_param['text_missing']))
            return True
        elif not self.location and 'location_missing' in intent_param:
            assistant.speak(random.choice(intent_param['location_missing']))
            return True

    def say(self):
        """ произнести фразу ассоциированную с данным интентом """
        if 'replies' in CONFIG['intents'][self.intent].keys():
            assistant.speak(random.choice(CONFIG['intents'][self.intent]['replies']))

    def make_action(self):
        """ вызов функций, выполняющих действие """
        self.say()
        if self.name:
            print('action:', self.name)
            a = eval(self.name)
            assistant.alert()
            a()


""" Функции, выполняемые помощником """


def ctime():
    # сказать текущее время
    now = datetime.now()
    if now.hour < 3:
        day_part = 'ночи'
    elif now.hour < 12:
        day_part = 'утра'
    elif now.hour < 16:
        day_part = 'дня'
    else:
        day_part = 'вечера'
    hours = now.hour % 12

    assistant.speak("Сейчас {} {} {}".format(num_unit(hours, 'час'), num_unit(now.minute, 'минута'), day_part))


def timer():
    t = TimerThread(integer_from_phrase(context.text))
    t.start()


def age():
    td = datetime.now() - assistant.birthday
    days, hours, minutes, seconds = timedelta_to_dhms(td)
    my_age = 'мне {} {} {}'.format(num_unit(days, 'день'), num_unit(hours, 'час'), num_unit(minutes, 'минута'))
    assistant.speak(my_age)


def stop():
    assistant.sleep()


def name():
    assistant.speak(assistant.name)


def repeat():
    # повторить последний ответ
    if context.subject == 'slow':
        assistant.setup_voice(rate=80)
        assistant.speak(assistant.last_speech.replace(' ', ' , '))
        assistant.setup_voice()
    else:
        assistant.speak(assistant.last_speech)


def repeat_after_me():
    # повторить что только что сказал
    assistant.speak(new_context.phrase)


def usd():
    # курс доллара
    rates = ExchangeRates()
    rate = round(rates['USD'].rate, 2)
    cbrf = random.choice(['курс доллара ЦБ РФ {} {} за доллар', 'доллар сегодня {} {}'])
    rate_verbal = cbrf.format(num_unit(int(rate), 'рубль'),
                              num_unit(int(rate % 1 * 100), 'копейка'))
    assistant.speak(rate_verbal)


def btc():
    response = requests.get('https://api.blockchain.com/v3/exchange/tickers/BTC-USD')
    if response.status_code == 200:
        assistant.speak('1 биткоин ' + str(num_unit(int(response.json()['last_trade_price']), 'доллар')))


def mood_up():
    if assistant.mood < 2:
        assistant.mood += 1
    assistant.setup_voice()


def mood_down():
    assistant.mood = -1
    assistant.setup_voice(rate=90)


def my_mood():
    phrases = CONFIG['mood'][assistant.mood]
    assistant.speak(random.choice(phrases))


def die():
    exit()


def weather():
    weather_data = open_weather()
    assistant.speak(weather_data)


def find():
    url = CONFIG['intents']['find']['targets'][context.target]
    url += context.subject
    webbrowser.get().open(url)


def turn_on():
    print(context.subject)
    sp.Popen([r"C:\Program Files (x86)\AIMP\AIMP.exe", context.subject])


def app_open():
    path = CONFIG['intents']['app_open']['subject'][context.subject]
    try:
        print('applic:', path)
        sp.Popen(path)
    except FileNotFoundError:
        assistant.speak('Мне не удалось найти файл программы')
    except PermissionError:
        assistant.speak('Мне отказано в доступе к файлу программы')


def app_close():
    if context.subject in CONFIG['intents']['app_close']['targets'].keys():
        proc = CONFIG['intents']['app_close']['targets'][context.subject]
        print('app_close', proc)
        for process in (process for process in psutil.process_iter() if process.name() == proc):
            process.kill()


def whois():
    answer = request_yandex_fast(context.subject)
    print(answer)
    assistant.speak(answer)


def wikipedia():
    if not context.subject:
        return False

    def remove_nested_parens(input_str):
        """Returns a copy of 'input_str' with any parenthesized text removed. Nested parentheses are handled."""
        result = ''
        paren_level = 0
        for ch in input_str:
            if ch == '(':
                paren_level += 1
            elif (ch == ')') and paren_level:
                paren_level -= 1
            elif not paren_level:
                result += ch
        return result

    remove_nested_parens('example_(extra(qualifier)_text)_test(more_parens).ext')

    def clear_wiki(text):
        text = remove_nested_parens(text)
        for x in CONFIG['umlaut']:
            text = text.replace(x, CONFIG['umlaut'][x])
        return text

    wiki = wikipediaapi.Wikipedia(assistant.speech_language)
    wiki_page = wiki.page(context.subject)
    if wiki_page.exists():
        webbrowser.get().open(wiki_page.fullurl)
        wiki = clear_wiki(wiki_page.summary)
        assistant.speak('.'.join(wiki.split('.')[:2]))
        # TODO: исправить. Почему не работает яндекс факт?
    # else:
    #     assistant.speak(request_yandex_fast(context_now.subject))


def translate():
    translator = Translator(from_lang="ru", to_lang="en")
    target = context.subject.replace('по-английски', '')
    translation = translator.translate(target)
    assistant.speak(target)
    assistant.speak("по-английски")
    assistant.setup_voice("en")
    assistant.speak(translation)
    assistant.setup_voice("ru")


def cite():
    quotation(context.location)


def anecdote():
    import json
    url = 'http://rzhunemogu.ru/RandJSON.aspx?CType=1'
    response = requests.get(url)
    if response.status_code == 200:
        anecdote = response.content.decode('cp1251').replace('{"content":"', '')
        assistant.speak(anecdote)


def quotation(word=''):
    import pymysql
    connection = pymysql.connect('localhost', 'dude', 'StqMwx4DRdKrc6WWGcw2w8nZh', 'assistant')
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `quoteText`, `quoteAuthor` FROM `citation` WHERE `quoteText` LIKE '%{}%' " \
                  "ORDER BY timeCited ASC LIMIT 1".format(word)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                sql = "UPDATE `citation` SET `timeCited`=NOW() WHERE id={}".format((result[0]))
                cursor.execute(sql)
                connection.commit()
                if result[2]:
                    spoke = random.choice(['говорил', 'так говорил', 'как говорил когда-то', ''])
                else:
                    spoke = ''
                assistant.speak('{}... ({} {})'.format(result[1], spoke, result[2]))
    finally:
        connection.close()

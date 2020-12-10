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
    turn_on, app_open, app_close
TODO:
    - сделать request в web
        telegram_bot, email
    - повесить hook на телеграм, чтобы получать ответы
"""
import subprocess as sp
from va_config import CONFIG
import psutil
import random
from datetime import datetime
import webbrowser  # работа с использованием браузера по умолчанию
import requests

from va_assistant import assistant, context, new_context
from va_misc import num_unit, timedelta_to_dhms, request_yandex_fast, TimerThread, integer_from_phrase, initial_form, \
    weekday_rus
import wikipediaapi  # поиск определений в Wikipedia
from translate import Translator

from va_weather import open_weather
from pycbrf.toolbox import ExchangeRates


"""
Для каждого действия необходим ограниченный набор параметров (subject, target...)
Эти параметры получаются из словаря config по одноименному ключу из context
"""


def context_intent():
    if assistant.intent:
        config = CONFIG['intents'][assistant.intent]
        if 'subject' in config.keys():
            if context.subject in config['subject'].keys():
                context.subject_value = config['subject'][context.subject]
                context.text = context.text.replace(context.subject, '').strip()
        if 'targets' in config.keys():
            if context.target in config['targets'].keys():
                context.target_value = config['targets'][context.target]


class Action:
    """ Экземпляр action ассоциируется с интентом из контекста
    экземпляры класса получают параметры от функций определения интента и из контекста
        Если действие назначено интентом, но параметров не хватает, необхоимо запросить отдельно
     """

    def __init__(self):
        if assistant.intent:
            config = CONFIG['intents'][assistant.intent]
            self.name = self._get_action(config)
            context_intent()
            if not self._parameter_missing(config):
                self.make_action()
        else:
            return

    @staticmethod
    def _get_action(config):
        if 'action' in config.keys():
            return config['action']

    @staticmethod
    def _parameter_missing(config):
        if not context.subject and 'subject_missing' in config:
            assistant.speak(random.choice(config['subject_missing']))
            return True
        elif 'not_exists' in config and context.subject_value not in list(config['subject'].values()):
            assistant.speak(random.choice((config['not_exists'])))
            return True
        if not context.target and 'target_missing' in config:
            assistant.speak(random.choice(config['target_missing']))
            return True
        if not context.location and 'location_missing' in config:
            assistant.speak(random.choice(config['location_missing']))
            return True
        if not context.text and 'text_missing' in config:
            assistant.speak(random.choice(config['text_missing']))
            return True

    @staticmethod
    def say():
        """ произнести фразу ассоциированную с данным интентом """
        intent = CONFIG['intents'][assistant.intent]
        if 'replies' in intent.keys():
            assistant.speak(random.choice(intent['replies']))

    def make_action(self):
        """ вызов функций, выполняющих действие """
        print(context_landscape())
        self.say()
        if self.name:
            print('action start:', self.name)
            function = eval(self.name)
            assistant.alert()
            function()


action = Action()


def context_landscape():
    """ Для отладки """
    intent = assistant.intent
    landscape = 'imperative:\t{c.imperative}\n' \
                'target:\t\t{c.target}\n' \
                'subject:\t{c.subject}\n' \
                'location:\t{c.location}\n' \
                'adverb:\t\t{c.adverb}\n' \
                'addressee:\t{c.addressee}\n' \
                'text:\t\t{c.text}\n' \
                'assistant.intent:\t{intent}'.format(c=context, intent=intent)
    return landscape


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


def weekday():
    now = datetime.now()
    weekday = weekday_rus(now.weekday())
    assistant.speak('сегодня ' + weekday)


def age():
    td = datetime.now() - assistant.birthday
    days, hours, minutes, seconds = timedelta_to_dhms(td)
    my_age = 'мне {} {} {}'.format(num_unit(days, 'день'), num_unit(hours, 'час'), num_unit(minutes, 'минута'))
    assistant.speak(my_age)


def forget():
    context = None


def stop():
    assistant.sleep()


def name():
    assistant.speak('меня зовут ' + assistant.name)


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
    for req in CONFIG['intents']['repeat_after_me']['requests']:
        if req in context.text:
            context.text = context.text.replace(req, '').strip()
    assistant.speak(context.text)


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
    weather_data = open_weather(context.location, context.adverb)
    assistant.speak(weather_data)


def find():
    url = context.target_value
    url += context.text
    webbrowser.get().open(url)


def turn_on():
    sp.Popen([r"C:\Program Files (x86)\AIMP\AIMP.exe", context.subject_value])


def app_open():
    try:
        print('applic:', context.subject_value)
        sp.Popen(context.subject_value)
    except FileNotFoundError:
        assistant.speak('Мне не удалось найти файл программы')
    except PermissionError:
        assistant.speak('Мне отказано в доступе к файлу программы')


def app_close():
    proc = context.subject_value
    print('app_close', proc)
    for process in (process for process in psutil.process_iter() if process.name() == proc):
        process.kill()


def whois():
    answer = request_yandex_fast(context.subject_value)
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
    #     assistant.speak(request_yandex_fast(context.subject_value))


def translate():
    translator = Translator(from_lang="ru", to_lang="en")
    target = context.subject.replace('по-английски', '')
    translation = translator.translate(target)
    assistant.speak(target)
    assistant.speak("по-английски")
    assistant.setup_voice("en")
    assistant.speak(translation)
    assistant.setup_voice("ru")


def think():
    quotation(initial_form(context.location))


def anecdote():
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

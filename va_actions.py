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
"""
from subprocess import Popen
from va_config import CONFIG
import psutil
import random
from datetime import datetime
import webbrowser  # работа с использованием браузера по умолчанию
import requests
import pymysql
import wikipediaapi  # поиск определений в Wikipedia
from translate import Translator
from pycbrf.toolbox import ExchangeRates
from pymorphy2 import MorphAnalyzer

from va_assistant import assistant, context, old_context
from va_misc import timedelta_to_dhms, request_yandex_fast, TimerThread, integer_from_phrase, initial_form
from va_weather import open_weather


class Action:
    """ Экземпляр action ассоциируется с интентом из контекста
    экземпляры класса получают параметры от функций определения интента и из контекста
     """

    def __init__(self):
        self.name = None
        if context.intent:
            config = CONFIG['intents'][context.intent]
            if 'action' in config.keys():
                self.name = config['action']
            if not self._parameter_missing(config):
                self.make_action()
        else:
            assistant.fail()

    @staticmethod
    def _parameter_missing(config):
        if not context.get_subject_value() or not context.get_target_value():
            return True
        print('missing? csv', context.subject_value)

        if not context.location and 'location_missing' in config:
            assistant.say(random.choice(config['location_missing']))
            return True
        if not context.text and 'text_missing' in config:
            assistant.say(random.choice(config['text_missing']))
            return True

    @staticmethod
    def reply_by_config():
        """ произнести фразу ассоциированную с данным интентом """
        intent = CONFIG['intents'][context.intent]
        if 'replies' in intent.keys():
            assistant.say(random.choice(intent['replies']))

    def make_action(self):
        """ вызов функций, выполняющих действие """
        print('cntx changed:', context != old_context)
        if context != old_context:
            self.reply_by_config()
            if self.name:
                # print('function:', self.name)
                function = eval(self.name)
                assistant.alert()
                function()
        else:
            assistant.fail()


action = Action()


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

    # assistant.say("Сейчас {} {} {}".format(num_unit(hours, 'час'), num_unit(now.minute, 'минута'), day_part))
    assistant.say("Сейчас {} час {} минута {}".format(hours, now.minute, day_part))


def timer():
    # TODO: - Таймер - напоминание через ... минут + текст напоминания
    minutes = integer_from_phrase(context.text)
    print('min:', minutes)
    if type(minutes) == int:
        t = TimerThread(minutes)
        t.start()
        context.intent = None
    else:
        # TODO: почему спрашивает сколько?
        assistant.say('сколько минут?')
        return


def weekday():
    wd = datetime.now().weekday()
    dtn = datetime.now().timetuple()
    assistant.say('сегодня ' + CONFIG['weekday'][wd] + ' ' + str(dtn[2]) + 'ое ' + CONFIG['month'][dtn[1]])


def days_until():
    today = datetime.today()  # текущая дата
    print(f"{today:%j}")  # номер дня в году с 1


def age():
    td = datetime.now() - assistant.birthday
    days, hours, minutes, seconds = timedelta_to_dhms(td)
    # my_age = 'мне {} {} {}'.format(num_unit(days, 'день'), num_unit(hours, 'час'), num_unit(minutes, 'минута'))
    my_age = 'мне {} день {} час {} минута'.format(days, hours, minutes)
    assistant.say(my_age)


def forget():
    assistant.play_wav('decay-475')
    context.intent = None


def stop():
    assistant.play_wav('decay-475')
    assistant.sleep()


def name():
    assistant.say('меня зовут ' + assistant.name)


def repeat():
    # повторить последний ответ
    if context.subject == 'slow':
        assistant.say(assistant.last_speech.replace(' ', ' , '), rate=80)
    else:
        assistant.say(assistant.last_speech)


def repeat_after_me():
    # повторить что только что сказал
    for req in CONFIG['intents']['repeat_after_me']['requests']:
        if req in context.text:
            context.text = context.text.replace(req, '').strip()
    assistant.say(context.text)


def usd():
    assistant.play_wav('wind-up-3-536')
    # курс доллара
    rates = ExchangeRates()
    rate = round(rates['USD'].rate, 2)
    cbrf = random.choice(['курс доллара ЦБ РФ {} рубль {} копейка за доллар', 'доллар сегодня {} рубль {} копейка'])
    rate_verbal = cbrf.format(int(rate), int(rate % 1 * 100))
    assistant.say('💵 ' + rate_verbal)


def btc():
    assistant.play_wav('wind-up-3-536')
    response = requests.get('https://api.blockchain.com/v3/exchange/tickers/BTC-USD')
    if response.status_code == 200:
        assistant.say('Один биткоин {} доллар 💵'.format(int(response.json()['last_trade_price'])))


def praise():
    if assistant.mood < 2:
        assistant.mood += 1
    phrase = random.choice(CONFIG['intents']['praise']['status'])
    assistant.say(phrase)


def abuse():
    assistant.play_wav('rising-to-the-surface-333')
    assistant.mood = -1
    phrase = random.choice(CONFIG['intents']['abuse']['status'])
    assistant.say('💘 ' + phrase)


def my_mood():
    phrase = random.choice(CONFIG['intents']['mood']['status'][assistant.mood])
    assistant.say(phrase)


def redneck():
    assistant.play_wav('decay-475')
    assistant.redneck = True


def casual():
    assistant.play_wav('slow-spring-board-longer-tail-571')
    assistant.redneck = False


def die():
    assistant.play_wav('vuvuzela-power-down-126')
    exit()


def days_ahead(word, morph=MorphAnalyzer()):
    if word:
        word = morph.parse(word.split()[-1])[0][2]  # начальная форма слова
        if word == 'выходной':
            word = CONFIG['weekday'][5]

        if word in CONFIG['nearest_day']:
            return CONFIG['nearest_day'].index(word)
        elif word in CONFIG['weekday']:
            weekday_today = datetime.now().weekday()
            weekday_then = CONFIG['weekday'].index(word)
            return (8 + weekday_then - weekday_today) % 7


def weather():
    weather_data = open_weather(context.location, days_ahead(context.adverb))
    if weather_data:
        assistant.say('🌤 ' + weather_data)


def find():
    assistant.play_wav('solemn-522')
    url = context.target_value
    url += context.subject
    webbrowser.get().open(url)


def turn_on():
    Popen([r"C:\Program Files (x86)\AIMP\AIMP.exe", context.subject_value])


def app_open():
    try:
        print('applic:', context.subject_value)
        Popen(context.subject_value)
    except FileNotFoundError:
        assistant.say('Мне не удалось найти файл программы')
    except PermissionError:
        assistant.say('Мне отказано в доступе к файлу программы')


def app_close():
    proc = context.subject_value
    print('app_close', proc)
    for process in (process for process in psutil.process_iter() if process.name() == proc):
        process.kill()


def whois():
    answer = request_yandex_fast(context.subject_value)
    print(answer)
    assistant.say(answer)


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
        assistant.say('.'.join(wiki.split('.')[:2]))
        # TODO: исправить. Почему не работает яндекс факт?
    # else:
    #     assistant.speak(request_yandex_fast(context.subject_value))


def translate():
    translator = Translator(from_lang="ru", to_lang="en")
    target = context.text.replace('по-английски', '')
    translation = translator.translate(target)
    assistant.say(target)
    assistant.say("по-английски")
    assistant.say(translation, lang='en')


def think():
    assistant.play_wav('434476__dersuperanton__page-turn-over-flip')
    quotation(initial_form(context.location))


def anecdote():
    assistant.play_wav('136778__davidbain__page-turn')
    url = 'http://rzhunemogu.ru/RandJSON.aspx?CType=1'
    response = requests.get(url)
    if response.status_code == 200:
        anecdote = response.content.decode('cp1251').replace('{"content":"', '')
        assistant.say(anecdote)


def quotation(word=''):
    connection = pymysql.connect('localhost', 'assistant', 'StqMwx4DRdKrc6WWGcw2w8nZh', 'assistant')
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
                assistant.say('{}... ({} {})'.format(result[1], spoke, result[2]))
    finally:
        connection.close()

# TODO:
#     - добавить список дел, задач (бд) dateparse
#     - "Что ты думаешь про...", "Что ты знаешь о" = Поиск по словам в бд
#     - добавь в список покупок (в бд), чтобы когда я спрошу "что купить" она напоминала
#          - напомни купить...
#     - Громче - Тише
#     - Закрывать открытые вкладки Ctrl + F4
#     - Сохранять беседу в БД. Запросы, ответы, м.б. контекст?
#     - Сколько времени сохранять контекст в памяти?
#     - расширение конфига в отдельных словарях
#     - Поиск подпапок по имени (возможно со словарем) для музыки
#     - Отправлять сообщения в вотсап веб, читать новые?
#     - сделать request в web
#         telegram_bot, email
#     - повесить hook на телеграм, чтобы получать ответы

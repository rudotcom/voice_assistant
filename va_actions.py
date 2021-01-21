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
import os
import time
from subprocess import Popen

import pytils
from fpdf import FPDF
from fuzzywuzzy import fuzz, process
import keyboard

import APIKeysLocal  # локально хранятся ключи и пароли
from reminders import db_get_reminder
from va_config import CONFIG
import psutil
import random
from datetime import datetime, timedelta
import webbrowser  # работа с использованием браузера по умолчанию
import requests
import pymysql
import wikipediaapi  # поиск определений в Wikipedia
from translate import Translator
from pycbrf.toolbox import ExchangeRates
from pymorphy2 import MorphAnalyzer

from va_assistant import assistant, context, old_context
from va_gui import girl
from va_misc import is_color_in_text, timedelta_to_dhms, request_yandex_fast, TimerThread, integer_from_phrase, \
    initial_form
from va_weather import open_weather
from va_keyboard import volume_up, volume_down, track_next, track_prev, play_pause


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
        elif context.phrase:
            assistant.fail(context.phrase)

    @staticmethod
    def _parameter_missing(config):
        if not context.get_subject_value() or not context.get_target_value():
            return True
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
        context.persist = False
        """ вызов функций, выполняющих действие """
        # print('cntx changed:', context != old_context)
        self.reply_by_config()
        # print('action:', self.name)
        if self.name:
            function = eval(self.name)
            assistant.alert()
            function()
            self.check_reminders()

    @staticmethod
    def check_reminders():
        reminders = db_get_reminder()
        if reminders:
            r = 'Разреши напомнить. ' + '.\n Разреши также напомнить. '.join(reminders)
            assistant.say(r)


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
    if hours == 0:
        hours = 12

    # assistant.say("Сейчас {} {} {}".format(num_unit(hours, 'час'), num_unit(now.minute, 'минута'), day_part))
    assistant.say("Сейчас {} час {} минута {}".format(hours, now.minute, day_part))


def timer():
    # TODO: - Таймер - напоминание через ... минут + текст напоминания
    minutes = integer_from_phrase(context.text)
    # print('min:', minutes)
    if type(minutes) == int:
        assistant.say(f'{minutes} минута время пошло!')
        t = TimerThread(minutes)
        t.start()
    else:
        assistant.say('сколько минут?')
        context.persist = True


def weekday():
    day = pytils.dt.ru_strftime(u"сегодня - %A, %d %B", inflected=True, date=datetime.now())
    assistant.say(day, correct=True)


def days_until():
    # TODO: внедрить
    today = datetime.today()  # текущая дата
    print(f"{today:%j}")  # номер дня в году с 1


def age():
    td = datetime.now() - assistant.birthday
    days, hours, minutes, seconds = timedelta_to_dhms(td)
    # my_age = 'мне {} {} {}'.format(num_unit(days, 'день'), num_unit(hours, 'час'), num_unit(minutes, 'минута'))
    my_age = 'мне {} день {} час {} минута'.format(days, hours, minutes)
    assistant.say(my_age)
    assistant.play_wav('giggle' + str(int(random.randint(0, 6))))


def forget():
    assistant.play_wav('decay-475')
    context.persist = False


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
    cbrf = random_phrase('usd_today')
    rate_verbal = cbrf.format(int(rate), int(rate % 1 * 100))
    assistant.say(rate_verbal)
    assistant.play_wav('hm')


def btc():
    assistant.play_wav('phonekeys1')
    response = requests.get('https://api.blockchain.com/v3/exchange/tickers/BTC-USD')
    if response.status_code == 200:
        assistant.say('Один биткоин {} доллар'.format(int(response.json()['last_trade_price'])))


def praise():
    time.sleep(1)
    if assistant.mood < 2:
        assistant.mood += 1
    # phrase = random.choice(CONFIG['intents']['praise']['replies'])
    assistant.play_wav('moan' + str(int(random.randint(0, 8))))
    # assistant.say(phrase)


def abuse():
    assistant.play_wav('sob1')
    time.sleep(0.8)
    assistant.mood = -1
    phrase = random.choice(CONFIG['intents']['abuse']['replies'])
    assistant.say(phrase)


def my_mood():
    phrase = random.choice(CONFIG['intents']['mood']['status'][assistant.mood])
    assistant.say(phrase)


def redneck():
    assistant.play_wav('decay-475')
    assistant.redneck = True


def casual():
    assistant.play_wav('slow-spring-board-longer-tail-571')
    assistant.redneck = False
    assistant.play_wav('giggle' + str(int(random.randint(0, 6))))


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
        assistant.say(weather_data)
    context.persist = True


def find():
    assistant.play_wav('keyboard1')
    url = context.target_value
    url += context.subject
    webbrowser.get().open(url)
    context.persist = True


def turn_on():
    Popen([r"C:\Program Files (x86)\AIMP\AIMP.exe", context.subject_value])


def app_open():
    assistant.play_wav('keyboard1')
    try:
        print('applic:', context.subject_value)
        Popen(context.subject_value)
    except FileNotFoundError:
        assistant.say('Мне не удалось найти файл программы')
    except PermissionError:
        assistant.say('Мне отказано в доступе к файлу программы')
    context.persist = True


def app_close():
    proc = context.subject_value
    print('app_close', proc)
    for process in (process for process in psutil.process_iter() if process.name() == proc):
        process.kill()
    context.persist = True


def whois():
    answer = request_yandex_fast(context.subject_value)
    print(answer)
    assistant.say(answer)


def wikipedia():
    assistant.play_wav('inhale5')
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
        assistant.play_wav('giggle' + str(int(random.randint(0, 6))))


def quotation(word=''):
    connection = pymysql.connect('localhost', 'assistant', APIKeysLocal.mysql_pass, 'assistant')
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `quoteText`, `quoteAuthor` FROM `citation` WHERE `quoteText` LIKE '%{}%' " \
                  "ORDER BY timeCited, RAND() ASC LIMIT 1".format(word)
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


def unmute():
    assistant.active = True
    assistant.play_wav('giggle' + str(int(random.randint(0, 6))))


def whm_breathe():
    rounds = integer_from_phrase(context.text)
    # assistant.sleep()
    # assistant.active = False
    # context.subject_value = CONFIG['intents']['turn_on']['subject']['музыку дыхания']
    # turn_on()
    # Popen(r'python breathe.py {}'.format(rounds))
    assistant.dress_up_as('Person-Female-Light-icon')
    from breathe import workout
    workout.breathe(rounds)
    assistant.alert()


def whm_breath_stat():
    out_file = 'breath_log.pdf'
    sql = "SELECT `timeBreath`, `result` FROM `whm_breath` ORDER BY `timeBreath` DESC LIMIT 1000"

    pdf = FPDF()
    # Add a page
    pdf.add_page()
    pdf.add_font('Arial', '', r'c:\Windows\Fonts\arial.ttf', uni=True)
    pdf.set_font('Arial', '', 9)
    connection = pymysql.connect('localhost', 'assistant', APIKeysLocal.mysql_pass, 'assistant')
    try:
        with connection.cursor() as cursor:
            pdf.cell(w=190, h=7, txt="Тренировки до 4ч утра относятся к предыдущим суткам", ln=1, align='R')
            # Read a single record
            cursor.execute(sql)
            date = ''
            for result in cursor:
                if date != (result[0] - timedelta(hours=4)).strftime("%d.%m"):
                    date = (result[0] - timedelta(hours=4)).strftime("%d.%m")
                    pdf.cell(w=100, h=7, txt=date, ln=1, align='C')
                mins = result[1] // 60
                secs = result[1] % 60
                round = '[ {:0>2d}:{:0>2d} ] '.format(mins, secs)

                txt = result[0].strftime("%H:%M:   ") + round
                txt += '|' * int(result[1])
                pdf.cell(w=200, h=4, txt=txt, ln=1)
            # save the pdf with name .pdf
            pdf.output(out_file)
            os.startfile(out_file)
    finally:
        connection.close()


def random_phrase(param):
    return random.choice(CONFIG[param])


def diary():
    """ Запись текста в дневник. Запись построчно. Редактирование записанного текста перед отправкой в б.д.
     Если новая строка похожа на одну из записанных, эта записанная строка заменяется.
    """
    hex = is_color_in_text(context.text)

    def process_text(text, voice_text):
        """ сопоставляем уже написанный текст с новой строкой """
        for i in range(len(text)):
            # если новая строка заканчивается на эти слова - ее совпадение удалить
            if voice_text.split(' ')[-1] in ["удали", 'сотри']:
                if text[i] == ' '.join(voice_text.split(' ')[:-1]):
                    text.pop(i)
                    assistant.say('Удалила')
                    return text

            # если совпадение по Левенштейну - заменить строку на новую
            elif fuzz.WRatio(voice_text, text[i]) > 70:
                text[i] = voice_text
                assistant.say('окей,' + text[i])
                return text

        assistant.say(voice_text)
        # если замены не было, дописать
        text.append(voice_text)
        return text

    assistant.say(random_phrase('writing_to_diary'))
    text = []
    # Сохранение в бд при одном из этих слов
    while True:
        voice_text = assistant.recognize()
        if voice_text in CONFIG['diary_saver']:
            break
        elif voice_text in CONFIG['diary_canceler']:
            # прекращение функции при этих словах
            assistant.say(random_phrase("diary_cancel"))
            return
        elif voice_text in CONFIG['diary_repeater']:
            # Повторить, что записала, перед сохранением
            assistant.say('\n'.join(text))
            continue

        elif voice_text is not None:
            text = process_text(text, voice_text)
            if text and iter(text):
                print('\n', '=' * 30, '\n', '\n'.join(text), '\n', '=' * 30)
        assistant.alert()

    diary_text = '\n'.join(text)
    connection = pymysql.connect('localhost', 'assistant', APIKeysLocal.mysql_pass, 'assistant')
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = f"INSERT INTO `diary` (`text`, `color`) VALUES ('{diary_text.strip()}', UNHEX('{hex}'))"
            cursor.execute(sql)
            connection.commit()
            assistant.say('Записала!')
    finally:
        connection.close()


def diary_to_pdf():
    out_file = "diary.pdf"
    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()
    # Add a page
    pdf.add_page()
    pdf.add_font('Arial', '', r'c:\Windows\Fonts\arial.ttf', uni=True)
    pdf.set_font('Arial', '', 14)

    connection = pymysql.connect('localhost', 'assistant', APIKeysLocal.mysql_pass, 'assistant')
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `ts`, `text`, hex(`color`) FROM `diary` ORDER BY `ts` DESC"
            cursor.execute(sql)
            for result in cursor:
                hex = result[3] if result[3] else '3a3a3a'
                rgb = tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))

                day = pytils.dt.ru_strftime(u" %A, %d %B %Y", inflected=True, date=result[1])
                time = result[1].strftime("%H:%M")
                pdf.set_text_color(50, 80, 110)
                pdf.cell(200, 10, txt=f"[№ {str(result[0])}] {time} {day}", ln=1, align='L')
                pdf.set_text_color(rgb[0], rgb[1], rgb[2])
                pdf.set_draw_color(150, 130, 200)
                pdf.multi_cell(190, 6, txt=result[2], border=1)

            # save the pdf with name .pdf
            pdf.output(out_file)
            os.startfile(out_file)

    finally:
        connection.close()


# TODO:
#   - утром при получении голосового ввода напоминать о дыхании, гимнастике, задачах на день
#   - днем, если не было дыхательной практики, напомнить об этом
#     - добавить список дел, задач (бд) dateparse
#     - "Что ты думаешь про...", "Что ты знаешь о" = Поиск по словам в бд
#     - добавь в список покупок (в бд), чтобы когда я спрошу "что купить" она напоминала
#          - напомни купить...
#     - Закрывать открытые вкладки Ctrl + F4
#     - Сохранять беседу в БД. Запросы, ответы, м.б. контекст?
#     - Сколько времени сохранять контекст в памяти?
#     - расширение конфига в отдельных словарях
#     - Поиск подпапок по имени (возможно со словарем) для музыки
#   - сколько будет 5% от или 2 умножить на 2 или 2 в степени

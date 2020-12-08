"""
Здесь инициируются все действия, распознанные по интентам, императиам и т.п.
"""
import subprocess as sp
from main import assistant, context
from va_config import CONFIG
import psutil
import random
from datetime import datetime
import webbrowser  # работа с использованием браузера по умолчанию
import requests

from va_intent import reply_by_intent
from va_misc import num_unit, timedelta_to_dhms, request_yandex_fast, btc, TimerThread, integer_from_phrase
import wikipediaapi  # поиск определений в Wikipedia
from translate import Translator
from va_weather import open_weather
from pycbrf.toolbox import ExchangeRates


def act():
    action = context.action
    print('action <-', context.action)
    context.imperative = None
    assistant.speak(reply_by_intent())

    if action == 'ctime':
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

    elif action == 'timer':

        t = TimerThread(integer_from_phrase(context.text))
        t.start()

    elif action == 'age':
        td = datetime.now() - assistant.birthday
        days, hours, minutes, seconds = timedelta_to_dhms(td)
        my_age = 'мне {} {} {}'.format(num_unit(days, 'день'), num_unit(hours, 'час'), num_unit(minutes, 'минута'))
        assistant.speak(my_age)

    elif action == 'stop':
        assistant.speak(assistant.sleep())

    elif action == 'name':
        assistant.speak(assistant.name)

    elif action == 'repeat':
        # повторить последний ответ
        if context.subject == 'slow':
            assistant.setup_voice(rate=80)
            assistant.speak(assistant.last_speech.replace(' ', ' , '))
            assistant.setup_voice()
        else:
            assistant.speak(assistant.last_speech)

    elif action == 'repeat_after_me':
        # повторить что только что сказал
        assistant.speak(context.phrase)

    elif action == 'usd':
        # курс доллара
        rates = ExchangeRates()
        rate = round(rates['USD'].rate, 2)
        cbrf = random.choice(['курс доллара ЦБ РФ {} {} за доллар', 'доллар сегодня {} {}'])
        rate_verbal = cbrf.format(num_unit(int(rate), 'рубль'),
                                  num_unit(int(rate % 1 * 100), 'копейка'))
        assistant.speak(rate_verbal)

    elif action == 'btc':
        # курс биткоина
        assistant.speak(btc())

    elif action == 'mood_up':
        if assistant.mood < 2:
            assistant.mood += 1
        assistant.setup_voice()

    elif action == 'mood_down':
        assistant.mood = -1
        assistant.setup_voice(rate=90)

    elif action == 'my_mood':
        phrases = CONFIG['mood'][assistant.mood]
        assistant.speak(random.choice(phrases))

    elif action == 'die':
        exit()

    elif action == 'weather':
        weather = open_weather()
        assistant.speak(weather)

    elif action == 'youtube':
        url = "https://www.youtube.com/results?search_query=" + context.subject
        webbrowser.get().open(url)

    elif action == 'browse_google':
        assistant.last_action = action
        url = "https://www.google.ru/search?q=" + context.subject
        webbrowser.get().open(url)

    elif action == 'browse_yandex':
        url = "https://yandex.ru/search/?text=" + context.subject
        webbrowser.get().open(url)

    elif action == 'yandex_maps':
        url = "https://yandex.ru/maps/?text=" + context.subject
        webbrowser.get().open(url)

    elif action == 'turn_on':
        sp.Popen([r"C:\Program Files (x86)\AIMP\AIMP.exe", context.subject])

    elif action == 'application':
        path = CONFIG['intents']['app_open']['targets'][context.subject]
        try:
            print('applic:', path)
            sp.Popen(path)
        except FileNotFoundError:
            assistant.speak('Мне не удалось найти файл программы')
        except PermissionError:
            assistant.speak('Мне отказано в доступе к файлу программы')

    elif action == 'app_close':
        if context.subject in CONFIG['intents']['app_close']['targets'].keys():
            proc = CONFIG['intents']['app_close']['targets'][context.subject]
            print('app_close', proc)
            for process in (process for process in psutil.process_iter() if process.name() == proc):
                process.kill()

    elif action == 'whois':
        answer = request_yandex_fast(context.subject)
        print(answer)
        assistant.speak(answer)

    elif action == 'wikipedia':
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
        #     assistant.speak(request_yandex_fast(context.subject))

    elif action == 'translate':
        translator = Translator(from_lang="ru", to_lang="en")
        target = context.subject.replace('по-английски', '')
        translation = translator.translate(target)
        assistant.speak(target)
        assistant.speak("по-английски")
        assistant.setup_voice("en")
        assistant.speak(translation)
        assistant.setup_voice("ru")

    elif action == 'cite':
        assistant.speak('Я как раз обучаюсь думать, типа')

    elif action == 'anecdote':
        import json
        url = 'http://rzhunemogu.ru/RandJSON.aspx?CType=1'
        response = requests.get(url)
        if response.status_code == 200:
            anecdote = response.content.decode('cp1251').replace('{"content":"', '')
            assistant.speak(anecdote)

    elif action == 'quotation':
        word = context.subject
        import pymysql
        connection = pymysql.connect('localhost', 'dude', 'StqMwx4DRdKrc6WWGcw2w8nZh', 'assistant')
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `quoteText`, `quoteAuthor` FROM `citation` WHERE `quoteText` LIKE '%{}%' " \
                      "ORDER BY timeCited ASC LIMIT 1".format(word)
                cursor.execute(sql)
                result = cursor.fetchone()
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

    assistant.alert()
    return True

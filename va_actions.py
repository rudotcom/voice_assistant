import subprocess as sp
from va_assistant import assistant, context
from va_config import CONFIG
import psutil
import random
from datetime import datetime
import webbrowser  # работа с использованием браузера по умолчанию
from va_misc import num_unit, timedelta_to_dhms, request_yandex_fast, btc, TimerThread, integer_from_phrase
import wikipediaapi  # поиск определений в Wikipedia
from translate import Translator
from va_weather import open_weather
from pycbrf.toolbox import ExchangeRates


def open_pro():
    success = False
    for app in CONFIG['intents']['applications']['actions']:
        if app in context.subject:
            # assistant.speak(random.choice(CONFIG['intents']['applications']['responses']))
            success = application(context.subject)
            break
    if not success:
        assistant.speak('я не знаю такой программы')


def turn_off():
    if context.subject in CONFIG['intents']['app_close']['actions'].keys():
        app_close(CONFIG['intents']['app_close']['actions'][context.subject])


# def aimp(target):
#     aimp = r"C:\Program Files (x86)\AIMP\AIMP.exe"
#     if target == 'radio_like_fm':
#         sp.Popen([aimp, 'http://ic7.101.ru:8000/a219'])
#     elif target == 'radio_chillout':
#         sp.Popen([aimp, 'http://air2.radiorecord.ru:9003/chil_320'])
#     elif target == 'radio_office_lounge':
#         sp.Popen([aimp, 'http://ic7.101.ru:8000/a30'])
#     elif target == 'radio_chip':
#         sp.Popen([aimp, 'http://radio.4duk.ru/4duk256.mp3'])
#     elif target == 'radio_chillstep':
#         sp.Popen([aimp, 'http://ic5.101.ru:8000/a260'])
#     elif target == 'playlist_chillout':
#         sp.Popen([aimp, r'D:\Chillout.aimppl4'])
#     elif target == 'music_my':
#         sp.Popen([aimp, r'D:\2020'])
#     elif target == 'music_my_breathe':
#         sp.Popen([aimp, r'D:\2020\Breathe'])
#

def application(target):
    if target == 'telegram':
        path = r'C:\Users\go\AppData\Roaming\Telegram Desktop\Telegram.exe'
    elif target == 'whatsapp':
        path = r'C:\Users\go\AppData\Local\WhatsApp\app-2.2047.11\WhatsApp.exe'
    elif target == 'браузер':
        path = r'C:\Users\go\AppData\Local\Yandex\YandexBrowser\Application\browser.exe'
    elif target == 'яндекс музыка':
        path = r'C:\Users\go\AppData\Local\Yandex\YandexBrowser\Application\browser.exe ' \
               r'https://music.yandex.ru/home'
    elif target == 'калькулятор':
        path = r'calc'
    else:
        return False
    try:
        sp.Popen(path)
    except FileNotFoundError:
        assistant.speak('Мне не удалось найти файл программы')
    except PermissionError:
        assistant.speak('Мне отказано в доступе к файлу программы')

    return True


def app_close(proc):
    for process in (process for process in psutil.process_iter() if process.name() == proc):
        process.kill()


def act():
    context.imperative = None
    action = context.action
    assistant.speak(context.reply)
    print('action:', action, '| subj:', context.subject, '| repl:', context.reply)

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
        assistant.speak(assistant.last_speech)

    elif action == 'repeat_slow':
        # повторить последний ответ медленно
        assistant.setup_voice(rate=80)
        assistant.speak(assistant.last_speech.replace(' ', ' , '))
        assistant.setup_voice()

    elif action == 'repeat_after_me':
        # повторить что только что сказал
        assistant.speak(action)

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

    elif action == 'whois':
        answer = request_yandex_fast(context.subject)
        print(answer)
        assistant.speak(answer)

    elif action == 'wikipedia':
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

    assistant.alert()
    return True

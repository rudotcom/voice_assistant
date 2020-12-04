import subprocess as sp
from va_assistant import CONFIG, assistant, new_context, context
import psutil
import random
from datetime import datetime, timedelta
import webbrowser  # работа с использованием браузера по умолчанию
from va_misc import num_unit, timedelta_to_dhms, request_yandex_fast, btc, TimerThread, integer_from_phrase
import wikipediaapi  # поиск определений в Wikipedia
from translate import Translator
from fuzzywuzzy import process
from va_weather import open_weather
import re
from pycbrf.toolbox import ExchangeRates


def get_intent(levenshtein=90):
    phrase = ' '.join([new_context.imperative, new_context.source, new_context.subject])
    intent_now = response = action = ''
    for intent, intent_data in CONFIG['intents'].items():
        levenshtein_distance = process.extractOne(phrase, intent_data['requests'])
        if levenshtein_distance[1] >= levenshtein:
            levenshtein = levenshtein_distance[1]  # оценка совпадения
            intent_now = intent
            intent_words = levenshtein_distance[0].strip()  # само совпадение

    if intent_now:
        phrase = phrase.replace(intent_words, '')
        if 'actions' in CONFIG['intents'][intent_now].keys():
            for actions in CONFIG['intents'][intent_now]['actions'].keys():
                action = CONFIG['intents'][intent_now]['actions'][actions]

        if 'replies' in CONFIG['intents'][intent_now].keys():
            response = random.choice(CONFIG['intents'][intent_now]['replies'])
        print('resp', response, 'action', action)
        act(response, action)
        return True
    return False  # если интент не найден


def remove_alias(voice_text):
    for alias in assistant.alias:
        return voice_text.replace(alias, "", 1).strip()


def turn_on():
    """ проверяем, есть ли радио или музыка в контексте"""
    for sound in CONFIG['intents']['music']['requests']:
        if sound in context.subject:
            """ если есть, находим action """
            for action in CONFIG['intents']['music']['requests']:
                """ если action есть, включаем плеер"""
                if context.subject in CONFIG['intents']['music']['actions']:
                    aimp(CONFIG['intents']['music']['actions'][context.subject])
                    return
                else:
                    # если такого радио или музыки нет
                    # assistant.speak(context.target + ' ' + random.choice(CONFIG['intents']['music']['not_exists']))
                    return
            break
        else:
            please_specify('что включить:', 'target')
            break


def open_pro():
    success = False
    for app in CONFIG['intents']['applications']['actions']:
        if app in context.subject:
            # assistant.speak(random.choice(CONFIG['intents']['applications']['responses']))
            success = application(context.subject)
            break
    if not success:
        assistant.speak('я не знаю такой программы')


def please_specify(where, what):
    if what == 'target':
        assistant.speak('уточни, ' + where)
    if what == 'tool':
        print('где именно?')
    # assistant.speak(random.choice(CONFIG['intents']['music']['spec']))
    pass


def find_out():
    print('get_to_know')
    action, response = get_intent_action(context.subject, context.adverb)
    if action or response:
        target = ' '.join([context.subject, context.adverb])
        """ передаем действию предварительную фразу, само действие и цель действия """
        act(response, action, target)


def turn_off():
    if context.subject in CONFIG['intents']['app_close']['actions'].keys():
        app_close(CONFIG['intents']['app_close']['actions'][context.subject])


def aimp(target):
    aimp = r"C:\Program Files (x86)\AIMP\AIMP.exe"
    if target == 'radio_like_fm':
        sp.Popen([aimp, 'http://ic7.101.ru:8000/a219'])
    elif target == 'radio_chillout':
        sp.Popen([aimp, 'http://air2.radiorecord.ru:9003/chil_320'])
    elif target == 'radio_office_lounge':
        sp.Popen([aimp, 'http://ic7.101.ru:8000/a30'])
    elif target == 'radio_chip':
        sp.Popen([aimp, 'http://radio.4duk.ru/4duk256.mp3'])
    elif target == 'radio_chillstep':
        sp.Popen([aimp, 'http://ic5.101.ru:8000/a260'])
    elif target == 'playlist_chillout':
        sp.Popen([aimp, r'D:\Chillout.aimppl4'])
    elif target == 'music_my':
        sp.Popen([aimp, r'D:\2020'])
    elif target == 'music_my_breathe':
        sp.Popen([aimp, r'D:\2020\Breathe'])


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
            if 'replies' in source.keys(): reply = random.choice(source['replies'])
            if 'action' in source.keys(): action = source['action']
            return reply, action
    else:
        return None, None


def act_by_intent(text):
    if text:
        intent, action, response = get_intent(text, 70)
        print('i:', intent, 'a:', action, 'r:', response)
        if intent:
            act('', action, text)
            return True
    return False


def get_intent_action(imperative):
    """Получение интента (intents) из текста (сравнение с перечнем интентов в CONFIG)"""
    if imperative:
        intent, action, response = get_intent(70)

        if intent:
            return action, response
        else:
            assistant.fail()
            return '', ''


def app_close(proc):
    for process in (process for process in psutil.process_iter() if process.name() == proc):
        process.kill()


def act(reply, action):
    assistant.speak(reply)
    print('action:', action, '|', context.subject)

    if action == 'ctime':
        # сказать текущее время
        now = datetime.now()
        if now.hour < 3:
            day_part = 'ночи'
        elif now.hour < 12:
            day_part = 'утра'
        elif now.hour < 16:
            day_part = 'дня'
        elif now.hour < 23:
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
        cbrf = random.choice(['курс ЦБ РФ {} {} за доллар', 'доллар сегодня {} {}'])
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

    elif action == 'whois':
        answer = request_yandex_fast(context.subject)
        print(answer)
        assistant.speak(answer)

    elif action == 'wikipedia':
        def clear_wiki(text):
            re.sub(r'\([^)]+\)|/', ' ', text)
            for x in CONFIG['umlaut']:
                text = text.replace(x, CONFIG['umlaut'][x])
            return text

        wiki = wikipediaapi.Wikipedia(assistant.speech_language)
        wiki_page = wiki.page(context.subject)
        # webbrowser.get().open(wiki_page.fullurl)
        wiki = clear_wiki(wiki_page.summary)
        assistant.speak((wiki.replace('\n', '').split(".")[:2]))

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

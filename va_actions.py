import subprocess as sp
from va_assistant import CONFIG, assistant
import psutil
import random
import pyttsx3
from datetime import datetime, timedelta
import webbrowser  # работа с использованием браузера по умолчанию
from va_misc import units_ru, timedelta_to_dhms, request_yandex_fast, btc
import wikipediaapi  # поиск определений в Wikipedia
from translate import Translator
from fuzzywuzzy import fuzz, process
from va_weather import open_weather
import re
from pycbrf.toolbox import ExchangeRates


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
        speak('Мне не удалось найти файл программы')
    except PermissionError:
        speak('Мне отказано в доступе к файлу программы')

    return True


def get_intent(phrase, levenshtein):
    intent_now = response = action = ''
    for intent, intent_data in CONFIG['intents'].items():
        if 'requests' in intent_data:
            levenshtein_distance = process.extractOne(phrase, intent_data['requests'])
            if levenshtein_distance[1] >= levenshtein:
                levenshtein = levenshtein_distance[1]
                intent_now = intent

    if intent_now:
        if 'responses' in CONFIG['intents'][intent_now]:
            response = random.choice(CONFIG['intents'][intent_now]['responses'])
        if 'actions' in CONFIG['intents'][intent_now]:
            action = CONFIG['intents'][intent_now]['actions']['']
    return intent_now, action, response


def act_by_intent(text):
    if text:
        intent, action, response = get_intent(text, 70)
        if intent:
            act('', action, text)
            return True
    return False


def get_intent_action(target, adverb=''):
    target = ' '.join([adverb, target])
    """Получение интента (intents) из текста (сравнение с перечнем интентов в CONFIG)"""
    if target:
        intent, action, response = get_intent(target, 70)

        if intent:
            return action, response
        else:
            speak(random.choice(CONFIG['failure_phrases']))
            return '', ''


def app_close(proc):
    for process in (process for process in psutil.process_iter() if process.name() == proc):
        process.kill()


def speak(what):
    if not what:
        return
    """Воспроизведение текста голосом"""
    assistant.last_speech = what
    print(what)
    tts.say(what)
    tts.runAndWait()
    tts.stop()


def setup_assistant_voice(lang="ru"):
    """Установка параметров голосового движка"""
    assistant.speech_language = lang
    voices = tts.getProperty("voices")
    tts.setProperty('rate', assistant.speech_rate)
    tts.setProperty('volume', assistant.speech_volume)

    if assistant.speech_language == "en":
        assistant.recognition_language = "en-US"
        if assistant.sex == "female":
            # Microsoft Zira Desktop - English (United States)
            tts.setProperty("voice", voices[2].id)
        else:
            # Microsoft David Desktop - English (United States)
            tts.setProperty("voice", voices[1].id)
    else:
        tts.setProperty("voice", voices[assistant.speech_voice].id)


def act(response, action, target=''):
    speak(response)
    print('act:', action, '|', target)

    if action == 'age':
        td = datetime.now() - assistant.birthday
        days, hours, minutes, seconds = timedelta_to_dhms(td)
        my_age = 'мне ' + units_ru(days, 'days') + ' ' + \
                 units_ru(hours, 'hours') + ' ' + units_ru(minutes, 'minutes')
        speak(my_age)

    elif action == 'repeat':
        # повторить последний ответ
        speak(assistant.last_speech)

    elif action == 'repeat_slow':
        # повторить последний ответ медленно
        tts.setProperty('rate', 80)
        speak(assistant.last_speech.replace(' ', ' , '))
        tts.setProperty('rate', assistant.speech_rate)

    elif action == 'repeat_after_me':
        # повторить что только что сказал
        speak(action)

    elif action == 'usd':
        # курс доллара
        rates = ExchangeRates()
        rate = round(rates['USD'].rate, 2)
        rate_verbal = 'курс ЦБ РФ' + units_ru(int(rate), 'rub') + units_ru(int(rate % 1 * 100), 'kop') + 'за доллар'
        speak(rate_verbal)

    elif action == 'btc':
        # курс биткоина
        speak(btc())

    elif action == 'mood_up':
        if assistant.mood < 2:
            assistant.mood += 1

    elif action == 'mood_down':
        assistant.mood = -1

    elif action == 'my_mood':
        phrases = CONFIG['mood'][assistant.mood]
        speak(random.choice(phrases))

    elif action == 'die':
        exit()

    elif action == 'weather':
        print('tt', target)
        target.replace('погода', '').strip()
        print('t', target)
        weather = open_weather(target)
        speak(weather)

    elif action == 'youtube':
        url = "https://www.youtube.com/results?search_query=" + target
        webbrowser.get().open(url)

    elif action == 'browse_google':
        assistant.last_action = action
        url = "https://www.google.ru/search?q=" + target
        webbrowser.get().open(url)

    elif action == 'browse_yandex':
        url = "https://yandex.ru/search/?text=" + target
        webbrowser.get().open(url)

    elif action == 'yandex_maps':
        url = "https://yandex.ru/maps/?text=" + target
        webbrowser.get().open(url)

    elif action == 'whois':
        answer = request_yandex_fast(target)
        print(answer)
        speak(answer)

    elif action == 'wikipedia':
        wiki = wikipediaapi.Wikipedia(assistant.speech_language)
        wiki_page = wiki.page(target)
        # webbrowser.get().open(wiki_page.fullurl)
        wiki = re.sub(r'\([^)]+\)|/', ' ', wiki_page.summary)
        speak((wiki.replace('\n', '').split(".")[:2]))

    elif action == 'translate':
        translator = Translator(from_lang="ru", to_lang="en")
        target = target.replace('по-английски', '')
        translation = translator.translate(target)
        speak(target)
        speak("по-английски")
        setup_assistant_voice("en")
        speak(translation)
        setup_assistant_voice("ru")

    assistant.last_input = datetime.now()


tts = pyttsx3.init()

# имя проекта: voice-assistant
# номер версии: 0.1
# имя файла: main.py
# автор: Трошков А.В.
# дата создания: 24.11.2020
# описание: голосовой помощник
# версия Python: 3.8
import random
import os
from datetime import datetime, timedelta
import subprocess as sp
import webbrowser  # работа с использованием браузера по умолчанию
from va_voice_recognition import recognize_offline, recognize_online
from va_assistant import VoiceAssistant, CONFIG
from va_misc import units_ru, timedelta_to_dhms, request_yandex_fast, btc
import wikipediaapi  # поиск определений в Wikipedia
from translate import Translator
from fuzzywuzzy import fuzz, process
from va_weather import open_weather
import re
from pycbrf.toolbox import ExchangeRates
import pyttsx3


def get_intent(request):
    """Получение интента (intents) из текста (сравнение с перечнем интентов в CONFIG)"""
    threshold = 70
    intent_now = ''
    if request:
        for intent, intent_data in CONFIG['intents'].items():
            levenstein_intent = process.extractOne(request, intent_data['requests'])
            if levenstein_intent[1] >= threshold:
                threshold = levenstein_intent[1]
                intent_now = intent
                # если новый интент есть, удаляем старый экшен
                assistant.last_action = ''
        # удалить запросы интента из текста
        if intent_now:
            for intent_requests in CONFIG['intents'][intent_now]['requests']:
                i_r = request.partition(intent_requests)
                request = (i_r[0] + i_r[2]).strip()
    assistant.last_intent = intent_now
    return [intent_now, request]


def get_action(intent, request):
    """Получение экшенов (actions) из текста (сравнение запроса с перечнем экшенов в интенте)"""
    threshold = 60
    action_now = ''
    if 'actions' in CONFIG['intents'][intent].keys():
        for action in (CONFIG['intents'][intent]['actions']).keys():
            levenstein_action = fuzz.WRatio(action, request)
            if levenstein_action >= threshold:
                threshold = levenstein_action
                action_now = (CONFIG['intents'][intent]['actions'])[action]
                # удаляем часть фразы, оставляем только после action
                request = request.partition(action)[2].strip()
        return {
            'action': action_now,
            'request': request
        }


def filter_text(text):
    """Замена нестандартных символов (Wikipedia), удаление мусора"""
    if text:
        text.replace('а́', 'а')
        text.replace('у́', 'у')
        text.replace('е́́', 'е')
        text.replace('о́́́', 'о')
        text.replace('и́́́́', 'и')
        text.replace('я́́́́', 'я')

        for x in CONFIG['alias']:
            text = text.replace(x, "", 1).strip()

        for x in CONFIG['tbr']:
            # удаляем все бессмысленные словосочетания
            text = text.replace(x, "").strip()
    return text


def get_answer_by_intent(intent):
    """Получение одного из ответов (responses) интента"""
    if intent in CONFIG['intents']:
        # Если у интента есть голосовой ответ, выдаем его
        phrases = CONFIG['intents'][intent]['responses']
        return random.choice(phrases)


def reask(action):
    """Запрос уточнения экшена"""
    phrases = CONFIG['intents']['actions']['reask']
    speak(random.choice(phrases))
    return


def act_request(action, request):
    """Выполнение действия, требующего доп запроса"""
    print('act_request...')

    speak(get_answer_by_intent(assistant.last_intent))
    if action == 'weather':
        assistant.last_object = request
        weather = open_weather(request)
        print(weather)
        speak(weather)
    elif action == 'youtube':
        url = "https://www.youtube.com/results?search_query=" + request
        webbrowser.get().open(url)
    elif action == 'browse_yandex':
        assistant.last_action = action
        url = "https://yandex.ru/search/?text=" + request
        webbrowser.get().open(url)
    elif action == 'whois':
        assistant.last_action = action
        answer = request_yandex_fast(request)
        print(answer)
        speak(answer)
    elif action == 'wikipedia':
        assistant.last_action = action
        wiki = wikipediaapi.Wikipedia(assistant.speech_language)
        wiki_page = wiki.page(request)
        webbrowser.get().open(wiki_page.fullurl)
        wiki = re.sub(r'\([^)]+\)|/', ' ', wiki_page.summary)
        print(wiki)
        speak((wiki.replace('\n', '').split(".")[:2]))
    elif action == 'translate':
        assistant.last_action = action
        translator = Translator(from_lang="ru", to_lang="en")
        translation = translator.translate(request)
        speak(request)
        speak("по-английски будет. ")
        setup_assistant_voice("en")
        print(translation)
        speak(translation)
        setup_assistant_voice("ru")


def act(action=None, request=None):
    """Выполнение действия"""
    print('trying to act...', 'action:', action, 'request:', request)
    aimp = r"C:\Program Files (x86)\AIMP\AIMP.exe"

# действия с дополнительным запросом отправляем в функцию с обязательным текстовым запроом act_request
    if action in ['youtube', 'browse_yandex', 'whois', 'wikipedia', 'translate', 'weather']:
        # сохранить action, а если текстового запроса нет, вернуть на переспрашивание
        assistant.last_action = action
        if request or action == 'weather':
            act_request(action, request)
        return

    # действия без обязательного дополнительного запроса
    if assistant.last_intent != 'repeat':
        speak(get_answer_by_intent(assistant.last_intent))
    if action == 'stop':
        assistant.recognition_mode = 'offline'
        assistant.last_input = datetime.now() - timedelta(seconds=sec_to_offline)
        return
    elif action == 'ctime':
        # сказать текущее время
        now = datetime.now()
        speak("Сейчас " + units_ru(now.hour, 'hours') + units_ru(now.minute, 'minutes'))
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
        speak(request)
    elif action == 'usd':
        # курс доллара
        rates = ExchangeRates()
        rate = round(rates['USD'].rate, 2)
        rate_verbal = 'ЦБ РФ' + units_ru(int(rate), 'rub') + units_ru(int(rate % 1 * 100), 'kop') + 'за доллар'
        print(rate_verbal)
        speak(rate_verbal)
    elif action == 'btc':
        # курс биткоина
        speak(btc())
    elif action == 'my_age':
        td = datetime.now() - assistant.birthday
        days, hours, minutes, seconds = timedelta_to_dhms(td)
        my_age = 'мне ' + units_ru(days, 'days') + ' ' + \
                 units_ru(hours, 'hours') + ' ' + units_ru(minutes, 'minutes')
        print(my_age)
        speak(my_age)
    elif action == 'music_yandex':
        url = "https://music.yandex.ru/home"
        webbrowser.get().open(url)
    elif action == 'radio_like_fm':
        sp.Popen([aimp, 'http://ic7.101.ru:8000/a219'])
    elif action == 'radio_chillout':
        sp.Popen([aimp, 'http://air2.radiorecord.ru:9003/chil_320'])
    elif action == 'radio_office_lounge':
        sp.Popen([aimp, 'http://ic7.101.ru:8000/a30'])
    elif action == 'radio_chip':
        sp.Popen([aimp, 'http://radio.4duk.ru/4duk256.mp3'])
    elif action == 'radio_chillstep':
        sp.Popen([aimp, 'http://ic5.101.ru:8000/a260'])
    elif action == 'playlist_chillout':
        sp.Popen([aimp, r'D:\Chillout.aimppl4'])
    elif action == 'music_my':
        sp.Popen([aimp, r'D:\2020'])
    elif action == 'music_my_breathe':
        sp.Popen([aimp, r'D:\2020\Breathe'])
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
    else:
        phrases = CONFIG['failure_phrases']
        speak(random.choice(phrases))
    assistant.last_input = datetime.now()


def recognize(mode):
    """Выбор режима распознавания"""
    if mode == 'online':
        return recognize_online()
    else:
        return recognize_offline()


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
            tts.setProperty("voice", voices[assistant.speech_voice].id)
        else:
            # Microsoft David Desktop - English (United States)
            tts.setProperty("voice", voices[assistant.speech_voice].id)
    else:
        tts.setProperty("voice", voices[assistant.speech_voice].id)


def speak(what):
    """Воспроизведение текста голосом"""
    assistant.last_speech = what
    tts.say(what)
    tts.runAndWait()
    tts.stop()
    logging(' --- ', what)


def logging(*args):
    pass
    # print(args)
    # with open('enquiries.txt', 'a') as log:
    #      log.write(''.join(args) + '\n')


if __name__ == "__main__":

    tts = pyttsx3.init()
    assistant = VoiceAssistant()
    assistant.name = CONFIG['alias'][0]
    setup_assistant_voice()

    whazzup = assistant.name + ' ' + CONFIG['whazzup'][assistant.recognition_mode]
    speak(whazzup)
    assistant.last_input = datetime.now()
    sec_to_offline = 40

    while True:
        #   если timedelta прошла, переход в офлайн или
        #   "Помолчи" - переход в офлайн
        fresh_talk = datetime.now() - assistant.last_input < timedelta(seconds=sec_to_offline)
        # print('fresh', fresh_talk, 'last', assistant.last_input)
        if fresh_talk:
            assistant.recognition_mode = 'online'
            print("online")
        else:
            assistant.recognition_mode = 'offline'
            print("offline...")

        # print(assistant.recognition_mode, datetime.now() - assistant.last_input)

        voice_text = recognize(assistant.recognition_mode)
        if type(voice_text) == 'dict' and voice_text['status'] == 'fail':
            assistant.recognition_mode = 'offline'
            speak("Интернет пропал, я затупила, скажи еще раз, но теперь разборчиво")
            continue

        if voice_text:
            logging(voice_text)
            print('voice_text:', voice_text)
            # print(datetime.now(), assistant.last_input)
            # условия бодрствования
            # если предыдущее сообщение было недавно или сообщение начинается с имени
            awake = any([fresh_talk, voice_text.startswith(CONFIG["alias"])])
            if awake:
                assistant.last_input = datetime.now()
                assistant.recognition_mode = 'online'
                filtered_text = filter_text(voice_text)
                # print('filtered:', filtered_text)

                # узнать интент пользователя
                if filtered_text:
                    # print(' -- > get_intent')  # debugging
                    intent_now, request = get_intent(filtered_text)
                    # print('intent:', intent_now)  # debugging
                    # print('lasting action:', assistant.last_action)  # debugging
                    assistant.recognition_mode = 'online'

                    # если нет ни интента ни сохраненного экшена
                    if not intent_now and not assistant.last_action:
                        speak(random.choice(CONFIG['failure_phrases']))
                        assistant.last_input = datetime.now()
                        continue

                    # если есть интент
                    elif intent_now:
                        intent_par = CONFIG['intents'][intent_now]
                        # если в интенте нет экшенов
                        if 'actions' not in intent_par.keys():
                            speak(get_answer_by_intent(intent_now))
                        # если в интенте только один экшен, запускать его
                        elif 'actions' in intent_par and len(intent_par['actions']) == 1:
                            action_now = str(*CONFIG['intents'][intent_now]['actions'].values())
                            logging('a: ', action_now, ' r: ', request, ' >act')
                            act(action_now, request)
                        else:
                            # Понять какое действие соответствует интенту
                            # print(' -- > get_action')  # debugging
                            action_now = get_action(intent_now, request)
                            # print('action_now:', action_now)  # debugging
                            if action_now and action_now['action']:
                                log_line = ['a:', action_now['action'], '--', 'r:', action_now['request'], ' >act']
                                # print(log_line)  # debugging
                                # print(' -- > act')  # debugging
                                logging(log_line)
                                act(action_now['action'], action_now['request'])
                            else:
                                speak(random.choice(CONFIG['failure_phrases']))
                                speak(request)

                    # если есть сохрененный экшен (т.е. не было интента), значит это уточнение экшена
                    elif assistant.last_action:
                        # если экшен сохранен, действовать с новым запросом
                        # если экшен есть произносим ответ
                        log_line = ['lasting action:', assistant.last_action, '--', 'r:', request, ' >act']
                        # print(log_line)  # debugging
                        logging(log_line)
                        act(assistant.last_action, request)

                else:
                    speak(random.choice(CONFIG['reply_for_name']))
            else:
                # если не было активности
                assistant.recognition_mode = 'offline'

# TODO: Для выяснения намерений разложить на глаголы и существительные
#   - выключить плеер
#   - включить музыку для дыхания
#   - прилагательные ?
#   - speak в отдельном потоке
#   - будильник Windows:
#   explorer.exe shell:Appsfolder\Microsoft.WindowsAlarms_8wekyb3d8bbwe!App
#   - Делать скриншот (модуль клавиатуры)
#   - сохранять контекст:
#       [intent], [action], ??[object]??
#   менять голос, если настроение хуже
#   - морфологический разбор: какая завтра погода, какая погода завтра, погода какая завтра, завтра какая погода
#   - вырезать наречия союзы и т.д.

# имя проекта: voice-assistant
# номер версии: 0.1
# имя файла: main.py
# автор: Трошков А.В.
# дата создания: 24.11.2020
# описание: голосовой помощник
# версия Python: 3.8
import random
from os import system
from datetime import datetime, timedelta
import subprocess as sp
import webbrowser  # работа с использованием браузера по умолчанию
from va_voice_recognition import recognize_offline, recognize_online
from va_assistant import VoiceAssistant, CONFIG, Context
from va_misc import units_ru, timedelta_to_dhms, request_yandex_fast, btc
import wikipediaapi  # поиск определений в Wikipedia
from translate import Translator
from fuzzywuzzy import fuzz, process
from va_weather import open_weather
import re
from pycbrf.toolbox import ExchangeRates
import pyttsx3


def get_intent(text):
    """ getting intent to intent_now"""
    intent_now = text
    if intent_now:
        context.new_intent(intent_now)
    else:
        intent_now = context.intent

    return intent_now


def get_action(intent, text):
    action_now = ''
    if intent:
        """ если в интенте только response, отвечаем response """
        if 'actions' not in CONFIG['intents'][intent]:
            answer_by_intent(intent)
        """ если экшенов много выбираем по target """
        elif
    else:
    """ если интента нету пытаемся получить экшен из контекста """
        action_now = context.action
    """ а также пытаемся получить новый экшен """
        action_now = ........
    if action_now:
        context.new_action(action_now, target)
    else:
        """ экшена нет, заглушка """
        phrases = CONFIG['failure_phrases']
        speak(random.choice(phrases))

    return action_now


def answer_by_intent(intent):
    """Получение одного из ответов (responses) интента"""
    if intent in CONFIG['intents']:
        # Если у интента есть голосовой ответ, выдаем его
        phrases = CONFIG['intents'][intent]['responses']
        return random.choice(phrases)


def specify_action():
    pass


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


def recognize(mode):
    """Выбор режима распознавания"""
    if mode == 'online':
        return recognize_online()
    else:
        return recognize_offline()


if __name__ == "__main__":

    tts = pyttsx3.init()
    assistant = VoiceAssistant()
    context = Context()
    assistant.name = CONFIG['alias'][0]
    setup_assistant_voice()

    whazzup = assistant.name + ' ' + CONFIG['whazzup'][assistant.recognition_mode]
    speak(whazzup)
    assistant.last_input = datetime.now()
    sec_to_offline = 40

    while True:
        """если timedelta прошла, переход в офлайн или "Помолчи" - переход в офлайн"""
        fresh_talk = datetime.now() - assistant.last_input < timedelta(seconds=sec_to_offline)
        # print('fresh', fresh_talk, 'last', assistant.last_input)
        if fresh_talk:
            assistant.recognition_mode = 'online'
            print("online")
        else:
            assistant.recognition_mode = 'offline'
            print("offline...")

        voice_text = recognize(assistant.recognition_mode)
        if voice_text:
            print('voice_text:', voice_text)
            # print(datetime.now(), assistant.last_input)
            # условия бодрствования
            # если предыдущее сообщение было недавно или сообщение начинается с имени
            awake = any([fresh_talk, voice_text.startswith(CONFIG["alias"])])
            if awake:
                assistant.last_input = datetime.now()
                assistant.recognition_mode = 'online'
                user_text = filter_text(voice_text)
                # print('filtered:', filtered_text)

                # узнать интент пользователя
                if user_text:
                    # print(' -- > get_intent')  # debugging
                    intent = get_intent(user_text)
                    action = get_action(intent, user_text)

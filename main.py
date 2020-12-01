# имя проекта: voice-assistant
# номер версии: 0.1
# имя файла: main1.py
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
from va_assistant import assistant, context, CONFIG
from va_misc import units_ru, timedelta_to_dhms, request_yandex_fast, btc
import wikipediaapi  # поиск определений в Wikipedia
from translate import Translator
from fuzzywuzzy import fuzz, process
from va_weather import open_weather
import re
from pycbrf.toolbox import ExchangeRates
import pyttsx3


def get_intent(ctx):
    """Получение интента (intents) из контекста (сравнение с перечнем интентов в CONFIG)"""
    threshold = 70
    intent_now = ''
    for intent, intent_data in CONFIG['intents'].items():
        levenstein_intent = process.extractOne(ctx.target, intent_data['requests'])
        if levenstein_intent[1] >= threshold:
            threshold = levenstein_intent[1]
            intent_now = intent
    return intent_now

def answer_by_intent(intent):
    """Получение одного из ответов (responses) интента"""
    if intent in CONFIG['intents']:
        # Если у интента есть голосовой ответ, выдаем его
        phrases = CONFIG['intents'][intent]['responses']
        return random.choice(phrases)


def specify_target():
    # если есть imperative, но нет target, уточнить target
    speak(random.choice(CONFIG['intents']['music']['spec']))
    pass


def remove_alias(text):
    for x in CONFIG['alias']:
        text = text.replace(x, "", 1).strip()
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
            awake = any([fresh_talk, voice_text.startswith(assistant.alias)])
            if awake:
                assistant.last_input = datetime.now()
                assistant.recognition_mode = 'online'
                user_text = remove_alias(voice_text)
                # print('filtered:', filtered_text)

                # узнать интент пользователя
                if user_text:
                    # print(' -- > get_intent')  # debugging
                    context.context_by_phrase(user_text)
                    print('imperative:', context.imperative)
                    print('tool:', context.tool)
                    print('target:', context.target)
                    print('adverb:', context.adverb)
                    print('addressee:', context.addressee)
                    if context.target:
                        intent_now = get_intent(context)
                        print('intent:', intent_now)

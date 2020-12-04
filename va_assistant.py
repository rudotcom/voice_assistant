from datetime import datetime
import pymorphy2
import pyttsx3
import random
from datetime import datetime, timedelta
from va_voice_recognition import recognize_offline, recognize_online
import re

tts = pyttsx3.init()
morph = pymorphy2.MorphAnalyzer()


class VoiceAssistant:
    """ Настройки голосового ассистента """
    name = 'мурзилка'
    alias = ('мурзилка', 'морозилка')
    birthday = datetime(2020, 11, 24, 23, 54, 22)
    sec_to_offline = 40
    last_active = None
    last_speech = ''

    def __init__(self):
        self.recognition_mode = "online"
        self.sex = "female"
        self.recognition_language = "ru-RU"
        self.speech_voice = 3  # голосовой движок
        self.speech_language = "ru"
        self.speech_rate = 130  # скорость речи 140 самый норм
        self.speech_volume = 1  # громкость (0-1)
        self.mood = 0

    def is_alert(self):
        alert = datetime.now() - self.last_active < timedelta(seconds=self.sec_to_offline)
        if not alert:
            self.sleep()
        return alert

    def alert(self):
        self.last_active = datetime.now()
        self.recognition_mode = 'online'

    def sleep(self):
        self.last_active = datetime.now() - timedelta(seconds=self.sec_to_offline)
        self.recognition_mode = 'offline'

    def setup_voice(self, lang="ru", rate=130):
        """Установка параметров голосового движка"""
        self.speech_language = lang
        voices = tts.getProperty("voices")
        tts.setProperty('rate', rate)

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

    def speak(self, what):
        if not what:
            return
        """Воспроизведение текста голосом"""
        if context.addressee:
            listen = random.choice(['слушай', 'тебе говорю', 'короче', 'прикинь', 'только вкинься'])
            what = ', '.join([context.addressee, listen, what, ])
        self.last_speech = what
        print(what)
        tts.say(what)
        tts.runAndWait()
        tts.stop()

    def recognize(self):
        """Выбор режима распознавания"""
        if self.recognition_mode == 'online':
            return recognize_online()
        else:
            return recognize_offline()

    def use_source(self):
        print('source:', context.source)
        print('subject', context.subject)
        response = random.choice(CONFIG['intents']['find']['responses'])
        if context.source in CONFIG['intents']['find']['actions'].keys():
            print(context.source, CONFIG['intents']['find']['actions'].keys())
            action = CONFIG['intents']['find']['actions'][context.source]
            return response, action, context.subject
        else:
            self.speak('Там я не умею искать')

    def fail(self):
        self.speak(random.choice(CONFIG['failure_phrases']))


class Context:

    def __init__(self):
        self.imperative = ''
        self.source = ''
        self.subject = ''
        self.location = ''
        self.adverb = ''
        self.addressee = ''
        self.text = ''
        self.action = ''
        self.reply = ''

    def __str__(self):
        # для отладки
        return 'imperative:\t{self.imperative} \
               \nsource:\t\t{self.source} \
               \nsubject:\t{self.subject} \
               \nlocation:\t{self.location} \
               \nadverb:\t\t{self.adverb} \
               \naddressee:\t{self.addressee} \
               \ntext:\t{self.text}\n'.format(self=self)

    def get_from_phrase(self, phrase):
        prep = imperative = imperative_word = action = reply = \
            source = subject = location = addressee = adverb = ''
        """ сначала раскладываем на морфемы """
        for word in phrase.split():
            p = morph.parse(word)[0]
            if word in CONFIG['litter']:
                # удаляем все бессмысленные словосочетания
                phrase = phrase.replace(word, "").strip()
            elif p.tag.POS in ['PRED', 'INTJ']:  # удаляем союзы, частицы, предикативы, междометия
                phrase = phrase.replace(word, "").strip()
            elif p.tag.mood == 'impr':  # императив
                imperative_word = word
                imperative = p[2]
            elif p.tag.POS == 'PREP':
                prep = word
            elif p.tag.POS == 'NOUN' or word in CONFIG['eng_nouns']:

                """ объединяем существительное с предстоящим предлогом """
                noun = ' '.join([prep, word])
                if noun in CONFIG['intents']['find']['sources'].keys():
                    """ если это слово содержится в источниках поиска, значит это - инструмент поиска source"""
                    source = ' '.join([source, noun])
                elif p.tag.case in ('accs', 'gent', 'nomn'):
                    """винит, родит, иминит Кого? Чего? Кого? Что? Кому? Чему?"""
                    subject = ' '.join([subject, p[2]])
                elif p.tag.case == 'loct':
                    """предложный падеж - где?"""
                    location = ' '.join([location, noun])
                elif p.tag.case == 'datv':
                    """дат Кому? Чему?"""
                    addressee = ' '.join([addressee, p[2]])
                    phrase = phrase.replace(word, '')
                prep = ''  # этот предлог больше не будет относиться к другим существительным

            elif 'LATN' in p.tag:
                subject = ' '.join([subject, word])
            elif 'NUMB' in p.tag:
                subject = ' '.join([subject, word])
            elif p.tag.POS == 'ADVB':
                adverb = p[2]
            elif p.tag.POS in ('ADJF', 'ADJS'):
                pass

        """ есть ли вопросительное слово ? """
        interrogative = words_in_phrase(CONFIG['intents']['find_out']['requests'], phrase)

        if interrogative:
            imperative = 'узнать'
            sources = CONFIG['intents']['find_out']['sources']
            for source_key in sources.keys():
                source_request = words_in_phrase(sources[source_key]['requests'], phrase)
                if source_request:
                    phrase = phrase.replace(source_request, '')
                    for source_param in sources[source_key].keys():
                        if source_param == 'replies':
                            reply = random.choice(sources[source_key][source_param])
                        if source_param == 'action':
                            action = sources[source_key]['action']
                    break

        elif imperative in CONFIG['intents']['find']['requests']:
            """ находим имератив imperative"""
            # значит намерение искать с помощью поискового инструмента
            imperative = 'найти'
            if source:
                phrase = phrase.replace(imperative_word, '')
                subject = phrase.replace(source, '')
                action = CONFIG['intents']['find']['sources'][source]

        self.addressee = addressee.strip()
        self.action = action
        self.reply = reply
        self.imperative = imperative
        self.subject = subject.strip()
        self.location = location
        self.source = source.strip()
        self.adverb = adverb.strip()
        self.text = phrase


assistant = VoiceAssistant()
context = Context()
new_context = Context()

CONFIG = {
    'intents': {
        'hello': {
            'requests': ['привет', 'добрый день', 'здравствуй', 'доброе утро', 'добрый вечер'],
            'replies': ['Привет босс!', 'давай говори чего хочешь'],
        },
        'stop': {
            'requests': ['помолчи', 'не подслушивай', 'тихо', 'потеряйся',
                         'пока', 'до свидания', 'прощай', 'спокойной ночи'],
            'replies': ['молчу', 'Счаст ливо', 'Еще увидимся', 'Если что я тут'],
            'actions': {'': 'stop'}
        },
        'die': {
            'requests': ['умери', 'сдохни'],
            'replies': ['увидимся в следующей жизни', 'Если что, знаешь где меня искать', 'пока-пока'],
            'actions': {'': 'die'}
        },
        'name': {
            'requests': ['как твоё имя', 'как тебя зовут'],
            'replies': ['меня зовут Мурзилка'],
        },
        'think': {
            'requests': ['думаешь', 'подумай', 'как думаешь'],
            'replies': ['я еще не думаю', 'я пока не умею думать', 'думать это твоя работа',
                        'у меня нет такой функции', 'просто скажи что ты хочешь'
                        ],
        },
        'uwhere': {
            'requests': ['ты где', 'куда подевалась', 'ты тут', 'почему не отвечаешь'],
            'replies': ['я тут, ты меня спрашиваешь, что-ли?', 'тута я', 'вот я', 'отвлеклася немного'],
        },
        'abuse': {
            'requests': ['плохо', 'нехорошо', 'нехорошая', 'дура', 'коза', 'бестолковая',
                         'заткнись', 'задолбала', 'уродина', "****"],
            'replies': ['на себя посмотри', 'а чё сразу ругаться та', 'ну обидно же',
                        'за что', 'я тебя запомню!', 'нормально же общались', 'фак ю вэри мач'],
            'actions': {'': 'mood_down'},
        },
        'praise': {
            'requests': ['красава', 'молодец', 'хорошо', 'отлично', 'хороший', 'приятно поговорить',
                         'спасибо', 'благодарю', 'прикольно', 'умница', 'замечательно', 'супер'],
            'replies': ['спасибо', 'мне очень приятно', 'стараюсь'],
            'actions': {'': 'mood_up'},
        },
        'app_close': {
            'requests': ['выключи', 'закрой', ],
            'replies': ['выключаю', 'как скажешь', 'хорошо', 'ладно', ''],
            'actions': {'радио': 'AIMP.exe', 'player': 'AIMP.exe', 'музыку': 'AIMP.exe'}
        },
        'music': {
            'requests': ['радио', 'музыку', 'radio', 'playlist', 'плейлист', 'включи'],
            'replies': ['включаю', 'как скажешь', 'сама с удовольствием послушаю', 'хорошо', 'а га', '', ],
            'actions': {
                'радио чилаут': 'radio_chillout',
                'радио like fm': 'radio_like_fm',
                'радио лайк': 'radio_like_fm',
                'радио офис lounge': 'radio_office_lounge',
                'радио офис лаунж': 'radio_office_lounge',
                'радио office lounge': 'radio_office_lounge',
                'плейлист чилаут': 'playlist_chillout',
                'playlist chill out': 'playlist_chillout',
                'радио чилстеп': 'radio_chillstep',
                'радио chillstep': 'radio_chillstep',
                'радио чипльдук': 'radio_chip',
                'мою музыку': 'music_my',
                'музыку для дыхания': 'music_my_breathe',
            },
            'spec': ['что включить', 'что ты хочешь послушать', 'что именно', 'а конкретнее'],
            'not_exists': ['у меня такого нет', 'такого нет, выбери другое']
        },
        'applications': {
            'requests': ['открой'],
            'replies': ['открываю', 'как скажешь', 'интересно что же там', ],
            'actions': {
                'яндекс музыку': 'yandex_music',
                'telegram': 'telegram',
                'whatsapp': 'whatsapp',
                'браузер': 'chrome',
                'телеграмму': 'telegram',
                'калькулятор': 'calc',
            },
        },
        'repeat': {
            'requests': ['повтори', 'еще раз', 'что ты говоришь'],
            'replies': [''],
            'actions': {'': 'repeat', 'помедленнее': 'repeat_slow'},
        },
        'repeat_after_me': {
            'requests': ['повтори за мной', 'произнеси'],
            'replies': [''],
            'actions': {'': 'repeat_after_me'}
        },
        'find': {
            'requests': ['найди', 'спроси у', 'загугли', 'поищи', 'пошукай', 'где'],
            'replies': ['пошла искать', 'уже ищу', 'секундочку', 'это где-то здесь', 'что-то нашла'],
            'sources': {
                'в яндекс музыке': 'yandex_music',
                'в яндексе': 'browse_yandex',
                'в википедии': 'wikipedia',
                'в гугле': 'browse_google',
                'загуголь': 'browse_google',
                'в youtube': 'youtube',
                'находится': 'yandex_maps',
                'где': 'yandex_maps',
                'на карте': 'yandex_maps',
            },
        },
        'find_out': {
            'requests': ['почему', 'зачем', 'когда', 'сколько', 'какая', 'какой', 'как', 'какие', 'что за', 'скажи',
                         'посчитай', 'что ты', 'что с', 'кто такой', 'кто такая', 'что такое', 'что есть', 'почём'],
            'sources': {
                'can': {
                    'requests': ['что ты умеешь', 'твои способности', 'что ты можешь', 'что ты знаешь'],
                    'replies': ['я умею отвечать кто такой и что такое, \
                                  говорить время, \
                                  включать радио и музыку, \
                                  говорить погоду в любом месте на земле, \
                                  искать в яндэксе, гугле, ютубе и википедии, \
                                  знаю свой возраст, могу повторять за тобой. \
                                  Могу узнать курс доллара или биткоина. \
                                  Ты меня не обижай'],
                },
                'mood': {
                    'requests': ['как настроение', 'как дела', 'как себя чувствуешь'],
                    'action': 'my_mood',
                },
                'ctime': {
                    'requests': ['текущее время', 'сколько время', 'сколько времени', 'который час'],
                    'action': 'ctime',
                },
                'age': {
                    'requests': ['сколько тебе лет', 'твой возраст'],
                    'action': 'age',
                },
                'whois': {
                    'requests': ['что такое', 'кто такой'],
                    'action': 'who_wikipedia',
                },
                'translate': {
                    'requests': ['переведи', 'по-английски'],
                    'action': 'translate',
                },
                'weather': {
                    'requests': ['какая погода', 'погода', 'сколько градусов', 'на улице', 'холодно',
                                 'тепло', 'что с погодой', 'завтра погода', 'влажность'],
                    'action': 'weather',
                },
                'usd': {
                    'requests': ['курс доллара', 'почём доллар'],
                    'action': 'usd',
                },
                'btc': {
                    'requests': ['курс биткоина', 'почём биткоин', 'курс битка', 'bitcoin'],
                    'action': 'btc',
                },
                'calculate': {
                    'requests': ['посчитай', 'сколько будет'],
                    'replies': ['Я только учусь считать'],
                },
                'days_to': {
                    'requests': ['сколько дней до'],
                    'replies': ['еще не знаю', 'разработчик сказал научит до нового года но не сказал до какого'],
                }
            },
        }
    },
    'failure_phrases': [
        'Вот это сейчас что было?',
        'Что-то не понятно',
        'А можно как-то попроще выразиться?',
        'К сожалению, я не смогу помочь вам с этим вопросом',
        'Слишком сложно для меня',
        'Здесь как говорится наши полномочия всё',
        'Моя твоя не понимай',
        'Уточни вопрос, пожалуйста',
        'Ничего не поняла, но о очень интересно',
        'Вас людей не всегда поймешь',
        'Я не совсем тебя поняла',
        'Как это понимать?',
        'Но-но, Полегче!',
        'Запуталася я с вами совсем.',
        'Меня такому не учили',
        'Может мы забудем, что ты сказал?',
        'Ещё ра зочек можно?',
        'Мне не понятно.',
        'Я правильно интерпретирую семантику вопроса, но полностью игнорирую его суть',
        'Прости, чёт не вкурила',
        'ты пытаешься меня запутать?!',
        'Туплю... повто ри',
        'Это точно правильные слова?',
        'Я не поняла твоих намерений',
        'Я же всего лишь бот. Скажи попроще',
        'Я поняла, что я не поняла',
        'Со рян не поняла',
        'Сначала я ничего не поняла, а потом я тоже ничего не поняла',
    ],
    "litter": ('слушай',
               'послушай',
               'будет',
               'говорить',
               'хочу',
               'хочется',
               'что-то',
               'слушай',
               'пожалуйста',
               'можно',
               'можешь',
               'ка',
               "ну",
               'сейчас',
               'нынче',
               'да',
               'ладно',
               'если',
               'скажи',
               'поведай',
               'расскажи',
               'если',
               'подскажи', ),
    'reply_for_name': ('ты еще помнишь моё имя', 'я тут', 'я слушаю', 'слушаю внимательно',
                       'говори уже', 'да, это моё имя'),
    'mood': {
        2: ('просто замечательно', 'просто великолепно', 'супер'),
        1: ('очень хорошо', 'прекрасно', 'отлично'),
        0: ('ничего', 'нормально', 'не жалуюсь'),
        -1: ('плохо', 'отвратительно', 'не очень'),
    },
    'wiki': ('кто такой', 'кто такая', 'кто это', 'что такое', 'что за'),
    'umlaut': {'а́': 'а', 'у́': 'у', 'е́́': 'е', 'о́́́': 'о', 'и́́́́': 'и', 'я́́́́': 'я'},
    'eng_nouns': ['youtube', 'google', 'player']
}


def words_in_phrase(tuple1, phrase):
    for word in tuple(tuple1):
        if word in phrase:
            return word

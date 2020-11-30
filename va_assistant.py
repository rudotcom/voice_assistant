from datetime import datetime


class VoiceAssistant:
    """
    Настройки голосового ассистента
    """
    name = "мурзилка"
    recognition_mode = "online"
    birthday = datetime(2020, 11, 24, 23, 54, 22)
    sex = "female"
    recognition_language = "ru-RU"
    speech_voice = 3  # голосовой движок
    speech_language = "ru"
    speech_rate = 130  # скорость речи 140 самый норм
    speech_volume = 1  # громкость (0-1)
    last_input = 0
    last_intent = ''
    last_action = ''
    last_speech = ''
    mood = 0


CONFIG = {
    'intents': {
        'abilities': {
            'requests': ['что ты умеешь', 'твои способности', 'что ты можешь', 'что ты знаешь'],
            'responses': ['я умею отвечать кто такой и что такое, \
                          говорить время, \
                          включать радио и музыку, \
                          говорить погоду в любом месте на земле, \
                          искать в яндэксе, гугле, ютубе и википедии, \
                          знаю свой возраст, могу повторять за тобой. \
                          Могу узнать курс доллара или биткоина. \
                          Ты меня не обижай'],
        },
        'hello': {
            'requests': ['привет', 'добрый день', 'здравствуй', 'доброе утро', 'добрый вечер'],
            'responses': ['Привет, босс', 'давай говори чего хочешь'],
        },
        'stop': {
            'requests': ['помолчи', 'не подслушивай', 'тихо', 'потеряйся',
                         'пока', 'до свидания', 'прощай', 'спокойной ночи'],
            'responses': ['молчу', 'Счаст ливо', 'Еще увидимся', 'Если что я тут'],
            'actions': {'': 'stop'}
        },
        'die': {
            'requests': ['умри', 'сдохни'],
            'responses': ['увидимся в следующей жизни', 'Если что, знаешь где меня искать', 'пока-пока'],
            'actions': {'': 'die'}
        },
        'name': {
            'requests': ['как твоё имя', 'как тебя зовут'],
            'responses': ['меня зовут Мурзилка'],
        },
        'think': {
            'requests': ['думаешь', 'подумай', 'думать'],
            'responses': ['я еще не думаю', 'я пока не умею думать', 'думать это твоя работа'],
        },
        'uwhere': {
            'requests': ['ты где', 'куда подевалась', 'ты тут', 'почему не отвечаешь'],
            'responses': ['я тут, ты меня спрашиваешь, что-ли?', 'тута я', 'вот я', 'отвлеклася немного'],
        },
        'abuse': {
            'requests': ['плохо', 'нехорошо', 'нехорошая', 'дура', 'коза', 'бестолковая',
                         'заткнись', 'задолбала', 'уродина', "****"],
            'responses': ['на себя посмотри', 'а чё сразу ругаться та', 'ну обидно же',
                          'за что?', 'я тебя запомню!', 'нормально же общались', 'фак ю вэри мач'],
            'actions': {'': 'mood_down'},
        },
        'praise': {
            'requests': ['красава', 'молодец', 'хорошо', 'отлично', 'хороший', 'приятно поговорить',
                         'спасибо', 'благодарю', 'прикольно', 'умница', 'замечательно', 'супер'],
            'responses': ['спасибо', 'мне очень приятно', 'стараюсь'],
            'actions': {'': 'mood_up'},
        },
        'mood': {
            'requests': ['как настроение', 'как дела', 'как себя чувствуешь'],
            'responses': [''],
            'actions': {'': 'my_mood'},
        },
        'ctime': {
            'requests': ['текущее время', 'сколько время', 'сколько времени', 'который час'],
            'responses': [''],
            'actions': {'время': 'ctime'}
        },
        'age': {
            'requests': ['сколько тебе лет', 'твой возраст'],
            'responses': ['я еще молода'],
            'actions': {'возраст лет': 'my_age'}
        },
        'whois': {
            'requests': ['что такое', 'кто такой'],
            'responses': [''],
            'actions': {'такое': 'wikipedia'}
        },
        'translate': {
            'requests': ['переведи', 'как будет по-английски'],
            'responses': [''],
            'actions': {'переведи': 'translate'}
        },
        'music_off': {
            'requests': ['выключи плеер', 'выключи радио'],
            'responses': ['выключаю', 'как скажешь', 'хорошо', 'ладно', ''],
            'actions': {'выключи', 'kill_aimp'}
        },
        'music': {
            'requests': ['включи радио', 'послушать радио', 'послушать музыку', 'включи музыку', 'хочу послушать'],
            'responses': ['включаю', 'как скажешь', 'сама с удовольствием послушаю', 'хорошо', 'а га', ''],
            'actions': {
                'like fm': 'radio_like_fm',
                'лайк фм': 'radio_like_fm',
                'офис lounge': 'radio_office_lounge',
                'офис лаунж': 'radio_office_lounge',
                'office lounge': 'radio_office_lounge',
                'плейлист чилаут': 'playlist_chillout',
                'чилстеп': 'radio_chillstep',
                'chillstep': 'radio_chillstep',
                'чипльдук': 'radio_chip',
                'мою музыку': 'music_my',
                'музыку для дыхания': 'music_my_breathe',
            },
            'spec': ['уточни', 'что ты хочешь послушать', 'что именно', 'а конкретнее']
        },
        'browse': {
            'requests': ['открой'],
            'responses': ['открываю', 'как скажешь', 'интересно что же там', ],
            'actions': {
                'яндекс музыку': 'music_yandex',
            }
        },
        'start': {
            'requests': ['открой программу'],
            'responses': ['открываю', 'есть', ],
            'actions': {
                'notepad': 'notepad',
            }
        },
        'weather': {
            'requests': ['какая погода', 'погода', 'сколько градусов', 'на улице', 'холодно',
                         'тепло', 'что с погодой', 'завтра погода'],
            'responses': [''],
            'actions': {'': 'weather', }
        },
        'usd': {
            'requests': ['курс доллара', 'почем доллар'],
            'responses': [''],
            'actions': {'': 'usd', }
        },
        'btc': {
            'requests': ['курс биткоина', 'почем биткоин', 'курс битка', 'почем биток', 'bitcoin'],
            'responses': [''],
            'actions': {'': 'btc', }
        },
        'repeat': {
            'requests': ['повтори', 'еще раз', 'что ты говоришь'],
            'responses': [''],
            'actions': {'': 'repeat', 'помедленнее': 'repeat_slow'},
        },
        'repeat_after_me': {
            'requests': ['повтори за мной', 'повторяй за мной', 'произнеси'],
            'responses': [''],
            'actions': {'': 'repeat_after_me'}
        },
        'find': {
            'requests': ['найди', 'спроси у', 'загугли', 'поищи'],
            'responses': ['пошла искать', 'уже ищу', 'секундочку', 'это где-то здесь', 'что-то нашла'],
            'actions': {
                'яндексе': 'browse_yandex',
                'википедии': 'wikipedia',
                'гугла': 'browse_google',
                'загугли': 'browse_google',
                'youtube': 'youtube',
                'ютюбе': 'youtube',
            }
        },
    },
    'calculate': {
        'requests': ['посчитай', 'сколько будет'],
        'responses': ['Я только учусь считать'],
        # 'actions': {'': 'calculate', }
    },
    'failure_phrases': [
        'Вот это сейчас что было?',
        'Что-то не понятно',
        'А можно как-то попроще выразиться?',
        'К сожалению, я не смогу помочь вам с этим вопросом',
        'Слишком сложно для меня',
        'Здесь наши полномочия всё',
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
    "tbr": (
        'будет',
        'можешь сказать',
        'говорю',
        'хочу',
        'хочется',
        'что-то',
        'скажи',
        'расскажи',
        'покажи',
        'слушай',
        'пожалуйста',
        'если можно',
        'если можешь',
        'ка мне',
        'потому что',
        "ну",
        'сейчас',
        'где',
        'нынче',
        'да ладно'
    ),
    'alias': ('мурзилка', 'морозилка'),
    'reply_for_name': ('ты еще помнишь моё имя', 'я тут', 'я слушаю', 'слушаю внимательно',
                       'говори уже', 'да, это моё имя'),

    'mood': {
        2: ('просто замечательно', 'просто великолепно', 'супер'),
        1: ('очень хорошо', 'прекрасно', 'отлично'),
        0: ('ничего', 'нормально', 'не жалуюсь'),
        -1: ('плохо', 'отвратительно', 'не очень'),
    },
    'whazzup': {
        'offline': ' работает в оф лайн режиме. Поэтому говори очень разборчиво',
        'online': ' слушает',
    }
}


class Context:
    intent = ''
    action = ''
    address = ''
    imperative = ''
    target = ''  # если в intent есть фразы 'spec' значит target нужен, и фразы использются для его запроса
    location = ''
    adverb = ''

    def new_intent(self, intent):
        self.intent = intent

    def new_action(self, action, target):
        self.action = action
        self.target = target

    def normal_phrase(self,):
        pass
from datetime import datetime
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


class VoiceAssistant:
    """ Настройки голосового ассистента """
    name = 'мурзилка'
    alias = ('мурзилка', 'морозилка')
    birthday = datetime(2020, 11, 24, 23, 54, 22)

    def __init__(self):
        self.recognition_mode = "online"
        self.sex = "female"
        self.recognition_language = "ru-RU"
        self.speech_voice = 3  # голосовой движок
        self.speech_language = "ru"
        self.speech_rate = 130  # скорость речи 140 самый норм
        self.speech_volume = 1  # громкость (0-1)
        self.mood = 0


class Context:

    def __init__(self):
        self.imperative = None
        self.tool = None
        self.target = None
        self.adverb = None
        self.addressee = None
        self.text = None

    def context_by_phrase(self, phrase):
        target_where = prep = imperative = imperative_word = \
                        tool = target = addressee = adverb = ''
        """ сначала раскладываем на блоки """
        for word in phrase.split():
            p = morph.parse(word)[0]
            if word in CONFIG['litter']:
                # удаляем все бессмысленные словосочетания
                phrase = phrase.replace(word, "").strip()
            elif p.tag.mood == 'impr':  # императив
                imperative_word = word
                imperative = p[2]
            elif 'LATN' in p.tag:
                target = ' '.join([target, word])
            elif 'NUMB' in p.tag:
                target = ' '.join([target, word])
            elif p.tag.POS == 'PREP':
                prep = word
            elif p.tag.POS == 'NOUN':
                noun = ' '.join([prep, word])
                prep = ''
                if noun in CONFIG['tool']:
                    tool = ' '.join([tool, noun])
                elif p.tag.case in ('accs', 'gent', 'nomn'):
                    """винит, родит, иминит Кого? Чего? Кого? Что? Кому? Чему?"""
                    target = ' '.join([target, p[2]])
                elif p.tag.case == 'loct':
                    """предложный падеж - где?"""
                    target_where = ' '.join([tool, noun])
                elif p.tag.case == 'datv':
                    """дат Кому? Чему?"""
                    addressee = ' '.join([addressee, p[2]])
                    phrase = phrase.replace(word, '')
            elif p.tag.POS == 'ADVB':
                adverb = p[2]
            elif p.tag.POS in ('ADJF', 'ADJS'):
                pass
        target = ' '.join([target, target_where])

        """ сначала находим вопросительные слова interrogative, значит императив "найти"
        или узнать """
        """ потом находим имератив imperative"""
        if imperative in CONFIG['imper_find']:  # значит намерение искать
            phrase = phrase.replace(imperative_word, '')
            imperative = 'найти'
            target = phrase.replace(tool, '')
        else:
            for interrog in CONFIG['interrogative']:
                if interrog in phrase:
                    imperative = 'найти'
                    if tool:
                        target = phrase.partition(tool)[2]
                    else:
                        if interrog in ['где', 'где находится']:
                            tool = 'яндекс карты'
                        else:
                            tool = 'wikipedia'
                        target = phrase.replace(interrog, '')
                    phrase = phrase.replace(interrog, '')
                    target = target.replace(addressee, '')
                    break
                else:
                    for quiz in CONFIG['quiz']:
                        if quiz in phrase:
                            imperative = 'узнать'
                            target = phrase
                            tool = ''
                            break
        target = target.replace(adverb, '')
        self.addressee = addressee
        if imperative:
            self.imperative = imperative
        if target:
            self.target = target
        self.tool = tool
        self.adverb = adverb
        self.text = phrase


def clear_wiki(text):
    for x in CONFIG['umlaut']:
        text = text.replace(x, CONFIG['umlaut'][x])
    return text


assistant = VoiceAssistant()
context = Context()

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
            'responses': ['я еще не думаю', 'я пока не умею думать', 'думать это твоя работа',
                          'у меня нет такой функции'
                          ],
        },
        'uwhere': {
            'requests': ['ты где', 'куда подевалась', 'ты тут', 'почему не отвечаешь'],
            'responses': ['я тут, ты меня спрашиваешь, что-ли?', 'тута я', 'вот я', 'отвлеклася немного'],
        },
        'abuse': {
            'requests': ['плохо', 'нехорошо', 'нехорошая', 'дура', 'коза', 'бестолковая',
                         'заткнись', 'задолбала', 'уродина', "****"],
            'responses': ['на себя посмотри', 'а чё сразу ругаться та', 'ну обидно же',
                          'за что', 'я тебя запомню!', 'нормально же общались', 'фак ю вэри мач'],
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
            'requests': ['включить', 'включи радио', 'включи музыку', 'послушать радио', 'послушать музыку',
                         'послушать', 'включи'],
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
                'телеграм': 'start_telegram',
                'whatsapp': 'start_whatsapp'
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
            'requests': ['найди', 'спроси у', 'загугли', 'поищи', 'найти'],
            'responses': ['пошла искать', 'уже ищу', 'секундочку', 'это где-то здесь', 'что-то нашла'],
            'actions': {
                'яндексе': 'browse_yandex',
                'википедии': 'wikipedia',
                'гугла': 'browse_google',
                'загугли': 'browse_google',
                'youtube': 'youtube',
                'ютюбе': 'youtube',
                'где': 'yandex_maps',
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
    "litter": (
        'слушай',
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
        'подскажи',
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
    },
    'imper_find': ('найти', 'поискать', 'искать', 'показать'),
    'tool': ('в youtube', 'в google', 'в yandex', 'в ютубе', 'в гугле', 'в яндексе', 'в википедии', 'в маркете'),
    'quiz': ('почему', 'зачем', 'когда', 'сколько', 'какая', 'какой', 'как',),
    'interrogative': ('где находится', 'где', 'кто такой', 'кто такая', 'кто это', 'что такое',),
    'umlaut': {'а́': 'а', 'у́': 'у', 'е́́': 'е', 'о́́́': 'о', 'и́́́́': 'и', 'я́́́́': 'я'},
}

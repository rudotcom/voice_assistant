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
        self.imperative = ''
        self.tool = ''
        self.target = ''
        self.adverb = ''
        self.addressee = ''
        self.text = ''

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
            elif p.tag.POS == 'PREP':
                prep = word
            elif p.tag.POS == 'NOUN' or word in CONFIG['eng_nouns']:
                noun = ' '.join([prep, word])
                prep = ''
                if noun in CONFIG['intents']['find']['actions'].keys():
                    tool = ' '.join([tool, noun])
                elif p.tag.case in ('accs', 'gent', 'nomn'):
                    """винит, родит, иминит Кого? Чего? Кого? Что? Кому? Чему?"""
                    target = ' '.join([target, p[2]])
                elif p.tag.case == 'loct':
                    """предложный падеж - где?"""
                    target_where = ' '.join([word, noun])
                elif p.tag.case == 'datv':
                    """дат Кому? Чему?"""
                    addressee = ' '.join([addressee, p[2]])
                    phrase = phrase.replace(word, '')

            elif 'LATN' in p.tag:
                target = ' '.join([target, word])
            elif 'NUMB' in p.tag:
                target = ' '.join([target, word])
            elif p.tag.POS == 'ADVB':
                adverb = p[2]
            elif p.tag.POS in ('ADJF', 'ADJS'):
                pass
        target = ' '.join([target, target_where])

        """ сначала находим имератив imperative"""
        if imperative in CONFIG['imper_find']:  # значит намерение искать
            phrase = phrase.replace(imperative_word, '')
            imperative = 'найти'
            target = phrase.replace(tool, '')
        else:
            """ потом находим вопросительные слова (wiki), значит императив "найти" """
            for interrog in CONFIG['wiki']:
                if interrog in phrase:
                    imperative = 'найти'
                    if tool:
                        target = phrase.partition(tool)[2]
                    else:
                        if interrog in ['где', 'где находится']:
                            tool = 'карта'
                        else:
                            tool = 'wikipedia'
                        target = phrase.replace(interrog, '')
                    phrase = phrase.replace(interrog, '')
                    target = target.replace(addressee, '')
                    break
                else:
                    """ потом находим вопросительные слова (quiz), значит императив узнать """
                    for quiz in CONFIG['quiz']:
                        if quiz in phrase:
                            imperative = 'узнать'
                            target = phrase.replace(quiz, '')
                            tool = ''
                            break
        target = target.replace(adverb, '')
        self.addressee = addressee.strip()
        if imperative:
            self.imperative = imperative
        if target:
            self.target = target.strip()
        self.tool = tool.strip()
        self.adverb = adverb.strip()
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
            'requests': ['помолчать', 'не подслушивать', 'тихо', 'потеряться',
                         'пока', 'до свидания', 'прощай', 'спокойной ночи'],
            'responses': ['молчу', 'Счаст ливо', 'Еще увидимся', 'Если что я тут'],
            'actions': {'': 'stop'}
        },
        'die': {
            'requests': ['умереть', 'сдохнуть'],
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
            'actions': {'': 'ctime'}
        },
        'age': {
            'requests': ['сколько тебе лет', 'твой возраст'],
            'responses': ['я еще молода'],
            'actions': {'': 'age'}
        },
        'whois': {
            'requests': ['что такое', 'кто такой'],
            'responses': [''],
            'actions': {'такое': 'wikipedia'}
        },
        'translate': {
            'requests': ['переведи', 'по-английски'],
            'responses': [''],
            'actions': {'': 'translate'}
        },
        'app_close': {
            'responses': ['выключаю', 'как скажешь', 'хорошо', 'ладно', ''],
            'actions': {'радио': 'AIMP.exe', 'player': 'AIMP.exe', 'музыка': 'AIMP.exe'}
        },
        'music': {
            'requests': ['радио', 'музыку', 'radio', 'playlist', 'плейлист', ],
            'responses': ['включаю', 'как скажешь', 'сама с удовольствием послушаю', 'хорошо', 'а га', '', ],
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
            'responses': ['открываю', 'как скажешь', 'интересно что же там', ],
            'actions': [
                'яндекс музыка',
                'telegram',
                'whatsapp',
                'браузер',
                'телеграмму',
                'калькулятор'
            ]
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
                # 'в яндекс музыке': 'yandex_music',
                'в яндексе': 'browse_yandex',
                'в википедии': 'wikipedia',
                'wikipedia': 'wikipedia',
                'в гугле': 'browse_google',
                'загуголь': 'browse_google',
                'в youtube': 'youtube',
                'карта': 'yandex_maps',
            }
        },
        'calculate': {
            'requests': ['посчитай', 'сколько будет'],
            'responses': ['Я только учусь считать'],
            'actions': {'': 'calculate', },
        },
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
    'quiz': ('почему', 'зачем', 'когда', 'сколько', 'какая', 'какой', 'как',),
    'wiki': ('где находится', 'где', 'кто такой', 'кто такая', 'кто это', 'что такое',),
    'umlaut': {'а́': 'а', 'у́': 'у', 'е́́': 'е', 'о́́́': 'о', 'и́́́́': 'и', 'я́́́́': 'я'},
    'eng_nouns': ['youtube', 'google', ]
}

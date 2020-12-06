import pymorphy2
import pyttsx3
import random
from datetime import datetime, timedelta
from va_voice_recognition import recognize_offline, recognize_online

tts = pyttsx3.init()
morph = pymorphy2.MorphAnalyzer()


class VoiceAssistant:
    """ Настройки голосового ассистента """
    name = 'мурзилка'
    alias = ('мурзилка', 'морозилка')
    birthday = datetime(2020, 11, 24, 23, 54, 22)
    sec_to_offline = 40
    last_active = datetime.now() - timedelta(seconds=sec_to_offline)
    last_speech = ''

    def __init__(self):
        self.recognition_mode = "offline"
        self.sex = "female"
        self.recognition_language = "ru-RU"
        self.speech_voice = 3  # голосовой движок
        self.speech_language = "ru"
        self.speech_rate = 130  # скорость речи 140 самый норм
        self.speech_volume = 1  # громкость (0-1)
        self.mood = 0

    def pays_attention(self, phrase):
        """ будет ли помощник слушать фразу?
        да, если он активен, либо его позвали по имени
        переходит в активный режим и возвращает boolean """
        if self.is_alert():
            return True
        elif phrase.startswith(self.alias):
            self.alert()
            return True
        else:
            return False

    def is_alert(self):
        """ помощник активен, т.к. время последнего отклика было меньше лимита sec_to_offline """
        alert = datetime.now() - self.last_active < timedelta(seconds=self.sec_to_offline)
        if not alert:
            self.sleep()
        return alert

    def alert(self):
        """ активация помощника: обновление времени последнего отклика и переход в активное состоятие из offline """
        self.last_active = datetime.now()
        if self.recognition_mode == 'offline':
            self.recognition_mode = 'online'
            self.speak(self.name + ' слушает')

    def sleep(self):
        """ переход в offline при истечении лимита прослушивания sec_to_offline """
        self.last_active = datetime.now() - timedelta(seconds=self.sec_to_offline)
        if self.recognition_mode == 'online':
            self.recognition_mode = 'offline'
            print('... went offline')

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
        """Воспроизведение текста голосом и вывод его в консоль"""
        if context.addressee:
            listen = random.choice(['слушай', 'тебе говорю', 'короче', 'прикинь', 'только вкинься'])
            what = ', '.join([context.addressee, listen, what, ])
        self.last_speech = what
        print(what)
        tts.say(what)
        tts.runAndWait()
        tts.stop()

    def recognize(self):
        """Выбор режима распознавания, запуск распознавания и возврат распознанной фразы """
        if self.recognition_mode == 'online':
            return recognize_online()
        else:
            return recognize_offline()

    def use_source(self):
        # TODO: забыл для чего метод, разобраться позже
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

    def i_cant(self):
        self.speak(random.choice(CONFIG['i_cant']))


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
               \ntext:\t{self.text} \
               \naction:\t{self.action}\n'.format(self=self)

    def phrase_morph_parse(self, phrase):
        prep = imperative = adj = action = reply = \
            source = subject = location = addressee = adverb = ''
        """ сначала раскладываем на морфемы """
        for word in phrase.split():
            p = morph.parse(word)[0]
            if word in CONFIG['litter']:
                # удаляем все бессмысленные словосочетания
                phrase = phrase.replace(word, "").strip()
            elif p.tag.POS in ['PRED', 'INTJ']:  # удаляем союзы, частицы, предикативы, междометия
                phrase = phrase.replace(word, "").strip()
            elif p.tag.mood == 'impr':  # выделяем императив в отдельный параметр контекста
                if p[2] in ['включить', 'выключить', 'открыть', 'закрыть', 'найти', 'поискать', 'повторять',
                            'спросить', 'произнести', 'пошукать']:
                    imperative = p[2]
                    phrase = phrase.replace(word, '').strip()
            elif p.tag.POS == 'PREP':
                prep = word
            elif p.tag.POS in ('ADJF', 'ADJS'):
                    adj = ' '.join([adj, p[2]])
            elif p.tag.POS == 'NOUN' or word in CONFIG['eng_nouns']:

                """ объединяем существительное с предстоящим предлогом и предстоящим прилагательным (местоим) """
                noun = ' '.join([prep, word])
                if noun in CONFIG['intents']['find']['sources'].keys():
                    """ если это слово содержится в источниках поиска, значит это - инструмент поиска source"""
                    source = ' '.join([source, noun]).strip()
                    phrase = phrase.replace(noun, '').strip()
                elif p.tag.case in ('accs', 'gent', 'nomn'):
                    """винит, родит, иминит Кого? Чего? Кого? Что? Кому? Чему?"""
                    if adj:
                        subject = ' '.join([adj, p[0]]).strip()
                    else:
                        subject = ' '.join([subject, p[0]]).strip()
                elif p.tag.case == 'loct':
                    """предложный падеж - где?"""
                    location = ' '.join([location, noun])
                elif p.tag.case == 'datv':
                    """дат Кому? Чему?"""
                    addressee = ' '.join([addressee, p[2]])
                    phrase = phrase.replace(word, '')
                prep = adj = ''  # эти предлог и прилагательные больше не будет относиться к другим существительным

            elif 'LATN' in p.tag:
                subject = ' '.join([subject, word])
            elif 'NUMB' in p.tag:
                subject = ' '.join([subject, word])
            elif p.tag.POS == 'ADVB':
                adverb = p[2]

        self.addressee = addressee.strip()
        self.action = action
        self.reply = reply
        self.imperative = imperative
        self.source = source.strip()
        self.subject = subject.strip()
        self.location = location
        self.adverb = adverb.strip()
        self.text = phrase

    def refresh(self, new):
        if new.subject:
            self.subject = new.subject
        if new.text:
            self.text = new.text
        if new.adverb:
            self.adverb = new.adverb
        if new.location:
            self.location = new.location
        if new.imperative:
            self.imperative = new.imperative
            self.source = new.source
            if new.action:
                self.action = new.action
            if new.reply:
                self.reply = new.reply


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
            'replies': ['на себя посмотри', 'а чё сразу ругаться та', 'ну обидно же', 'за что', 'я тебя запомню!',
                        'ну чё ты, нормально же общались', 'фак ю вэри мач', 'похоже это что-то обидное'],
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
        'turn_on': {
            'requests': ['радио', 'музыку', 'radio', 'playlist', 'плейлист', 'включить'],
            'replies': ['включаю', 'как скажешь', 'сама с удовольствием послушаю', 'хорошо', 'а га', '', ],
            'sources': {
                'радио чилаут': 'http://air2.radiorecord.ru:9003/chil_320',
                'радио like fm': 'http://ic7.101.ru:8000/a219',
                'радио лайк': 'http://ic7.101.ru:8000/a219',
                'радио офис lounge': 'http://ic7.101.ru:8000/a30',
                'радио офис лаунж': 'http://ic7.101.ru:8000/a30',
                'радио office lounge': 'http://ic7.101.ru:8000/a30',
                'playlist chill out': r'D:\Chillout.aimppl4',
                'плейлист чилаут': r'D:\Chillout.aimppl4',
                'радио чилстеп': 'http://ic5.101.ru:8000/a260',
                'радио chillstep': 'http://ic5.101.ru:8000/a260',
                'радио чипльдук': 'http://radio.4duk.ru/4duk256.mp3',
                'мой музыку': r'D:\2020',
                'музыка дыхание': r'D:\2020\Breathe',
            },
            'spec': ['что включить', 'что ты хочешь послушать', 'что именно', 'а конкретнее'],
            'not_exists': ['у меня такого нет', 'такого нет, выбери другое']
        },
        'find': {
            'requests': ['найти', 'спросить у', 'загуглить', 'поискать', 'пошукать'],
            'replies': ['пошла искать', 'уже ищу', 'секундочку', 'это где-то здесь', 'что-то нашла'],
            'sources': {
                'в яндекс музыке': 'yandex_music',
                'в яндексе': 'browse_yandex',
                'в википедии': 'wikipedia',
                'в гугле': 'browse_google',
                'загуголь': 'browse_google',
                'в youtube': 'youtube',
            },
            'spec': ['что где найти', 'уточни что и где искать', 'что именно', 'а конкретнее'],
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
            'spec': ['что открыть', 'что именно', 'а конкретнее'],
        },
        'repeat': {
            'requests': ['повтори', 'еще раз', 'что ты говоришь'],
            'replies': [''],
            'actions': {'помедленнее': 'repeat_slow', '': 'repeat', },
        },
        'repeat_after_me': {
            'requests': ['повтори за мной', 'произнеси'],
            'actions': {'': 'repeat_after_me'}
        },
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
            'requests': ['настроение', 'дела', ' себя чувствуешь'],
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
        },
        'find_out_where': {
            'requests': ['где находится', 'где', ],
            'replies': ['сейчас поищем', 'где-то здесь', ],
            'action': 'yandex_maps',
        },
        'find_out_wiki': {
            'requests': ['кто такой', 'кто такая', 'что такое', 'что есть', 'кто', 'что', ],
            'actions': 'wikipedia',
        },
    },
    'i_cant': ['а самому слабоо?', 'меня этому не обучали', 'может когда-нибудь научусь', 'попробуй сам', ],
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
               'подскажи',),
    'reply_for_name': ('ты еще помнишь моё имя', 'я тут', 'я слушаю', 'слушаю внимательно',
                       'говори уже', 'да, это моё имя'),
    'mood': {
        2: ('просто замечательно', 'просто великолепно', 'супер'),
        1: ('очень хорошо', 'прекрасно', 'отлично'),
        0: ('ничего', 'нормально', 'не жалуюсь'),
        -1: ('плохо', 'отвратительно', 'не очень'),
    },
    'umlaut': {'а́': 'а', 'у́': 'у', 'е́́': 'е', '́́е': 'е', 'о́́́': 'о', 'и́́́́': 'и', 'я́́́́': 'я'},
    'eng_nouns': ['youtube', 'google', 'player']
}



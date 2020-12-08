import pymorphy2
import pyttsx3
import random
from main import assistant, new_context, context
from datetime import datetime, timedelta
from va_voice_recognition import recognize_offline, recognize_online
from va_config import CONFIG

tts = pyttsx3.init()
morph = pymorphy2.MorphAnalyzer()


class VoiceAssistant:
    """ Класс голосового помощника
    Именование помощника, слова, на которые откликается"""
    name = 'мурзилка'
    alias = ('мурзилка', 'морозилка')
    birthday = datetime(2020, 11, 24, 23, 54, 22)
    sec_to_offline = 60
    last_active = datetime.now() - timedelta(seconds=sec_to_offline)
    last_speech = ''

    def __init__(self):
        self.setup_voice()  # выбор голосового движка и его параметров
        self.alert()  # для запуска в активном режиме
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
        переходит в активный режим и возвращает boolean
        сохраняем фразу в новый контекст"""
        if self.is_alert():
            new_context.phrase = phrase
            return True
        elif phrase.startswith(self.alias):
            new_context.phrase = remove_alias(phrase)
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
            if not new_context.phrase:
                self.speak(self.name + ' слушает')

    def sleep(self):
        """ переход в offline при истечении лимита прослушивания sec_to_offline """
        self.last_active = datetime.now() - timedelta(seconds=self.sec_to_offline)
        if self.recognition_mode == 'online':
            self.recognition_mode = 'offline'
            print('... went offline')

    def setup_voice(self, lang="ru", rate=130):
        """ Установка параметров голосового движка """
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
            listen = random.choice(CONFIG['address'])
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

    def fail(self):
        self.speak(random.choice(CONFIG['failure_phrases']))

    def i_cant(self):
        self.speak(random.choice(CONFIG['i_cant']))


class Context:
    """ Класс объектов для сохранения и обновления контекста """
    phrase = ''

    def __init__(self):
        self.imperative = ''
        self.source = ''
        self.subject = ''
        self.location = ''
        self.adverb = ''
        self.addressee = ''
        self.text = ''
        self.action = ''
        self.intent = ''

    def __str__(self):
        # для отладки
        return 'phrase:\t{self.phrase} \
               \nimperative:\t{self.imperative} \
               \nsource:\t\t{self.source} \
               \nsubject:\t{self.subject} \
               \nlocation:\t{self.location} \
               \nadverb:\t\t{self.adverb} \
               \naddressee:\t{self.addressee} \
               \ntext:\t{self.text} \
               \naction:\t{self.action} \
               \nintent:\t{self.intent}'.format(self=self)

    def phrase_morph_parse(self):
        phrase = self.phrase
        prep = imperative = adj = action = \
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
                if p[2] in CONFIG['imperatives']:
                    imperative = p[2]
                    phrase = phrase.replace(word, '').strip()
            elif p.tag.POS == 'PREP':
                prep = word
            elif p.tag.POS in ('ADJF', 'ADJS'):
                adj = ' '.join([adj, p[2]])
            elif p.tag.POS == 'NOUN' or word in CONFIG['eng_nouns']:

                """ объединяем существительное с предстоящим предлогом и предстоящим прилагательным (местоим) """
                noun = ' '.join([prep, word])
                if noun in CONFIG['intents']['find']['targets'].keys():
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
                    """предложный падеж - где? - location """
                    location = ' '.join([location, noun])
                elif p.tag.case == 'datv':
                    """дат Кому? Чему? - addressee """
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
        self.imperative = imperative
        self.source = source.strip()
        self.subject = subject.strip()
        self.location = location
        self.adverb = adverb.strip()
        self.text = phrase

    def refresh(self, new):
        """ Принимает параметры нового контекста для установки в текущем """
        self.addressee = new.addressee
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


def remove_alias(voice_text):
    for alias in assistant.alias:
        return voice_text.replace(alias, "", 1).strip()

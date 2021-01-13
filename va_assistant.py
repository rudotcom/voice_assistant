import sys
import threading
import time
import pytils
import pyglet
import pymorphy2
import pyttsx3
import random
from datetime import datetime, timedelta
from fuzzywuzzy import process
import warnings

from va_gui import girl
from va_voice_recognition import recognize_offline, recognize_online
from va_config import CONFIG

warnings.filterwarnings("ignore")
morph = pymorphy2.MorphAnalyzer()


def correct_numerals(phrase):
    """ согласование рода числительных """
    new_phrase = []
    py_gen = 1
    phrase = phrase.split(' ')
    while phrase:
        word = phrase.pop(-1)
        p = morph.parse(word)[0]
        if 'NUMB' in p.tag:
            minus = 'минус ' if int(word) < 0 else ''
            new_phrase.append(minus + pytils.numeral.sum_string(abs(int(word)), py_gen))
        else:
            new_phrase.append(word)
            if 'femn' in p.tag:
                py_gen = pytils.numeral.FEMALE
            else:
                py_gen = pytils.numeral.MALE
    return ' '.join(new_phrase[::-1])


def numerals_reconciliation(phrase):
    """ согласование существительных с числительными, стоящими перед ними """
    result = ''

    phrases = phrase.strip().split('\n')
    for phrase in phrases:
        numeral = sign = ''
        new_phrase = []
        for word in phrase.split(' '):
            if word and word[-1] in ',.!&:@#$%^&*()_+':
                word, sign = word[0:-1], word[-1]
            p = morph.parse(word)[0]
            # print(p[2], p.tag)
            if numeral:
                word = str(p.make_agree_with_number(abs(int(numeral))).word)
            if 'NUMB' in p.tag:
                numeral = word
            elif not p.tag.POS or 'NOUN' in p.tag.POS:
                numeral = ''
            new_phrase.append(word + sign)
            sign = ''
        phrase = ' '.join(new_phrase)

        result = '\n'.join([result, phrase])

    return result


def redneck_what(what):
    phrase = ''
    for word in what.split(' '):
        if morph.parse(word)[0].tag.POS in ['PREP', 'NUMR']:
            phrase = ' '.join([phrase, word])
        else:
            phrase = ' '.join(
                [phrase, word, random.choice(CONFIG['redneck'] + [''] * int(len(CONFIG['redneck']) * 3))])
    return phrase


class VoiceAssistant:
    """ Настройки голосового ассистента """
    name = 'Мурзилка '
    alias = ('мурзилка', 'морозилка', 'узелка', 'развилка', 'мурка')
    birthday = datetime(2020, 11, 24, 23, 54, 22)
    sec_to_offline = 60
    last_active = datetime.now() - timedelta(seconds=sec_to_offline)
    last_speech = ''

    def __init__(self):
        self.active = False
        self.recognition_mode = "offline"
        self.sex = "female"
        self.recognition_language = "ru-RU"
        self.speech_voice = 3  # голосовой движок
        self.speech_language = "ru"
        self.speech_rate = 130  # скорость речи 140 самый норм
        self.speech_volume = 1  # громкость (0-1)
        self.mood = 0  # настроение помощника
        self.lock = threading.Lock()  # взаимоблокировка отдельных голосовых потоков
        self.redneck = False  # режим пацана
        self.intent = None
        girl.root.title(self.name)

    def pays_attention(self, phrase):
        """ будет ли помощник слушать фразу?
        да, если он активен, либо его позвали по имени
        переходит в активный режим и возвращает boolean
        сохраняем фразу в новый контекст"""
        if self.is_alert():
            context.phrase = phrase
            return True
        elif phrase.startswith(self.alias):
            context.phrase = remove_alias(phrase)
            self.alert()
            return True
        else:
            return False

    def is_alert(self):
        """ помощник активен, т.к. время последнего отклика было меньше лимита sec_to_offline """
        alert = self.active or datetime.now() - self.last_active < timedelta(seconds=self.sec_to_offline)
        if not alert:
            self.sleep()
        return alert

    def alert(self):
        """ активация помощника: обновление времени последнего отклика и переход в активное состоятие из offline """
        self.last_active = datetime.now()
        if self.recognition_mode == 'offline':
            self.recognition_mode = 'online'
            if not context.phrase:
                self.say(random.choice(CONFIG['im_ready']))

    def sleep(self):
        """ переход в offline, active = False """
        self.last_active = datetime.now() - timedelta(seconds=self.sec_to_offline)
        self.active = False
        if self.recognition_mode == 'online':
            self.recognition_mode = 'offline'
            # print('... 🚬 ...')

    def speak(self, what, lang='ru', rate=130, correct=False):
        if not what:
            return
        if self.redneck:
            what = redneck_what(what)
        """Установка параметров голосового движка"""
        self.speech_language = lang
        tts = pyttsx3.init()
        voices = tts.getProperty("voices")
        if self.mood < 0:
            rate = 90
            tts.setProperty('volume', 0.8)
        tts.setProperty('rate', rate)

        if assistant.speech_language == "en":
            assistant.recognition_language = "en-US"
            if assistant.sex == "female":
                # Microsoft Zira Desktop - English (United States)
                tts.setProperty("voice", voices[1].id)
            else:
                # Microsoft David Desktop - English (United States)
                tts.setProperty("voice", voices[2].id)
        else:
            tts.setProperty("voice", voices[assistant.speech_voice].id)

        """Воспроизведение текста голосом и вывод его в консоль"""
        if context.addressee:
            listen = random.choice(CONFIG['address'])
            what = ', '.join([context.addressee, listen, what, ])
        # if context != old_context:
        assistant.play_wav('inhale4')
        time.sleep(0.4)
        self.last_speech = what
        if not correct:
            what = numerals_reconciliation(what).strip()
        # print('🔊', what)
        girl.type(what)
        what = correct_numerals(what)
        tts.say(what)
        tts.runAndWait()
        tts.stop()

    def say(self, what, lang='ru', rate=130, correct=False):
        self.lock.acquire()
        thread1 = threading.Thread(target=self.speak, kwargs={'what': what, 'lang': lang,
                                                              'rate': rate, 'correct': correct, })
        thread1.start()
        thread1.join()
        self.lock.release()

    @staticmethod
    def play_wav(src):
        wav_file = sys.path[0] + '\\static\\wav\\' + src + '.wav'
        try:
            alert = pyglet.media.load(wav_file)
            alert.play()
        except FileNotFoundError:
            print('Файл не найден:', wav_file)
        # time.sleep(alert.duration - overlap)

    def recognize(self):
        """Выбор режима распознавания, запуск распознавания и возврат распознанной фразы """
        if self.is_alert():
            return recognize_online()
        else:
            return recognize_offline()

    def fail(self, echo=''):
        self.play_wav('decay-475')
        if echo:
            self.say(echo, rate=280)
        self.say(random.choice(CONFIG['failure_phrases']))

    def i_cant(self):
        self.say(random.choice(CONFIG['i_cant']))


class Context:
    phrase = ''

    def __init__(self):
        self.imperative = ''
        self.intent = None
        self.target = ''
        self.subject = ''
        self.target_value = ''
        self.subject_value = ''
        self.location = ''
        self.adverb = ''
        self.addressee = ''
        self.text = ''
        self.persist = False

    def phrase_morph_parse(self):
        phrase = self.phrase
        prep = imperative = adj = \
            target = subject = location = addressee = adverb = ''
        """ сначала раскладываем на морфемы """
        for word in phrase.split():
            p = morph.parse(word)[0]
            if word in CONFIG['litter']:
                # удаляем все бессмысленные словосочетания
                phrase = phrase.replace(word, "").strip()
            elif p.tag.POS in ['PRED', 'INTJ']:  # удаляем союзы, частицы, предикативы, междометия
                phrase = phrase.replace(word, "").strip()
            elif p.tag.mood == 'impr':  # выделяем императив в отдельный параметр контекста
                # if p[2] in ['включить', 'выключить', 'открыть', 'закрыть', 'найти', 'поискать', 'повторять',
                #             'спросить', 'произнести', 'пошукать']:
                imperative = p[2]
                phrase = phrase.replace(word, '').strip()
            elif p.tag.POS == 'PREP':
                prep = word
            elif p.tag.POS in ('ADJF', 'ADJS'):
                adj = ' '.join([adj, p[2]])
            elif p.tag.POS == 'NOUN' or word in CONFIG['eng_nouns']:

                """ объединяем существительное с предстоящим предлогом и предстоящим прилагательным (местоим) """
                noun = ' '.join([prep, word])
                if noun in CONFIG['intents']['find']['target'].keys():
                    """ если это слово содержится в источниках поиска, значит это - инструмент поиска target"""
                    target = ' '.join([target, noun]).strip()
                    phrase = phrase.replace(noun, '').strip()
                elif p[2] in CONFIG['nearest_day'] + CONFIG['weekday'] + ['выходной']:
                    adverb = noun
                elif p.tag.case in ('accs', 'gent', 'nomn'):
                    """винит, родит, иминит Кого? Чего? Кого? Что? Кому? Чему?"""
                    if adj:
                        subject = ' '.join([adj, p[0]]).strip()
                    else:
                        subject = ' '.join([subject, p[0]]).strip()
                elif p.tag.case in ['loct', 'datv']:
                    """предложный падеж - где?"""
                    if 'скажи' in phrase:
                        addressee = ' '.join([addressee, p[2]])
                    else:
                        location = ' '.join([location, noun])
                    phrase = phrase.replace(word, '')
                prep = adj = ''  # эти предлог и прилагательные больше не будет относиться к другим существительным

            elif prep in ['в', 'на', 'во']:
                location = ' '.join([prep, word])

            elif 'LATN' in p.tag:
                subject = ' '.join([subject, word])
            elif 'NUMB' in p.tag:
                subject = ' '.join([subject, word])
            elif p.tag.POS == 'ADVB':
                adverb = p[2]

        if not self.persist:
            # если контекст неустойчив (не требует уточнений), очищаем его.
            self.__init__()
        self.addressee = addressee.strip()
        self.text = phrase
        self.imperative = imperative
        if target:
            self.target = target.strip()
        if subject:
            self.subject = subject.strip()
        if location:
            self.location = location
        if adverb:
            self.adverb = adverb.strip()

    def adopt_intent(self, other):
        if isinstance(other, Context):
            # Если контекст сохраняется, но нового интента нет, контекст дополняется старым контекстом
            if context.persist:
                if not self.intent:
                    self.intent = other.intent
                    # print('ctx: prev intent:', other.intent)
                if not self.subject:
                    self.subject = other.subject
                    # print('ctx: prev subject:', other.subject)
                if not self.target:
                    self.target = other.target
                    # print('ctx: prev target:', other.target)
                if not self.adverb:
                    self.adverb = other.adverb
                    # print('ctx: prev adverb:', other.adverb)
                if not self.location:
                    self.location = other.location
                    # print('ctx: prev location:', other.location)
        else:
            return NotImplemented

    def get_subject_value(self):
        # Возвращаем False если чего-то не хватает
        config = CONFIG['intents'][self.intent]
        if 'subject' in config.keys():
            if self.subject:
                # Блиайшее по Левенштейну значение subject, совпадение не менее 90%
                levenshtein = process.extractOne(self.subject, config['subject'].keys())
                if levenshtein[1] > 90:
                    self.subject_value = config['subject'][levenshtein[0]]
                    self.text = context.text.replace(self.subject, '').strip()
                    return True
                elif 'not_exists' in config:
                    assistant.say(random.choice((config['not_exists'])))
                    return False
            else:
                if not context.subject and 'subject_missing' in config:
                    assistant.say(random.choice(config['subject_missing']))
                    return False
        else:
            return True

    def get_target_value(self):
        # Возвращаем False если чего-то не хватает
        config = CONFIG['intents'][self.intent]
        if 'target' in config.keys():
            # Блиайшее по Левенштейну значение target, совпадение не менее 90%
            levenshtein = process.extractOne(self.target, config['target'].keys())
            if levenshtein[1] > 90:
                self.target_value = config['target'][levenshtein[0]]
                self.text = context.text.replace(self.target, '').strip()
                return True
            elif 'target_missing' in config:
                assistant.say(random.choice(config['target_missing']))
                return False
        else:
            return True

    def empty(self):
        self.__init__()

    def __eq__(self, other):
        # сравнение двух контекстов
        if isinstance(other, Context):
            return (self.intent == other.intent and
                    self.subject == other.subject and
                    self.adverb == other.adverb and
                    self.location == other.location and
                    self.target == other.target)
        # иначе возвращаем NotImplemented
        return NotImplemented


assistant = VoiceAssistant()
old_context = Context()
context = Context()


def remove_alias(voice_text):
    for alias in assistant.alias:
        return voice_text.replace(alias, "", 1).strip()

""" Дыхательная тренировка по методу Вима Хофа. Несколько раундов по 30 вдохов. Количество раундов принимается от
голосового помощника командой Давай подышим 4 раунда (по умолчанию 3 раунда) """
import sys
import time
from math import sqrt
import APIKeysLocal  # локально хранятся ключи и пароли
import pymorphy2
import pyglet
import pymysql
import pyttsx3
import threading
import warnings
import pytils
from pynput import mouse


warnings.filterwarnings("ignore")

""" Количество раундов, вдохов в раунде, задержка дыхания на вдохе"""


def on_move(x, y):
    cursor = workout.mouse_coords
    if cursor == (0, 0):
        workout.mouse_coords = (x, y)
        return True
    if int(sqrt(abs(cursor[0] - x) + abs(cursor[1] - y))) > 20:
        return False


def on_click(x, y, button, pressed):
    if not pressed:
        workout.statistics()
        exit(0)


def play_wav(src):
    wav_file = sys.path[0] + '\\src\\wav\\' + src + '.wav'
    try:
        wav = pyglet.media.load(wav_file)
        wav.play()
        time.sleep(wav.duration)
    except FileNotFoundError:
        print('Файл не найден:', wav_file)


def play_wav_inline(src):
    wav_file = sys.path[0] + '\\src\\wav\\' + src + '.wav'
    try:
        wav = pyglet.media.load(wav_file)
        wav.play()
    except FileNotFoundError:
        print('Файл не найден:', wav_file)


def correct_numerals(phrase, morph=pymorphy2.MorphAnalyzer()):
    """согласование числительных по родам со словами стоящими за ними: два-две """
    new_phrase = []
    py_gen = 1
    phrase = phrase.split(' ')
    while phrase:
        word = phrase.pop(-1)
        if 'NUMB' in morph.parse(word)[0].tag:
            new_phrase.append(pytils.numeral.sum_string(int(word), py_gen))
        else:
            new_phrase.append(word)
        py_gen = pytils.numeral.FEMALE if 'femn' in morph.parse(word)[0].tag else pytils.numeral.MALE
    return ' '.join(new_phrase[::-1])


def nums(phrase, morph=pymorphy2.MorphAnalyzer()):
    """ согласование существительных с числительными, стоящими перед ними: 1 минута, 2 минуты """
    phrase = phrase.replace('  ', ' ').replace(',', ' ,')
    numeral = ''
    new_phrase = []
    for word in phrase.split(' '):
        if 'NUMB' in morph.parse(word)[0].tag:
            numeral = word
        if numeral:
            word = str(morph.parse(word)[0].make_agree_with_number(abs(int(numeral))).word)
        new_phrase.append(word)

    return ' '.join(new_phrase).replace(' ,', ',')


def speak(what):
    speech_voice = 3  # голосовой движок
    rate = 120
    tts = pyttsx3.init()
    voices = tts.getProperty("voices")
    tts.setProperty('rate', rate)
    tts.setProperty("voice", voices[speech_voice].id)
    print('🔊', what)
    what = correct_numerals(what)
    tts.say(what)
    tts.runAndWait()
    # tts.stop()


def db_record(seconds):
    """ Запись результатаов раунда в бд """
    connection = pymysql.connect('localhost', 'assistant', APIKeysLocal.mysql_pass, 'assistant')
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = 'INSERT INTO `whm_breath` (`timeBreath`, `result`) VALUES (NOW(), {})'.format(seconds)
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()


class Workout:
    mouse_coords = (0, 0)

    def __init__(self, rounds=3, breaths=30, hold=15):
        self.rounds = rounds
        self.breaths = breaths
        self.hold = hold
        self.round_times = []
        self.lock = threading.Lock()  # взаимоблокировка отдельных голосовых потоков

    def __str__(self):
        return '\n♻{} 🗣{} ⏱{}'.format(self.rounds, self.breaths, self.hold)

    def __hold_breath(self):
        """ Задержка дыхания прекращается при смещении мыши на 20 пикселей"""
        start_time = time.time()
        with mouse.Listener(on_move=on_move) as listener:
            listener.join()
        seconds = int(time.time() - start_time)
        db_record(seconds)
        self.mouse_coords = (0, 0)
        mins = seconds // 60
        secs = seconds % 60
        self.round_times.append('{:02}:{:02}'.format(mins, secs))
        play_wav_inline('gong')
        play_wav_inline('inhale')
        self.say('Глубокий вдох. ' + nums("{} минута {} секунда".format(mins, secs)))

    def __clock_tick(self):
        """ отсчет 5 секунд перед завершением задержки дыхания в конце раунда """
        for i in range(self.hold):
            if i < hold - 5:
                time.sleep(1)
            else:
                play_wav('clock')
        play_wav_inline('gong2')

    def __breathe_round(self, round):
        """ раунд дахания. Воспроизводится звук дыхания и гонг по каждые вдохов """
        last_round = 'Заключительный ' if round == self.rounds else ''
        self.say(last_round + 'раунд ' + str(round))
        time.sleep(1)
        for i in range(self.breaths):
            if i % 10 == 0:
                play_wav_inline('bronze_bell')
            play_wav('inhale')
            if i == self.breaths - 1:
                play_wav_inline('gong2')
            print(i + 1, end=' ')
            play_wav('exhale')
        print()

        self.say('Задерживаем дыхание на выдохе')
        self.__hold_breath()
        # self.say('Держим ' + nums(str(self.hold) + ' секунда'))
        self.__clock_tick()
        play_wav_inline('exhale')
        self.say('Выдох')
        time.sleep(1.7)

    def breathe(self):
        """ Запуск тренировки дыхания, запуск раундов """
        self.say('Выполняем ' + nums(str(self.rounds) + ' раунд'))
        self.say('Каждый раунд это ' + nums(str(self.breaths) + ' глубокий вдох - и спокойный выдох'))
        time.sleep(0.5)
        self.say('Приготовились...')
        time.sleep(1)
        for i in range(self.rounds):
            self.__breathe_round(i + 1)
        self.say('Восстанавливаем дыхание.')

    def statistics(self):
        """ вывод статистики по текущей тренировке"""
        print('=============')
        for i in range(len(self.round_times)):
            print('Раунд', i, self.round_times[i])
        print('=============')

    def say(self, what):
        self.lock.acquire()
        thread = threading.Thread(target=speak, kwargs={'what': what})
        thread.start()
        thread.join()
        self.lock.release()


if __name__ == "__main__":
    rounds, breaths, hold = 3, 30, 13
    """ получение параметра количества раундов из внешней команды """
    if len(sys.argv) == 2 and type(sys.argv[1]) == str:
        rounds = int(sys.argv[1])
    workout = Workout(rounds, breaths, hold)
    workout.breathe()

    workout.statistics()

    time.sleep(6)  # чтобы дозвучал гонг

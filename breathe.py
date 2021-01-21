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
from va_assistant import assistant

warnings.filterwarnings("ignore")

""" Количество раундов, вдохов в раунде, задержка дыхания на вдохе"""


def listen_mouse_click():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def on_move(x, y):
    cursor = workout.mouse_coords
    if cursor == (0, 0):
        workout.mouse_coords = (x, y)
        return True
    if int(sqrt(abs(cursor[0] - x) + abs(cursor[1] - y))) > 20:
        return False


def on_click(x, y, button, pressed):
    if not pressed and button == mouse.Button.middle:
        workout.enough = True
        return False


def play_wav(src):
    wav_file = sys.path[0] + '\\static\\wav\\' + src + '.wav'
    try:
        wav = pyglet.media.load(wav_file)
        wav.play()
        time.sleep(wav.duration)
    except FileNotFoundError:
        print('Файл не найден:', wav_file)


def play_wav_inline(src):
    wav_file = sys.path[0] + '\\static\\wav\\' + src + '.wav'
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

    def __init__(self, breaths=30, hold=15):
        self.breaths = breaths
        self.hold = hold
        self.round_times = []
        self.enough = False  # Завершение при изменении флага
        self.lock = threading.Lock()  # взаимоблокировка отдельных голосовых потоков

    def __str__(self):
        return '\n🗣{} ⏱{}'.format(self.breaths, self.hold)

    def __hold_breath(self, round):
        """ Задержка дыхания прекращается при смещении мыши на 20 пикселей"""
        start_time = time.time()
        with mouse.Listener(on_move=on_move) as listener:
            listener.join()
        seconds = int(time.time() - start_time)
        db_record(seconds)
        self.mouse_coords = (0, 0)
        mins = seconds // 60
        secs = seconds % 60
        self.round_times.append(seconds)
        if round == 1:
            message = "{} минута {} секунда".format(mins, secs)
        else:
            diff = self.round_times[round - 2] - self.round_times[round - 1]
            more = 'Плюс' if diff < 0 else 'Минус'
            message = "{} {} секунда".format(more, abs(diff))
        play_wav_inline('gong')
        play_wav_inline('inhale')

        assistant.say('Глубокий вдох. ' + message)

    def __clock_tick(self):
        """ отсчет 5 секунд перед завершением задержки дыхания в конце раунда """
        for i in range(self.hold):
            if i < self.hold - 4:
                time.sleep(1)
            else:
                play_wav('clock')
        play_wav_inline('gong2')

    def __breathe_round(self, round):
        """ Запуск потока, слушающего мышь. Если она сместилась, прекратать тренировку """
        t = threading.Thread(target=listen_mouse_click)
        t.start()

        """ раунд дахания. Воспроизводится звук дыхания и каждые 10 вдохов гонг """
        assistant.say('раунд ' + str(round))
        time.sleep(1)

        for i in range(self.breaths):
            if self.enough:
                t.join()
                return
            if i % 10 == 0:
                play_wav_inline('bronze_bell')
            play_wav('inhale')
            if i == self.breaths - 1:
                play_wav_inline('gong3')
            print(i + 1, end=' ')
            play_wav('exhale')

        assistant.say('Выдох. Задерживаем дыхание')
        self.__hold_breath(round)
        # assistant.say('Держим ' + nums(str(self.hold) + ' секунда'))
        self.__clock_tick()
        play_wav_inline('exhale')
        assistant.say('Выдох')
        time.sleep(1.7)

    def __finish(self):
        assistant.say('Завершаем гимнастику.')
        self.statistics()
        # time.sleep(6)  # чтобы дозвучал гонг
        # sys.exit(0)

    def breathe(self, rounds=None):
        play_wav_inline('gong')
        """ Запуск тренировки дыхания, запуск раундов """
        if rounds:
            assistant.say(f'Выполняем {rounds}  раунд')
        else:
            assistant.say('Выполняем дыхательную гимнастику')
        assistant.say(f'Каждый раунд это {self.breaths} глубокий вдох - и спокойный выдох')
        assistant.say('Чуть позже подправлю.')
        print('* Завершить тренировку - клик средней кнопкой мыши')
        print('** Чтобы остановить отсчёт задержки дыхания, подвигай мышку')
        time.sleep(2)
        assistant.say('Приготовились...')
        time.sleep(1)
        i = 1
        while self.enough is not True:
            self.__breathe_round(i)
            i += 1
        self.__finish()

    def statistics(self):
        """ вывод статистики по текущей тренировке"""
        if self.round_times:
            assistant.say('Молодец, спасибо.')
            if len(self.round_times) > 1:
                ave = int(sum(self.round_times) / len(self.round_times))
                assistant.say(f'Всего {len(self.round_times)} раунд')
                assistant.say('Среднее значение: {} минута {} секунда'.format(ave // 60, ave % 60))
            maxi = max(self.round_times)
            assistant.say('Максимальное значение: {} минута {} секунда'.format(maxi // 60, maxi % 60))


workout = Workout()


if __name__ == "__main__":
    """ получение параметра количества раундов из внешней команды """
    rounds = int(sys.argv[1]) if len(sys.argv) == 2 and type(sys.argv[1]) == str else None

    workout.breathe(rounds)

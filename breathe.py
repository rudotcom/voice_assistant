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

morph=pymorphy2.MorphAnalyzer()
warnings.filterwarnings("ignore")

""" Количество раундов, вдохов в раунде, задержка дыхания на вдохе"""


def listen_mouse_click():
    with mouse.Listener(on_click=on_click) as click_listener:
        click_listener.join()


def listen_mouse_move():
    with mouse.Listener(on_move=on_move) as move_listener:
        move_listener.join()


def on_move(x, y):
    cursor = workout.mouse_coords
    if cursor == (0, 0):
        workout.mouse_coords = (x, y)
        return True
    if int(sqrt(abs(cursor[0] - x) + abs(cursor[1] - y))) > 20:
        workout.stop_inhale = True
        play_wav_inline('hold-your-horses-468')
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


def db_record(seconds):
    if seconds < 10:
        return
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
        self.stop_inhale = False
        self.lock = threading.Lock()  # взаимоблокировка отдельных голосовых потоков

    def __str__(self):
        return '\n🗣{} ⏱{}'.format(self.breaths, self.hold)

    def __hold_breath(self, round):
        self.mouse_coords = (0, 0)
        """ Задержка дыхания прекращается при смещении мыши на 20 пикселей через 5 сек"""
        start_time = time.time()
        time.sleep(5)
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
        """ Запуск потока, слушающего мышь. Если она сместилась, прекратить тренировку """
        mouse_click_thread = threading.Thread(target=listen_mouse_click)
        mouse_click_thread.start()

        self.stop_inhale = False
        """ раунд дыхания. Воспроизводится звук дыхания и каждые 10 вдохов гонг """
        assistant.say('раунд ' + str(round))
        time.sleep(1)

        for i in range(self.breaths):
            if i == 4:
                """ Запуск потока, слушающего мышь. После 4 раунда если она сместилась, прекратить вдохи """
                mouse_move_thread = threading.Thread(target=listen_mouse_move)
                mouse_move_thread.start()

            if self.enough:
                mouse_click_thread.join()
                return
            elif self.stop_inhale:
                mouse_move_thread.join()
                break
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
        self.enough = False
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

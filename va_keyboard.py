from pynput.keyboard import Key, Controller
import time

keyboard = Controller()


def volume_up(points=8):
    for i in range(points):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        time.sleep(0.1)


def volume_down(points=6):
    for i in range(points):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        time.sleep(0.1)


def track_next():
    keyboard.press(Key.media_next)
    keyboard.release(Key.media_next)


def track_prev():
    keyboard.press(Key.media_next)
    keyboard.release(Key.media_next)


def play_pause():
    keyboard.press(Key.media_play_pause )
    keyboard.release(Key.media_play_pause )

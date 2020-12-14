import pyglet
import time

alert = pyglet.media.load(r'src\wav\inflicted-601.wav')
alert2 = pyglet.media.load(r'src\wav\deduction-588.wav')
print(alert.duration)
print(alert2.duration)
alert2.play()
time.sleep(alert2.duration - 1)
alert.play()
time.sleep(alert.duration - 1)

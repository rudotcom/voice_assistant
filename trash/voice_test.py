import pyttsx3
tts = pyttsx3.init() # Инициализировать голосовой движок.
voices = tts.getProperty('voices')  # Получить список голосов


# Перебрать установленные голоса и вывести имя каждого
def list_voices(what):
    for voice in voices:
        print(voice.name)
        tts.setProperty("voice", voice.id)
        tts.say(what)
        tts.runAndWait()
        tts.stop()


def one_voice(what, v, r):
    tts.setProperty('rate', r)
    tts.setProperty("voice", voices[v].id)
    tts.say(what)
    tts.runAndWait()
    tts.stop()

what = """
Ехал грека через реку, видит грека в реке рак. Сунул руку грека в реку, греку рак за руку цап"""

list_voices(what)
one_voice(what, 3, 140)

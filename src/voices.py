import pyttsx3


speech_voice = 9  # голосовой движок
speech_language = "ru"
rate = 130
tts = pyttsx3.init()
voices = tts.getProperty("voices")
tts.setProperty('rate', rate)


"""Воспроизведение текста голосом и вывод его в консоль"""

what = 'Привет, как дела. Я сегодня не занята. Я готова поговорить, если ты не против'
what = 'Ехал грека через реку, видит грека в реке рак'
for i in range(0, 9):
    tts.setProperty("voice", voices[i].id)
    print(i, voices[i].name, '🔊 ', what)
    tts.say(what)
    tts.runAndWait()
    tts.stop()


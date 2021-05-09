""" Офлайн и онлайн распознавание голоса
"""
import os  # работа с файловой системой
import pyaudio
import speech_recognition
from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk

from va_gui import girl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.join(BASE_DIR, "models"):
    print(os.path.abspath(''))
    print(
        "Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit(1)

model = Model("models/vosk-model-small-ru-0.4")


def recognize_online():
    with microphone:
        girl.root.attributes("-topmost", True)
        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=0.5)

        try:
            # print(" 🎤 ", end='')
            girl.dress_up_as('Occupations-Pilot-Female-Light-icon')
            recognizer.pause_threshold = 1
            audio = recognizer.listen(microphone, None, None)
            # TODO: пропробовать слушать в фоне. Так он не должен прерываться на паузы, а слушать все время
            # audio = recognizer.listen_in_background(microphone)

        except speech_recognition.WaitTimeoutError:  # если не дождались речи в timeout
            print("Тишина...")
            return

        # использование online-распознавания через Google
        try:
            girl.dress_up_as('Occupations-Pilot-Female-Dark-icon')
            # print("👂", end='')
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()
            # print(' 💬', recognized_data)
            if recognized_data:
                girl.type('💬 ' + recognized_data, 'voice_in')
            return recognized_data
        except speech_recognition.UnknownValueError:
            # print(' ⏳')
            pass
        # в случае проблем с доступом в Интернет происходит выброс ошибки
        except speech_recognition.RequestError:
            girl.type('💬 Нет связи с сетью')
            return False
        except TimeoutError:
            girl.type('💬 Ошибка связи с сетью')
            return False
        except ConnectionResetError:
            girl.type('💬 Удаленный хост принудительно разорвал существующее подключение')
            return False


def recognize_offline():
    girl.root.attributes("-topmost", False)
    girl.dress_up_as('Occupations-Pilot-Military-Female-Light-icon')
    # print('☕ ', end='')
    rec = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    while True:
        data = stream.read(30000)
        if len(data) == 0:
            return
        if rec.AcceptWaveform(data):
            stream.stop_stream()
            girl.dress_up_as('Rest-Person-Coffee-Break-Female-Light-icon')
            # print('.. ', end='')
            recognized_text = eval(rec.Result())['text']
            if recognized_text:
                girl.type('💬 ' + recognized_text, 'voice_in')
            return recognized_text


# инициализация инструментов распознавания и ввода речи
recognizer = speech_recognition.Recognizer()
microphone = speech_recognition.Microphone()
with microphone:
    recognizer.adjust_for_ambient_noise(microphone, duration=0.5)
    recognizer.dynamic_energy_threshold = False

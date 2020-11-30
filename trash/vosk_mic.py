from vosk import Model, KaldiRecognizer
import os
import pyaudio

model = Model("../models/vosk-model-small-ru-0.4")


def use_offline_recognition():
    """
    Переключение на оффлайн-распознавание речи
    :return: распознанная фраза
    """
    recognized_data = ""
    if not os.path.exists("../models"):
        print(
            "Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)


    rec = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    while True:
        data = stream.read(4000)
        if len(data) == 0:
            return
        if rec.AcceptWaveform(data):
            stream.stop_stream()
            return eval(rec.Result())['text']
        # else:
        #     print(rec.PartialResult())



while True:
    voice_input = use_offline_recognition()
    print(voice_input)
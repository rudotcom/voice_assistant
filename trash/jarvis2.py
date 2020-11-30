import speech_recognition as sr

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("name: \"{1}\" for Mic(devIndex=\"{0}\")".format(index, name))

r = sr.Recognizer()
with sr.Microphone(device_index=1) as source:
    print("Говори")
    audio = r.listen(source)

query = r.recognize_google(audio, language="ru-RU")
print(" - - " + query.lower())

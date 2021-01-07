# имя проекта: voice-assistant
# имя файла: main.py
# автор: Трошков А.В.
# дата создания: 24.11.2020
# описание: голосовой помощник
# версия Python: 3.8
from va_assistant import Context, assistant, context, old_context
from va_actions import Action
from va_intent import intent_by_levenshtein, intent_by_latent, intent_in_phrase, intent_by_imperative
import tkinter as tk # Python 3
from win32gui import GetForegroundWindow


def is_active(process_name):
    return process_name == GetForegroundWindow()


if __name__ == "__main__":
    root = tk.Tk()
    # The image must be stored to Tk or it will be garbage collected.
    root.image = tk.PhotoImage(file='static/img/Person-Female-Light-icon.png')
    label = tk.Label(root, image=root.image, bg='silver')
    root.overrideredirect(True)
    # root.geometry("+250+250")
    # root.lift()
    # root.wm_attributes("-topmost", True)
    # root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "silver")
    label.pack()

    # assistant.play_wav('vuvuzelas-warming-up-27')
    assistant.alert()  # для запуска в активном режиме

    while True:
        print(is_active(32641916))

        voice_text = assistant.recognize()
        if voice_text:
            """ если ассистент бодрствует  или сообщение начинается с имени """
            if assistant.pays_attention(voice_text):
                if context.phrase:
                    """ получаем контекст из фразы путем морфологического разбора"""
                    context.phrase_morph_parse()

                    if intent_by_latent(context.phrase):
                        pass

                    elif intent_by_levenshtein(context.phrase, 90):
                        pass

                    elif intent_by_imperative():
                        pass

                    elif intent_in_phrase(context.phrase):  # Проверка наличия слов из интента во фразе
                        pass

                    # print(context.__dict__)
                    if not context.intent:
                        # Если интента таки нету, текущий контекст дополнится прежним контекстом
                        context.adopt_intent(old_context)
                    action = Action()
                    old_context = context


# имя проекта: voice-assistant
# номер версии: 0.3
# имя файла: main.py
# автор: Трошков А.В.
# дата создания: 24.11.2020
# описание: голосовой помощник
# версия Python: 3.8
from va_assistant import assistant, context, new_context
from va_actions import Action
from va_intent import intent_by_levenshtein, intent_by_latent, intent_in_phrase, intent_by_imperative
from va_sand_box import context_landscape

if __name__ == "__main__":

    assistant.setup_voice()
    assistant.alert()  # для запуска в активном режиме
    action = None

    while True:
        voice_text = assistant.recognize()
        if voice_text:
            """ если ассистент бодрствует  или сообщение начинается с имени """
            if assistant.pays_attention(voice_text):
                if new_context.phrase:
                    """ получаем контекст из фразы путем морфологического разбора"""
                    new_context.phrase_morph_parse()
                    """ обновляем предыдущий контекст для дальнейшго использования"""
                    context.refresh(new_context)

                    if intent_by_latent(new_context.phrase):
                        action = Action(context)

                    elif intent_by_levenshtein(new_context.phrase, 90):
                        action = Action(context)

                        # TODO после распознанной фразы очищать контекст - перенести в name
                        assistant.intent = None
                        context.phrase = None
                        context.imperative = None
                        # context_now.name = None

                    elif intent_by_imperative():
                        action = Action(context)

                    elif intent_in_phrase(new_context.phrase):  # Проверка наличия слов из интента во фразе
                        action = Action(context)

                    elif action:
                        print(context_landscape())
                        print('action:', action.name)
                        action.make_action()

                    else:
                        print(context_landscape())
                        assistant.fail()

# имя проекта: voice-assistant
# имя файла: main.py
# автор: Трошков А.В.
# дата создания: 24.11.2020
# описание: голосовой помощник
# версия Python: 3.8
from va_assistant import assistant, context, old_context
from va_actions import Action
from va_intent import intent_by_levenshtein, intent_by_latent, intent_in_phrase, intent_by_imperative

if __name__ == "__main__":
    # assistant.play_wav('vuvuzelas-warming-up-27', 0.4)
    assistant.alert()  # для запуска в активном режиме
    action = None

    while True:
        voice_text = assistant.recognize()
        if voice_text:
            print('voice:', voice_text)
            """ если ассистент бодрствует  или сообщение начинается с имени """
            if assistant.pays_attention(voice_text):
                if context.phrase:
                    context.import_from(old_context)
                    context.landscape()
                    """ получаем контекст из фразы путем морфологического разбора"""
                    context.phrase_morph_parse()
                    """ обновляем предыдущий контекст для дальнейшго использования"""
                    context.landscape()

                    if intent_by_latent(context.phrase):
                        action = Action()

                    elif intent_by_levenshtein(context.phrase, 90):
                        action = Action()

                    elif intent_by_imperative():
                        action = Action()

                    elif intent_in_phrase(context.phrase):  # Проверка наличия слов из интента во фразе
                        action = Action()

                    elif action:
                        action.make_action()
# TODO: - Если контекст не изменился от новой фразы, то "Я не поняла"
                    else:
                        assistant.fail()

# TODO:
#   voice: выключи музыку
#   >>intent_by_levenshtein =  turn_on
#   voice: выключи player
#   >>intent_by_imperative =  app_close
#   закрыть что?
#   Если нет action, только голос - went offline

# имя проекта: voice-assistant
# номер версии: 0.3
# имя файла: main.py
# автор: Трошков А.В.
# дата создания: 24.11.2020
# описание: голосовой помощник
# версия Python: 3.8
from va_assistant import assistant, context, new_context, Intent, Action
from va_intent import intent_by_levenshtein, intent_by_latent, intent_in_phrase
from va_actions import act
from va_sand_box import context_landscape


if __name__ == "__main__":

    assistant.setup_voice()
    assistant.alert()  # для запуска в активном режиме

    while True:
        intent = None
        voice_text = assistant.recognize()
        if voice_text:
            """ если ассистент бодрствует  или сообщение начинается с имени """
            if assistant.pays_attention(voice_text):
                if new_context.phrase:
                    """ получаем контекст из фразы путем морфологического разбора"""
                    new_context.phrase_morph_parse()
                    print(context_landscape())
                    """ обновляем предыдущий контекст для дальнейшго использования"""
                    context.refresh(new_context)

                    if intent_by_latent(new_context.phrase):
                        print('_ has latent intent')
                        print('intent <-', context.intent)
                        intent = Intent('find')
                        action = Action(intent, context)

                    elif intent_by_levenshtein(new_context.phrase, 90):
                        print('_ intent_by_levenshtein')
                        intent = Intent('find')
                        action = Action(intent, context)

                        # TODO после распознанной фразы очищать контекст - перенести в action
                        context.intent = None
                        context.phrase = None
                        context.imperative = None
                        # context_now.action = None

                    elif intent_by_imperative():
                        print('_ get_action_by_imperative')
                        print('intent <-', context.intent)
                        act()

                    elif intent_in_phrase(new_context.phrase):  # Проверка наличия слов из интета во фразе
                        action = Action(intent, context)

                    elif context.action:
                        print('_ context_now action')
                        act()

                    else:
                        assistant.fail()

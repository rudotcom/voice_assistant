# имя проекта: voice-assistant
# номер версии: 0.3
# имя файла: main1.py
# автор: Трошков А.В.
# дата создания: 24.11.2020
# описание: голосовой помощник
# версия Python: 3.8
from va_assistant import assistant, context, new_context
from va_intent import action_by_intent, has_latent, get_action_by_imperative, intent_in_phrase
from va_actions import act

if __name__ == "__main__":

    assistant.setup_voice()
    assistant.alert()  # для запуска в активном режиме

    while True:
        voice_text = assistant.recognize()
        if voice_text:
            """ если ассистент бодрствует  или сообщение начинается с имени """
            if assistant.pays_attention(voice_text):
                print('context phrase:', context.phrase)
                if context.phrase:
                    """ получаем контекст из фразы путем морфологического разбора"""
                    new_context.phrase_morph_parse()
                    """ обновляем предыдущий контекст для дальнейшго использования"""
                    context.refresh(new_context)
                    print(context)

                    if has_latent():
                        print('has latent intent')
                        act()

                    elif action_by_intent(90):
                        print('act by intent')
                        act()
                        # TODO после распознанной фразы очищать контекст???
                        context.imperative = None

                    elif context.imperative:
                        print('get_action_by_imperative')
                        if get_action_by_imperative():
                            act()

                    elif intent_in_phrase():  # Проверка наличия слов из интета во фразе
                        print('intent in phrase')
                        act()

                    elif context.action:
                        print('context action')
                        act()

                    else:
                        assistant.fail()

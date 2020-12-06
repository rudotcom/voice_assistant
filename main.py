# имя проекта: voice-assistant
# номер версии: 0.3
# имя файла: main1.py
# автор: Трошков А.В.
# дата создания: 24.11.2020
# описание: голосовой помощник
# версия Python: 3.8
from va_assistant import assistant, context, new_context
from va_actions import remove_alias, act, action_by_intent, has_latent, get_action_by_imperative

if __name__ == "__main__":

    assistant.setup_voice()
    """если необходимо, чтобы запускалась в активном режиме, иначе для активации необходимо назвать имя помощника"""
    assistant.alert()

    while True:
        voice_text = assistant.recognize()
        if voice_text:
            """ если ассистент бодрствует  или сообщение начинается с имени """
            print('alert:', assistant.is_alert())
            if assistant.pays_attention(voice_text):
                phrase = remove_alias(voice_text)

                if phrase:
                    """ получаем контекст из фразы путем морфологического разбора"""
                    new_context.phrase_morph_parse(phrase)
                    """ обновляем предыдущий контекст для дальнейшго использования"""
                    context.refresh(new_context)
                    print(context)

                    if has_latent(phrase):
                        act()

                    elif action_by_intent(90):
                        act()
                        # TODO после распознанной фразы очищать контекст???
                        context.imperative = None

                    elif context.imperative:
                        print('get_action_by_imperative')
                        if get_action_by_imperative():
                            act()

                    elif context.action:
                        act()

                    else:
                        assistant.fail()

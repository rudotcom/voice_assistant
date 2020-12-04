# имя проекта: voice-assistant
# номер версии: 0.1
# имя файла: main1.py
# автор: Трошков А.В.
# дата создания: 24.11.2020
# описание: голосовой помощник
# версия Python: 3.8
from va_actions import get_intent_action, please_specify, turn_off, turn_on, open_pro, \
    find_source_action, act, remove_alias, get_intent
from va_assistant import assistant, context, new_context


def apply_new_context():
    if new_context.imperative:
        context.imperative = new_context.imperative
    if new_context.source:
        context.source = new_context.source
    if new_context.subject:
        context.subject = new_context.subject
    if new_context.location:
        context.location = new_context.location
    if new_context.action:
        context.action = new_context.action
    if new_context.reply:
        context.reply = new_context.reply
    if new_context.adverb:
        context.adverb = new_context.adverb
    if new_context.text:
        context.text = new_context.text


if __name__ == "__main__":

    assistant.setup_voice()
    assistant.alert()
    assistant.speak(assistant.name + ' слушает')

    while True:
        voice_text = assistant.recognize()
        if voice_text:
            """ если ассистент бодрствует  или сообщение начинается с имени """
            # print('alert:', assistant.is_alert())
            if any([assistant.is_alert(), voice_text.startswith(assistant.alias)]):
                assistant.alert()
                phrase = remove_alias(voice_text)
                print('voice_text: [', voice_text, '] phrase: [', phrase, ']')

                # узнать интент пользователя
                if phrase:
                    """ получаем контекст из фразы путем морфологического разбора"""
                    new_context.get_from_phrase(phrase)
                    print(context)

                    if get_intent(90):
                        continue
                    else:
                        apply_new_context()

                    if context.imperative == 'узнать':
                        print('act_src:', context.reply, context.action)
                        if context.reply or context.action:
                            act(reply=context.reply, action=context.action)

                    elif context.imperative == 'найти':
                        if context.source:
                            if context.subject:
                                assistant.use_tool()
                            else:
                                please_specify('что найти:', 'target')
                        else:
                            please_specify('найти где?', 'tool')

                    elif context.imperative == 'включить':
                        turn_on()

                    elif context.imperative == 'выключить':
                        turn_off()

                    elif context.imperative == 'открыть':
                        if context.subject:
                            open_pro()
                        else:
                            please_specify('что открыть:', 'target')

                    else:
                        get_intent_action(context.imperative)

            else:
                """ если ассистент уснул и сообщение не начинается с имени"""
                assistant.sleep()

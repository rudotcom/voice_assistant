# имя проекта: voice-assistant
# номер версии: 0.1
# имя файла: main1.py
# автор: Трошков А.В.
# дата создания: 24.11.2020
# описание: голосовой помощник
# версия Python: 3.8
import random
from os import system
from datetime import datetime, timedelta

from va_actions import aimp, application, app_close, get_intent_action, act, speak, setup_assistant_voice, act_by_intent
from va_voice_recognition import recognize_offline, recognize_online
from va_assistant import assistant, context, CONFIG


def remove_alias(text):
    for x in CONFIG['alias']:
        text = text.replace(x, "", 1).strip()
    return text


def recognize(mode):
    """Выбор режима распознавания"""
    if mode == 'online':
        return recognize_online()
    else:
        return recognize_offline()


def use_tool():
    print('tool:', context.tool)
    print('target', context.target)
    response = random.choice(CONFIG['intents']['find']['responses'])
    if context.tool in CONFIG['intents']['find']['actions'].keys():
        print(context.tool, CONFIG['intents']['find']['actions'].keys())
        action = CONFIG['intents']['find']['actions'][context.tool]
        act(response, action, context.target)
    else:
        speak('Там я не умею искать')


def turn_on():
    """ проверяем, есть ли радио или музыка в контексте"""
    for sound in CONFIG['intents']['music']['requests']:
        if sound in context.target:
            """ если есть, находим action """
            for action in CONFIG['intents']['music']['requests']:
                """ если action есть, включаем плеер"""
                if context.target in CONFIG['intents']['music']['actions']:
                    aimp(CONFIG['intents']['music']['actions'][context.target])
                    return
                else:
                    # если такого радио или музыки нет
                    speak(context.target + ' ' + random.choice(CONFIG['intents']['music']['not_exists']))
                    return
            break
        else:
            please_specify('что включить:', 'target')
            break


def open_pro():
    success = False
    for app in CONFIG['intents']['applications']['actions']:
        if app in context.target:
            speak(random.choice(CONFIG['intents']['applications']['responses']))
            success = application(context.target)
            break
    if not success:
        speak('я не знаю такой программы')


def please_specify(where, what):
    if what == 'target':
        speak('уточни, ' + where)
    if what == 'tool':
        print('где именно?')
    # speak(random.choice(CONFIG['intents']['music']['spec']))
    pass


def get_to_know():
    print('get_to_know')
    action, response = get_intent_action(context.target, context.adverb)
    if action or response:
        target = ' '.join([context.target, context.adverb])
        """ передаем действию предварительную фразу, само действие и цель действия """
        act(response, action, target)


def turn_off():
    if context.target in CONFIG['intents']['app_close']['actions'].keys():
        app_close(CONFIG['intents']['app_close']['actions'][context.target])


if __name__ == "__main__":

    assistant.name = CONFIG['alias'][0]
    setup_assistant_voice()

    whazzup = assistant.name + ' ' + CONFIG['whazzup'][assistant.recognition_mode]
    speak(whazzup)
    assistant.last_input = datetime.now()
    sec_to_offline = 40

    while True:
        """если timedelta прошла, переход в офлайн или "Помолчи" - переход в офлайн"""
        fresh_talk = datetime.now() - assistant.last_input < timedelta(seconds=sec_to_offline)
        # print('fresh', fresh_talk, 'last', assistant.last_input)
        if fresh_talk:
            if assistant.recognition_mode == 'offline':
                assistant.recognition_mode = 'online'
                print("online")
        elif assistant.recognition_mode == 'online':
            assistant.recognition_mode = 'offline'
            print("offline...")
        print('.')

        voice_text = recognize(assistant.recognition_mode)
        if voice_text:
            print('voice_text:', voice_text)
            # print(datetime.now(), assistant.last_input)
            # условия бодрствования
            # если предыдущее сообщение было недавно или сообщение начинается с имени
            awake = any([fresh_talk, voice_text.startswith(assistant.alias)])
            if awake:
                assistant.last_input = datetime.now()
                assistant.recognition_mode = 'online'
                user_text = remove_alias(voice_text)
                # print('filtered:', filtered_text)

                # узнать интент пользователя
                if user_text:
                    # print(' -- > get_intent')  # debugging
                    context.context_by_phrase(user_text)
                    print('\timperative:', context.imperative)
                    print('\ttool:', context.tool)
                    print('\ttarget:', context.target)
                    print('\tadverb:', context.adverb)
                    print('\taddressee:', context.addressee)
                    print('\ttext:', context.text)

                    if act_by_intent(context.text):
                        pass

                    elif context.imperative == 'узнать':
                        if context.target:
                            get_to_know()
                        else:
                            please_specify('что ты хочешь узнать:', 'target')

                    elif context.imperative == 'найти':
                        if context.tool:
                            if context.target:
                                use_tool()
                            else:
                                please_specify('что найти:', 'target')
                        else:
                            please_specify('найти где?', 'tool')

                    elif context.imperative == 'включить':
                        turn_on()

                    elif context.imperative == 'выключить':
                        turn_off()

                    elif context.imperative == 'открыть':
                        if context.target:
                            open_pro()
                        else:
                            please_specify('что открыть:', 'target')

                    else:
                        get_intent_action(context.imperative)

# имя проекта: voice-assistant
# имя файла: main.py
# автор: Трошков А.В.
# дата создания: 24.11.2020
# описание: голосовой помощник
# версия Python: 3.8
from va_assistant import assistant, context, old_context
from va_actions import Action
from va_intent import intent_by_levenshtein, intent_by_latent, intent_in_phrase, intent_by_imperative
from va_misc import cls


if __name__ == "__main__":

    # assistant.play_wav('vuvuzelas-warming-up-27')
    assistant.alert()  # для запуска в активном режиме

    while True:
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

                    context.adopt_intent(old_context)  # Если интента таки нету, контекст дополнится старым контекстом
                    # print(context.landscape())
                    action = Action()

# TODO: "что дальше" не удаляет интент. Интента быть не должно. почему он остается?
# TODO:
#   сколько будет 5% от или 2 умножить на 2 или 2 в степени
#   если в location осталась фраза, погода не работает
#   Если нет action, только голос - went offline


""" если интента нет - берется старый и прикручиваются старые параметры, т.е. повторяется предыдущее действие
даже если говоришь не в тему
"""

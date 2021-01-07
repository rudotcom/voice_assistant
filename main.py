from va_assistant import Context, assistant, context, old_context
from va_actions import Action
from va_intent import intent_by_levenshtein, intent_by_latent, intent_in_phrase, intent_by_imperative


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

                    # print(context.__dict__)
                    if not context.intent:
                        # Если интента таки нету, текущий контекст дополнится прежним контекстом
                        context.adopt_intent(old_context)
                    action = Action()
                    old_context = context


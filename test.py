from va_config import CONFIG
from va_assistant import assistant, context
import random


class Intent:

    def __init__(self, name):
        self.name = name
        self.param = {}

        intent_data = CONFIG['intents'][name]
        intent_name = intent_data.keys()

        for key in intent_name:
            self.param[key] = intent_data[key]


class Action:
    """ Экземпляр action ассоциируется с интентом из конфига
    экземпляры класса получают параметры от функций определения интента и из контекста """

    def __init__(self, intent_obj, context):
        self.intent = intent_obj
        self.subject = context.subject
        self.target = context.target
        self.text = context.text

    def inquire_missing_parameters(self):
        """ если параметра target нет, но в конфиге есть запрос параметра, запросить """
        if not self.target and 'target_missing' in intent.param.keys():
            assistant.speak(random.choice(self.intent.param['target_missing']))

    def say(self):
        """ произнести фразу ассоциированную с данным интентом """
        if self.intent.param['replies']:
            assistant.speak(random.choice(self.intent.param['replies']))

    def make_action(self):
        self.inquire_missing_parameters()
        self.say()
        """ вызов функций, выполняющих действие
        Действия, которые способен выполнять помощник:
        - только сказать что прописано в интенте
        - получить инфу из функции или от assistant и произнести полученный текст
            ctime, age, repeat, repeat_after_me, usd, btc, my_mood, mood_up, mood_down, die, weather, app_close, whois,
            wikipedia, translate, anecdote, quotation
        - открыть определенную страницу браузера с запросом
            youtube, browse google, yandex, maps
        - Запустить (остановить) процесс Windows
            turn_on, application, app_close
        - сделать request в web
            telegram_bot, email
        - повесить hook на телеграм, чтобы получать ответы
        Для каждого действия необходим ограниченный набор параметров (source, target...)
        Если действие назначено интентом, но параметров не хватает, необхоимо запросить отдельно
        """


intent = Intent('repeat')
print(intent.__dict__)

action = Action(intent, context)

action.make_action()

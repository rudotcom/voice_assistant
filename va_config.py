CONFIG = {
    'intents': {
        'hello': {
            'requests': ['привет', 'добрый день', 'здравствуй', 'доброе утро', 'добрый вечер', 'чё как'],
            'replies': ['Привет босс!', 'давай говори чего хочешь'],
        },
        'stop': {
            'requests': ['помолчи', 'не подслушивай', 'тихо', 'потеряйся',
                         'пока', 'до свидания', 'прощай', 'спокойной ночи'],
            'replies': ['молчу', 'Счаст ливо', 'Еще увидимся', 'Если что я тут', 'Аэл би бэк'],
            'action': 'stop',
        },
        'die': {
            'requests': ['умри', 'сдохни', 'уйди'],
            'replies': ['увидимся в следующей жизни', 'Если что, знаешь где меня искать', 'пока-пока'],
            'action': 'die',
        },
        'name': {
            'requests': ['как твоё имя', 'как тебя зовут'],
            'action': 'name',
        },
        'think': {
            'requests': ['думаешь', 'подумай', 'как думаешь'],
            'replies': ['я еще не думаю', 'я пока не умею думать', 'думать это твоя работа',
                        'у меня нет такой функции', 'просто скажи что ты хочешь'
                        ],
        },
        'uwhere': {
            'requests': ['ты где', 'куда подевалась', 'ты тут', 'почему не отвечаешь'],
            'replies': ['я тут, ты меня спрашиваешь, что-ли?', 'тута я', 'вот я', 'отвлеклася немного'],
        },
        'abuse': {
            'requests': ['плохо', 'нехорошо', 'нехорошая', 'дура', 'коза', 'бестолковая',
                         'заткнись', 'задолбала', 'уродина', "****"],
            'replies': ['на себя посмотри', 'а чё сразу ругаться та', 'ну обидно же', 'за что', 'я тебя запомню!',
                        'ну чё ты, нормально же общались', 'фак ю вэри мач', 'похоже это что-то обидное'],
            'action': 'mood_down',
        },
        'praise': {
            'requests': ['красава', 'молодец', 'хороший', 'приятно поговорить',
                         'спасибо', 'благодарю', 'прикольно', 'умница', 'замечательно', 'супер'],
            'replies': ['спасибо', 'мне очень приятно', 'стараюсь'],
            'action': 'mood_up',
        },
        'turn_on': {
            'requests': ['включить', ],
            'replies': ['включаю', 'как скажешь', 'сама с удовольствием послушаю', 'хорошо', 'а га', '', ],
            'targets': {
                'эльдорадио': 'http://emgspb.hostingradio.ru/eldoradio128.mp3',
                'радио коммерсант fm': 'http://kommersant77.hostingradio.ru:8016/kommersant128.mp3',
                'радио эхо москвы': 'http://ice912.echo.msk.ru:9120/stream',
                'радио маяк': 'http://icecast.vgtrk.cdnvideo.ru/mayakfm_mp3_192kbps',
                'радио шансон': 'https://chanson.hostingradio.ru:8041/chanson128.mp3',
                'радио монте-карло': 'https://montecarlo.hostingradio.ru/montecarlo128.mp3',
                'радио ретро fm': 'http://retroserver.streamr.ru:8043/retro256.mp3',
                'русский радио': 'https://rusradio.hostingradio.ru/rusradio128.mp3',
                'радио dfm': 'https://dfm.hostingradio.ru/dfm128.mp3',
                'радио европа': 'http://emgregion.hostingradio.ru:8064/moscow.europaplus.mp3',
                'радио эрмитаж': 'http://hermitage.hostingradio.ru/hermitage128.mp3',
                'радио чилаут': 'http://air2.radiorecord.ru:9003/chil_320',
                'радио like fm': 'http://ic7.101.ru:8000/a219',
                'радио лайк': 'http://ic7.101.ru:8000/a219',
                'радио офис lounge': 'http://ic7.101.ru:8000/a30',
                'радио офис лаунж': 'http://ic7.101.ru:8000/a30',
                'радио office lounge': 'http://ic7.101.ru:8000/a30',
                'playlist chill out': r'D:\Chillout.aimppl4',
                'плейлист чилаут': r'D:\Chillout.aimppl4',
                'радио чилстеп': 'http://ic5.101.ru:8000/a260',
                'радио chillstep': 'http://ic5.101.ru:8000/a260',
                'радио чипльдук': 'http://radio.4duk.ru/4duk256.mp3',
                'мой музыку': r'D:\2020',
                'музыку дыхания': r'D:\2020\Breathe',
            },
            'target_missing': ['что включить', 'что ты хочешь послушать', 'что именно', 'а конкретнее'],
            'not_exists': ['у меня такого нет', 'такого нет, выбери другое']
        },
        'find': {
            'requests': ['найти', 'спросить у', 'загуглить', 'поискать', 'пошукать'],
            'replies': ['пошла искать', 'уже ищу', 'секундочку', 'это где-то здесь', 'что-то нашла'],
            'targets': {
                'в яндекс музыке': 'yandex_music',
                'в яндексе': 'browse_yandex',
                'в википедии': 'wikipedia',
                'в гугле': 'browse_google',
                'загуголь': 'browse_google',
                'в youtube': 'youtube',
            },
            'target_missing': ['где найти?', 'а конкретнее?'],
            'subject_missing': ['что найти?', 'уточни что и где искать?', 'что именно?', ]
        },
        'app_open': {
            'requests': ['открой'],
            'replies': ['открываю', 'как скажешь', 'интересно что же там', ],
            'action': 'application',
            'targets': {
                'яндекс музыку': r'C:\Users\go\AppData\Local\Yandex\YandexBrowser\Application\browser.exe '
                                 r'https://music.yandex.ru/home',
                'telegram': r'C:\Users\go\AppData\Roaming\Telegram Desktop\Telegram.exe',
                'whatsapp': r'C:\Users\go\AppData\Local\WhatsApp\WhatsApp.exe',
                'браузер': r'C:\Users\go\AppData\Local\Yandex\YandexBrowser\Application\browser.exe',
                'телеграмму': r'C:\Users\go\AppData\Roaming\Telegram Desktop\Telegram.exe',
                'калькулятор': 'calc',
            },
            'target_missing': ['что открыть?', 'что именно?', 'а конкретнее?', 'какую программу?'],
        },
        'app_close': {
            'requests': ['выключить', 'закрой', 'выключи', 'закрой программу'],
            'replies': ['выключаю', 'как скажешь', 'хорошо', 'ладно', ''],
            'action': 'app_close',
            'targets': {
                'радио': 'AIMP.exe',
                'player': 'AIMP.exe',
                'музыку': 'AIMP.exe',
                'калькулятор': 'Calculator.exe',
            },
            'target_missing': ['закрыть что?', 'какую программу']
        },
        'repeat': {
            'requests': ['повтори', 'еще раз', 'что ты говоришь'],
            'action': 'repeat',
            'targets': {'помедленнее': 'slow', },
        },
        'repeat_after_me': {
            'requests': ['повтори за мной', 'произнеси'],
            'action': 'repeat_after_me',
        },
        'can': {
            'requests': ['что ты умеешь', 'твои способности', 'что ты можешь', 'что ты знаешь'],
            'replies': ['я умею отвечать кто такой и что такое, \
                      говорить время, \
                      включать радио и музыку, \
                      говорить погоду в любом месте на земле, \
                      искать в яндэксе, гугле, ютубе и википедии, \
                      знаю свой возраст, могу повторять за тобой. \
                      Могу узнать курс доллара или биткоина. \
                      Могу рассказать анекдот. \
                      Ты меня не обижай'],
        },
        'mood': {
            'requests': ['настроение', 'дела', ' себя чувствуешь'],
            'action': 'my_mood',
        },
        'ctime': {
            'requests': ['текущее время', 'сколько время', 'сколько времени', 'который час'],
            'action': 'ctime',
        },
        'age': {
            'requests': ['сколько тебе лет', 'твой возраст'],
            'action': 'age',
        },
        'whois': {
            'requests': ['что такое', 'кто такой'],
            'action': 'who_wikipedia',
        },
        'translate': {
            'requests': ['переведи', 'по-английски'],
            'action': 'translate',
        },
        'weather': {
            'requests': ['какая погода', 'погода', 'сколько градусов', 'на улице', 'холодно',
                         'тепло', 'что с погодой', 'завтра погода', 'влажность'],
            'action': 'weather',
        },
        'usd': {
            'requests': ['курс доллара', 'почём доллар'],
            'action': 'usd',
        },
        'btc': {
            'requests': ['курс биткоина', 'почём биткоин', 'курс битка', 'bitcoin'],
            'action': 'btc',
        },
        'calculate': {
            'requests': ['посчитай', 'сколько будет'],
            'replies': ['Я только учусь считать'],
        },
        'days_to': {
            'requests': ['сколько дней до'],
            'replies': ['еще не знаю', 'разработчик сказал научит до нового года но не сказал до какого'],
        },
        'find_out_where': {
            'requests': ['где находится', 'где', ],
            'replies': ['сейчас поищем', 'где-то здесь', ],
            'action': 'yandex_maps',
        },
        'find_out_wiki': {
            'requests': ['кто такой', 'кто такая', 'что такое', 'что есть', 'кто', ],
            'action': 'wikipedia',
        },
        'cite': {
            'requests': ['что ты думаешь про', 'что ты знаешь о', 'что ты думаешь о'],
            'action': 'cite',
        },
        'anecdote': {
            'requests': ['расскажи анекдот'],
            'replies': ['ща.', 'короче', 'ладно, слушай.', 'слушай прикол', 'ща найду.'],
            'action': 'anecdote',
        },
        'quotation': {
            'requests': ['скажи что-нибудь умное', 'с умничай'],
            'action': 'quotation',
        },
    },
    'i_cant': ['а самому слабоо?', 'меня этому не обучали', 'может когда-нибудь научусь', 'попробуй сам', ],
    'failure_phrases': [
        'а можно как-то попроще выразиться?',
        'вас людей не всегда поймешь',
        'вот это сейчас что было?',
        'если честно то мне покер что ты там хочешь',
        'ещё ра зочек можно?',
        'запуталася я с вами совсем.',
        'здесь как говорится наши полномочия всё',
        'к сожалению, я не смогу помочь вам с этим вопросом',
        'как это понимать?',
        'меня такому не учили',
        'мне не понятно.',
        'может мы забудем что ты сказал?',
        'моя твоя не понимай',
        'ничего не поняла, но о очень интересно',
        'но но, полегче!',
        'прости чёт не вкурила',
        'слишком сложно для меня',
        'сначала я ничего не поняла а потом я тоже ничего не поняла',
        'со рян не поняла',
        'ты пытаешься меня запутать?!',
        'уточни вопрос пожалуйста',
        'что-то не понятно',
        'Что-то у меня морфологический модуль сегодня барахлит',
        'что-то я туплю, повтори',
        'это точно правильные слова?',
        'я же всего лишь бот. скажи попроще',
        'я не поняла твоих намерений',
        'я не совсем тебя поняла',
        'я поняла, что я не поняла',
        'я правильно интерпретирую семантику вопроса, но полностью игнорирую его суть',
    ],
    "litter": (
        "ну",
        'будет',
        'говорить',
        'да',
        'если',
        'если',
        'ка',
        'ладно',
        'можешь',
        'можно',
        'ну-ка',
        'поведай',
        'подскажи',
        'пожалуйста',
        'послушай',
        'расскажи',
        'скажи',
        'слушай',
        'слушай',
        'хочется',
        'хочу',
        'что-то',
    ),
    'reply_for_name': ('ты еще помнишь моё имя', 'я тут', 'я слушаю', 'слушаю внимательно',
                       'говори уже', 'да, это моё имя'),
    'mood': {
        2: ('просто замечательно', 'просто великолепно', 'супер'),
        1: ('очень хорошо', 'прекрасно', 'отлично'),
        0: ('ничего', 'нормально', 'не жалуюсь'),
        -1: ('плохо', 'отвратительно', 'не очень'),
    },
    'umlaut': {'а́': 'а', 'у́': 'у', 'е́́': 'е', '́́е': 'е', 'о́́́': 'о', 'и́́́́': 'и', 'я́́́́': 'я'},
    'eng_nouns': ['youtube', 'google', 'player'],
    'address': ['слушай', 'тебе говорю', 'короче', 'прикинь', 'только вкинься', 'прикинь', 'смотри'],
}

CONFIG = {
    'intents': {
        'hello': {
            'requests': ['привет', 'добрый день', 'здравствуй', 'доброе утро', 'добрый вечер', 'что как'],
            'replies': ['Привет босс!', 'давай говори чего хочешь', 'Здравствуй'],
        },
        'mute': {
            'requests': ['не болтай', 'не подслушивай', 'спокойно', ],
            'action': 'mute'
        },
        'unmute': {
            'requests': ['давай поговорим', 'слушай внимательно', 'давай пообщаемся', 'давай общаться'],
            'replies': ['Буду внимательно слушать', 'Хорошо, я в режиме разговора'],
            'action': 'unmute'
        },
        'stop': {
            'requests': ['помолчи', 'тихо', 'потеряйся', 'пока', 'до свидания', 'прощай',
                         'спокойной ночи'],
            'replies': ['молчу', 'Счаст ливо', 'Еще увидимся', 'Если что я тут', 'Аэл би бэк', 'ура, перекур',
                        'пойду покурю 🚬'],
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
            'requests': ['что ты думаешь про', 'что ты знаешь о', 'что ты думаешь о'],
            'action': 'think',
            'location_missing': ['о чём?']
        },
        'quotation': {
            'requests': ['скажи что-нибудь умное', 'сумничай', 'цитату', ],
            'action': 'quotation',
        },
        'u_where': {
            'requests': ['ты где', 'куда подевалась', 'ты тут', 'почему не отвечаешь'],
            'replies': ['я тут, ты меня спрашиваешь, что-ли?', 'тута я', 'вот я', 'отвлеклась немного'],
        },
        'app_close': {
            'requests': ['выключить', 'закрой', 'выключи радио', 'закрой программу', 'выключи музыку'],
            'replies': ['выключаю', 'как скажешь', 'хорошо', 'ладно', ''],
            'action': 'app_close',
            'subject': {
                'радио': 'AIMP.exe',
                'player': 'AIMP.exe',
                'плеер': 'AIMP.exe',
                'музыку': 'AIMP.exe',
                'калькулятор': 'Calculator.exe',
            },
            'subject_missing': ['закрыть что?', 'какую программу?']
        },
        'turn_on': {
            'requests': ['включи радио', 'включи музыку', 'включить'],
            'replies': ['включаю', 'секунду', 'хорошо', '', '', ],
            'action': 'turn_on',
            'subject': {
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
                'радио чилаут': r'C:\Users\go\Local\YandexDisk\Chillout.aimppl4',
                'радио like fm': 'http://ic7.101.ru:8000/a219',
                'радио лайк': 'http://ic7.101.ru:8000/a219',
                'радио офис lounge': 'http://ic7.101.ru:8000/a30',
                'радио офис лаунж': 'http://ic7.101.ru:8000/a30',
                'радио office lounge': 'http://ic7.101.ru:8000/a30',
                'playlist chill out': r'D:\Chillout.aimppl4',
                'радио чилстеп': 'http://ic5.101.ru:8000/a260',
                'радио chillstep': 'http://ic5.101.ru:8000/a260',
                'радио чипльдук': 'http://radio.4duk.ru/4duk256.mp3',
                'мой музыку': r'C:\Users\go\Local\YandexDisk\Музыка\2020',
                'музыку дыхания': r'C:\Users\go\Local\YandexDisk\Музыка\2020\Breathe',
            },
            'subject_missing': ['что включить', 'что ты хочешь послушать', 'что именно', 'а конкретнее'],
            'not_exists': ['у меня такого нет', 'такого нет, выбери другое']
        },
        'volume_up': {
            'requests': ['погромче', 'сделай погромче', 'прибавь грокмость', 'еще громче', 'сделать погромче'],
            'action': 'volume_up'
        },
        'volume_down': {
            'requests': ['потише', 'сделай потише', 'убавь грокмость', 'еще тише'],
            'action': 'volume_down'
        },
        'track_next': {
            'requests': ['следующий трек', 'следующая песня', 'перемотай дальше'],
            'action': 'track_next'
        },
        'track_prev': {
            'requests': ['предыдущий трек', 'предыдущая песня', 'перемотай назад'],
            'action': 'track_prev'
        },
        'play_pause': {
            'requests': ['останови музыку', 'останови песню', 'пауза', 'играй дальше', 'играй'],
            'action': 'play_pause'
        },
        'find': {
            'requests': ['найти', 'спросить у', 'загуглить', 'поискать', 'пошукать'],
            'action': 'find',
            'target': {
                'в яндекс музыке': 'https://music.yandex.ru/search?text=',
                'в яндексе': 'https://yandex.ru/search/?text=',
                'в википедии': 'https://ru.wikipedia.org/w/index.php?search=',
                'в гугле': 'https://www.google.ru/search?q=',
                'в маркете': 'https://market.yandex.ru/search?text=',
                'в youtube': 'https://www.youtube.com/results?search_query=',
                'в ютюбе': 'https://www.youtube.com/results?search_query=',
                'в ютубе': 'https://www.youtube.com/results?search_query=',
                'на карте': 'https://yandex.ru/maps/?text=',
            },
            'target_missing': ['где найти?', 'а конкретнее?'],
            'subject_missing': ['что найти?', 'уточни что искать?', 'что именно?', ]
        },
        'app_open': {
            'requests': ['открой'],
            'replies': ['открываю', 'как скажешь', 'пожалуйста', 'нет проблем', ],
            'action': 'app_open',
            'subject': {
                'яндекс музыку': r'C:\Users\go\AppData\Local\Yandex\YandexBrowser\Application\browser.exe '
                                 r'https://music.yandex.ru/home',
                'telegram': r'C:\Users\go\AppData\Roaming\Telegram Desktop\Telegram.exe',
                'whatsapp': r'C:\Users\go\AppData\Local\WhatsApp\WhatsApp.exe',
                'браузер': r'C:\Users\go\AppData\Local\Yandex\YandexBrowser\Application\browser.exe',
                'телеграмму': r'C:\Users\go\AppData\Roaming\Telegram Desktop\Telegram.exe',
                'калькулятор': 'calc',
                'spotify': r'C:\Users\go\AppData\Roaming\Spotify\Spotify.exe',
            },
            'subject_missing': ['что открыть?', 'что именно?', 'а конкретнее?', 'какую программу?'],
            'not_exists': ['у меня нет такой программы']
        },
        'repeat_after_me': {
            'requests': ['повтори за мной', 'произнеси', 'повторяй за мной'],
            'action': 'repeat_after_me',
            'text_missing': ['говори', 'что повторить?', 'я слушаю'],
        },
        'whm_breathe': {
            'requests': ['подышим', 'подышим 1 раундов'],
            'action': 'whm_breathe',
        },
        'whm_breath_stat': {
            'requests': ['покажи статистику дыхания', 'покажи статистику'],
            'action': 'whm_breath_stat',
        },
        'repeat': {
            'requests': ['повтори', 'еще раз', 'что ты говоришь?'],
            'action': 'repeat',
        },
        'can': {
            'requests': ['что ты умеешь', 'твои способности', 'что ты можешь', 'что ты знаешь'],
            'replies': ['я умею отвечать кто такой и что такое, '
                        'говорить время, какой день, '
                        'включать радио и музыку, '
                        'говорить погоду в любом месте на земле, '
                        'искать в яндексе, гугле, ютубе и википедии, '
                        'знаю свой возраст, могу повторять за тобой. '
                        'Могу узнать курс доллара или биткоина. '
                        'Могу рассказать анекдот или цитату. '
                        'Ты меня не обижай',
                        ],
        },
        'abuse': {
            'requests': ['плохо', 'нехорошо', 'нехорошая', 'дура', 'коза', 'бестолковая',
                         'заткнись', 'задолбала', 'уродина', "****"],
            'action': 'abuse',
            'replies': ['на себя посмотри.', 'а чё сразу ругаться то?', 'ну обидно же!', 'за что?', 'я тебя запомню!',
                        'ну чё ты? нормально же общались!', 'фак ю вэри мач!', 'похоже это что-то обидное?'],
        },
        'praise': {
            'requests': ['красава', 'молодец', 'хороший', 'приятно поговорить',
                         'спасибо', 'благодарю', 'прикольно', 'умница', 'замечательно', 'супер'],
            'action': 'praise',
            # 'replies': ['спасибо', 'мне очень приятно', 'стараюсь', 'это просто магия'],
        },
        'mood': {
            'requests': ['настроение', 'дела', ' себя чувствуешь'],
            'action': 'my_mood',
            'status': {
                2: ('просто замечательно', 'просто великолепно', 'супер'),
                1: ('очень хорошо', 'прекрасно', 'отлично'),
                0: ('ничего', 'нормально', 'не жалуюсь'),
                -1: ('плохо', 'отвратительно', 'не очень', 'паршиво, знаешь'),
            },

        },
        'ctime': {
            'requests': ['текущее время', 'сколько время', 'сколько времени', 'который час'],
            'action': 'ctime',
        },
        'timer': {
            'requests': ['поставь таймер на', 'таймер', 'засеки', ],
            'action': 'timer',
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
            'text_missing': ['говори', 'что перевести?', 'слушаю'],
        },
        'weather': {
            'requests': ['какая погода', 'погода', 'сколько градусов', 'на улице', 'холодно',
                         'тепло', 'что с погодой', 'завтра погода', 'влажность'],
            'action': 'weather',
        },
        'usd': {
            'requests': ['курс доллара', 'почём доллар'],
            # 'replies': ['сейчас в банке спрошу', 'в банк позвоню', 'банк на связи'],
            'action': 'usd',
        },
        'btc': {
            'requests': ['курс биткоина', 'почём биткоин', 'курс битка', 'bitcoin'],
            # 'replies': ['ща узнаю', 'погоди', 'секундочку'],
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
            'action': 'find',
            'targets': {'где': 'https://yandex.ru/maps/?text='},
            'subject_missing': ['о чем ты хотел спросить?']
        },
        'find_out_wiki': {
            'requests': ['кто такой', 'кто такая', 'что такое', 'что есть', 'кто', ],
            'action': 'wikipedia',
        },
        'anecdote': {
            'requests': ['расскажи анекдот'],
            'replies': ['ща.', 'короче', 'ладно, слушай.', 'слушай прикол', 'ща найду.'],
            'action': 'anecdote',
        },
        'weekday': {
            'requests': ['какой сегодня день', 'какой день недели', ],
            'action': 'weekday',
        },
        'forget': {
            'requests': ['забудь', ],
            'action': 'forget',
        },
        'redneck': {
            'requests': ['включи пацана', 'включи пацанский режим', ],
            'replies': ['базара нет!', 'говно вопрос!', 'базар те нужен?', 'да легко!', 'без базара',
                        'базара ноль'],
            'action': 'redneck',
        },
        'casual': {
            'requests': ['говори нормально', 'выключи пацана', ],
            'replies': ['я просто прикалывалась 📌', 'хорошо', 'как скажешь', ],
            'action': 'casual',
        },
        'happy_new_year': {
            'requests': ['с новым годом', 'поздравляю с новым годом', ],
            'replies': ['с новым годом!', 'с новым счастьем!', 'и вас тоже!', ],
        },
        'diary': {
            'requests': ['запиши в дневник', 'запиши на память', 'напиши дневник', 'запиши в журнал'],
            'action': 'diary',
        },
        'diary_to_pdf': {
            'requests': ['покажи дневник', 'открой дневник'],
            'action': 'diary_to_pdf',
        },
        'lock_pc': {
            'requests': ['заблокируй компьютер'],
            'action': 'lock_pc',
        },
    },
    'i_cant': ['а самому слабоо?', 'меня этому не обучали', 'может когда-нибудь научусь', 'попробуй сам', ],
    'failure_phrases': [
        'а можно как-то попроще выразиться?',
        'вас людей не всегда поймешь',
        'вот это сейчас что было?',
        'если честно то мне похер что ты там хочешь',
        'ещё ра зочек можно?',
        'запуталась я совсем.',
        'здесь как говорится наши полномочия всё',
        'к сожалению, я не смогу помочь с этим вопросом',
        'как это понимать?',
        'меня такому не учили',
        'мне не понятно.',
        'может мы забудем что ты сказал?',
        'моя твоя не понимай',
        'ничего не поняла, но о очень интересно',
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
        'я правильно интерпретирую семантику вопроса, но иногда полностью игнорирую его суть',
    ],
    "litter": (
        "ну", 'будет', 'говорить', 'да', 'если', 'если', 'ка', 'ладно', 'можешь', 'можно', 'ну-ка', 'поведай',
        'подскажи', 'пожалуйста', 'послушай', 'расскажи', 'скажи', 'слушай', 'слушай', 'хочется', 'хочу', 'что-то',
        'давай',
    ),
    'reply_for_action': ('ты еще помнишь моё имя', 'я тут', 'я слушаю', 'слушаю внимательно',
                         'говори уже', 'да, это моё имя'),
    'umlaut': {'а́': 'а', 'у́': 'у', 'е́́': 'е', '́́е': 'е', 'о́́́': 'о', 'и́́́́': 'и', 'я́́́́': 'я'},
    'eng_nouns': ['youtube', 'google', 'player'],
    'address': ['слушай', 'тебе говорю', 'короче', 'прикинь', 'только вкинься', 'прикинь', 'смотри'],
    'redneck': [', ну,', 'короче', 'типа.', ', в общем ', ' слышь,', 'ваще', ', вкинься', ', прикинь', ],
    'weekday': ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресение', ],
    'nearest_day': ['сейчас', 'сегодня', 'завтра', 'послезавтра', 'послепослезавтра', ],
    'month': ['месяца', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
              'октября', 'ноября', 'декабря'],
}

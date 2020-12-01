import requests


def units_ru(number: int, span='days'):
    ending = {
        'hours': {0: 'часов', 1: 'час', 2: 'часа'},
        'minutes': {0: 'минут', 1: 'минутa', 2: 'минуты'},
        'days': {0: 'дней', 1: 'день', 2: 'дня'},
        'deg': {0: 'градусов', 1: 'градус', 2: 'градуса'},
        'deg_neg': {0: 'градусов', 1: 'градуса', 2: 'градусов'},  # в родительном (от 0 до 21 градуса)
        'm': {0: 'метров', 1: 'метр', 2: 'метра'},
        'perc': {0: 'процентов', 1: 'процент', 2: 'процента'},
        'rub': {0: 'рублей', 1: 'рубль', 2: 'рубля'},
        'usd': {0: 'долларов', 1: 'доллар', 2: 'доллара'},
        'kop': {0: 'копеек', 1: 'копейка', 2: 'копейки'},
    }

    if abs(number) in [0, 11, 12, 13, 14]:
        e = ending[span][0]
    elif abs(number) % 10 == 1:
        e = ending[span][1]
    elif abs(number) % 10 in [2, 3, 4]:
        e = ending[span][2]
    else:
        e = ending[span][0]

    return ' ' + str(number) + ' ' + e + ' '


def timedelta_to_dhms(duration):
    # преобразование в дни, часы, минуты и секунды
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds


def request_yandex_fast(request):
    response = requests.post('https://yandex.ru/search/?text=' + request)
    html = response.text
    html = html.partition('<div class="fact-answer')[2]
    html = html.partition('>')[2]
    html = html.partition('</div>')[0]
    html = html.replace('<b>', '')
    html = html.replace('</b>', '')
    return html


def btc():
    response = requests.get('https://api.blockchain.com/v3/exchange/tickers/BTC-USD')
    if response.status_code == 200:
        return '1 биткоин' + str(units_ru(int(response.json()['last_trade_price']), 'usd'))

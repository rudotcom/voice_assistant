import requests
import pymorphy2
import time
import threading
from va_assistant import assistant

morph = pymorphy2.MorphAnalyzer()


def num_unit(number: int, span: str):
    """ согласование слова с числительным """
    phrase = morph.parse(span)[0].make_agree_with_number(abs(number)).word
    return ' '.join([str(number), phrase])


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
        return '1 биткоин ' + str(num_unit(int(response.json()['last_trade_price']), 'доллар'))


def integer_from_phrase(phrase):
    for word in phrase.split():
        p = morph.parse(word)[0]
        if 'NUMB' in p.tag:
            # TODO: дописать преобразование числителных в число
            return word


class TimerThread(threading.Thread):
    def __init__(self, minutes, reminder=''):
        threading.Thread.__init__(self)
        self.daemon = True
        self.minutes = minutes
        self.reminder = reminder

    def run(self):
        assistant.speak(num_unit(self.minutes, 'минута') + ' Время пошло')
        seconds = self.minutes * 60
        time.sleep(seconds)
        # Показываем текст напоминания
        if self.reminder:
            self.reminder = 'Ты просил напомнить, ' + self.reminder
        else:
            self.reminder = 'Время вышло. Ты просил напомнить'
        assistant.speak(self.reminder)


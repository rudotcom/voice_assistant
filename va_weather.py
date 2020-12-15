"""
Модуль получения погоды. Возвращает текст с погодой или прогнозом погоды
"""
import requests
from va_assistant import context
import pymorphy2

ow_api_key = '4d51145e022c6c17ebe4fd2107710da4'


def pos(word, morph=pymorphy2.MorphAnalyzer()):
    "Return a likely part of speech for the *word*."""
    return morph.parse(word)[0].tag.POS


def wind_dir(deg):
    if 23 <= deg < 68:
        return 'северо-восточный'
    elif 68 <= deg < 113:
        return 'восточный'
    elif 113 <= deg < 158:
        return 'юго-восточный'
    elif 158 <= deg < 203:
        return 'южный'
    elif 203 <= deg < 248:
        return 'юго-западный'
    elif 248 <= deg < 293:
        return 'западный'
    elif 293 <= deg < 338:
        return 'северо-западный'
    else:
        return 'северный'


def weather_now(in_city, key=ow_api_key):
    city = city_nominal(in_city)
    url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + key + '&units=metric&lang=ru&q=' + city

    response = requests.post(url)
    if response.status_code == 200:
        json = response.json()
        description = str(json['weather'][0]['description'])
        degrees = int(json['main']['temp'])
        wind = int(json['wind']['speed'])
        direction = wind_dir(int(json['wind']['deg']))
        # humidity = json['main']['humidity']
        if 'rain' in json:
            rain = 'не забудь зонтик'
        else:
            rain = ''

        return 'сейчас {} {} {} градус,\nВетер {}, {} метр в секунду. {}'.format(in_city, description, degrees,
                                                                                 direction,
                                                                                 wind, rain)
    elif response.status_code == 404:
        context.location = ''
        return city + '. Я не знаю такого города'
    else:
        print(response.status_code)


def weather_forecast(in_city, day, key=ow_api_key):
    city = city_nominal(in_city)
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' + city + \
          '&cnt=' + str(day) + '&appid=' + key + '&lang=ru&units=metric'

    response = requests.post(url)
    if response.status_code == 200:
        json = response.json()['list'][day - 1]
        desc = json['weather'][0]['description']
        t_min = str(int(json['temp']['min']))
        t_max = str(int(json['temp']['max']))
        wind = str(int(json['speed']))
        direction = wind_dir(int(json['deg']))
        # humidity = json['humidity']
        if t_min != t_max:
            temperature = ' от ' + t_min + ' до ' + t_max + ' градуса'
        else:
            temperature = str(int(t_min)) + ' градус'

        return '{} {} {} {},\nВетер {} {} метр в секунду'.format(context.adverb, in_city, desc, temperature,
                                                                  direction, wind)


def city_nominal(city, morph=pymorphy2.MorphAnalyzer()):
    functors_pos = {'PREP', 'CONJ'}  # function words
    city = ' '.join(word for word in city.split() if pos(word) not in functors_pos)
    city = morph.parse(city)[0][2]
    return city


def open_weather(city='', days_ahead=''):
    city = city.replace(' на улице', '').strip()
    if not city:
        city = 'в Санкт-Петербурге'
    if days_ahead:
        return weather_forecast(city, days_ahead)
    else:
        return weather_now(city)

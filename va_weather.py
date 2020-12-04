import requests
from va_assistant import context
from va_misc import num_unit
import pymorphy2

ow_api_key = '4d51145e022c6c17ebe4fd2107710da4'


def pos(word, morph=pymorphy2.MorphAnalyzer()):
    "Return a likely part of speech for the *word*."""
    return morph.parse(word)[0].tag.POS


def weather_now(key=ow_api_key):
    city = city_nominal(context.location)
    url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + key + '&units=metric&lang=ru&q=' + city

    response = requests.post(url)
    if response.status_code == 200:
        json = response.json()
        description = str(json['weather'][0]['description'])
        degrees = str(num_unit(int(json['main']['temp']), 'градус'))
        wind = str(num_unit(int(json['wind']['speed']), 'метр'))
        humidity = str(num_unit(json['main']['humidity'], 'процент'))

        return 'сейчас {} {}, {},\nВетер {},\nВлажность {}'.format(context.location, description, degrees, wind, humidity)


def weather_forecast(day, key=ow_api_key):
    city = city_nominal(context.location)
    print(city)
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' + city + \
          '&cnt=' + str(day) + '&appid=' + key + '&lang=ru&units=metric'

    response = requests.post(url)
    if response.status_code == 200:
        json = response.json()['list'][day - 1]
        desc = str(json['weather'][0]['description'])
        t_min = str(int(json['temp']['min']))
        t_max = str(int(json['temp']['max']))
        wind = str(num_unit(int(json['speed']), 'метр'))
        humidity = str(num_unit(json['humidity'], 'процент'))
        if t_min != t_max:
            temperature = ' от ' + t_min + ' до ' + num_unit(int(t_max), 'градуса')
        else:
            temperature = num_unit(int(t_min), 'градус')

        return '{} {} {}\n{},\nВетер {},\nВлажность {}'.format(context.adverb, context.location, desc, temperature,
                                                               wind, humidity)


def city_nominal(city, morph=pymorphy2.MorphAnalyzer()):
    if city == '':
        city = 'в Санкт-Петербурге'
    functors_pos = {'PREP', 'CONJ'}  # function words
    city = ' '.join(word for word in city.split() if pos(word) not in functors_pos)
    city = morph.parse(city)[0][2]
    return city


def open_weather():
    when = context.adverb
    if when in ['послепослезавтра', 'через день']:
        return weather_forecast(3)
    elif when == 'послезавтра':
        return weather_forecast(2)
    elif when == 'завтра':
        return weather_forecast(1)
    elif when == 'сегодня':
        return weather_forecast(0)
    else:
        return weather_now()

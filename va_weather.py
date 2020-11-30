import requests
from va_misc import units_ru
import pymorphy2

ow_api_key = '4d51145e022c6c17ebe4fd2107710da4'


def pos(word, morth=pymorphy2.MorphAnalyzer()):
    "Return a likely part of speech for the *word*."""
    return morth.parse(word)[0].tag.POS


def weather_now(city, key=ow_api_key):
    city = city_nominal(city)
    url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + key + '&units=metric&lang=ru&q=' + city

    response = requests.post(url)
    if response.status_code == 200:
        json = response.json()

        return location + ' ' + \
                        str(json['weather'][0]['description']) + ' ' + \
                        str(units_ru(int(json['main']['temp']), 'deg')) + \
                        ', Ветер ' + str(units_ru(int(json['wind']['speed']), 'm')) + \
                        ', Влажность ' + str(units_ru(json['main']['humidity'], 'perc'))


def weather_forecast(city, day, key=ow_api_key):
    city = city_nominal(city)
    print(city)
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' + city + \
          '&cnt=' + str(day) + '&appid=' + key + '&lang=ru&units=metric'

    response = requests.post(url)
    if response.status_code == 200:
        json = response.json()['list'][day - 1]
        desc = str(json['weather'][0]['description'])
        t_min = str(int(json['temp']['min']))
        t_max = str(int(json['temp']['max']))
        wind = str(units_ru(int(json['speed']), 'm'))

        weather = location + ' ' + desc
        if t_min != t_max:
            weather += ' от ' + t_min + ' до' + units_ru(int(t_max), 'deg_neg')
        else:
            weather += units_ru(int(t_min), 'deg')

        weather += ', Ветер ' + str(units_ru(int(json['speed']), 'm'))
        weather += ', Влажность ' + str(units_ru(json['humidity'], 'perc'))
        return weather


def city_nominal(city, morph=pymorphy2.MorphAnalyzer()):
    if city == '':
        city = 'в Санкт-Петербурге'
    functors_pos = {'PREP', 'CONJ'}  # function words
    city = ' '.join(word for word in city.split() if pos(word) not in functors_pos)
    city = morph.parse(city)[0][2]
    return city


def open_weather(request):
    global location
    location = request
    if 'послепослезавтра' in request:
        request = (request.replace('послепослезавтра', '')).strip()
        return weather_forecast(request, 3)
    elif 'послезавтра' in request:
            request = (request.replace('послезавтра', '')).strip()
            return weather_forecast(request, 2)
    elif 'завтра' in request:
        request = (request.replace('завтра', '')).strip()
        print('req;', request)
        return weather_forecast(request, 1)
    elif 'сегодня' in request:
        request = (request.replace('сегодня', '')).strip()
        return weather_forecast(request, 0)
    else:
        request = (request.replace('сейчас', '')).strip()
        return weather_now(request)

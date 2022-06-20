import requests
from datetime import datetime
from aiogram.types import InputFile


def get_weather(lat, lon):
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=A38F35208F286B933F4763D53096AE2F&units=metric').json()

    weatherPhoto = ''
    smile = ''
    weatherData = {"Clear": ["ясно \U00002600", InputFile(path_or_bytesio='Media/ClearWeather.jpg')],
                   "Clouds": ["пасмурно \U00002601", InputFile(path_or_bytesio='Media/CloudsWeather.jpg')],
                   "Rain": ["дождь \U00002614", InputFile(path_or_bytesio='Media/RainWeather.jpg')],
                   "Drizzle": ["моросит \U00002614", InputFile(path_or_bytesio='Media/DrizzleWeather.jpg')],
                   "Thunderstorm": ["гроза \U000026A1", InputFile(path_or_bytesio='Media/ThunderstormWeather.jpg')],
                   "Snow": ["снег \U0001F328", InputFile(path_or_bytesio='Media/SnowWeather.jpg')],
                   "Mist": ["туман \U0001F32B", InputFile(path_or_bytesio='Media/MistWeather.jpg')]
                   }

    if response['weather'][0]['main'] in weatherData:
        smile = weatherData[response['weather'][0]['main']][0]
        weatherPhoto = weatherData[response['weather'][0]['main']][1]

    data = {'city': response['name'],
            'temp': response['main']['temp'],
            'wind': response['wind']['speed'],
            'sunrise': datetime.fromtimestamp(response['sys']['sunrise']).strftime("%H:%M"),
            'sunset': datetime.fromtimestamp(response['sys']['sunset']).strftime("%H:%M"),
            'data_now': datetime.today().strftime("%d.%m.%Y %H:%M"),
            'smile': smile,
            'weatherPhoto': weatherPhoto
            }

    return data

# http://api.openweathermap.org/data/2.5/weather?lat=54.075526&lon=52.534621&appid=A38F35208F286B933F4763D53096AE2F&units=metric&lang=ru

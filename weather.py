from flask import Flask
import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('API_key')


@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int


def get_lat_lon(city_name, state_code, country_code, API_key):
    resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit=&appid={API_key}').json()
    data = resp[0]

    lat = data.get('lat')
    lon = data.get('lon')
    return lat, lon



def get_current_weather(lat, lon, API_key):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    # print(resp)
    data = WeatherData(
        main=resp.get('weather')[0].get('main').capitalize(),
        description=resp.get('weather')[0].get('description').capitalize (),
        icon=resp.get('weather')[0].get('icon'),
        temperature=int(resp.get('main').get('temp'))
    )

    return data


def main(city_name, state_name, country_name):
    lat, lon = get_lat_lon(city_name, state_name, country_name, api_key)
    weather_data = get_current_weather(lat, lon, api_key)
    return weather_data




if __name__ == "__main__":
    lat, lon = get_lat_lon('Lagos', 'Lagos', 'Nigeria', api_key)
    print(get_current_weather(lat, lon, api_key))
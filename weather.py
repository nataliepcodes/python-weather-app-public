import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from antarctica_research_stations import stations_list
import datetime

load_dotenv()
weather_api_key = os.getenv('WEATHER_API_KEY')
geocoding_api_key = os.getenv('GEO_API_KEY')

@dataclass
class CurrentWeatherData:
    # This information will be accessed from API JSON data
    location: str
    condition: str
    icon: str
    temp_c: int
    feelslike_c: str
    humidity: int

@dataclass
class ForecastWeatherData:
    date_list: list
    icon_list: list
    temp_list: list


# Get location latitude and longitude for cities
def get_lat_lon_city(name):
    """ Geocoding API call for a city"""
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={name}&appid={weather_api_key}&units=metric').json()
    lat = response.get('coord').get('lat')
    lon = response.get('coord').get('lon')
    
    return lat, lon


# Get location latitude and longitude for Antarctica and its base stations
def get_lat_lon_antarctica_stations(name):
    """ Geocoding API call for a Antarctica stations """
    # LocationIQ API call
    response = requests.get(f'https://us1.locationiq.com/v1/search?key={geocoding_api_key}&q={name}&format=json').json()
    lat = response[0]['lat']
    lon = response[0]['lon']

    return lat, lon


# Filtering location between the city, Antarctica research stations and others
def filter_location(name):
    if name in stations_list:
        lat, lon = get_lat_lon_antarctica_stations(name)
    elif name == 'South Pole':
        lat, lon =  -90.0000, 0.0000
    elif name == 'Isle of Sky':
        lat, lon = 57.3619,  -6.24727
    else:
        lat, lon = get_lat_lon_city(name)

    return lat, lon


# Get location current / today's weather data
def get_current_weather(name):
    lat, lon = filter_location(name)

    # API call for location weather data
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric').json()
   
    data = CurrentWeatherData(
        location = response.get('name'),
        condition = response.get('weather')[0].get('description').title(),
        icon = response.get('weather')[0].get('icon'),
        temp_c = round(response.get('main').get('temp')),
        feelslike_c = round(response.get('main').get('feels_like')),
        humidity = round(response.get('main').get('humidity')),
    )

    return data


# Get location 5-day forecast weather data (note: response gives weather every 3-hours)
# Time slots: 01:00, 04:00, 07:00, 10:00, 13:00, 16:00, 19:00, 22:00
def get_forecast(name):
    lat, lon = filter_location(name)
    response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric').json()
    
    dates, icons, temps = [], [], []

    # Response gives weather every 3-hours. This program takes first occurence of next day
    today = datetime.date.today()

    for item in response['list']:
        dt = item['dt']
        icon = item['weather'][0]['icon']
        temp = round(item['main']['temp'])
        date_stamp = datetime.datetime.fromtimestamp(dt) # 2025-05-08 13:00:00
        current_date = date_stamp.date()

        if current_date == today:
            continue

        hour = date_stamp.hour # 13

        # Collecting data from mid-day data set
        if hour != 13:
            continue  # Only taking the 13:00:00 slot


        dates.append(current_date.strftime('%A')) # '%A %d %B %Y' >> Wednesday 07 May 2025
        icons.append(icon)
        temps.append(temp)


    data = ForecastWeatherData(
        date_list = dates,
        icon_list = icons,
        temp_list = temps
    )

    return data


get_forecast('Edinburgh')

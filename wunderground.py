#!/usr/bin/env python3
"""
Retrieve weather with Python 3 script and wunderground.com API

Api doc: https://www.wunderground.com/weather/api/d/docs?d=data/index&MR=1

Request:
GET http://api.wunderground.com/api/insert_api_key/features/settings/q/query.format

Stratus plan features:
* Geolookup: geolookup
* Autocomplete: ?
* Current conditions: conditions
* 3-day forecast summary: forecast
* Astronomy: astronomy
* Almanac for today: almanac

Settings:
* lang:FR
* pws:0 (no personal weather station)

Notes:
* Pressure: sea level standard is about 1,013 millibars.
"""
import json
import os
import urllib.request
from pprint import pprint

base_url = 'http://api.wunderground.com/api/'
my_key = os.environ['WUNDERGROUND_KEY']
settings = 'lang:FR/'
location = os.environ['LOCATION']

forecast = base_url + my_key + '/forecast/' + settings + 'q/' + location + '.json'
conditions = base_url + my_key + '/conditions/' + settings + 'q/' + location + '.json'
astronomy = base_url + my_key + '/astronomy/' + settings + 'q/' + location + '.json'


def print_astronomy():
    d = get_data(astronomy)
    sunrise = d['sun_phase']['sunrise']['hour'] + ':' + d['sun_phase']['sunrise']['minute']
    sunset = d['sun_phase']['sunset']['hour'] + ':' + d['sun_phase']['sunset']['minute']
    phase = d['moon_phase']['phaseofMoon']

    print('Lever du soleil:', sunrise)
    print('Coucher du soleil:', sunset)
    print('Phase de la lune:', phase)
    return


def print_conditions():
    d = get_data(conditions)
    current = d['current_observation']

    city = current['display_location']['city']
    local_time = current['local_time_rfc822']
    temp_c = current['temp_c']
    feelslike_c = current['feelslike_c']
    weather = current['weather']
    r_humidity = current['relative_humidity']
    win_dir = current['wind_dir']
    wind_kph = current['wind_kph']
    wind_gust_kph = current['wind_gust_kph']
    pressure_mb = current['pressure_mb']

    pressure_trend = current['pressure_trend']  # rising, falling, steady
    if pressure_trend == '-':
        trend = 'falling'
    elif pressure_trend == '+':
        trend = 'rising'
    else:
        trend = 'steady'

    observation_time = current['observation_time']
    observation_location = current['observation_location']['full']
    station_id = current['station_id']

    precip_1hr_metric = current['precip_1hr_metric']
    precip_today_metric = current['precip_today_metric']
    visibility_km = current['visibility_km']
    windchill_c = current['windchill_c']

    print(city, local_time)
    print(temp_c, 'C', weather)
    print()
    print('Humidité:', r_humidity, '(' + feelslike_c, 'C' + ')')
    print('Pression:', pressure_mb, 'mb', trend)
    print('Vents', win_dir, wind_kph, 'km/h',
          'avec rafales', wind_gust_kph, 'km/h')
    print()
    print(observation_time)
    print(observation_location)
    print(station_id)
    # pprint(current)
    return


def get_data(url):
    with urllib.request.urlopen(url) as response:
        r = response.read()
        data = json.loads(r.decode('utf-8'))
    return data


print_conditions()
print()
print_astronomy()

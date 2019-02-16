#!/usr/bin/env python3
"""
Personal weather report with Python 3 script and wunderground.com API

Api doc:
https://www.wunderground.com/weather/api/d/docs?d=data/index&MR=1

Request:
http://api.wunderground.com/api/insert_api_key/features/settings/q/query.format

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
* Key and location stored in environment variables.
* Pressure: sea level standard is about 1,013 millibars.
"""
import json
import os
import time
import urllib.request

base_url = 'http://api.wunderground.com/api/'
my_key = os.environ['WUNDERGROUND_KEY']

# Location example 'Australia/Sydney', pws:KCASANFR70, KJFK (aircodes)
location = os.environ['LOCATION']

settings = 'lang:FR'

astronomy = "".join(
    [base_url, my_key, '/astronomy/', settings, '/q/', location, '.json'])
conditions = "".join(
    [base_url, my_key, '/conditions/', settings, '/q/', location, '.json'])
forecast = "".join(
    [base_url, my_key, '/forecast/', settings, '/q/', location, '.json'])
everything = "".join(
    [base_url, my_key, '/astronomy/conditions/forecast/', settings, '/q/',
     location, '.json'])


def get_data(url):
    # Takes a url and return json data

    with urllib.request.urlopen(url) as response:
        r = response.read()
        data = json.loads(r.decode('utf-8'))
    return data


def print_astronomy(data):
    # print astronomy data

    if not data:
        data = get_data(astronomy)

    sunrise = ":".join([data['sun_phase']['sunrise']['hour'],
                        data['sun_phase']['sunrise']['minute']])
    sunset = ":".join([data['sun_phase']['sunset']['hour'],
                       data['sun_phase']['sunset']['minute']])
    phase = data['moon_phase']['phaseofMoon']

    print('Lever du soleil:', sunrise)
    print('Coucher du soleil:', sunset)
    print('Phase de la lune:', phase)
    return


def print_conditions(data):
    # print current conditions

    if not data:
        data = get_data(conditions)

    current = data['current_observation']

    city = current['display_location']['city']
    temp_c = current['temp_c']

    # What it feels like. heat index or windchill
    feelslike_c = current['feelslike_c']

    weather = current['weather']
    r_humidity = current['relative_humidity']
    win_dir = current['wind_dir']
    wind_kph = current['wind_kph']
    wind_gust_kph = current['wind_gust_kph']

    # some stations return pressure with '-' before the measure. (-9987)
    pressure_mb = current['pressure_mb'].lstrip('-')

    pressure_trend = current['pressure_trend']
    if pressure_trend == '-':
        # falling
        trend = 'en baisse'
    elif pressure_trend == '+':
        # rising
        trend = 'à la hausse'
    else:
        # steady
        trend = 'stable'

    observation_time = current['observation_time']
    observation_location = current['observation_location']['full']
    station_id = current['station_id']
    forecast_url = current['forecast_url']

    print(city, time.strftime('%H:%M', time.localtime()))
    if temp_c == int(feelslike_c):
        print(temp_c, 'C')
    else:
        print(temp_c, 'C', '(', feelslike_c, 'C', ')')

    print(weather)
    print()
    print('Humidité:', r_humidity)
    print('Pression:', pressure_mb, 'mb', trend)
    print('Vents:', win_dir, wind_kph, 'km/h',
          'avec rafales', wind_gust_kph, 'km/h')
    print()
    print(observation_time)
    print(observation_location, '(', station_id, ')')
    print(forecast_url)
    return


def print_forecast(data):
    # print 3 days forecast

    if not data:
        data = get_data(forecast)
    fc = data['forecast']['simpleforecast']['forecastday']
    print("Prévisions pour aujourd'hui et les 3 prochains jours:")
    print()
    for i in fc:
        period = i['period']
        day = i['date']['day']
        monthname = i['date']['monthname']
        weekday = i['date']['weekday']
        year = i['date']['year']

        avehumidity = i['avehumidity']
        avewind_dir = i['avewind']['dir']
        avewind_kph = i['avewind']['kph']
        conditions = i['conditions']
        high = i['high']['celsius']
        low = i['low']['celsius']
        pop = i['pop']  # prob of precipitations
        qpf_allday = i['qpf_allday']['mm']  # rain
        snow_allday = i['snow_allday']['cm']

        if period == 1:
            print("Aujourd'hui", weekday, day, monthname, year)
        else:
            print(weekday.capitalize(), day, monthname, year)

        print(high, '/', low, 'celsius')
        print(conditions)
        print('Humidité:', avehumidity, '%')
        print('Vent:', avewind_dir, avewind_kph, 'km/h')

        if pop > 0:
            print('Précipitation:', pop, '%')
            if qpf_allday > 0:
                print(qpf_allday, 'mm', 'de pluie')
            if snow_allday > 0:
                print(snow_allday, 'cm', 'de neige')
        print()


def print_report():
    # print current conditions and detailed 3 days forecast

    weather_data = get_data(everything)

    print_conditions(weather_data)
    print()
    print_forecast(weather_data)
    print()
    print_astronomy(weather_data)
    return


def print_txt_forecast(data):
    # print one line per period forecast

    if not data:
        data = get_data(forecast)
    fc = data['forecast']['txt_forecast']['forecastday']

    for i in fc:
        print(i['title'].capitalize(), ':', i['fcttext_metric'])


def print_txt_report():
    # print current conditions and txt forecast

    weather_data = get_data(everything)

    print_conditions(weather_data)
    print()
    print_txt_forecast(weather_data)
    print()
    print_astronomy(weather_data)
    return


print_txt_report()

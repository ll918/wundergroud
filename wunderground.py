#!/usr/bin/env python3
"""
Personal weather report with Python 3 script and wunderground.com API

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
* Key and location stored in environment variables.
* Pressure: sea level standard is about 1,013 millibars.
"""
import json
import os
import urllib.request
import time

base_url = 'http://api.wunderground.com/api/'
my_key = os.environ['WUNDERGROUND_KEY']
settings = 'lang:FR'
location = os.environ['LOCATION']  # Example 'Australia/Sydney'

astronomy = base_url + my_key + '/astronomy/' + settings + '/q/' + location + '.json'
conditions = base_url + my_key + '/conditions/' + settings + '/q/' + location + '.json'
forecast = base_url + my_key + '/forecast/' + settings + '/q/' + location + '.json'

# TODO: use 1 combined request when printing everything at same time
everything = base_url + my_key + '/astronomy/conditions/forecast/' + settings + 'q/' + location + '.json'


def get_data(url):
    # Takes a url and return json data

    with urllib.request.urlopen(url) as response:
        r = response.read()
        data = json.loads(r.decode('utf-8'))
    return data


def print_astronomy():
    # print astronomy data

    d = get_data(astronomy)
    sunrise = d['sun_phase']['sunrise']['hour'] + ':' + \
              d['sun_phase']['sunrise']['minute']
    sunset = d['sun_phase']['sunset']['hour'] + ':' + d['sun_phase']['sunset'][
        'minute']
    phase = d['moon_phase']['phaseofMoon']

    print('Lever du soleil:', sunrise)
    print('Coucher du soleil:', sunset)
    print('Phase de la lune:', phase)
    return


def print_conditions():
    # print current conditions

    d = get_data(conditions)
    current = d['current_observation']

    city = current['display_location']['city']
    local_time = current['local_time_rfc822']  # personalize
    local_epoch = current['local_epoch']
    temp_c = current['temp_c']
    feelslike_c = current['feelslike_c']
    weather = current['weather']
    r_humidity = current['relative_humidity']
    win_dir = current['wind_dir']
    wind_kph = current['wind_kph']
    wind_gust_kph = current['wind_gust_kph']
    pressure_mb = current['pressure_mb']

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
    observation_epoch = current['observation_epoch']
    observation_location = current['observation_location']['full']
    station_id = current['station_id']
    forecast_url = current['forecast_url']

    # TODO: something with those
    observation_epoch = current['observation_epoch']  # which epoch?
    dewpoint_c = current['dewpoint_c']
    precip_1hr_metric = current['precip_1hr_metric']
    precip_today_metric = current['precip_today_metric']
    visibility_km = current['visibility_km']
    windchill_c = current['windchill_c']
    heat_index_c = current['heat_index_c']

    print(city, time.strftime('%H:%M', time.localtime()))
    print(temp_c, 'C', weather)
    print()
    print('Humidité:', r_humidity, '(' + feelslike_c, 'C' + ')')
    print('Pression:', pressure_mb, 'mb', trend)
    print('Vents:', win_dir, wind_kph, 'km/h',
          'avec rafales', wind_gust_kph, 'km/h')
    print(forecast_url)
    print()
    print(observation_time)
    print(observation_location, '(' + station_id + ')')
    return


def print_forecast():
    # print 3 days forecast

    d = get_data(forecast)
    fc = d['forecast']['simpleforecast']['forecastday']
    print('Prévisions 3 prochains jours:')
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


def print_txt_forecast():
    # print one line per period forecast

    d = get_data(forecast)
    fc = d['forecast']['txt_forecast']['forecastday']
    for i in fc:
        print(i['title'].capitalize() + ':', i['fcttext_metric'])
        print()


print_conditions()
# print()
# print_astronomy()
# print()
# print_forecast()
print()
# print_txt_forecast()

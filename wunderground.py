import json
import os
import urllib.request
from pprint import pprint

my_key = os.environ['WUNDERGROUND_KEY']
location = os.environ['LOCATION']

base_url = 'http://api.wunderground.com/api/'
url1 = base_url + my_key + '/forecast/lang:FR/q/' + location + '.json'
url2 = base_url + my_key + '/conditions/lang:FR/q/' + location + '.json'
url3 = base_url + my_key + '/astronomy/lang:FR/q/' + location + '.json'


def print_astronomy():
    d = get_data(url3)
    sunrise = d['sun_phase']['sunrise']['hour'] + ':' + \
              d['sun_phase']['sunrise']['minute']
    sunset = d['sun_phase']['sunset']['hour'] + ':' + d['sun_phase']['sunset'][
        'minute']
    phase = d['moon_phase']['phaseofMoon']

    print()
    print('Lever du soleil:', sunrise)
    print('Coucher du soleil:', sunset)
    print('Phase de la lune:', phase)
    return


def print_conditions():
    d = get_data(url2)
    current = d['current_observation']

    print(current['display_location']['city'], current['local_time_rfc822'])
    print(current['temp_c'], 'C', '(' + current['feelslike_c'], 'C' + ')',
          current['weather'])
    print()
    print('Humidité:', current['relative_humidity'])
    print('Vents du', current['wind_dir'], current['wind_kph'], 'km/h',
          'avec rafales:', current['wind_gust_kph'], 'km/h')
    print('Pression:', current['pressure_mb'], 'mb', current['pressure_trend'])
    print()
    print(current['observation_time'])
    print(current['observation_location']['full'])
    print(current['station_id'])
    # print()
    # print('---')
    # print(current['precip_1hr_metric'])
    # print(current['precip_today_metric'])
    # print(current['pressure_trend'])
    # print(current['visibility_km'])
    # print()
    # print('Facteur vent:', current['windchill_c'])

    # pprint(current)
    return


def get_data(url):
    with urllib.request.urlopen(url) as response:
        r = response.read()
        data = json.loads(r.decode('utf-8'))
    return data


print_conditions()
print_astronomy()

import requests
import json
from datetime import datetime


URL = 'http://efa.vrr.de/standard/'
DEFAULT_PARAMS = dict(
    language='de',
    useRealtime=True,
    outputFormat='json',
    coordOutputFormat='WGS84[DD.DDDDD]',
    UTFMacro=True,
)


def get_station_departures(station, time=None, limit=10):
    '''Abfahrtsmonitor, API docs S. 52ff'''

    params = DEFAULT_PARAMS.copy()
    params['type_dm'] = 'any'
    params['name_dm'] = station
    params['mode'] = 'direct'
    params['limit'] = limit
    params['useRealtime'] = True

    if time is None:
        time = datetime.now()
        params['itdDateDay'] = time.day
        params['itdDateMonth'] = time.month
        params['itdDateYear'] = time.year
        params['itdTimeHour'] = time.hour
        params['itdTimeMinute'] = time.minute

    ret = requests.get(
        URL + 'XML_DM_REQUEST',
        params=params,
        headers={'Accept': 'application/json'},
    )
    ret.raise_for_status()

    data = json.loads(ret.content.decode('utf-8'))
    if data['departureList'] is None:
        data['departureList'] = []

    for elem in data['departureList']:
        for key in ['dateTime', 'realDateTime']:
            if key in elem:
                elem[key] = parse_datetime(elem[key])

    return data


def parse_datetime(date):
    return datetime(
        year=int(date['year']),
        month=int(date['month']),
        day=int(date['day']),
        hour=int(date['hour']),
        minute=int(date['minute']),
    )

import ssl

from ..common import *

MAX_ROW = 1000
URL = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
COLUMNS = ['id', 'name', 'word', 'page', 'place', 'time']
PREFIX = 'NoLog'
SHORT_SLEEP = 5
LONG_SLEEP = 45


def GetColumn(column: str, service, sheet_name: str, timeout: int, name: str, sheet_id: str):
    Stamp(f'Trying to get column {column} from sheet {sheet_name}', 'i')
    ControlTimeout(timeout, name)
    try:
        res = service.spreadsheets().values().get(spreadsheetId=sheet_id,
                                                  range=f'{sheet_name}!{column}2:{column}{MAX_ROW}').execute().get('values', [])
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError, ssl.SSLEOFError) as err:
        Stamp(f'Status = {err} on getting column from sheet {sheet_name}', 'e')
        Sleep(LONG_SLEEP)
        res = GetColumn(column, service, sheet_name, timeout, name, sheet_id)
    else:
        if not res:
            Stamp(f'No elements in column {column} sheet {sheet_name} found', 'w')
        else:
            Stamp(f'Found {len(res)} elements from column {column} sheet {sheet_name}', 's')
            res = [item for sublist in res for item in sublist]
    return res


def GetData(timeout: int, name: str):
    Stamp(f'Trying to connect {URL}', 'i')
    ControlTimeout(timeout, name)
    try:
        response = requests.get(URL, params=PARAMS, headers=HEADERS)
    except requests.ConnectionError:
        Stamp(f'Connection on {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(timeout, name)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {URL}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response in empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {URL}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetData(timeout, name)
    return raw


def ProcessData(raw: dict, sheet_name: str, word: str, page: int):
    try:
        height = len(raw['data']['products'])
    except TypeError:
        height = 0
        Stamp(f'For sheet {sheet_name} found NO products', 'w')
    else:
        Stamp(f'For sheet {sheet_name} found {height} products', 's')
    list_real = []
    list_advertise = []
    for i in range(height):
        row_advertise = []
        row_real = []
        for column in COLUMNS:
            match column:
                case 'id':
                    row_advertise.append(str(raw['data']['products'][i]['id']))
                    row_real.append(str(raw['data']['products'][i]['id']))
                case 'name':
                    row_advertise.append(str(raw['data']['products'][i]['name']))
                    row_real.append(str(raw['data']['products'][i]['name']))
                case 'word':
                    row_advertise.append(word)
                    row_real.append(word)
                case 'page':
                    row_advertise.append(str(page))
                    row_real.append(str(page))
                case 'place':
                    row_real.append(str(i + 1))
                    try:
                        index_from_log = raw['data']['products'][i]['log']['position']
                    except KeyError:
                        row_advertise.append(str(i + 1))
                    else:
                        row_advertise.append(str(index_from_log + 1))
                case 'time':
                    row_advertise.append(str(datetime.now().strftime('%Y-%m-%d %H:%M')))
                    row_real.append(str(datetime.now().strftime('%Y-%m-%d %H:%M')))
        list_advertise.append(row_advertise)
        list_real.append(row_real)
    return list_advertise, list_real


PARAMS = {
    'TestGroup': 'control',
    'TestID': '367',
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'resultset': 'catalog',
    'sort': 'popular',
    'spp': '28',
    'suppressSpellcheck': 'false',
}

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9,cy;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wildberries.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D1%82%D0%B0%D1%80%D0%B5%D0%BB%D0%BA%D0%B8',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

from common import *

SHORT_SLEEP = 6
LONG_SLEEP = 45
TIMEOUT = 3600 * 3
BLANK_ROWS = 10000
PAGES_QUANTITY = 5
NAME = 'Hour Parser'
PREFIX = 'NoLog'
MAX_ROW = 1000
URL = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
COLUMNS = ['id', 'name', 'word', 'page', 'place', 'time']
SHEET_ID = '1luoj-fVTjBwEebIJ2ZySJKpQLS9a0Ui1LPQIO9u0OCg'

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

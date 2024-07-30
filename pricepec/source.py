from common import *

URL = 'https://card.wb.ru/cards/v2/detail'
COLUMNS = ['id', 'name', 'price', 'time']
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
SHORT_SLEEP = 6
LONG_SLEEP = 45
MAX_ATTEMPTS = 5

PARAMS = {
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'spp': '30',
    'nm': None,
    'ab_testing': 'false'
}

HEADERS = {
    'User-Agent': None,
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Origin': 'https://www.wildberries.ru',
    'Connection': 'keep-alive',
    'Referer': 'https://www.wildberries.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Priority': 'u=4',
}

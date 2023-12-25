from common import *

TIMEOUT = 3600
SHEET_ID = '1ocjGSj6YFNoOXMW-T_wxwAhTrBG5mbIqYG9DCdcoj4I'
LONG_SLEEP = 60
SHORT_SLEEP = 10
BLANK_ROWS = 5000
NAME = 'Analytics'
PREFIX = 'Month'
URL = 'https://api-seller.ozon.ru/v1/analytics/data'
COLUMNS = {'id': '+', 'name': '+', 'revenue': 0, 'ordered_units': 1, 'returns': 2, 'delivered_units': 3, 'position_category': 4}
START_OF_ALL = '2023-01-01'
START_OF_MONTH = datetime.now().strftime('%Y-%m') + '-01'
TODAY = datetime.now().strftime('%Y-%m-%d')
MSG = 'NoData'

SAMPLE = {
    'date_from': '',
    'date_to': '',
    'metrics': [
        'revenue',
        'ordered_units',
        'returns',
        'delivered_units',
        'position_category'
    ],
    'dimension': [
        'sku'
    ],
    'filters': [],
    'sort': [],
    'limit': 1000,
    'offset': 0
}

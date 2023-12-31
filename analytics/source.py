from common import *


TIMEOUT = 3600
LONG_SLEEP = 60
SHORT_SLEEP = 10
BLANK_ROWS = 5000
NAME = 'Analytics'
PREFIX = 'Month'
URL = 'https://api-seller.ozon.ru/v1/analytics/data'
COLUMNS = {'id': None, 'name': None, 'revenue': 0, 'ordered_units': 1, 'returns': 2, 'delivered_units': 3, 'position_category': 4}
START_OF_ALL = '2023-01-01'
SAMPLE = {
    'date_from': None,
    'date_to': None,
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

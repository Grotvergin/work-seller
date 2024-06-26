from common import *


LONG_SLEEP = 60
SHORT_SLEEP = 10
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
URL = 'https://api-seller.ozon.ru/v1/analytics/data'
COLUMNS = {'id': None, 'name': None, 'revenue': 0, 'ordered_units': 1, 'returns': 2, 'delivered_units': 3, 'position_category': 4}
START_OF_ALL = (datetime.now() - timedelta(days=360)).strftime('%Y-%m-%d')
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

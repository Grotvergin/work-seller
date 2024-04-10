from common import *

NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
URL = 'https://seller.ozon.ru/api/site/seller-analytics/v1/data/table'
LONG_SLEEP = 60
SHORT_SLEEP = 10
CABINETS = ['Bathroom']
COLUMNS = ['name', 'id', 'sellerId', 'source', 'amount', 'summ', 'basket', 'unique', 'showall', 'showsearch']
SAMPLE = {
    'group_by': 'SKU',
    'metrics': [
        'ordered_units',
        'revenue',
        'hits_tocart',
        'session_view_pdp',
        'hits_view',
        'position_category',
    ],
    'date_from': None,
    'date_to': None,
    'filters': [
        {
            'key': 'description_type',
            'value': None,
            'group': 'extra',
        },
    ],
    'limit': '200',
    'offset': '0',
    'sort': [
        {
            'key': 'ordered_units',
            'order': 'DESC',
        },
    ],
}
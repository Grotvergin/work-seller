from common import *

NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
URL_CAMPAIGNS = 'https://performance.ozon.ru/api/adv-api/v2/search_promo_campaign'
URL_GOODS = 'https://performance.ozon.ru/api/adv-api/v2/campaign/{}/search_promo/products'
LONG_SLEEP = 60
SHORT_SLEEP = 10
COLUMNS_CAMPAIGNS = ('createdAt', 'id', 'title', 'clicks', 'ctr', 'drr', 'expense', 'orders', 'ordersMoney', 'productsCount', 'productsWithBids')
COLUMNS_GOODS = ('campaign', 'bid', 'bidPrice', 'price', 'previousVisibilityIndex', 'sku', 'sourceSku', 'title', 'visibilityIndex', 'stateName',
                 'previousWeek', 'thisWeek', 'bid', 'bidPrice', 'updatedAt')
SAMPLE_CAMPAIGNS = {
    'status': [],
    'search': '',
    'sort': [
        {
            'desc': False,
            'field': 'SORT_FIELD_STATUS',
        },
    ],
    'statsTo': None,
    'statsFrom': None,
    'pageSize': 100,
    'page': 1,
}
SAMPLE_GOODS = {
    'filters': {
        'onlyDefaultBids': False,
        'status': 'SEARCH_PROMO_PRODUCT_STATUS_ALL',
    },
    'isBlocked': False,
    'page': 1,
    'pageSize': 100,
}
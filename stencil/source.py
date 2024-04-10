from common import *

NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
URL_CAMPAIGNS = 'https://performance.ozon.ru/api/adv-performance-facade/v2/campaign/product_campaign'
URL_INFO = 'https://performance.ozon.ru/api/adv-performance-facade/v2/campaign/{}/product'
LONG_SLEEP = 60
SHORT_SLEEP = 5
COLUMNS = ['id', 'sku', 'title', 'leafCategoryId', 'leafCategoryTitle', 'campaignId', 'bid', 'oldPrice', 'newPrice', 'sourceSku', 'createdAt',
           'views', 'orders', 'clicks', 'ctr', 'moneySpent', 'moneySpentRatio', 'gmv', 'viewsTop', 'ordersTop', 'clicksTop', 'ctrTop', 'gmvTop']
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
    'displayFields': [],
    'paymentMethod': [],
    'productAutopilotStrategy': [],
    'placement': [],
    'productCampaignMode': [],
    'pageSize': 200,
    'page': 1,
}
PARAMS_INFO = {
    'leafCategoryId': '0',
    'order': 'asc',
    'page': '1',
    'pageSize': '200',
    'statsIntervalFrom': None,
    'statsIntervalTo': None,
}
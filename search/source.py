from common import *

NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
LONG_SLEEP = 60
SHORT_SLEEP = 10
URL_PREPARE = 'https://performance.ozon.ru/api/adv-api/external/api/statistics'
URL_DOWNLOAD = 'https://performance.ozon.ru/api/adv-api/external/api/statistics/report'
URL_CAMPAIGNS = 'https://performance.ozon.ru/api/adv-api/v2/search_promo_campaign'
COLUMNS = ['Дата', 'ID заказа', 'Номер заказа', 'Ozon ID', 'Ozon ID продвигаемого товара', 'Артикул',
           'Наименование', 'Количество','Цена продажи', 'Стоимость, ₽', 'Ставка, %', 'Ставка, ₽', 'Расход, ₽']
SAMPLE_PREPARE = {
    'campaignId': None,
    'dateFrom': None,
    'dateTo': None,
    'groupBy': 'NO_GROUP_BY',
    'attributionDays': '30',
}
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
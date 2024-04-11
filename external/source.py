from common import *

URL_CAMPAIGNS = 'https://advert-api.wb.ru/adv/v1/promotion/count'
URL_STAT = 'https://advert-api.wb.ru/adv/v2/fullstats'
CABINETS = ['Первый', 'Второй', 'Третий']
COLUMNS = {'advertId': 'SPEC',
           'date': 'SPEC',
           'appType': 'SPEC',
           'companyType': 'SPEC',
           'nmId': None,
           'name': None,
           'views': None,
           'clicks': None,
           'ctr': None,
           'cpc': None,
           'sum': None,
           'atbs': None,
           'orders': None,
           'cr': None,
           'shks': None,
           'sum_price': None}
TYPES_AND_NAMES = {
    4: 'в каталоге',
    5: 'в карточке товара',
    6: 'в поиске',
    7: 'в рекомендациях на главной странице',
    8: 'автоматическая',
    9: 'поиск + каталог'
}
SLEEP = 60
PORTION = 100
THR_DELTA = 15

from common import *


URL_CAMPAIGNS = 'https://advert-api.wb.ru/adv/v1/promotion/count'
URL_STAT = 'https://advert-api.wb.ru/adv/v1/fullstats'
SHORT_SLEEP = 60
LONG_SLEEP = 60
PORTION = 100
BEGIN = '2023-01-01'
NAME = os.path.dirname(os.path.realpath(__file__)).rsplit('\\', 1)[-1]
COLUMNS = {'advertId': 'SPEC',
           'date': 'SPEC',
           'appType': 'SPEC',
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

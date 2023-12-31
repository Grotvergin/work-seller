from common import *


URL_CAMPAIGNS = 'https://advert-api.wb.ru/adv/v1/promotion/count'
URL_STAT = 'https://advert-api.wb.ru/adv/v1/fullstats'
TIMEOUT = 3600
SHORT_SLEEP = 60
LONG_SLEEP = 90
BLANK_ROWS = 50000
PORTION = 100
BEGIN = '2023-01-01'
NAME = 'Advert'
PREFIX = 'Month'
COLUMNS = {'advertId': 'SPEC',
           'date': 'SPEC',
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

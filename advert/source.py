from common import *

URL_CAMPAIGNS = 'https://advert-api.wb.ru/adv/v1/promotion/count'
URL_STAT = 'https://advert-api.wb.ru/adv/v2/fullstats'
TIMEOUT = 3600*4
SHORT_SLEEP = 60
LONG_SLEEP = 90
BLANK_ROWS = 60000
MONTH_BLANK = 20000
PORTION = 100
BEGIN = '2023-01-01'
START_OF_MONTH = datetime.now().strftime('%Y-%m') + '-01'
YEAR = datetime.now().strftime('%Y')
MONTH = datetime.now().strftime('%m')
TODAY = datetime.now().strftime('%Y-%m-%d')
MSG = 'No data'
SHEET_ID = '1yizHdvJXXdAcQ_P0d0fXJPOb0PaZS1-D85PczZ0cuWI'
NAME = 'Advert'
PREFIX = 'Month'

COLUMNS = {'advertId': 'SPEC',
           'date': 'SPEC',
           'nmId': '+',
           'name': '+',
           'views': '+',
           'clicks': '+',
           'ctr': '+',
           'cpc': '+',
           'sum': '+',
           'atbs': '+',
           'orders': '+',
           'cr': '+',
           'shks': '+',
           'sum_price': '+'}

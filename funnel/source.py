from common import *


PERIODS = {
    'Yesterday': {'Start': (date.today() - timedelta(days=1)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': (date.today() - timedelta(days=1)).strftime('%Y-%m-%d') + ' 23:59:59'},
    'DayBeforeYesterday': {'Start': (date.today() - timedelta(days=2)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': (date.today() - timedelta(days=2)).strftime('%Y-%m-%d') + ' 23:59:59'},
    '3Days': {'Start': (date.today() - timedelta(days=3)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    '6-3Days': {'Start': (date.today() - timedelta(days=6)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': (date.today() - timedelta(days=3)).strftime('%Y-%m-%d') + ' 23:59:59'},
    '3Months': {'Start': (date.today() - timedelta(days=91)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    '6-3Months': {'Start': (date.today() - timedelta(days=183)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': (date.today() - timedelta(days=91)).strftime('%Y-%m-%d') + ' 23:59:59'}
}
URL = 'https://suppliers-api.wb.ru/content/v1/analytics/nm-report/detail'
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
LONG_SLEEP = 60
SHORT_SLEEP = 20
COLUMNS = ['page', 'nmID', 'vendorCode', 'brandName', 'begin', 'end', 'openCardCount', 'addToCartCount', 'ordersCount', 'ordersSumRub', 'buyoutsCount', 'buyoutsSumRub', 'cancelCount', 'cancelSumRub',
           'avgPriceRub', 'avgOrdersCountPerDay', 'addToCartPercent', 'cartToOrderPercent', 'buyoutsPercent', 'stocksMp', 'stocksWb']
SAMPLE = {
    'period': {
        'begin': None,
        'end': None
    },
    'orderBy': {
        'field': 'ordersSumRub',
        'mode': 'desc'
        },
    'page': None
}

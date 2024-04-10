from common import *

NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
URL = 'https://performance.ozon.ru/api/search-performance-cpo/mainpage/v1/product/list'
LONG_SLEEP = 60
SHORT_SLEEP = 10
COLUMNS = ['bidAbs', 'bidPercent', 'categoryName', 'price', 'sku', 'sourceSku', 'title', 'clicks',
           'coveragePercent', 'ctrPercent', 'drrPercent', 'impressions', 'orders', 'searchPromoSales', 'spent']
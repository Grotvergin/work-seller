from common import *


URL = 'https://discounts-prices-api.wb.ru/api/v2/list/goods/filter'
SHORT_SLEEP = 5
LONG_SLEEP = 60
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
COLUMNS = ['nmID', 'vendorCode', 'sizeID', 'price', 'discountedPrice', 'discount', 'time']

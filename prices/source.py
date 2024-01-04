from common import *


URL = 'https://suppliers-api.wildberries.ru/public/api/v1/info'
SHORT_SLEEP = 5
LONG_SLEEP = 60
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
COLUMNS = ['nmId', 'price', 'discount', 'promoCode', 'time']

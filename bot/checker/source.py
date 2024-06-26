from common import *


LONG_SLEEP = 90
MAX_DIFF = 10
MAX_LEN = 3500
PATH = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')
TYPOLOGY = 'Test' if DEBUG_MODE else 'Main'
URL = 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
ROWS = ['supplierArticle', 'quantity', 'time']
DATE_FROM = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

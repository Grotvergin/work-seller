from common import *

LONG_SLEEP = 90
MAX_DIFF = 10
MAX_LEN = 3500
TIMEOUT = 100000
NAME = 'BotChecker'
URL = 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
ROWS = ['supplierArticle', 'quantity', 'time']
DATE_FROM = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
SHEET_ID = '1QfRcVy8pnxG3ZISe1x751akTh49FcMOu53FerNzXFQg'
#SHEET_ID = '1rmXz1joBFlYDkPK4gY0BkbNaqAzhQ9F6Nle6xe-w4LE'

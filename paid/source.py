from common import *

NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
URL = 'https://seller-analytics-api.wildberries.ru/api/v1/paid_storage'
LONG_SLEEP = 60
SHORT_SLEEP = 10
COLUMNS = ['date', 'logWarehouseCoef', 'officeId', 'warehouse', 'warehouseCoef', 'giId',
           'chrtId', 'size', 'barcode', 'subject', 'brand', 'vendorCode', 'nmId', 'volume',
           'calcType', 'warehousePrice', 'barcodesCount', 'palletPlaceCode', 'palletCount',
           'originalDate', 'loyaltyDiscount', 'giDate', 'giFixDateFrom', 'giFixDateTill']

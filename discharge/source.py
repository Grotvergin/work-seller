from common import *

TIMEOUT = 3600
LONG_SLEEP = 60
SHORT_SLEEP = 5
BLANK_ROWS = 50000
MONTHS_HISTORY = 14
DAYS_IN_MONTH = 28
CHUNK_SIZE = 100
TODAY = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
NAME = 'Discharge'

SHEETS = {
    'Products': {'GetAll': 'https://api-seller.ozon.ru/v2/product/list',
                 'InfoAboutAll': 'https://api-seller.ozon.ru/v2/product/info/list',
                 'GetRating': 'https://api-seller.ozon.ru/v1/product/rating-by-sku',
                 'Columns': ['offer_id', 'id', 'sku', 'barcode', 'name', 'rating', 'brand', 'state']
                 },
    'Warehouse': {'GetAll': 'https://api-seller.ozon.ru/v2/product/list',
                  'InfoAboutAll': 'https://api-seller.ozon.ru/v2/product/info/list',
                  'GetRating': 'https://api-seller.ozon.ru/v1/product/rating-by-sku',
                  'Columns': ['offer_id', 'id', 'sku', 'name', 'barcode', 'state', 'visible', 'present', 'reserved']
                  },
    'Transactions': {'GetData': 'https://api-seller.ozon.ru/v3/finance/transaction/list',
                     'Columns': ['operation_id',
                                 'operation_type',
                                 'operation_date',
                                 'operation_type_name',
                                 'delivery_charge',
                                 'return_delivery_charge',
                                 'accruals_for_sale',
                                 'sale_commission',
                                 'amount',
                                 'type',
                                 'delivery_schema',
                                 'order_date',
                                 'posting_number',
                                 'warehouse_id',
                                 'name',
                                 'sku',
                                 'services_sum'],
                     }
}

SAMPLE = {
    "filter": {
        "date": {
            "from": '',
            "to": ''
        },
        "operation_type": [],
        "posting_number": "",
        "transaction_type": "all"
    },
    "page": 1,
    "page_size": 1000
}

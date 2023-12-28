from common import *

TIMEOUT = 3600
LONG_SLEEP = 60
SHORT_SLEEP = 5
BLANK_ROWS = 50000
MONTHS_HISTORY = 14
DAYS_IN_MONTH = 28
CHUNK_SIZE = 100
DATE_FROM = '2023-11-11'
TODAY = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
NAME = 'Discharge'

SHEETS = {
    'Orders': {'GetData': 'https://api-seller.ozon.ru/v2/posting/fbo/list',
               'Columns': ('sku', 'quantity', 'price', 'commission_amount', 'commission_percent', 'payout', 'created_at', 'in_process_at')
               },
    'Products': {'GetAll': 'https://api-seller.ozon.ru/v2/product/list',
                 'InfoAboutAll': 'https://api-seller.ozon.ru/v2/product/info/list',
                 'GetRating': 'https://api-seller.ozon.ru/v1/product/rating-by-sku',
                 'Columns': ('offer_id', 'id', 'sku', 'barcode', 'name', 'rating', 'brand', 'state')
                 },
    'Warehouse': {'GetAll': 'https://api-seller.ozon.ru/v2/product/list',
                  'InfoAboutAll': 'https://api-seller.ozon.ru/v2/product/info/list',
                  'GetRating': 'https://api-seller.ozon.ru/v1/product/rating-by-sku',
                  'Columns': ('offer_id', 'id', 'sku', 'name', 'barcode', 'state', 'visible', 'present', 'reserved')
                  },
    'Transactions': {'GetData': 'https://api-seller.ozon.ru/v3/finance/transaction/list',
                     'Columns': ('operation_id',
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
                                 'services_sum'),
                     }
}

FIRST_SAMPLE = {
    'filter': {
        'date': {
            'from': '',
            'to': ''
        },
        'operation_type': [],
        'posting_number': '',
        'transaction_type': 'all'
    },
    'page': 1,
    'page_size': 1000
}

SECOND_SAMPLE = {
    'dir': 'ASC',
    'filter': {
        'since': DATE_FROM + 'T00:00:00.000Z',
        'status': '',
        'to': TODAY
    },
    'limit': 1000,
    'offset': 0,
    'translit': True,
    'with': {
        'analytics_data': False,
        'financial_data': True
    }
}

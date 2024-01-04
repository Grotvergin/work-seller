from common import *


PERC_COMM = 0.022249
LONG_SLEEP = 120
SHORT_SLEEP = 60
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
DATE_FROM = '2023-06-06'
DATE_X = '2023-11-27'
SHEETS = {
    'Incomes': {
        'URL': ['https://statistics-api.wildberries.ru/api/v1/supplier/incomes'],
        'Columns': {
            'incomeId': None,
            'number': None,
            'date': None,
            'lastChangeDate': None,
            'supplierArticle': None,
            'techSize': None,
            'barcode': None,
            'quantity': None,
            'totalPrice': None,
            'dateClose': None,
            'warehouseName': None,
            'nmId': None,
            'status': None
        }
    },
    'Realisations': {
        'URL': ['https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod',
                'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod'],
        'Columns': {
            'realizationreport_id': None,
            'suppliercontract_code': 'SPEC',
            'rrd_id': None,
            'gi_id': None,
            'subject_name': None,
            'nm_id': None,
            'brand_name': None,
            'sa_name': None,
            'ts_name': None,
            'barcode': None,
            'doc_type_name': None,
            'quantity': None,
            'nds': '0',
            'cost_amount': '0',
            'retail_price': None,
            'retail_amount': None,
            'retail_commission': 'SPEC',
            'sale_percent': None,
            'commission_percent': None,
            'customer_reward': '0',
            'supplier_reward': 'SPEC',
            'office_name': None,
            'supplier_oper_name': None,
            'order_dt': 'SPEC',
            'sale_dt': 'SPEC',
            'rr_dt': 'SPEC',
            'shk_id': None,
            'retail_price_withdisc_rub': None,
            'for_pay': 'SPEC',
            'for_pay_nds': '0',
            'delivery_amount': None,
            'return_amount': None,
            'delivery_rub': None,
            'gi_box_type_name': None,
            'product_discount_for_report': None,
            'supplier_promo': None,
            'supplier_spp': '0',
            'rid': None,
            'srid': 'SPEC'
        }
    },
    'Orders': {
        'URL': ['https://statistics-api.wildberries.ru/api/v1/supplier/orders'],
        'Columns': {
            'srid': 'SPEC',
            'date': None,
            'lastChangeDate': None,
            'supplierArticle': None,
            'techSize': None,
            'barcode': None,
            'quantity': '1',
            'totalPrice': None,
            'discountPercent': None,
            'warehouseName': None,
            'regionName': None,
            'incomeID': None,
            'odid': '',
            'nmId': None,
            'subject': None,
            'category': None,
            'brand': None,
            'isCancel': None,
            'cancelDate': None,
            'gNumber': None
        }
    },
    'Sales': {
        'URL': ['https://statistics-api.wildberries.ru/api/v1/supplier/sales'],
        'Columns': {
            'number': '',
            'supplierArticle': None,
            'techSize': None,
            'quantity': '1',
            'totalPrice': None,
            'discountPercent': None,
            'isSupply': None,
            'isRealization': None,
            'barcode': None,
            'orderId': '',
            'promoCodeDiscount': '',
            'warehouseName': None,
            'countryName': None,
            'oblastOkrugName': None,
            'regionName': None,
            'incomeID': None,
            'saleID': None,
            'odid': '',
            'spp': None,
            'forPay': None,
            'finishedPrice': None,
            'priceWithDisc': None,
            'nmId': None,
            'subject': None,
            'category': None,
            'brand': None,
            'IsStorno': '',
            'gNumber': None,
            'date': None,
            'lastChangeDate': None
        }
    },
    'Warehouse': {
        'URL': ['https://statistics-api.wildberries.ru/api/v1/supplier/stocks'],
        'Columns': {
            'lastChangeDate': None,
            'supplierArticle': None,
            'techSize': None,
            'barcode': None,
            'quantity': None,
            'isSupply': None,
            'isRealization': None,
            'quantityFull': None,
            'quantityNotInOrders': '',
            'warehouseName': None,
            'inWayToClient': None,
            'inWayFromClient': None,
            'nmId': None,
            'subject': None,
            'category': None,
            'daysOnSite': '',
            'brand': None,
            'SCCode': None,
            'Price': None,
            'Discount': None,
            'WarehouseID': ''
        }
    }
}

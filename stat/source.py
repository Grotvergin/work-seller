import sys
import datetime
import time
from googleapiclient.discovery import build
import httplib2
import requests
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import configparser
from pathlib import Path
import socket
from datetime import datetime
from colorama import Fore, Style, init

init()
START = time.time()
TIMEOUT = 3600*2
CREDS = service_account.Credentials.from_service_account_file('keys.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
PERC_COMM = 0.022249
LONG_SLEEP = 90
SHORT_SLEEP = 5
BLANK_ROWS = 50000

SHEETS_AND_URL = {
    'Realisations': 'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod',
    'Orders': 'https://statistics-api.wildberries.ru/api/v1/supplier/orders',
    'Sales': 'https://statistics-api.wildberries.ru/api/v1/supplier/sales',
    'Warehouse': 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
}

SHEETS_AND_COLS = {
    'Realisations': {'realizationreport_id': '+',
                     'suppliercontract_code': 'SPEC',
                     'rrd_id': '+',
                     'gi_id': '+',
                     'subject_name': '+',
                     'nm_id': '+',
                     'brand_name': '+',
                     'sa_name': '+',
                     'ts_name': '+',
                     'barcode': '+',
                     'doc_type_name': '+',
                     'quantity': '+',
                     'nds': '0',
                     'cost_amount': '0',
                     'retail_price': '+',
                     'retail_amount': '+',
                     'retail_commission': 'SPEC',
                     'sale_percent': '+',
                     'commission_percent': '+',
                     'customer_reward': '0',
                     'supplier_reward': 'SPEC',
                     'office_name': '+',
                     'supplier_oper_name': '+',
                     'order_dt': 'SPEC',
                     'sale_dt': 'SPEC',
                     'rr_dt': 'SPEC',
                     'shk_id': '+',
                     'retail_price_withdisc_rub': '+',
                     'for_pay': 'SPEC',
                     'for_pay_nds': '0',
                     'delivery_amount': '+',
                     'return_amount': '+',
                     'delivery_rub': '+',
                     'gi_box_type_name': '+',
                     'product_discount_for_report': '+',
                     'supplier_promo': '+',
                     'supplier_spp': '0',
                     'rid': '+',
                     'srid': 'SPEC'},
    'Orders': {'srid': 'SPEC',
               'date': '+',
               'lastChangeDate': '+',
               'supplierArticle': '+',
               'techSize': '+',
               'barcode': '+',
               'quantity': '1',
               'totalPrice': '+',
               'discountPercent': '+',
               'warehouseName': '+',
               'regionName': '+',
               'incomeID': '+',
               'odid': '',
               'nmId': '+',
               'subject': '+',
               'category': '+',
               'brand': '+',
               'isCancel': '+',
               'cancelDate': '+',
               'gNumber': '+'},
    'Sales': {'number': '',
              'supplierArticle': '+',
              'techSize': '+',
              'quantity': '1',
              'totalPrice': '+',
              'discountPercent': '+',
              'isSupply': '+',
              'isRealization': '+',
              'barcode': '+',
              'orderId': '',
              'promoCodeDiscount': '',
              'warehouseName': '+',
              'countryName': '+',
              'oblastOkrugName': '+',
              'regionName': '+',
              'incomeID': '+',
              'saleID': '+',
              'odid': '',
              'spp': '+',
              'forPay': '+',
              'finishedPrice': '+',
              'priceWithDisc': '+',
              'nmId': '+',
              'subject': '+',
              'category': '+',
              'brand': '+',
              'IsStorno': '',
              'gNumber': '+',
              'date': '+',
              'lastChangeDate': '+'},
    'Warehouse': {'lastChangeDate': '+',
                  'supplierArticle': '+',
                  'techSize': '+',
                  'barcode': '+',
                  'quantity': '+',
                  'isSupply': '+',
                  'isRealization': '+',
                  'quantityFull': '+',
                  'quantityNotInOrders': '',
                  'warehouseName': '+',
                  'inWayToClient': '+',
                  'inWayFromClient': '+',
                  'nmId': '+',
                  'subject': '+',
                  'category': '+',
                  'daysOnSite': '',
                  'brand': '+',
                  'SCCode': '+',
                  'Price': '+',
                  'Discount': '+',
                  'WarehouseID': ''}
}

RED = {
    'requests': [
        {
            'repeatCell': {
                'range': {
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 0
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {
                            'red': 1.0,
                            'green': 0.0,
                            'blue': 0.0,
                            'alpha': 0.5
                        }
                    }
                },
                'fields': 'userEnteredFormat.backgroundColor'
            }
        }
    ]
}

GREEN = {
    'requests': [
        {
            'repeatCell': {
                'range': {
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 0
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {
                            'red': 0.0,
                            'green': 1.0,
                            'blue': 0.0,
                            'alpha': 0.2
                        }
                    }
                },
                'fields': 'userEnteredFormat.backgroundColor'
            }
        }
    ]
}

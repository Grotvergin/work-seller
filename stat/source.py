import sys
import datetime
from time import sleep
from googleapiclient.discovery import build
import httplib2
import requests
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import configparser
from pathlib import Path
from tqdm import tqdm
from colorama import Fore, Style, init

init()
scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file('keys.json', scopes=scopes)
percent_commission = 0.022249
long_sleep = 90
short_sleep = 5

sheets_and_url = {
    'Realisations': 'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod',
    'Orders': 'https://statistics-api.wildberries.ru/api/v1/supplier/orders',
    'Sales': 'https://statistics-api.wildberries.ru/api/v1/supplier/sales',
    'Warehouse': 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
}

sheets_and_columns = {
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
               'oblastOkrugName': '+',
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

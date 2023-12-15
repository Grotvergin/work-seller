import sys
import time
from googleapiclient.discovery import build
import httplib2
import requests
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import configparser
from pathlib import Path
import socket
from datetime import datetime, timedelta
from colorama import Fore, Style, init
import smtplib
from email.mime.multipart import MIMEMultipart
import json

init()
START = time.time()
TIMEOUT = 3600
CREDS = service_account.Credentials.from_service_account_file('keys.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])

LONG_SLEEP = 60
SHORT_SLEEP = 5
BLANK_ROWS = 50000
MONTHS_HISTORY = 14
DAYS_IN_MONTH = 28
TODAY = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
SPREADSHEET_ID = '19Cxlu8rPETt58hdYGQOjiYXZ_GIxI-veqktkjwzjBDI'

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

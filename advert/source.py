import time
import sys
import socket
from datetime import datetime
from googleapiclient.discovery import build
import requests
import httplib2
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import configparser
from pathlib import Path
from colorama import Fore, Style, init
import smtplib
from email.mime.multipart import MIMEMultipart

init()
URL_CAMPAIGNS = 'https://advert-api.wb.ru/adv/v1/promotion/count'
URL_STAT = 'https://advert-api.wb.ru/adv/v1/fullstat'
START = time.time()
TIMEOUT = 3600*6
SHORT_SLEEP = 6
LONG_SLEEP = 90
BLANK_ROWS = 60000
MONTH_BLANK = 20000
START_OF_MONTH = datetime.now().strftime("%Y-%m") + '-01'
YEAR = datetime.now().strftime("%Y")
MONTH = datetime.now().strftime("%m")
MSG = 'No data'
SHEET_ID = '1yizHdvJXXdAcQ_P0d0fXJPOb0PaZS1-D85PczZ0cuWI'
CREDS = service_account.Credentials.from_service_account_file('keys.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])

COLUMNS = {'advertId': 'SPEC',
           'date': 'SPEC',
           'nmId': '+',
           'name': '+',
           'views': '+',
           'clicks': '+',
           'ctr': '+',
           'cpc': '+',
           'sum': '+',
           'atbs': '+',
           'orders': '+',
           'cr': '+',
           'shks': '+',
           'sum_price': '+'}

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

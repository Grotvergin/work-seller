import time
import sys
from googleapiclient.discovery import build
import requests
import httplib2
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import configparser
from pathlib import Path
import socket
from colorama import Fore, Style, init
import random
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart

init()
URL = 'https://suppliers-api.wildberries.ru/public/api/v1/info'
START = time.time()
SHORT_SLEEP = 5
LONG_SLEEP = 300
TIMEOUT = 3600*1
BLANK_ROWS = 10000
SHEET_ID = '1AfaZZg1o0Sa1eNYpneFQfUOrm3W9LFxJDfKPmCPF8rc'
CREDS = service_account.Credentials.from_service_account_file('keys.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
COLUMNS = ['nmId', 'price', 'discount', 'promoCode', 'time']
MSG = 'NoData'

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

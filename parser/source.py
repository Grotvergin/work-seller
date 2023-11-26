import time
import sys
from googleapiclient.discovery import build
import requests
import httplib2
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import configparser
from pathlib import Path
from tqdm import tqdm
from colorama import Fore, Style, init
import random
from datetime import datetime

random.seed()
init()
START = time.time()
SHORT_SLEEP = 60
LONG_SLEEP = 300
TIMEOUT = 3600 * 6
BLANK_ROWS = 10000
PAGES_QUANTITY = 5
URL = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
COLUMNS = ['id', 'name', 'word', 'page', 'place', 'time']
SHEET_ID = '1luoj-fVTjBwEebIJ2ZySJKpQLS9a0Ui1LPQIO9u0OCg'
SHEETS_AND_GIDS = {'Dishes': 0, 'Bathroom': 1599632956, 'Lighting': 887264526}
CREDS = service_account.Credentials.from_service_account_file('keys.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])

RED = {
    'requests': [
        {
            'repeatCell': {
                'range': {
                    'sheetId': 'SPEC',
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': 6
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
                    'sheetId': 'SPEC',
                    'startRowIndex': 0,
                    'endRowIndex': 1,
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

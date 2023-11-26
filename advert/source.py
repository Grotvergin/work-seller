from time import sleep
from googleapiclient.discovery import build
import requests
import httplib2
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import configparser
from pathlib import Path
from tqdm import tqdm
from colorama import Fore, Style, init

init()
url_for_all_campaigns = 'https://advert-api.wb.ru/adv/v0/adverts'
url_for_statistics = 'https://advert-api.wb.ru/adv/v1/fullstat'
short_sleep = 10
long_sleep = 300
message = 'No data'
scopes = ['https://www.googleapis.com/auth/spreadsheets']
spreadsheet_id = '1yizHdvJXXdAcQ_P0d0fXJPOb0PaZS1-D85PczZ0cuWI'
creds = service_account.Credentials.from_service_account_file('keys.json', scopes=scopes)

columns = {'advertId': 'SPEC',
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

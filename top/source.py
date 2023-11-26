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
import random

init()
url_for_auth = 'https://app.topvtop.pro/api/auth/callback/credentials'
url_for_data = 'https://app.topvtop.pro/api/paymenthistory/get'
short_sleep = 10
long_sleep = 300
blank_rows = 10000
scopes = ['https://www.googleapis.com/auth/spreadsheets']
spreadsheet_id = '1kQNuedNt7xFU6m4HJe8Lm6he0bokWvwwqN5FeoNGAHY'
creds = service_account.Credentials.from_service_account_file('keys.json', scopes=scopes)
columns = ['_id', 'article', 'basisoperation', 'comment', 'dataoperation', 'refRewarded', 'summ', 'type', 'typeoperations', 'user']
message = 'NoData'
cookies_auth = {
    '_ym_uid': '1699982868953556305',
    '_ym_d': '1699982868',
    '__Host-next-auth.csrf-token': '0d015f8072670419bb39cad5ebdab252f53a8e672c5966aee1f8618dcb9032c2%7C6b3f7df2154fe89bf01b634c451357194ceff763a3eb2fe38d5cdb987cae436d',
    '_ym_isad': '1',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fapp.topvtop.pro%2Fauth',
}

data_auth = {
    'redirect': 'false',
    'callbackUrl': '/stats?type=all&period=today',
    # 'email': '3125106@bk.ru',
    # 'password': 'Mpseller1',
    'csrfToken': '0d015f8072670419bb39cad5ebdab252f53a8e672c5966aee1f8618dcb9032c2',
    'json': 'true',
}

headers_auth = {
    'authority': 'app.topvtop.pro',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,cy;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': '_ym_uid=1699982868953556305; _ym_d=1699982868; __Host-next-auth.csrf-token=0d015f8072670419bb39cad5ebdab252f53a8e672c5966aee1f8618dcb9032c2%7C6b3f7df2154fe89bf01b634c451357194ceff763a3eb2fe38d5cdb987cae436d; _ym_isad=1; __Secure-next-auth.callback-url=https%3A%2F%2Fapp.topvtop.pro%2Fauth',
    'origin': 'https://app.topvtop.pro',
    'pragma': 'no-cache',
    'referer': 'https://app.topvtop.pro/auth',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36',
}

cookies_get = {
    '_ym_uid': '1699982868953556305',
    '_ym_d': '1699982868',
    '__Host-next-auth.csrf-token': '0d015f8072670419bb39cad5ebdab252f53a8e672c5966aee1f8618dcb9032c2%7C6b3f7df2154fe89bf01b634c451357194ceff763a3eb2fe38d5cdb987cae436d',
    '_ym_isad': '1',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fapp.topvtop.pro%2Fpaymenthistory',
    '_ym_visorc': 'w',
    '__Secure-next-auth.session-token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..slxG9EgiKqtpPggv.Y-llYy5HrrLrM6fEsOCddvvFFjIhrHtyzvSSEvrQjUzbDuUvJNwj3VM2tiyXcOwXi_QtOulw8H34Ely7LIfrVbgEQJutmKa4pC25Vow-PkI4bmqwfDmNzaAydts--5groXn4F5iuBedYGL9H4atHpYUzGdHR5A6O3Qmk98r9N8iJAF1i6b68VoIdqDfqflJNT6nP1gprxtmzl3s6j_C1DRCN-XUAg3LlWNsFfAQr1hSQ9xVbqowU6J4GGkglL5Wbqjq-gPmAA-SQpDFBpF-YHkqfQn_YgZr1kfI_IAbvN66EQ1N3O1eNhQtq-OHyUT13UtNqljAgveAk.YQlqGl7YAdsqeouKLG9o8A',
}

headers_get = {
    'authority': 'app.topvtop.pro',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,cy;q=0.8',
    'cache-control': 'no-cache',
    # 'cookie': '_ym_uid=1699982868953556305; _ym_d=1699982868; __Host-next-auth.csrf-token=0d015f8072670419bb39cad5ebdab252f53a8e672c5966aee1f8618dcb9032c2%7C6b3f7df2154fe89bf01b634c451357194ceff763a3eb2fe38d5cdb987cae436d; _ym_isad=1; __Secure-next-auth.callback-url=https%3A%2F%2Fapp.topvtop.pro%2Fpaymenthistory; _ym_visorc=w; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..slxG9EgiKqtpPggv.Y-llYy5HrrLrM6fEsOCddvvFFjIhrHtyzvSSEvrQjUzbDuUvJNwj3VM2tiyXcOwXi_QtOulw8H34Ely7LIfrVbgEQJutmKa4pC25Vow-PkI4bmqwfDmNzaAydts--5groXn4F5iuBedYGL9H4atHpYUzGdHR5A6O3Qmk98r9N8iJAF1i6b68VoIdqDfqflJNT6nP1gprxtmzl3s6j_C1DRCN-XUAg3LlWNsFfAQr1hSQ9xVbqowU6J4GGkglL5Wbqjq-gPmAA-SQpDFBpF-YHkqfQn_YgZr1kfI_IAbvN66EQ1N3O1eNhQtq-OHyUT13UtNqljAgveAk.YQlqGl7YAdsqeouKLG9o8A',
    'pragma': 'no-cache',
    'referer': 'https://app.topvtop.pro/paymenthistory',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36',
}

params_get = {
    'dateFilter': 'all',
    'type': 'all',
    'limit': '5000',
    'skip': '0',
}
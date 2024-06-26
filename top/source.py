from common import *


URL_AUTH = 'https://app.topvtop.pro/api/auth/callback/credentials'
URL_DATA = 'https://app.topvtop.pro/api/paymenthistory/get'
SHORT_SLEEP = 50
LONG_SLEEP = 300
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
COLUMNS = ['_id', 'article', 'basisoperation', 'comment', 'dataoperation', 'refRewarded', 'summ', 'type', 'typeoperations', 'user']

COOKIES_AUTH = {
    '_ym_uid': '1699982868953556305',
    '_ym_d': '1699982868',
    '__Host-next-auth.csrf-token': '0d015f8072670419bb39cad5ebdab252f53a8e672c5966aee1f8618dcb9032c2%7C6b3f7df2154fe89bf01b634c451357194ceff763a3eb2fe38d5cdb987cae436d',
    '_ym_isad': '1',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fapp.topvtop.pro%2Fauth',
}

DATA_AUTH = {
    'redirect': 'false',
    'callbackUrl': '/stats?type=all&period=today',
    'csrfToken': '0d015f8072670419bb39cad5ebdab252f53a8e672c5966aee1f8618dcb9032c2',
    'json': 'true',
}

HEADERS_AUTH = {
    'authority': 'app.topvtop.pro',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,cy;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
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

COOKIES_GET = {
    '_ym_uid': '1699982868953556305',
    '_ym_d': '1699982868',
    '__Host-next-auth.csrf-token': '0d015f8072670419bb39cad5ebdab252f53a8e672c5966aee1f8618dcb9032c2%7C6b3f7df2154fe89bf01b634c451357194ceff763a3eb2fe38d5cdb987cae436d',
    '_ym_isad': '1',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fapp.topvtop.pro%2Fpaymenthistory',
    '_ym_visorc': 'w',
    '__Secure-next-auth.session-token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..slxG9EgiKqtpPggv.Y-llYy5HrrLrM6fEsOCddvvFFjIhrHtyzvSSEvrQjUzbDuUvJNwj3VM2tiyXcOwXi_QtOulw8H34Ely7LIfrVbgEQJutmKa4pC25Vow-PkI4bmqwfDmNzaAydts--5groXn4F5iuBedYGL9H4atHpYUzGdHR5A6O3Qmk98r9N8iJAF1i6b68VoIdqDfqflJNT6nP1gprxtmzl3s6j_C1DRCN-XUAg3LlWNsFfAQr1hSQ9xVbqowU6J4GGkglL5Wbqjq-gPmAA-SQpDFBpF-YHkqfQn_YgZr1kfI_IAbvN66EQ1N3O1eNhQtq-OHyUT13UtNqljAgveAk.YQlqGl7YAdsqeouKLG9o8A',
}

HEADERS_GET = {
    'authority': 'app.topvtop.pro',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,cy;q=0.8',
    'cache-control': 'no-cache',
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

PARAMS_GET = {
    'dateFilter': 'all',
    'type': 'all',
    'limit': '10000',
    'skip': '0',
}

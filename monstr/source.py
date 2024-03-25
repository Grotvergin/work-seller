from common import *


URL_AUTH = 'https://app.marketmonstr.pro/api/auth/callback/credentials'
URL_DATA = 'https://app.marketmonstr.pro/api/paymenthistory/get'
SHORT_SLEEP = 50
LONG_SLEEP = 300
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
COLUMNS = ['_id', 'article', 'basisoperation', 'comment', 'dataoperation', 'refRewarded', 'summ', 'type', 'typeoperations', 'user', 'mp']

COOKIES_AUTH = {
    '_ym_uid': '1710527117741009329',
    '_ym_d': '1710527117',
    '_ga': 'GA1.1.1145579256.1710527117',
    '__Host-next-auth.csrf-token': '2528be3092459453990091eea312ad4e6e082011ad8049b12e3010b0e1233878%7C38feca2d92b3e11664cab459bbcc4cfadd6b1e3b958a72476b99afce1a5b3d0a',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    'accountsSessionToken': '%255B%255D',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fapp.marketmonstr.pro%2Fauth',
    '_ga_3CZQZ6GGTK': 'GS1.1.1711368815.3.1.1711368886.0.0.0',
}

HEADERS_AUTH = {
    'authority': 'app.marketmonstr.pro',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,cy;q=0.8',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': '_ym_uid=1710527117741009329; _ym_d=1710527117; _ga=GA1.1.1145579256.1710527117; __Host-next-auth.csrf-token=2528be3092459453990091eea312ad4e6e082011ad8049b12e3010b0e1233878%7C38feca2d92b3e11664cab459bbcc4cfadd6b1e3b958a72476b99afce1a5b3d0a; _ym_isad=1; _ym_visorc=w; accountsSessionToken=%255B%255D; __Secure-next-auth.callback-url=https%3A%2F%2Fapp.marketmonstr.pro%2Fauth; _ga_3CZQZ6GGTK=GS1.1.1711368815.3.1.1711368886.0.0.0',
    'origin': 'https://app.marketmonstr.pro',
    'referer': 'https://app.marketmonstr.pro/auth',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36',
}

DATA_AUTH = {
    'redirect': 'false',
    'callbackUrl': '/buyouts',
    'csrfToken': '2528be3092459453990091eea312ad4e6e082011ad8049b12e3010b0e1233878',
    'json': 'true',
}

COOKIES_GET = {
    '_ym_uid': '1710527117741009329',
    '_ym_d': '1710527117',
    '_ga': 'GA1.1.1145579256.1710527117',
    '__Host-next-auth.csrf-token': '2528be3092459453990091eea312ad4e6e082011ad8049b12e3010b0e1233878%7C38feca2d92b3e11664cab459bbcc4cfadd6b1e3b958a72476b99afce1a5b3d0a',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    '__Secure-next-auth.session-token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..6y97DvqgT8TmmS2Z.yd79vIC_trXNce3GLDp-t2FBs0hUR_6HtNaSNXtJI3I6LAcGWxL_qt_68uVcTx34tjAXieAmlLEm81hjjIqL6hS_c7JlclgPWU02-dljbrUi6S18NivfjQb3EFLW9MUtdlCjYBe9PxFM2p3F1O7DeXNNh4JhPBcpHMgQ4kxlP6aAC8dcH8IK6G2gPmnz9c64MYlk62edAtbIQjpQcqSzm6ZU0gCzsFCzxI2aRSAfQgLLYD29sRYgjIWrEB7uN_Z-8efVDHYm-e9IO-v_IrNg7Beoee1wc_05Hu80EupBhSBW-U6ZtduNFICjBes0s7yOJIFMl3Ju9AuIFRtfsbEmJhH6p2FJgxr1.upEkFf_iGf8-UIb9TVUQOQ',
    '__Secure-next-auth.callback-url': 'https%3A%2F%2Fapp.marketmonstr.pro%2Fpaymenthistory',
    'accountsSessionToken': '%5B%7B%22token%22%3A%22eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..6y97DvqgT8TmmS2Z.yd79vIC_trXNce3GLDp-t2FBs0hUR_6HtNaSNXtJI3I6LAcGWxL_qt_68uVcTx34tjAXieAmlLEm81hjjIqL6hS_c7JlclgPWU02-dljbrUi6S18NivfjQb3EFLW9MUtdlCjYBe9PxFM2p3F1O7DeXNNh4JhPBcpHMgQ4kxlP6aAC8dcH8IK6G2gPmnz9c64MYlk62edAtbIQjpQcqSzm6ZU0gCzsFCzxI2aRSAfQgLLYD29sRYgjIWrEB7uN_Z-8efVDHYm-e9IO-v_IrNg7Beoee1wc_05Hu80EupBhSBW-U6ZtduNFICjBes0s7yOJIFMl3Ju9AuIFRtfsbEmJhH6p2FJgxr1.upEkFf_iGf8-UIb9TVUQOQ%22%2C%22uuid%22%3A%22c8a73cd7-e411-4ed1-bf86-a527bf11a043%22%7D%5D',
    '_ga_3CZQZ6GGTK': 'GS1.1.1711368815.3.1.1711369494.0.0.0',
}

HEADERS_GET = {
    'authority': 'app.marketmonstr.pro',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,cy;q=0.8',
    'referer': 'https://app.marketmonstr.pro/paymenthistory',
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
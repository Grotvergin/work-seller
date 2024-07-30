from common import *


URL = 'https://search.wb.ru/exactmatch/ru/common/v5/search'
COLUMNS = ['id', 'name', 'word', 'page', 'place',  'price', 'time']
PREFIX = 'NoLog'
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
SHORT_SLEEP = 1
LONG_SLEEP = 20
PAGES_QUANTITY = 10
TYPE = sys.argv[1]

PARAMS = {
    'ab_testing': 'false',
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'resultset': 'catalog',
    'sort': 'popular',
    'spp': '30',
    'suppressSpellcheck': 'false',
}

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9,cy;q=0.8',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search={}',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-queryid': 'qid398444427171994228020240721103639',
}

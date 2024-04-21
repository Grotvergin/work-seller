from common import *


URL = 'https://search.wb.ru/exactmatch/ru/male/v4/search'
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
    'uclusters': '1',
    'uiv': '2',
    'uv': 'pcurgKtTrZ8qY7FdL0-vCjAuqbE02ShGqcouqqbDHJkn2yz0FGGv2aIRLv-ixSwpJrEYviqGIogjCy1DL54xnK4zsXqhGKcfqoAh-TAOLxIsyieRLX8uMayjrlUrz7IwrKguC6kIrqAk06nDIACllCi-pBmrN6eipJ6w-DCjMPsy0i0dKtirlq6aLbWqc6s0JaUoWy4BJN6yaKwfnyiw_SdaHssxoyoRkOssN6pYqY0vxaw5LIitOLDtsQqroaywKCuozagEL6MtIiRlINyZkKWYlkQnm6iJJ-gnprK9qzouZK3kFjoqUycilfea3LC0LdarCx5lsAokz6-umAUnVQ',
}

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9,cy;q=0.8',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D1%81%D0%BC%D0%B5%D1%81%D0%B8%D1%82%D0%B5%D0%BB%D1%8C',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-queryid': 'qid276998376170013136520240421113024',
}

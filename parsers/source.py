from common import *


URL = 'https://search.wb.ru/exactmatch/ru/male/v4/search'
COLUMNS = ['id', 'name', 'word', 'page', 'place',  'price', 'time']
PREFIX = 'NoLog'
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
SHORT_SLEEP = 2
LONG_SLEEP = 45
PAGES_QUANTITY = 10
TYPE = sys.argv[1]

PARAMS = {
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
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D1%81%D0%BC%D0%B5%D1%81%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%20%D0%B4%D0%BB%D1%8F%20%D1%80%D0%B0%D0%BA%D0%BE%D0%B2%D0%B8%D0%BD%D1%8B%20%D0%B2%20%D0%B2%D0%B0%D0%BD%D0%BD%D1%83',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': None,
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MDgyNTAwNzEsInZlcnNpb24iOjIsInVzZXIiOiI4NDA1NjM3MSIsInNoYXJkX2tleSI6IjIyIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiY2ZhYjg5MmE2NjA2NDEyYmFhYzQwYzc3NzU4OTAwZmIiLCJ1c2VyX3JlZ2lzdHJhdGlvbl9kdCI6MTY3MDk0OTkxNSwidmFsaWRhdGlvbl9rZXkiOiIwNjY2YWVmZDNiYmE1NTc4OWRiYzlkMzMxMDBjMTE0YmJhZDkzZjAzZDUwNzU3OGE2NjkzY2RlZGRmMWM2NmQwIiwicGhvbmUiOiJNNUNhUlo0T28yQ1VZSnljaXFIcktBPT0ifQ.Us3jvtApitjIxwVV6fznhK-IYm-MqAp6mUDN7p5R6weQei1QLW0u749ZBFrih2kGtZUgpYa55xf4oNeAFLP5aK7tz6xXG1AeR2NRpPWlBckOe5Eot9OczwsJ9cy_dlt9Ky1Fee74qZ4EAob9LfL5JqBm_u0OUN076uvMIsU9YrNzeb1Ty34UCVK_ZWHsQjkU7TszvWJeCz7qE3VjHwXxsewzFlwMhkDAzzgPSUMoRIz4phcGcZJawjthXYjdqvxoYRMX82g23_MXtyEnx_pGwgjoKKnqiiLVqm3JZUlcI1_-PsIqkO7bY9YiXNE7s9y-Zyr8nH5R1doaJ9-GCwnXHg',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-queryid': 'qid188546224169804623820240221123400',
    'x-userid': '84056371',
}

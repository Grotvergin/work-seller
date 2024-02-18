from common import *


URL = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
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
    'dest': '-445297',
    'resultset': 'catalog',
    'sort': 'popular',
    'spp': '30',
    'suppressSpellcheck': 'false',
    'uclusters': '1',
    'uiv': '2',
    'uv': 'KQapx6pbrAKnda4qMoMpoStSqj0mZqjcqE0xHSqxLxGtWa1UqeKoGyNXKHYo4iSUqxCsha2zLnuwei9GHnifdbBSJBChoicKLW0tWTEFogIsvazdJlcw7CcolIsnAazIq_EwWScgI3YyGqanrnuyXiOSLFothaTtLUiwYaR5LU8tVy7ProSmSSbAIdikF6v4MSKo3RmJL7Gt0KjPsgut-6vkrHwigDISodMd2igopYorRihrLriv76tXsfIgJyzRsZOtaykgMS4tHii6MhWsbKnoIN4wtCe3qP2uRbDPqrai46fKJISsrawmHf2via-lM32kKSyfqnetViyXrcyr1A',
}

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9,cy;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wildberries.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D1%82%D0%B0%D1%80%D0%B5%D0%BB%D0%BA%D0%B8',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': None,
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MDgyNzIwMDEsInZlcnNpb24iOjIsInVzZXIiOiIzOTM1MTkyMCIsInNoYXJkX2tleSI6IjI0IiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiMWM4NGM2ZjgwYTRjNGMyOGJiNTk1MDdjMTg4YTQ4MWIiLCJ1c2VyX3JlZ2lzdHJhdGlvbl9kdCI6MTY4NDkyMjY4OSwidmFsaWRhdGlvbl9rZXkiOiJmNGRmZDAyNWM3ZmVkNjgxOGIxNTMxNGM0MzI0MWI5YzFlNDE0YWNjMmY2ZjFkODdjMmE5MTVjYzkzMmE2OWU3IiwicGhvbmUiOiJFRTdZUy8yTzZCWWtvYUZFVjNqSHFnPT0ifQ.dCMg6Ynni6dqRrbguNPKeMHbp1A5UH6dxah2h1A8khVS2PNKGy-htzLTDxzENDuhiz85uxLwwLGbg7SuiJ6PPDX2uzTPL2cp4DvkS0rwgv7Mkg-PFvhczQ1kxyHNv_m1JwlMD8IrEzrXbR9ILDfzMUzvDFNB10gYS18ycu0xKSg99z9ItEBXSWNnSm3NldW24BlCXfwRuB3YWZl8B89Ae4MG5H0bxgqij3ZqkysIPBtsr7bvymdR9GdAxUIjJoJ2Lq1XykIJsbkWWBG5ZQ9WYXdi3Fa11dEQ-cmhpQwAIrQsRQW8Eq-X6c3AUyAhhdIRoWX7BEiwurjQSLWlCM9AsQ',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-queryid': 'qid276998376170013136520240218190003',
    'x-userid': '39351920',
}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57',
    'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
    'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/105.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/104.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/104.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/104.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0',
]

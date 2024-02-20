from common import *

URL = 'https://card.wb.ru/cards/v1/detail'
COLUMNS = ['id', 'name', 'price', 'time']
NAME = (os.path.dirname(os.path.realpath(__file__))).replace('\\', '/').split('/')[-1]
SHORT_SLEEP = 6
LONG_SLEEP = 45

PARAMS = {
    'appType': '1',
    'curr': 'rub',
    'dest': '-445297',
    'spp': '30',
    'nm': None
}

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9,cy;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wildberries.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://www.wildberries.ru/catalog/74219035/detail.aspx?targetUrl=SP',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': None,
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MDgyNzIwMDEsInZlcnNpb24iOjIsInVzZXIiOiIzOTM1MTkyMCIsInNoYXJkX2tleSI6IjI0IiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiMWM4NGM2ZjgwYTRjNGMyOGJiNTk1MDdjMTg4YTQ4MWIiLCJ1c2VyX3JlZ2lzdHJhdGlvbl9kdCI6MTY4NDkyMjY4OSwidmFsaWRhdGlvbl9rZXkiOiJmNGRmZDAyNWM3ZmVkNjgxOGIxNTMxNGM0MzI0MWI5YzFlNDE0YWNjMmY2ZjFkODdjMmE5MTVjYzkzMmE2OWU3IiwicGhvbmUiOiJFRTdZUy8yTzZCWWtvYUZFVjNqSHFnPT0ifQ.dCMg6Ynni6dqRrbguNPKeMHbp1A5UH6dxah2h1A8khVS2PNKGy-htzLTDxzENDuhiz85uxLwwLGbg7SuiJ6PPDX2uzTPL2cp4DvkS0rwgv7Mkg-PFvhczQ1kxyHNv_m1JwlMD8IrEzrXbR9ILDfzMUzvDFNB10gYS18ycu0xKSg99z9ItEBXSWNnSm3NldW24BlCXfwRuB3YWZl8B89Ae4MG5H0bxgqij3ZqkysIPBtsr7bvymdR9GdAxUIjJoJ2Lq1XykIJsbkWWBG5ZQ9WYXdi3Fa11dEQ-cmhpQwAIrQsRQW8Eq-X6c3AUyAhhdIRoWX7BEiwurjQSLWlCM9AsQ',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

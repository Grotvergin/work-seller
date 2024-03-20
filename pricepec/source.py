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
    'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%B7%D0%B0%D0%BD%D0%B0%D0%B2%D0%B5%D1%81%D0%BA%D0%B0',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': None,
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MTA5MTg0OTgsInZlcnNpb24iOjIsInVzZXIiOiIzOTM1MTkyMCIsInNoYXJkX2tleSI6IjI0IiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiMWM4NGM2ZjgwYTRjNGMyOGJiNTk1MDdjMTg4YTQ4MWIiLCJ1c2VyX3JlZ2lzdHJhdGlvbl9kdCI6MTY4NDkyMjY4OSwidmFsaWRhdGlvbl9rZXkiOiJmNGRmZDAyNWM3ZmVkNjgxOGIxNTMxNGM0MzI0MWI5YzFlNDE0YWNjMmY2ZjFkODdjMmE5MTVjYzkzMmE2OWU3IiwicGhvbmUiOiJFRTdZUy8yTzZCWWtvYUZFVjNqSHFnPT0ifQ.L_5e7jc1ylllYoUc6VQUO_oZInApPZRzW3DgBcrHr4A3yi5RDiwc6GhbX0eyjol4UEeAqlCpWekB1rUNFkPKUQvDyPChv09DIKRhqCcHBVF6WLbGy2itmmBSHPrREaNZVy2aW8YBr_8akvg1SKG9MeBiujCFiJRQTy2i3PqtPuUH3IoejxrnExL7WIilk_DlW4lFSCNTVJo0jbvOuGbhRZoxkVvCSKPmw_3vPXa_ziFiHX6_sST9xIGVRCjZBAaBNvFUwUIK1vxSfuW6sZQK43GkhREgLAkDsRsK7SdDTEZKRcYCepfGeIwUF7sRXDPgdtDiY69YYQLL_hLXk3iLCQ',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "YaBrowser";v="23"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-queryid': 'qid276998376170013136520240320070831',
    'x-userid': '39351920',
}

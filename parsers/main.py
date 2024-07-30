from parsers.source import *


@Inspector(NAME + TYPE)
def Main() -> None:
    config, sections = ParseConfig(NAME)
    service = BuildService()
    for heading in sections:
        Stamp(f'Processing {heading}', 'b')
        column, sheet_id, proxies = ParseCurrentHeading(config, heading)
        row = len(GetColumn('A', service, heading, sheet_id)) + 2 if TYPE == '-d' else 2
        barcodes = GetColumn(column, service, 'Barcodes', sheet_id)
        words = GetColumn(column, service, 'Words', sheet_id)
        if TYPE == '-h':
            CleanSheet(len(COLUMNS), heading, sheet_id, service)
            CleanSheet(len(COLUMNS), PREFIX + heading, sheet_id, service)
        for word in words:
            Stamp(f'Processing template: {word}', 'i')
            data = []
            for page in range(1, PAGES_QUANTITY + 1):
                Stamp(f'Processing page {page}', 'i')
                raw = GetAndCheck(page, word, proxies)
                real = ProcessData(raw, word, page)
                data += FilterByBarcode(real, barcodes)
                AccurateSleep(SHORT_SLEEP, 0.5)
            UploadData(data, heading, sheet_id, service, row)
            row += len(data)


def GetAndCheck(page: int, word: str, proxies: dict = None) -> dict:
    raw = GetData(page, word, proxies)
    if 'data' not in raw:
        Stamp('No key <<data>> in response, processing again', 'w')
        AccurateSleep(SHORT_SLEEP, 0.5)
        raw = GetAndCheck(page, word, proxies)
    elif 'products' not in raw['data']:
        Stamp('No key <<products>> in response, processing again', 'w')
        AccurateSleep(SHORT_SLEEP, 0.5)
        raw = GetAndCheck(page, word, proxies)
    elif SmartLen(raw['data']['products']) == 1:
        Stamp('Length of products list is equal 1, processing again', 'w')
        AccurateSleep(SHORT_SLEEP, 0.5)
        raw = GetAndCheck(page, word, proxies)
    else:
        Stamp('Good data', 's')
    return raw


def ParseCurrentHeading(config: ConfigParser, heading: str) -> (str, str, dict):
    column = config[heading]['Column']
    sheet_id = config['DEFAULT']['SheetID' + TYPE]
    proxies = {
        'http': f'http://{config['DEFAULT']['Login']}:{config['DEFAULT']['Password']}@{config['DEFAULT']['IP/Port']}',
        'https': f'http://{config['DEFAULT']['Login']}:{config['DEFAULT']['Password']}@{config['DEFAULT']['IP/Port']}'
    }
    return column, sheet_id, proxies


def FilterByBarcode(list_for_filter: list, barcodes: list) -> list:
    filtered_list = []
    for sublist in list_for_filter:
        if sublist[0] in barcodes:
            filtered_list.append(sublist)
    return filtered_list


@ControlRecursion
def GetData(page: int, word: str, proxies: dict) -> dict:
    Stamp(f'Trying to connect {URL}', 'i')
    PARAMS['page'] = page
    PARAMS['query'] = word
    HEADERS['User-Agent'] = random.choice(USER_AGENTS)
    HEADERS['Referer'] = HEADERS['Referer'].format(quote(word))
    try:
        if random.choice([True, False]):
            Stamp('Using proxy', 'i')
            response = requests.get(URL, params=PARAMS, headers=HEADERS, proxies=proxies)
        else:
            Stamp('Using normal ip', 'i')
            response = requests.get(URL, params=PARAMS, headers=HEADERS)
    except requests.ConnectionError:
        Stamp(f'Connection on {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(page, word, proxies)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {URL}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response is empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {URL}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetData(page, word, proxies)
    return raw


def ProcessData(raw: dict, word: str, page: int) -> (list, list):
    data = []
    for i in range(SmartLen(raw['data']['products'])):
        row = []
        for column in COLUMNS:
            match column:
                case 'id':
                    row.append(str(raw['data']['products'][i]['id']))
                case 'name':
                    row.append(str(raw['data']['products'][i]['name']))
                case 'word':
                    row.append(word)
                case 'page':
                    row.append(str(page))
                case 'place':
                    row.append(str(i + 1))
                case 'time':
                    row.append(str(datetime.now().strftime('%Y-%m-%d %H:%M')))
                case 'price':
                    row.append(str(round(int(raw['data']['products'][i]['sizes'][0]['price']['product']) / 100)))
        data.append(row)
    return data


if __name__ == '__main__':
    Main()

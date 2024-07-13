from pricepec.source import *


@Inspector(NAME)
def Main() -> None:
    config, sections = ParseConfig(NAME)
    service = BuildService()
    for heading in sections:
        Stamp(f'Processing {heading}', 'b')
        column, sheet_id, proxies = ParseCurrentHeading(config, heading)
        barcodes = GetColumn(column, service, 'Barcodes', sheet_id)
        CleanSheet(len(COLUMNS), heading, sheet_id, service)
        list_of_rows = []
        for barcode in barcodes:
            Stamp(f'Processing barcode: {barcode}', 'i')
            raw = GetData(barcode, proxies)
            if BarcodeIsValid(raw):
                Stamp('Barcode is valid', 'i')
                list_of_rows.append(ProcessData(raw['data']['products'][0]))
            else:
                Stamp('Barcode is not valid', 'w')
                list_of_rows.append([barcode] + ['BarcodeError'] * 2 + [str(datetime.now().strftime('%Y-%m-%d %H:%M'))])
            Sleep(SHORT_SLEEP, 0.5)
        UploadData(list_of_rows, heading, sheet_id, service)


def BarcodeIsValid(raw: dict) -> bool:
    if 'data' in raw and 'products' in raw['data'] and raw['data']['products']:
        if 'sizes' in raw['data']['products'][0] and raw['data']['products'][0]['sizes']:
            if raw['data']['products'][0]['sizes'][0] and 'price' in raw['data']['products'][0]['sizes'][0]:
                if raw['data']['products'][0]['sizes'][0]['price'] and 'total' in raw['data']['products'][0]['sizes'][0]['price']:
                    if raw['data']['products'][0]['sizes'][0]['price']['total']:
                        return True
    return False


def ProcessData(raw: dict) -> list[str]:
    one_row = []
    for column in COLUMNS:
        match column:
            case 'id':
                one_row.append(str(raw['id']))
            case 'name':
                one_row.append(str(raw['name']))
            case 'price':
                one_row.append(str(int(int(raw['sizes'][0]['price']['total']))/100))
            case 'time':
                one_row.append(str(datetime.now().strftime('%Y-%m-%d %H:%M')))
    return one_row


def ParseCurrentHeading(config: ConfigParser, heading: str) -> (str, str, dict):
    column = config[heading]['Column']
    sheet_id = config['DEFAULT']['SheetID']
    proxies = {
        'http': f'http://{config['DEFAULT']['Login']}:{config['DEFAULT']['Password']}@{config['DEFAULT']['IP/Port']}',
        'https': f'http://{config['DEFAULT']['Login']}:{config['DEFAULT']['Password']}@{config['DEFAULT']['IP/Port']}'
    }
    return column, sheet_id, proxies


@ControlRecursion
def GetData(barcode: str, proxies: dict) -> dict:
    Stamp(f'Trying to connect {URL}', 'i')
    PARAMS['nm'] = barcode
    HEADERS['User-Agent'] = random.choice(USER_AGENTS)
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
        raw = GetData(barcode, proxies)
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
            raw = GetData(barcode, proxies)
    return raw


if __name__ == '__main__':
    Main()

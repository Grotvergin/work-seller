from hour_parser.source import *


def main():
    config, sections = ParseConfig('hour_parser')
    service = BuildService()
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', heading, len(COLUMNS), SHEET_ID, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', PREFIX + heading, len(COLUMNS), SHEET_ID, service)
        row = 2
        words = GetColumn(config[heading]['Column'], service, 'Words')
        empty = PrepareEmpty(len(COLUMNS), BLANK_ROWS)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, heading, SHEET_ID, service, row)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, PREFIX + heading, SHEET_ID, service, row)
        for word in words:
            Stamp(f'Processing template: {word}', 'i')
            for page in range(1, PAGES_QUANTITY + 1):
                Stamp(f'Processing page {page}', 'i')
                PARAMS['page'] = page
                PARAMS['query'] = word
                raw = GetData()
                if raw:
                    advertise, real = ProcessData(raw, heading, word, page)
                    ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, advertise, heading, SHEET_ID, service, row)
                    ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, real, PREFIX + heading, SHEET_ID, service, row)
                    row += len(advertise)
                else:
                    Stamp(f'Page {page} is empty', 'w')
                Sleep(SHORT_SLEEP, 0.5)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', heading, len(COLUMNS), SHEET_ID, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', PREFIX + heading, len(COLUMNS), SHEET_ID, service)
        Stamp(f'End of processing {heading}', 'b')
    Finish(TIMEOUT, NAME)


def GetColumn(column: str, service, sheet_name: str):
    Stamp(f'Trying to get column {column} from sheet {sheet_name}', 'i')
    ControlTimeout(TIMEOUT, NAME)
    try:
        res = service.spreadsheets().values().get(spreadsheetId=SHEET_ID,
                                                  range=f'{sheet_name}!{column}2:{column}{MAX_ROW}').execute().get('values', [])
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror, HttpError) as err:
        Stamp(f'Status = {err} on getting column from sheet {sheet_name}', 'e')
        Sleep(LONG_SLEEP)
        res = GetColumn(column, service, sheet_name)
    else:
        if not res:
            Stamp(f'No elements in column {column} sheet {sheet_name} found', 'w')
        else:
            Stamp(f'Found {len(res)} elements from column {column} sheet {sheet_name}', 's')
            res = [item for sublist in res for item in sublist]
    return res


def GetData():
    Stamp(f'Trying to connect WB URL: {URL}', 'i')
    ControlTimeout(TIMEOUT, NAME)
    try:
        response = requests.get(URL, params=PARAMS, headers=HEADERS)
    except requests.ConnectionError:
        Stamp(f'Connection on WB URL: {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData()
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on WB URL: {URL}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response in empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on WB URL: {URL}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetData()
    return raw


def ProcessData(raw: dict, sheet_name: str, word: str, page: int):
    try:
        height = len(raw['data']['products'])
    except TypeError:
        height = 0
        Stamp(f'For sheet {sheet_name} found NO products', 'w')
    else:
        Stamp(f'For sheet {sheet_name} found {height} products', 's')
    list_real = []
    list_advertise = []
    for i in range(height):
        row_advertise = []
        row_real = []
        for column in COLUMNS:
            match column:
                case 'id':
                    row_advertise.append(str(raw['data']['products'][i]['id']))
                    row_real.append(str(raw['data']['products'][i]['id']))
                case 'name':
                    row_advertise.append(str(raw['data']['products'][i]['name']))
                    row_real.append(str(raw['data']['products'][i]['name']))
                case 'word':
                    row_advertise.append(word)
                    row_real.append(word)
                case 'page':
                    row_advertise.append(str(page))
                    row_real.append(str(page))
                case 'place':
                    row_real.append(str(i + 1))
                    try:
                        index_from_log = raw['data']['products'][i]['log']['position']
                    except KeyError:
                        row_advertise.append(str(i + 1))
                    else:
                        row_advertise.append(str(index_from_log + 1))
                case 'time':
                    row_advertise.append(str(datetime.now().strftime('%Y-%m-%d %H:%M')))
                    row_real.append(str(datetime.now().strftime('%Y-%m-%d %H:%M')))
        list_advertise.append(row_advertise)
        list_real.append(row_real)
    return list_advertise, list_real


if __name__ == '__main__':
    main()

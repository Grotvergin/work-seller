from prices.source import *


def main():
    config, sections = ParseConfig('prices')
    service = BuildService()
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        token = config[heading]['Token']
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', heading, len(COLUMNS), SHEET_ID, service)
        empty = PrepareEmpty(len(COLUMNS), BLANK_ROWS)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, heading, SHEET_ID, service)
        raw = GetData(token)
        if raw:
            prepared = ProcessData(raw, heading)
            ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, prepared, heading, SHEET_ID, service)
        else:
            Stamp(f'Sheet {heading} is empty', 'w')
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', heading, len(COLUMNS), SHEET_ID, service)
        Stamp(f'End of processing {heading}', 'b')
        Sleep(SHORT_SLEEP)
    Finish(TIMEOUT, NAME)


def GetData(token: str):
    Stamp(f'Trying to connect WB URL: {URL}', 'i')
    ControlTimeout(TIMEOUT, NAME)
    try:
        response = requests.get(URL, headers={'Authorization': token})
    except requests.ConnectionError:
        Stamp(f'Connection on WB URL: {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(token)
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
            raw = GetData(token)
    return raw


def ProcessData(raw: dict, sheet_name: str):
    try:
        height = len(raw)
    except TypeError:
        height = 0
        Stamp(f'For sheet {sheet_name} found NO rows', 'w')
    else:
        Stamp(f'For sheet {sheet_name} found {height} rows', 'i')
    list_of_rows = []
    for i in range(height):
        one_row = []
        for column in COLUMNS:
            if column == 'time':
                one_row.append(str(datetime.now().strftime('%m-%d %H:%M')))
            else:
                try:
                    one_row.append(str(raw[i][column]).replace('.', ','))
                except KeyError:
                    one_row.append(MSG)
        list_of_rows.append(one_row)
    return list_of_rows


if __name__ == '__main__':
    main()

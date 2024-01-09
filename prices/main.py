from prices.source import *


@Inspector(NAME)
def Main():
    config, sections = ParseConfig(NAME)
    service = BuildService()
    for heading in sections:
        Stamp(f'Processing {heading}', 'b')
        token, sheet_id = ParseCurrentHeading(config, heading)
        CleanSheet(len(COLUMNS), heading, sheet_id, service)
        raw = GetData(token)
        prepared = ProcessData(raw)
        UploadData(prepared, heading, sheet_id, service)


def ParseCurrentHeading(config: ConfigParser, heading: str) -> (str, str):
    token = config[heading]['Token']
    sheet_id = config['DEFAULT']['SheetID']
    return token, sheet_id


@ControlRecursion
def GetData(token: str) -> list:
    Stamp(f'Trying to connect {URL}', 'i')
    try:
        response = requests.get(URL, headers={'Authorization': token})
    except requests.ConnectionError:
        Stamp(f'Connection on {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(token)
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
            raw = GetData(token)
    return raw


def ProcessData(raw: list) -> list:
    list_of_rows = []
    for i in range(SmartLen(raw)):
        one_row = []
        for column in COLUMNS:
            if column == 'time':
                one_row.append(str(datetime.now().strftime('%Y-%m-%d %H:%M')))
            else:
                try:
                    one_row.append(str(raw[i][column]).replace('.', ','))
                except KeyError:
                    one_row.append(MSG)
        list_of_rows.append(one_row)
    return list_of_rows


if __name__ == '__main__':
    Main()

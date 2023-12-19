from top.source import *


def main():
    config, sections = ParseConfig('top')
    service = BuildService()
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        ExecuteRetry(START, TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', heading, len(COLUMNS), SHEET_ID, service)
        login, password = ParseCurrentHeading(config, heading)
        DATA_AUTH['email'] = login
        DATA_AUTH['password'] = password
        empty = PrepareEmpty(len(COLUMNS), BLANK_ROWS)
        ExecuteRetry(START, TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, heading, SHEET_ID, service)
        session = Authorize()
        raw = GetData(session)
        if raw:
            prepared = PrepareData(raw, heading, COLUMNS)
            ExecuteRetry(START, TIMEOUT, NAME, LONG_SLEEP, UploadData, prepared, heading, SHEET_ID, service)
        else:
            Stamp(f'Sheet {heading} is empty', 'w')
        ExecuteRetry(START, TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', heading, len(COLUMNS), SHEET_ID, service)
        Stamp(f'End of processing {heading}', 'b')
        Sleep(SHORT_SLEEP, 0.5)
    ControlTimeout(START, TIMEOUT, NAME)
    SendEmail(f'{NAME} OK: elapsed {int(time.time() - START)}')
    Stamp('All data was uploaded successfully', 'b')


def ParseCurrentHeading(config, heading: str):
    login = config[heading]['Login']
    password = config[heading]['Password']
    return login, password


def PrepareData(raw: dict, sheet_name: str, column_names: list):
    try:
        height = len(raw)
    except TypeError:
        height = 0
        Stamp(f'For sheet {sheet_name} found NO operations', 'w')
    else:
        Stamp(f'For sheet {sheet_name} found {height} operations', 'i')
    list_of_rows = []
    for i in range(height):
        one_row = []
        for column in column_names:
            try:
                if column == 'summ':
                    one_row.append(str(raw[i][column]).replace('.', ','))
                else:
                    one_row.append(str(raw[i][column]))
            except KeyError:
                one_row.append(MSG)
        list_of_rows.append(one_row)
    return list_of_rows


def Authorize():
    session = requests.Session()
    Stamp(f'Trying to authorize TopVTop URL: {URL_AUTH}', 'i')
    try:
        response = session.post(URL_AUTH, headers=HEADERS_AUTH, data=DATA_AUTH, cookies=COOKIES_AUTH)
    except requests.ConnectionError:
        Stamp('On authorization', 'e')
        Sleep(LONG_SLEEP)
        session = Authorize()
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on authorization', 's')
        else:
            Stamp(f'Status = {response.status_code} on authorization', 'e')
            Sleep(LONG_SLEEP)
            session = Authorize()
    return session


def GetData(session: requests.Session):
    Stamp(f'Trying to connect TopVTop URL: {URL_DATA}', 'i')
    try:
        response = session.get(URL_DATA, headers=HEADERS_GET, params=PARAMS_GET, cookies=COOKIES_GET)
    except requests.ConnectionError:
        Stamp(f'Connection on TopVTop URL: {URL_DATA}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(session)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on TopVTop URL: {URL_DATA}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response in empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on TopVTop URL: {URL_DATA}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetData(session)
    return raw


if __name__ == '__main__':
    main()

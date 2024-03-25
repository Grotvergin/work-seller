from monstr.source import *


@Inspector(NAME)
def Main() -> None:
    config, sections = ParseConfig(NAME)
    service = BuildService()
    for heading in sections:
        Stamp(f'Processing {heading}', 'b')
        sheet_id = ParseCurrentHeading(config, heading)
        CleanSheet(len(COLUMNS), heading, sheet_id, service)
        raw = GetData(Authorize())
        UploadData(ProcessData(raw), heading, sheet_id, service)
        Sleep(SHORT_SLEEP, 0.5)


@ControlRecursion
def GetData(session: requests.Session) -> list:
    Stamp(f'Trying to connect {URL_DATA}', 'i')
    try:
        response = session.get(URL_DATA, headers=HEADERS_GET, params=PARAMS_GET, cookies=COOKIES_GET)
    except requests.ConnectionError:
        Stamp(f'Connection on {URL_DATA}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(session)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {URL_DATA}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response is empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {URL_DATA}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetData(session)
    return raw


def ParseCurrentHeading(config: ConfigParser, heading: str) -> str:
    sheet_id = config['DEFAULT']['SheetID']
    DATA_AUTH['email'] = config[heading]['Login']
    DATA_AUTH['password'] = config[heading]['Password']
    return sheet_id


def ProcessData(raw: list) -> list:
    list_of_rows = []
    for i in range(SmartLen(raw)):
        one_row = []
        for column in COLUMNS:
            try:
                if column == 'summ':
                    one_row.append(str(raw[i][column]).replace('.', ','))
                else:
                    one_row.append(str(raw[i][column]))
            except KeyError:
                one_row.append(MSG)
        list_of_rows.append(one_row)
    return list_of_rows


@ControlRecursion
def Authorize() -> requests.Session:
    Stamp(f'Trying to authorize {URL_AUTH}', 'i')
    session = requests.Session()
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


if __name__ == '__main__':
    Main()

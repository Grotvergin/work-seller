from paid.secret import *
from paid.source import *


@Inspector(NAME)
def Main() -> None:
    service = BuildService()
    for cabinet, token in TOKENS.items():
        task = GetData(token, URL, {'dateFrom': YESTERDAY + 'T00:00:00',
                                       'dateTo': YESTERDAY + 'T23:59:59'})
        Sleep(SHORT_SLEEP)
        data = GetData(token, URL + '/tasks/' + task['data']['taskId'] + '/download')
        data = ProcessData(data)
        row = len(GetColumn('A', service, cabinet, SHEET_ID)) + 2
        UploadData(data, cabinet, SHEET_ID, service, row)


def ProcessData(data: dict) -> list:
    list_of_rows = []
    for row in data:
        one_row = []
        for column in COLUMNS:
            if IsNumber(row[column]):
                one_row.append((str(round(float(row[column]), 2))).replace('.', ','))
            else:
                one_row.append(row[column])
        list_of_rows.append(one_row)
    return list_of_rows


def IsNumber(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


@ControlRecursion
def GetData(token: str, url: str, params: dict = None) -> dict:
    Stamp(f'Trying to connect {url}', 'i')
    try:
        response = requests.get(url, params=params, headers={'Authorization': token})
    except requests.ConnectionError:
        Stamp(f'Connection on {url}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(token, url, params)
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
            raw = GetData(token, url, params)
    return raw


if __name__ == '__main__':
    Main()
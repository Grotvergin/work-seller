from graphs.source import *
from graphs.secret import *


@Inspector(NAME)
def Main() -> None:
    service = BuildService()
    for i, (cabinet, creds) in enumerate(CABINETS_AND_CREDS.items()):
        CleanSheet(len(COLUMNS), cabinet, SHEET_ID, service)
        final_data = []
        column = chr(i + ord('A'))
        date_from, date_to = GetColumn(column, service, 'Periods', SHEET_ID)
        category_codes = GetColumn(column, service, 'Categories', SHEET_ID)
        for code in category_codes:
            data = GetData(creds['Cookies'], creds['Headers'], code, date_from, date_to)
            data = PrepareData(data)
            final_data += data
            Sleep(SHORT_SLEEP, 0.5)
        UploadData(final_data, cabinet, SHEET_ID, service)


def PrepareData(data: dict) -> list:
    list_of_rows = []
    for good in data['result']['data']:
        one_row = []
        for i, column in enumerate(COLUMNS):
            if column in COLUMNS[:4]:
                one_row.append(str(good['dimensions'][0][column]))
            else:
                one_row.append(str(round(good['metrics'][i - 4])))
        list_of_rows.append(one_row)
    return list_of_rows


@ControlRecursion
def GetData(cookies: dict, headers:dict, code: str, date_from: str, date_to: str) -> dict:
    Stamp(f'Trying to connect {URL}', 'i')
    body = SAMPLE.copy()
    body['date_from'] = date_from
    body['date_to'] = date_to
    body['filters'][0]['value'] = code
    try:
        response = requests.post(URL, headers=headers, json=body, cookies=cookies)
    except requests.ConnectionError:
        Stamp(f'Connection on {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(cookies, headers, code, date_from, date_to)
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
            raw = GetData(cookies, headers, code, date_from, date_to)
    return raw


if __name__ == '__main__':
    Main()

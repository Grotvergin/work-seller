from search.source import *
from search.secret import *


@Inspector(NAME)
def Main():
    service = BuildService()
    for i, (cabinet, creds) in enumerate(CABINETS_AND_CREDS.items()):
        CleanSheet(len(COLUMNS), cabinet, SHEET_ID, service)
        column = chr(i + ord('A'))
        date_from, date_to = GetColumn(column, service, 'Periods', SHEET_ID)
        data = GetData(creds['Cookies'], creds['Headers'], date_from, date_to)
        data = PrepareData(data)
        UploadData(data, cabinet, SHEET_ID, service)
        Sleep(SHORT_SLEEP, 0.5)


def PrepareData(data: dict) -> list:
    list_of_rows = []
    for good in data['products']:
        one_row = []
        for column in COLUMNS:
            if column in COLUMNS[:7]:
                value = good[column]
            else:
                value = good['metrics'][column]
            if isinstance(value, (int, float)):
                formatted_value = "{:.3f}".format(value).replace('.', ',')
                one_row.append(formatted_value)
            else:
                one_row.append(str(value))
        list_of_rows.append(one_row)
    return list_of_rows


@ControlRecursion
def GetData(cookies: dict, headers: dict, date_from: str, date_to: str) -> dict:
    Stamp(f'Trying to connect {URL}', 'i')
    body = SAMPLE.copy()
    body['completeFilter']['metricsTimeBounds']['from'] = date_from
    body['completeFilter']['metricsTimeBounds']['to'] = date_to
    try:
        response = requests.post(URL, headers=headers, json=body, cookies=cookies)
    except requests.ConnectionError:
        Stamp(f'Connection on {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(cookies, headers, date_from, date_to)
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
            raw = GetData(cookies, headers, date_from, date_to)
    return raw


if __name__ == '__main__':
    Main()

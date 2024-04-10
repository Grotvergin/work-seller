from stencil.source import *
from stencil.secret import *


@Inspector(NAME)
def Main():
    service = BuildService()
    for i, (cabinet, creds) in enumerate(CABINETS_AND_CREDS.items()):
        final_data = []
        CleanSheet(len(COLUMNS), cabinet, SHEET_ID, service)
        column = chr(i + ord('A'))
        date_from, date_to = GetColumn(column, service, 'Periods', SHEET_ID)
        campaigns = GetCampaigns(creds['Cookies'], creds['Headers'], date_from, date_to)
        campaigns = [campaign for campaign in campaigns['campaigns'] if campaign['status'] != 'SERVING_STATE_ARCHIVED']
        for campaign in campaigns:
            data = GetDetailed(creds['Cookies'], creds['Headers'], date_from, date_to, campaign['id'])
            data = PrepareData(data)
            final_data += data
            Sleep(SHORT_SLEEP, 0.5)
        UploadData(final_data, cabinet, SHEET_ID, service)


def PrepareData(data: dict) -> list:
    list_of_rows = []
    for good in data['items']:
        one_row = []
        for column in COLUMNS:
            if column in COLUMNS[:11]:
                one_row.append(str(good[column]))
            else:
                one_row.append(str(round(float(good['stats']['stats'][column]), 3)).replace('.', ','))
        list_of_rows.append(one_row)
    return list_of_rows


@ControlRecursion
def GetDetailed(cookie: str, headers: str, date_from: str, date_to: str, id_campaign: str) -> list:
    url = URL_INFO.format(id_campaign)
    Stamp(f'Trying to connect {url}', 'i')
    params = PARAMS_INFO.copy()
    params['statsIntervalFrom'] = date_from
    params['statsIntervalTo'] = date_to
    try:
        response = requests.get(url, headers=headers, cookies=cookie, params=params)
    except requests.ConnectionError:
        Stamp(f'Connection on {url}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetDetailed(cookie, headers, date_from, date_to, id_campaign)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {url}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response is empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {url}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetDetailed(cookie, headers, date_from, date_to, id_campaign)
    return raw


@ControlRecursion
def GetCampaigns(cookie: str, headers: str, date_from: str, date_to: str) -> list:
    Stamp(f'Trying to connect {URL_CAMPAIGNS}', 'i')
    body = SAMPLE_CAMPAIGNS.copy()
    body['statsFrom'] = date_from
    body['statsTo'] = date_to
    try:
        response = requests.post(URL_CAMPAIGNS, headers=headers, json=body, cookies=cookie)
    except requests.ConnectionError:
        Stamp(f'Connection on {URL_CAMPAIGNS}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetCampaigns(cookie, headers, date_from, date_to)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {URL_CAMPAIGNS}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response is empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {URL_CAMPAIGNS}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetCampaigns(cookie, headers, date_from, date_to)
    return raw


if __name__ == '__main__':
    Main()
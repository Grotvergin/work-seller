from search.source import *
from search.secret import *


@Inspector(NAME)
def Main():
    service = BuildService()
    for i, (cabinet, creds) in enumerate(CABINETS_AND_CREDS.items()):
        Stamp(f'Processing {cabinet}', 'b')
        final_data = []
        CleanSheet(len(COLUMNS), cabinet, SHEET_ID, service)
        column = chr(i + ord('A'))
        date_from, date_to = GetColumn(column, service, 'Periods', SHEET_ID)
        data_campaigns = GetCampaigns(creds['Cookies'], creds['Headers'], date_from, date_to)
        for campaign in data_campaigns['campaigns']:
            report_uuid = GetReportUUID(creds['Cookies'], creds['Headers'], date_from[:10], date_to[:10], campaign['id'])
            Sleep(SHORT_SLEEP)
            data = GetData(creds['Cookies'], creds['Headers'], report_uuid['UUID'])
            final_data += data
        UploadData(final_data, cabinet, SHEET_ID, service)
        Sleep(SHORT_SLEEP)


@ControlRecursion
def GetData(cookie: str, headers: str, uuid: str) -> dict:
    Stamp(f'Trying to connect {URL_DOWNLOAD}', 'i')
    try:
        response = requests.get(URL_DOWNLOAD, headers=headers, cookies=cookie, params={'UUID': uuid, 'vendor': 'false'})
    except requests.ConnectionError:
        Stamp(f'Connection on {URL_DOWNLOAD}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(cookie, headers, uuid)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {URL_DOWNLOAD}', 's')
            if response.content:
                csv_data = StringIO(response.text)
                reader = csv.reader(csv_data, delimiter=';')
                raw = list(reader)[2:]
                if raw:
                    raw.pop(-1)
            else:
                Stamp('Response is empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {URL_DOWNLOAD}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetData(cookie, headers, uuid)
    return raw


@ControlRecursion
def GetReportUUID(cookie: str, headers: str, date_from: str, date_to: str, id_campaign: str) -> dict:
    Stamp(f'Trying to connect {URL_PREPARE}', 'i')
    body = SAMPLE_PREPARE.copy()
    body['dateTo'] = date_to + 'T00:00:00.000Z'
    body['dateFrom'] = date_from + 'T00:00:00.000Z'
    body['campaignId'] = id_campaign
    try:
        response = requests.post(URL_PREPARE, headers=headers, json=body, cookies=cookie)
    except requests.ConnectionError:
        Stamp(f'Connection on {URL_PREPARE}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetReportUUID(cookie, headers, date_from, date_to, id_campaign)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {URL_PREPARE}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response is empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {URL_PREPARE}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetReportUUID(cookie, headers, date_from, date_to, id_campaign)
    return raw


@ControlRecursion
def GetCampaigns(cookies: dict, headers: dict, date_from: str, date_to: str) -> dict:
    Stamp(f'Trying to connect {URL_CAMPAIGNS}', 'i')
    body = SAMPLE_CAMPAIGNS.copy()
    body['statsFrom'] = date_from + 'T00:00:00.000Z'
    body['statsTo'] = date_to + 'T00:00:00.000Z'
    try:
        response = requests.post(URL_CAMPAIGNS, headers=headers, json=body, cookies=cookies)
    except requests.ConnectionError:
        Stamp(f'Connection on {URL_CAMPAIGNS}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetCampaigns(cookies, headers, date_from, date_to)
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
            raw = GetCampaigns(cookies, headers, date_from, date_to)
    return raw


if __name__ == '__main__':
    Main()

from oldsearch.source import *
from oldsearch.secret import *


@Inspector(NAME)
def Main():
    service = BuildService()
    for i, (cabinet, creds) in enumerate(CABINETS_AND_CREDS.items()):
        CleanSheet(len(COLUMNS_CAMPAIGNS), cabinet + ' Campaigns', SHEET_ID, service)
        CleanSheet(len(COLUMNS_GOODS), cabinet + ' Goods', SHEET_ID, service)
        column = chr(i + ord('A'))
        date_from, date_to = GetColumn(column, service, 'Periods', SHEET_ID)
        data_campaigns = GetCampaigns(creds['Cookies'], creds['Headers'], date_from, date_to)
        data_for_upload = ProcessCampaigns(data_campaigns)
        UploadData(data_for_upload, cabinet + ' Campaigns', SHEET_ID, service)
        Sleep(SHORT_SLEEP, 0.5)
        data_goods = []
        for campaign in data_campaigns['campaigns']:
            data_good = GetGoods(creds['Cookies'], creds['Headers'], campaign['id'])
            data_good = ProcessGoods(data_good, campaign['id'])
            data_goods += data_good
            Sleep(SHORT_SLEEP, 0.5)
        UploadData(data_goods, cabinet + ' Goods', SHEET_ID, service)


def ProcessCampaigns(data: dict) -> list[list[str]]:
    list_of_rows = []
    for campaign in data['campaigns']:
        one_row = []
        for column in COLUMNS_CAMPAIGNS:
            if column == 'createdAt':
                one_row.append(str(campaign[column][:16]))
            elif column in ('id', 'title'):
                one_row.append(str(campaign[column]))
            else:
                one_row.append(str(campaign['metrics'][column]).replace('.', ','))
        list_of_rows.append(one_row)
    return list_of_rows


def ProcessGoods(data: dict, campaign_id: str) -> list[list[str]]:
    list_of_rows = []
    for good in data['products']:
        one_row = []
        for column in COLUMNS_GOODS:
            try:
                if column == 'campaign':
                    one_row.append(str(campaign_id))
                elif column in ('previousWeek', 'thisWeek'):
                    one_row.append(str(good['views'][column]).replace('.', ','))
                elif column in ('bid', 'bidPrice', 'updatedAt'):
                    one_row.append(str(good['previousBid'][column]).replace('.', ','))
                else:
                    one_row.append(str(good[column]).replace('.', ','))
            except (TypeError, KeyError, ValueError):
                one_row.append(MSG)
        list_of_rows.append(one_row)
    return list_of_rows


@ControlRecursion
def GetCampaigns(cookies: dict, headers: dict, date_from: str, date_to: str) -> dict:
    Stamp(f'Trying to connect {URL_CAMPAIGNS}', 'i')
    body = SAMPLE_CAMPAIGNS.copy()
    body['statsFrom'] = date_from
    body['statsTo'] = date_to
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


@ControlRecursion
def GetGoods(cookies: dict, headers: dict, id_good: str) -> dict:
    url = URL_GOODS.format(id_good)
    Stamp(f'Trying to connect {url}', 'i')
    try:
        response = requests.post(url, headers=headers, json=SAMPLE_GOODS, cookies=cookies)
    except requests.ConnectionError:
        Stamp(f'Connection on {url}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetCampaigns(cookies, headers, id_good)
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
            raw = GetCampaigns(cookies, headers, id_good)
    return raw


if __name__ == '__main__':
    Main()
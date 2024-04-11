from external.source import *
from external.secret import *


def Main() -> None:
    service = BuildService()
    threads = []
    for i, cabinet in enumerate(CABINETS):
        column = chr(i + 1 + ord('A'))
        res = GetColumn(column, service, 'Данные', SHEET_ID)
        if len(res) == 2:
            token, date_from = res
            date_to = TODAY
        else:
            token, date_from, date_to = res
        thread = Thread(target=ParallelThreads, args=(token, date_from, date_to, service, cabinet))
        thread.start()
        threads.append(thread)
        Sleep(THR_DELTA, 0.5)
    for thread in threads:
        thread.join()


def ParallelThreads(token: str, date_from: str, date_to: str, service: googleapiclient.discovery.Resource, heading: str):
    with stamp_lock:
        Stamp(f'Opened thread for {heading}', 'b')
    with upload_lock:
        CleanSheet(len(COLUMNS), heading, SHEET_ID, service)
    campaigns = PrepareCampaigns(token)
    ProcessData(date_from, date_to, campaigns, heading, token, SHEET_ID, service)
    with stamp_lock:
        Stamp(f'Closed thread for {heading}', 'b')


def PrepareCampaigns(token: str) -> dict:
    raw = GetData(URL_CAMPAIGNS, token)
    dict_of_campaigns = {}
    for i in range(SmartLen(raw['adverts'])):
        for j in range(SmartLen(raw['adverts'][i]['advert_list'])):
            dict_of_campaigns[raw['adverts'][i]['advert_list'][j]['advertId']] = raw['adverts'][i]['type']
    return dict_of_campaigns


@ControlRecursion
def GetData(url: str, token:str, body: list = None) -> dict:
    Stamp(f'Trying to connect {url}', 'i')
    try:
        if body is None:
            response = requests.get(url, headers={'Authorization': token})
        else:
            response = requests.post(url, headers={'Authorization': token}, data=json.dumps(body))
    except requests.ConnectionError:
        Stamp(f'Connection on {url}', 'e')
        Sleep(SLEEP)
        raw = GetData(url, token, body)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on URL: {url}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response is empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {url}', 'e')
            Sleep(SLEEP)
            raw = GetData(url, token, body)
    return raw


def ProcessData(date_from: str, date_to: str, raw: dict, sheet_name: str, token: str, sheet_id: str, service: googleapiclient.discovery.Resource) -> None:
    row = 2
    with stamp_lock:
        Stamp(f'For sheet {sheet_name} found {SmartLen(raw)} companies', 'i')
    for i in range(0, SmartLen(raw), PORTION):
        with stamp_lock:
            Stamp(f'Processing {PORTION} campaigns from {i} out of {SmartLen(raw)}', 'i')
        portion_of_campaigns = list(raw.keys())[i:i + PORTION]
        list_for_request = [{'id': campaign, 'interval': {'begin': date_from, 'end': date_to}} for campaign in portion_of_campaigns]
        data = GetData(URL_STAT, token, list_for_request)
        list_of_rows = []
        for t in range(SmartLen(data)):
            for j in range(SmartLen(data[t]['days'])):
                for k in range(SmartLen(data[t]['days'][j]['apps'])):
                    for nm in range(SmartLen(data[t]['days'][j]['apps'][k]['nm'])):
                        one_row = []
                        for key, value in COLUMNS.items():
                            try:
                                if value is None:
                                    one_row.append(str(data[t]['days'][j]['apps'][k]['nm'][nm][key]).replace('.', ','))
                                elif key == 'advertId':
                                    one_row.append(str(data[t]['advertId']))
                                elif key == 'date':
                                    one_row.append(str(data[t]['days'][j]['date'])[:10])
                                elif key == 'appType':
                                    one_row.append(str(data[t]['days'][j]['apps'][k][key]))
                                elif key == 'companyType':
                                    one_row.append(str(TYPES_AND_NAMES[int(raw[data[t]['advertId']])]))
                                else:
                                    one_row.append(value.replace('.', ','))
                            except KeyError:
                                one_row.append(MSG)
                        list_of_rows.append(one_row)
        with upload_lock:
            UploadData(list_of_rows, sheet_name, sheet_id, service, row)
        row += len(list_of_rows)
        Sleep(SLEEP)


if __name__ == '__main__':
    upload_lock = Lock()
    stamp_lock = Lock()
    Main()

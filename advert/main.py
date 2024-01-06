from advert.source import *


@Inspector(NAMES[NAME])
def Main() -> None:
    config, sections = ParseConfig(NAME)
    service = BuildService()
    for heading in sections:
        Stamp(f'Processing {heading}', 'b')
        token, sheet_id = ParseCurrentHeading(config, heading)
        CleanSheet(len(COLUMNS), heading, sheet_id, service)
        CleanSheet(len(COLUMNS), PREFIX_MONTH + heading, sheet_id, service)
        campaigns = PrepareCampaigns(token)
        ProcessData(campaigns, heading, token, sheet_id, service)


def ParseCurrentHeading(config: ConfigParser, heading: str) -> (str, str):
    token = config[heading]['Token']
    sheet_id = config['DEFAULT']['SheetID']
    return token, sheet_id


def CheckCurMonth(cur_date: str) -> bool:
    if cur_date[:4] == YEAR and cur_date[5:7] == MONTH:
        return True
    return False


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
        Sleep(LONG_SLEEP)
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
            Sleep(LONG_SLEEP)
            raw = GetData(url, token, body)
    return raw


def ProcessData(raw: dict, sheet_name: str, token: str, sheet_id: str, service: googleapiclient.discovery.Resource) -> None:
    row_all = 2
    row_month = 2
    Stamp(f'For sheet {sheet_name} found {SmartLen(raw)} companies', 'i')
    for i in range(0, SmartLen(raw), PORTION):
        Stamp(f'Processing {PORTION} campaigns from {i} out of {SmartLen(raw)}', 'i')
        portion_of_campaigns = list(raw.keys())[i:i + PORTION]
        list_for_request = [{'id': campaign, 'interval': {'begin': BEGIN, 'end': TODAY}} for campaign in portion_of_campaigns]
        data = GetData(URL_STAT, token, list_for_request)
        list_of_all = []
        list_of_month = []
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
                        list_of_all.append(one_row)
                        if CheckCurMonth(one_row[1]):
                            list_of_month.append(one_row)
        UploadData(list_of_all, sheet_name, sheet_id, service, row_all)
        UploadData(list_of_month, PREFIX_MONTH + sheet_name, sheet_id, service, row_month)
        row_all += len(list_of_all)
        row_month += len(list_of_month)
        Sleep(SHORT_SLEEP)


if __name__ == '__main__':
    Main()

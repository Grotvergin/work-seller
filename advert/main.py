from advert.source import *


def main():
    config, sections = ParseConfig('advert')
    service = BuildService()
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', heading, len(COLUMNS), SHEET_ID, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', PREFIX + heading, len(COLUMNS), SHEET_ID, service)
        token = config[heading]['Token']
        big_empty = PrepareEmpty(len(COLUMNS), BLANK_ROWS)
        small_empty = PrepareEmpty(len(COLUMNS), int(0.2 * BLANK_ROWS))
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, big_empty, heading, SHEET_ID, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, small_empty, PREFIX + heading, SHEET_ID, service)
        campaigns = PrepareCampaigns(token)
        ProcessData(campaigns, heading, token, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', heading, len(COLUMNS), SHEET_ID, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', PREFIX + heading, len(COLUMNS), SHEET_ID, service)
        Stamp(f'End of processing {heading}', 'b')
    Finish(TIMEOUT, NAME)


def CheckCurMonth(cur_date: str):
    if cur_date[:4] == YEAR and cur_date[5:7] == MONTH:
        return True
    return False


def PrepareCampaigns(token):
    raw = GetData(URL_CAMPAIGNS, token)
    list_of_campaigns = []
    for advert in raw['adverts']:
        for lst in advert['advert_list']:
            list_of_campaigns.append(lst['advertId'])
    return list_of_campaigns


def GetData(url: str, token:str, body=None):
    Stamp(f'Trying to connect {url}', 'i')
    ControlTimeout(TIMEOUT, NAME)
    try:
        if body is None:
            response = requests.get(url, headers={'Authorization': token})
        else:
            response = requests.post(url, headers={'Authorization': token}, data=body)
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


def ProcessData(raw: list, sheet_name: str, token: str, service):
    row_all = 2
    row_month = 2
    Stamp(f'For sheet {sheet_name} found {SmartLen(raw)} companies', 'i')
    for i in range(0, SmartLen(raw), PORTION):
        Stamp(f'Processing {PORTION} campaigns from {i} out of {SmartLen(raw)}', 'i')
        portion_of_campaigns = raw[i:i + PORTION]
        list_for_request = [{'id': campaign, 'interval': {'begin': BEGIN, 'end': TODAY}} for campaign in portion_of_campaigns]
        data = GetData(URL_STAT, token, json.dumps(list_for_request, indent=2))
        list_of_all = []
        list_of_month = []
        for t in range(SmartLen(data)):
            for j in range(SmartLen(data[t]['days'])):
                for k in range(SmartLen(data[t]['days'][j]['apps'])):
                    for nm in range(SmartLen(data[t]['days'][j]['apps'][k]['nm'])):
                        one_row = []
                        for key, value in COLUMNS.items():
                            try:
                                if value == '+':
                                    one_row.append(str(data[t]['days'][j]['apps'][k]['nm'][nm][key]).replace('.', ','))
                                elif key == 'advertId':
                                    one_row.append(str(data[t]['advertId']))
                                elif key == 'date':
                                    one_row.append(str(data[t]['days'][j]['date']))
                                else:
                                    one_row.append(value.replace('.', ','))
                            except KeyError:
                                one_row.append(MSG)
                        list_of_all.append(one_row)
                        if CheckCurMonth(one_row[1]):
                            list_of_month.append(one_row)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, list_of_all, sheet_name, SHEET_ID, service, row_all)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, list_of_month, PREFIX + sheet_name, SHEET_ID, service, row_month)
        row_all += len(list_of_all)
        row_month += len(list_of_month)
        Sleep(SHORT_SLEEP)


if __name__ == '__main__':
    main()

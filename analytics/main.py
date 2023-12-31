from analytics.source import *


def Main() -> None:
    config, sections = ParseConfig(NAME.lower())
    service = BuildService()
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        token, client_id, sheet_id = ParseCurrentHeading(config, heading)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', heading, len(COLUMNS), sheet_id, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', PREFIX + heading, len(COLUMNS), sheet_id, service)
        empty = PrepareEmpty(len(COLUMNS), BLANK_ROWS)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, heading, sheet_id, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, PREFIX + heading, sheet_id, service)
        data_all = GetData(token, client_id, START_OF_ALL, TODAY)
        Sleep(SHORT_SLEEP)
        data_month = GetData(token, client_id, START_OF_MONTH, TODAY)
        data_all = ProcessData(data_all, heading)
        data_month = ProcessData(data_month, heading)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, data_all, heading, sheet_id, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, data_month, PREFIX + heading, sheet_id, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', heading, len(COLUMNS), sheet_id, service)
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', PREFIX + heading, len(COLUMNS), sheet_id, service)
    Finish(TIMEOUT, NAME)


def ProcessData(raw: dict, sheet_name: str) -> list:
    Stamp(f"For sheet {sheet_name} found {SmartLen(raw['result']['data'])} datasets", 'i')
    list_of_rows = []
    for i in range(SmartLen(raw['result']['data'])):
        one_row = []
        for key, value in COLUMNS.items():
            match value:
                case None:
                    one_row.append(str(raw['result']['data'][i]['dimensions'][0][key]))
                case _:
                    try:
                        one_row.append(str(int(raw['result']['data'][i]['metrics'][value])).replace('.', ','))
                    except IndexError:
                        one_row.append(MSG)
        list_of_rows.append(one_row)
    return list_of_rows


def ParseCurrentHeading(config: ConfigParser, heading: str) -> (str, str, str):
    token = config[heading]['Token']
    client_id = config[heading]['ClientID']
    sheet_id = config['DEFAULT']['SheetID']
    return token, client_id, sheet_id


def GetData(token: str, client_id: str, date_from: str, date_to: str) -> dict:
    Stamp(f'Trying to connect {URL}', 'i')
    ControlTimeout(TIMEOUT, NAME)
    body = SAMPLE.copy()
    body['date_from'] = date_from
    body['date_to'] = date_to
    try:
        response = requests.post(URL, headers={'Client-Id': client_id, 'Api-Key': token}, data=json.dumps(body))
    except requests.ConnectionError:
        Stamp(f'Connection on {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(token, client_id, date_from, date_to)
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
            raw = GetData(token, client_id, date_from, date_to)
    return raw


if __name__ == '__main__':
    Main()

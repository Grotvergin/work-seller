from source import *
from pprint import pprint


def main():
    config, sections = ParseConfig()
    service = BuildService()
    for heading in sections:
        print(Fore.YELLOW + f"Start of processing {heading}..." + Style.RESET_ALL)
        ExecuteRetry(SwitchIndicator, RED, heading, len(COLUMNS), service)
        token = config[heading]['Token']
        print(Fore.LIGHTBLUE_EX + f"Configuration: \nToken = {token}" + Style.RESET_ALL)
        empty = PrepareEmpty(len(COLUMNS))
        ExecuteRetry(UploadData, empty, heading, len(COLUMNS), 2, service)
        campaigns = PrepareCampaigns(token)
        if campaigns:
            ProcessData(campaigns, heading, COLUMNS, token, service)
        else:
            print(Fore.LIGHTBLUE_EX + f"Sheet {heading} is empty." + Style.RESET_ALL)
        print(Fore.YELLOW + f"End of processing {heading}." + Style.RESET_ALL)
        ExecuteRetry(SwitchIndicator, GREEN, heading, len(COLUMNS), service)
    ControlTimeout()
    print(Fore.GREEN + f'All data was uploaded successfully!' + Style.RESET_ALL)


def PrepareCampaigns(token):
    list_of_campaigns = []
    raw = GetData(URL_CAMPAIGNS, token)
    for advert in raw['adverts']:
        for lst in advert['advert_list']:
            list_of_campaigns.append(lst['advertId'])
    pprint(list_of_campaigns)
    return list_of_campaigns


def ExecuteRetry(func, *args):
    while not func(*args):
        ControlTimeout()
        Sleep(LONG_SLEEP)


def SwitchIndicator(color: dict, sheet_name: str, width:int, service):
    color['requests'][0]['repeatCell']['range']['endColumnIndex'] = width
    try:
        response = service.spreadsheets().get(spreadsheetId=SHEET_ID, ranges=[sheet_name], includeGridData=False).execute()
        color['requests'][0]['repeatCell']['range']['sheetId'] = response.get('sheets')[0].get('properties').get('sheetId')
        service.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body=color).execute()
    except HttpError as err:
        print(Fore.RED + f'Error status = {err} on switching indicator for sheet {sheet_name}!' + Style.RESET_ALL)
        return False
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror):
        print(Fore.RED + f'Connection error on switching indicator for sheet {sheet_name}!' + Style.RESET_ALL)
        return False
    else:
        print(Fore.GREEN + f"Switching success." + Style.RESET_ALL)
        return True


def MakeColumnIndexes():
    indexes = {}
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i, letter in enumerate(alphabet):
        indexes[i] = letter
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            indexes[len(alphabet) + i * len(alphabet) + j] = alphabet[i] + alphabet[j]
    return indexes


def GetData(url: str, token:str, key='', value=''):
    headers = {'Authorization': token}
    params = {key: value}
    print(Fore.LIGHTBLUE_EX + f'Trying to connect WB URL: {url}...' + Style.RESET_ALL)
    try:
        if key != '' and value != '':
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.get(url, headers=headers)
    except requests.ConnectionError:
        print(Fore.RED + f'Connection error on WB URL: {url}!' + Style.RESET_ALL)
        Sleep(LONG_SLEEP)
        ControlTimeout()
        raw = GetData(url, token, key, value)
    else:
        ControlTimeout()
        if response.status_code == 200:
            print(Fore.GREEN + f'Success status = {response.status_code} on WB URL: {url}.' + Style.RESET_ALL)
            raw = response.json()
        else:
            print(Fore.RED + f'Error status = {response.status_code} on WB URL: {url}!' + Style.RESET_ALL)
            Sleep(LONG_SLEEP)
            raw = GetData(url, token, key, value)
    return raw


def ControlTimeout():
    current = time.time()
    if (current - START) > TIMEOUT:
        print(Fore.RED + f'Timeout error: elapsed time is {int(current - START)}, while allowed is {TIMEOUT}!' + Style.RESET_ALL)
        sys.exit()
    else:
        print(Fore.GREEN + f'Timeout OK: elapsed time is {int(current - START)}, while allowed is {TIMEOUT}.' + Style.RESET_ALL)


def Sleep(timer: int):
    print(Fore.LIGHTBLUE_EX + f'Sleeping for {timer} seconds...')
    if timer == SHORT_SLEEP:
        time.sleep(SHORT_SLEEP)
    else:
        for _ in range(timer):
            time.sleep(1)


def ProcessData(raw: list, sheet_name: str, column_names: dict, token: str, service):
    width = len(column_names)
    row = 2
    try:
        campaigns_number = len(raw)
    except TypeError:
        campaigns_number = 0
        print(Fore.LIGHTMAGENTA_EX + f'For sheet {sheet_name} found NO companies!' + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f'For sheet {sheet_name} found {campaigns_number} companies.' + Style.RESET_ALL)

    for i in range(campaigns_number):
        print(f'Processing campaign {i} out of {campaigns_number}...')
        data = GetData(URL_STAT, token, 'id', raw[i])
        Sleep(SHORT_SLEEP)

        list_of_rows = []
        try:
            days_number = len(data['days'])
        except TypeError:
            days_number = 0
            print(Fore.LIGHTMAGENTA_EX + f"For AdvertID {raw[i]} found NO days!" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"For AdvertID {raw[i]} found {days_number} days." + Style.RESET_ALL)

        for j in range(days_number):
            try:
                app_number = len(data['days'][j]['apps'])
            except TypeError:
                app_number = 0
                print(Fore.LIGHTMAGENTA_EX + f"For date {data['days'][j]['date']} found NO apps!" + Style.RESET_ALL)
            else:
                print(Fore.GREEN + f"For date {data['days'][j]['date']} found {app_number} apps." + Style.RESET_ALL)

            for k in range(app_number):
                try:
                    nm_number = len(data['days'][j]['apps'][k]['nm'])
                except TypeError:
                    nm_number = 0
                    print(
                        Fore.LIGHTMAGENTA_EX + f"For app {data['days'][j]['apps'][k]['appType']} found NO nm_numbers!" + Style.RESET_ALL)
                else:
                    print(
                        Fore.GREEN + f"For app {data['days'][j]['apps'][k]['appType']} found {nm_number} nm_numbers." + Style.RESET_ALL)

                for nm in range(nm_number):
                    one_row = []
                    for key, value in column_names.items():
                        if value == '+':
                            try:
                                one_row.append(str(data['days'][j]['apps'][k]['nm'][nm][key]).replace('.', ','))
                            except KeyError:
                                one_row.append(MSG)
                        elif key == 'advertId':
                            try:
                                one_row.append(str(data[key]))
                            except KeyError:
                                one_row.append(MSG)
                        elif key == 'date':
                            try:
                                one_row.append(str(data['days'][j][key]))
                            except KeyError:
                                one_row.append(MSG)
                        else:
                            one_row.append(value.replace('.', ','))
                    list_of_rows.append(one_row)
        ExecuteRetry(UploadData, list_of_rows, sheet_name, width, row, service)
        row += len(list_of_rows)


def UploadData(list_of_rows: list, sheet_name: str, width: int, row: int, service):
    body = {'values': list_of_rows}
    try:
        res = service.spreadsheets().values().update(spreadsheetId=SHEET_ID,
                                                     range=f'{sheet_name}!A{row}:{column_indexes[width]}{row + len(list_of_rows)}',
                                                     valueInputOption='USER_ENTERED', body=body).execute()
    except HttpError as err:
        print(Fore.RED + f'Error status = {err} on uploading data to sheet {sheet_name}!' + Style.RESET_ALL)
        return False
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror):
        print(Fore.RED + f'Connection error on uploading data to sheet {sheet_name}!' + Style.RESET_ALL)
        return False
    else:
        print(Fore.GREEN + f"Uploading success: {res.get('updatedRows')} rows in range {res.get('updatedRange')}." + Style.RESET_ALL)
        return True


def ParseConfig():
    config = configparser.ConfigParser()
    config.read(Path(Path.cwd(), 'config.ini'), encoding='utf-8')
    sections = config.sections()
    return config, sections


def PrepareEmpty(width: int):
    list_of_empty = []
    one_row = [''] * width
    for k in range(BLANK_ROWS):
        list_of_empty.append(one_row)
    return list_of_empty


def BuildService():
    print(Fore.LIGHTBLUE_EX + f'Trying to build service...' + Style.RESET_ALL)
    try:
        service = build('sheets', 'v4', credentials=CREDS)
    except (HttpError, TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror):
        print(Fore.RED + f'Connection error on building service!' + Style.RESET_ALL)
        Sleep(LONG_SLEEP)
        ControlTimeout()
        BuildService()
    else:
        print(Fore.GREEN + f'Built service successfully.' + Style.RESET_ALL)
        return service


if __name__ == '__main__':
    column_indexes = MakeColumnIndexes()
    main()

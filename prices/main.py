from source import *


def main():
    config, sections = ParseConfig()
    service = BuildService()
    for heading in sections:
        print(Fore.YELLOW + f"Start of processing {heading}..." + Style.RESET_ALL)
        token = config[heading]['Token']
        ExecuteRetry(SwitchIndicator, RED, heading, len(COLUMNS), service)
        empty = PrepareEmpty(COLUMNS)
        ExecuteRetry(UploadData, empty, heading, 2, service)
        raw = GetData(token)
        if raw:
            prepared = PrepareData(raw, heading, COLUMNS)
            ExecuteRetry(UploadData, prepared, heading, 2, service)
        else:
            print(Fore.LIGHTMAGENTA_EX + f'Sheet {heading} is empty.')
        Sleep(SHORT_SLEEP)
        print(Fore.YELLOW + f"End of processing {heading}." + Style.RESET_ALL)
        ExecuteRetry(SwitchIndicator, GREEN, heading, len(COLUMNS), service)
    ControlTimeout()
    print(Fore.GREEN + f'All data was uploaded successfully!' + Style.RESET_ALL)


def ExecuteRetry(func, *args):
    while not func(*args):
        ControlTimeout()
        Sleep(LONG_SLEEP)


def PrepareData(raw: list, sheet_name: str, column_names: list):
    try:
        height = len(raw)
    except TypeError:
        height = 0
        print(Fore.LIGHTMAGENTA_EX + f'For sheet {sheet_name} found NO rows!' + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f'For sheet {sheet_name} found {height} rows.' + Style.RESET_ALL)

    list_of_rows = []
    for i in range(height):
        one_row = []
        for column in column_names:
            try:
                if column == 'time':
                    one_row.append(str(datetime.now().strftime('%m-%d %H:%M')))
                else:
                    one_row.append(str(raw[i][column]).replace('.', ','))
            except KeyError:
                one_row.append(MSG)
        list_of_rows.append(one_row)
    return list_of_rows


def GetData(token:str):
    headers = {'Authorization': token}
    print(Fore.LIGHTBLUE_EX + f'Trying to connect WB URL: {URL}...' + Style.RESET_ALL)
    try:
        response = requests.get(URL, headers=headers)
    except requests.ConnectionError:
        print(Fore.RED + f'Connection error on WB URL: {URL}!' + Style.RESET_ALL)
        Sleep(LONG_SLEEP)
        ControlTimeout()
        raw = GetData(token)
    else:
        ControlTimeout()
        if response.status_code == 200:
            print(Fore.GREEN + f'Success status = {response.status_code} on WB URL: {URL}.' + Style.RESET_ALL)
            raw = response.json()
        else:
            print(Fore.RED + f'Error status = {response.status_code} on WB URL: {URL}!' + Style.RESET_ALL)
            Sleep(LONG_SLEEP)
            raw = GetData(token)
    return raw


def PrepareEmpty(column_names: dict):
    width = len(column_names)
    list_of_empty = []
    one_row = [''] * width
    for k in range(BLANK_ROWS):
        list_of_empty.append(one_row)
    return list_of_empty


def UploadData(list_of_rows: list, sheet_name: str, row: int, service):
    body = {'values': list_of_rows}
    try:
        res = service.spreadsheets().values().update(spreadsheetId=SHEET_ID,
                                                     range=f'{sheet_name}!A{row}:{column_indexes[len(COLUMNS)]}{row + len(list_of_rows)}',
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


def ControlTimeout():
    current = time.time()
    if (current - START) > TIMEOUT:
        print(Fore.RED + f'Timeout error: elapsed time is {int(current - START)}, while allowed is {TIMEOUT}!' + Style.RESET_ALL)
        sys.exit()
    else:
        print(Fore.GREEN + f'Timeout OK: elapsed time is {int(current - START)}, while allowed is {TIMEOUT}.' + Style.RESET_ALL)


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


def ParseConfig():
    config = configparser.ConfigParser()
    config.read(Path(Path.cwd(), 'config.ini'), encoding='utf-8')
    sections = config.sections()
    return config, sections


def BuildService():
    print(Fore.LIGHTBLUE_EX + f'Trying to build service...' + Style.RESET_ALL)
    try:
        service = build('sheets', 'v4', credentials=CREDS)
    except (HttpError, TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror):
        print(Fore.RED + f'Connection error on building service!' + Style.RESET_ALL)
        Sleep(LONG_SLEEP)
        BuildService()
    else:
        print(Fore.GREEN + f'Built service successfully.' + Style.RESET_ALL)
        return service


def MakeColumnIndexes():
    indexes = {}
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i, letter in enumerate(alphabet):
        indexes[i] = letter
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            indexes[len(alphabet) + i * len(alphabet) + j] = alphabet[i] + alphabet[j]
    return indexes


def Sleep(timer: int):
    rand_time = random.randint(int(0.5 * timer), int(1.5 * timer))
    print(Fore.LIGHTBLUE_EX + f'Sleeping for {rand_time} seconds...')
    for _ in range(rand_time):
        time.sleep(1)


if __name__ == '__main__':
    column_indexes = MakeColumnIndexes()
    main()

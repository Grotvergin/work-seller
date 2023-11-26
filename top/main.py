from source import *
from pprint import pprint


def main():
    config, sections = ParseConfig()
    data_auth['email'] = '3125106@bk.ru'
    data_auth['password'] = 'Mpseller1'
    service = BuildService()
    for heading in sections:
        print(Fore.YELLOW + f"Start of processing {heading}..." + Style.RESET_ALL)
        empty = PrepareEmpty(columns)
        while not UploadData(empty, heading, 2, service):
            Sleep(long_sleep)
        session = requests.Session()
        session = Authorize(session)
        Sleep(short_sleep)
        raw = GetData(session)
        if raw:
            prepared = PrepareData(raw, heading, columns)
            while not UploadData(prepared, heading, 2, service):
                Sleep(long_sleep)
        else:
            print(Fore.LIGHTMAGENTA_EX + f'Sheet {heading} is empty.')
        Sleep(short_sleep)
        print(Fore.YELLOW + f"End of processing {heading}." + Style.RESET_ALL)
    print(Fore.GREEN + f'All data was uploaded successfully!' + Style.RESET_ALL)


def PrepareData(raw: dict, sheet_name: str, column_names: list):
    try:
        height = len(raw)
    except TypeError:
        height = 0
        print(Fore.LIGHTMAGENTA_EX + f'For sheet {sheet_name} found NO operations!' + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f'For sheet {sheet_name} found {height} operations.' + Style.RESET_ALL)

    list_of_rows = []
    for i in range(height):
        one_row = []
        for column in column_names:
            try:
                one_row.append(str(raw[i][column]))
            except KeyError:
                one_row.append(message)
        list_of_rows.append(one_row)
    return list_of_rows


def UploadData(list_of_rows: list, sheet_name: str, row: int, service):
    body = {'values': list_of_rows}
    try:
        res = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                                     range=f'{sheet_name}!A{row}:{column_indexes[len(columns)]}{row + len(list_of_rows)}',
                                                     valueInputOption='USER_ENTERED', body=body).execute()
    except HttpError as err:
        print(Fore.RED + f'Error status = {err} on uploading data to sheet {sheet_name}!' + Style.RESET_ALL)
        return False
    except (TimeoutError, httplib2.error.ServerNotFoundError):
        print(Fore.RED + f'Connection error on uploading data to sheet {sheet_name}!' + Style.RESET_ALL)
        return False
    else:
        print(Fore.GREEN + f"Uploading success: {res.get('updatedRows')} rows in range {res.get('updatedRange')}." + Style.RESET_ALL)
        return True


def PrepareEmpty(column_names: dict):
    width = len(column_names)
    list_of_empty = []
    one_row = [''] * width
    for k in range(blank_rows):
        list_of_empty.append(one_row)
    return list_of_empty


def ParseConfig():
    config = configparser.ConfigParser()
    config.read(Path(Path.cwd(), 'config.ini'), encoding='utf-8')
    sections = config.sections()
    return config, sections


def BuildService():
    print(Fore.LIGHTBLUE_EX + f'Trying to build service...' + Style.RESET_ALL)
    try:
        service = build('sheets', 'v4', credentials=creds)
    except (HttpError, TimeoutError, httplib2.error.ServerNotFoundError):
        print(Fore.RED + f'Connection error on building service!' + Style.RESET_ALL)
        Sleep(long_sleep)
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


def Sleep(time: int):
    print(Fore.LIGHTBLUE_EX + f'Sleeping for some time...')
    for _ in tqdm(range(random.randint(int(0.7 * time), int(1.3 * time)))):
        sleep(1)
    print()


def Authorize(session: requests.Session):
    print(Fore.LIGHTBLUE_EX + f'Trying to authorize TopVTop URL: {url_for_auth}...' + Style.RESET_ALL)
    try:
        response = session.post(url_for_auth, headers=headers_auth, data=data_auth, cookies=cookies_auth)
    except requests.ConnectionError:
        print(Fore.RED + f'Connection error on authorization!' + Style.RESET_ALL)
        Sleep(long_sleep)
        session = Authorize(session)
    else:
        if response.status_code == 200:
            print(Fore.GREEN + f'Success status = {response.status_code} on authorization.' + Style.RESET_ALL)
        else:
            print(Fore.RED + f'Error status = {response.status_code} on authorization!' + Style.RESET_ALL)
            Sleep(long_sleep)
            session = Authorize(session)
    return session


def GetData(session: requests.Session):
    print(Fore.LIGHTBLUE_EX + f'Trying to connect TopVTop URL: {url_for_data}...' + Style.RESET_ALL)
    try:
        response = session.get(url_for_data, headers=headers_get, params=params_get, cookies=cookies_get)
    except requests.ConnectionError:
        print(Fore.RED + f'Connection error on TopVTop URL: {url_for_data}!' + Style.RESET_ALL)
        Sleep(long_sleep)
        raw = GetData(session)
    else:
        if response.status_code == 200:
            print(Fore.GREEN + f'Success status = {response.status_code} on TopVTop URL: {url_for_data}.' + Style.RESET_ALL)
            raw = response.json()
        else:
            print(Fore.RED + f'Error status = {response.status_code} on TopVTop URL: {url_for_data}!' + Style.RESET_ALL)
            Sleep(long_sleep)
            raw = GetData(session)
    return raw


if __name__ == '__main__':
    column_indexes = MakeColumnIndexes()
    main()

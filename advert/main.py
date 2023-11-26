from source import *


def main():
    config, sections = ParseConfig()
    service = BuildService()
    for heading in sections:
        print(Fore.YELLOW + f"Start of processing {heading}..." + Style.RESET_ALL)
        token, blank_rows = ParseCurrentHeading(config, heading)
        print(Fore.LIGHTBLUE_EX + f"Configuration: \nToken = {token}\nBlank rows = {blank_rows}" + Style.RESET_ALL)
        empty = PrepareEmpty(len(columns), blank_rows)
        while not UploadData(empty, heading, len(columns), 2, service):
            Sleep(long_sleep)
        raw = GetData(url_for_all_campaigns, token, 'order', 'create')
        if raw:
            ProcessData(raw, heading, columns, token, service)
        else:
            print(Fore.LIGHTBLUE_EX + f"Sheet {heading} is empty." + Style.RESET_ALL)
        print(Fore.YELLOW + f"End of processing {heading}." + Style.RESET_ALL)
    print(Fore.GREEN + f'All data was uploaded successfully!' + Style.RESET_ALL)


def MakeColumnIndexes():
    indexes = {}
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i, letter in enumerate(alphabet):
        indexes[i] = letter
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            indexes[len(alphabet) + i * len(alphabet) + j] = alphabet[i] + alphabet[j]
    return indexes


def GetData(url: str, token:str, key:str, value:str):
    headers = {'Authorization': token}
    params = {key: value}
    print(Fore.LIGHTBLUE_EX + f'Trying to connect WB URL: {url}...' + Style.RESET_ALL)
    try:
        response = requests.get(url, headers=headers, params=params)
    except requests.ConnectionError:
        print(Fore.RED + f'Connection error on WB URL: {url}!' + Style.RESET_ALL)
        Sleep(long_sleep)
        raw = GetData(url, token, key, value)
    else:
        if response.status_code == 200:
            print(Fore.GREEN + f'Success status = {response.status_code} on WB URL: {url}.' + Style.RESET_ALL)
            raw = response.json()
        else:
            print(Fore.RED + f'Error status = {response.status_code} on WB URL: {url}!' + Style.RESET_ALL)
            Sleep(long_sleep)
            raw = GetData(url, token, key, value)
    return raw


def Sleep(time: int):
    print(Fore.LIGHTBLUE_EX + f'Sleeping for {time} seconds...')
    if time == short_sleep:
        sleep(short_sleep)
    else:
        for _ in tqdm(range(time)):
            sleep(1)
        print()


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

    for i in tqdm(range(campaigns_number)):
        print()
        data = GetData(url_for_statistics, token, 'id', raw[i]['advertId'])
        Sleep(short_sleep)

        list_of_rows = []
        try:
            days_number = len(data['days'])
        except TypeError:
            days_number = 0
            print(Fore.LIGHTMAGENTA_EX + f"For AdvertID {raw[i]['advertId']} found NO days!" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"For AdvertID {raw[i]['advertId']} found {days_number} days." + Style.RESET_ALL)

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
                                one_row.append(message)
                        elif key == 'advertId':
                            try:
                                one_row.append(str(data[key]))
                            except KeyError:
                                one_row.append(message)
                        elif key == 'date':
                            try:
                                one_row.append(str(data['days'][j][key]))
                            except KeyError:
                                one_row.append(message)
                        else:
                            one_row.append(value.replace('.', ','))
                    list_of_rows.append(one_row)

        while not UploadData(list_of_rows, sheet_name, width, row, service):
            Sleep(long_sleep)
        row += len(list_of_rows)


def UploadData(list_of_rows: list, sheet_name: str, width: int, row: int, service):
    body = {'values': list_of_rows}
    try:
        res = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                                     range=f'{sheet_name}!A{row}:{column_indexes[width]}{row + len(list_of_rows)}',
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


def ParseConfig():
    config = configparser.ConfigParser()
    config.read(Path(Path.cwd(), 'config.ini'), encoding='utf-8')
    sections = config.sections()
    return config, sections


def ParseCurrentHeading(config, heading: str):
    token = config[heading]['Token']
    blank_rows = int(config[heading]['BlankSpace'])
    return token, blank_rows


def PrepareEmpty(width: int, blank_rows: int):
    list_of_empty = []
    one_row = [''] * width
    for k in range(blank_rows):
        list_of_empty.append(one_row)
    return list_of_empty


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


if __name__ == '__main__':
    column_indexes = MakeColumnIndexes()
    main()

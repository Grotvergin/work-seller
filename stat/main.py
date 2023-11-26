from source import *


def main():
    config, sections = ParseConfig()
    service = BuildService()

    for heading in sections:
        print(Fore.YELLOW + f'Start of processing {heading}...' + Style.RESET_ALL)
        token, dateFrom, dateTo, blank_rows, spreadsheet_id = ParseCurrentHeading(config, heading)
        print(Fore.LIGHTBLUE_EX + f'Configuration: \nToken = {token}\nDateFrom = {dateFrom}\nDateTo = {dateTo}\nBlank rows = {blank_rows}\nSpreadsheet ID = {spreadsheet_id}' + Style.RESET_ALL)

        for sheet, url in sheets_and_url.items():
            empty = PrepareEmpty(len(sheets_and_columns[sheet]), blank_rows)
            while not UploadData(empty, sheet, len(sheets_and_columns[sheet]), spreadsheet_id, service):
                Sleep(long_sleep)
            raw = GetData(url, token, dateFrom, dateTo)
            if raw:
                raw = Normalize(raw)
                if sheet == 'Realisations':
                    raw = SortByRRD_ID(raw)
                prepared = PrepareData(raw, sheet, sheets_and_columns[sheet])
                while not UploadData(prepared, sheet, len(sheets_and_columns[sheet]), spreadsheet_id, service):
                    Sleep(long_sleep)
            else:
                print(Fore.LIGHTBLUE_EX + f"Sheet {sheet} is empty from {dateFrom} to {dateTo}." + Style.RESET_ALL)
            Sleep(long_sleep)
        print(Fore.YELLOW + f"End of processing {heading}." + Style.RESET_ALL)
    print(Fore.GREEN + f'All data was uploaded successfully!' + Style.RESET_ALL)


def ParseConfig():
    config = configparser.ConfigParser()
    config.read(Path(Path.cwd(), 'config.ini'), encoding='utf-8')
    sections = config.sections()
    return config, sections


def ParseCurrentHeading(config, heading: str):
    token = config[heading]['Token']
    dateFrom = config[heading]['DateFrom']
    blank_rows = int(config[heading]['BlankSpace'])
    spreadsheet_id = config[heading]['SpreadsheetID']
    try:
        dateTo = config[heading]['DateTo']
    except KeyError:
        dateTo = datetime.datetime.now().strftime("%Y-%m-%d")
    return token, dateFrom, dateTo, blank_rows, spreadsheet_id


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


def Normalize(raw: list):
    print(Fore.LIGHTBLUE_EX + 'Start of data normalising...' + Style.RESET_ALL)
    unique_keys = set()
    for dataset in raw:
        unique_keys.update(dataset.keys())
    for dataset in raw:
        for key in unique_keys:
            if key not in dataset:
                dataset[key] = '0'
    for dataset in raw:
        for key, value in dataset.items():
            if value is None:
                dataset[key] = '0'
    print(Fore.GREEN + 'Data normalising success.' + Style.RESET_ALL)
    return raw


def GetData(url: str, token:str, dateFrom:str, dateTo: str):
    headers = {'Authorization': token}
    params = {'dateFrom': dateFrom, 'dateTo': dateTo}
    print(Fore.LIGHTBLUE_EX + f'Trying to connect WB URL: {url}...' + Style.RESET_ALL)
    try:
        response = requests.get(url, headers=headers, params=params)
    except requests.ConnectionError:
        print(Fore.RED + f'Connection error on WB URL: {url}!' + Style.RESET_ALL)
        Sleep(long_sleep)
        raw = GetData(url, token, dateFrom, dateTo)
    else:
        if response.status_code == 200:
            print(Fore.GREEN + f'Success status = {response.status_code} on WB URL: {url}.' + Style.RESET_ALL)
            raw = response.json()
        else:
            print(Fore.RED + f'Error status = {response.status_code} on WB URL: {url}!' + Style.RESET_ALL)
            Sleep(long_sleep)
            raw = GetData(url, token, dateFrom, dateTo)
    return raw


def Sleep(time: int):
    print(Fore.LIGHTBLUE_EX + f'Sleeping for {time} seconds...')
    if time == short_sleep:
        sleep(short_sleep)
    else:
        for _ in tqdm(range(time)):
            sleep(1)
        print()


def PrepareEmpty(width: int, blank_rows: int):
    list_of_empty = []
    one_row = [''] * width
    for k in range(blank_rows):
        list_of_empty.append(one_row)
    return list_of_empty


def UploadData(list_of_rows: list, sheet_name: str, width: int, spreadsheet_id: str, service):
    body = {'values': list_of_rows}
    try:
        res = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                                     range=f'{sheet_name}!A2:{column_indexes[width]}{2 + len(list_of_rows)}',
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


def PrepareData(raw: list, sheet_name: str, column_names: dict):
    num = 2
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
        for key, value in column_names.items():
            if value == '+':
                one_row.append(str(raw[i][key]).replace('.', ','))
            elif key == 'quantity' and raw[i]['totalPrice'] < 0:
                raw[i]['quantity'] = '-' + value
                one_row.append(raw[i]['quantity'])
            elif key == 'retail_commission':
                if float(raw[i]['ppvz_sales_commission']) != 0:
                    raw[i]['retail_commission'] = float(raw[i]['ppvz_vw_nds']) + float(
                        raw[i]['ppvz_sales_commission'])
                elif float(raw[i]['commission_percent']) != 0:
                    raw[i]['retail_commission'] = float(raw[i]['commission_percent']) * float(
                        raw[i]['retail_price_withdisc_rub']) - float(raw[i]['retail_price_withdisc_rub']) + float(
                        raw[i]['retail_amount'])
                else:
                    raw[i]['retail_commission'] = float(raw[i]['retail_amount']) * percent_commission
                one_row.append(str(raw[i]['retail_commission']).replace('.', ','))
            elif key == 'supplier_reward':
                raw[i]['supplier_reward'] = float(raw[i]['retail_amount']) - float(raw[i]['retail_commission'])
                one_row.append(str(raw[i]['supplier_reward']).replace('.', ','))
            elif key == 'for_pay':
                raw[i]['for_pay'] = (float(raw[i]['retail_amount'])
                                     - float(raw[i]['retail_commission'])
                                     + float(raw[i]['rebill_logistic_cost'])
                                     + float(raw[i]['acquiring_fee'])
                                     + float(raw[i]['ppvz_reward']))
                one_row.append(str(raw[i]['for_pay']).replace('.', ','))
            elif key == 'order_dt' or key == 'sale_dt' or key == 'rr_dt':
                raw[i][key] = raw[i][key][:10]
                one_row.append(str(raw[i][key]))
            elif key == 'srid':
                one_row.append(str(raw[i]['srid']))
            elif key == 'suppliercontract_code':
                one_row.append(f'=ЕСЛИ(И(AM{num}>0;AF{num}=0);AM{num};0)')
                num += 1
            else:
                one_row.append(value.replace('.', ','))
        list_of_rows.append(one_row)
    return list_of_rows


def SortByRRD_ID(raw: list):
    print(Fore.LIGHTBLUE_EX + 'Sorting by rrd_id started...' + Style.RESET_ALL)
    swap = True
    while swap:
        swap = False
        for i in range(len(raw) - 1):
            if raw[i]['rrd_id'] > raw[i + 1]['rrd_id']:
                raw[i], raw[i + 1] = raw[i + 1], raw[i]
                swap = True
    print(Fore.GREEN + 'Sorting by rrd_id finished.' + Style.RESET_ALL)
    return raw


if __name__ == '__main__':
    column_indexes = MakeColumnIndexes()
    main()

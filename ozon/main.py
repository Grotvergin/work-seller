from source import *


def main():
    config, sections = ParseConfig()
    service = BuildService()
    for heading in sections:
        print(Fore.YELLOW + Stamp() + f'Start of processing {heading}...' + Style.RESET_ALL)
        token, client_id = ParseCurrentHeading(config, heading)
        print(Fore.LIGHTBLUE_EX + Stamp() + f'Configuration: \nToken = {token}\nClientID = {client_id}' + Style.RESET_ALL)
        for sheet in SHEETS.keys():
            ExecuteRetry(SwitchIndicator, RED, sheet, len(SHEETS[sheet]['Columns']), SPREADSHEET_ID, service)
            empty = PrepareEmpty(len(SHEETS[sheet]['Columns']))
            ExecuteRetry(UploadData, empty, sheet, len(SHEETS[sheet]['Columns']), SPREADSHEET_ID, service)
            if sheet == 'Transactions':
                ProcessTransactions(token, client_id, service)
            else:
                ProcessProductsWarehouse(token, client_id, sheet, service)
            ExecuteRetry(SwitchIndicator, GREEN, sheet, len(SHEETS[sheet]['Columns']), SPREADSHEET_ID, service)
            Sleep(SHORT_SLEEP)
        print(Fore.YELLOW + Stamp() + f"End of processing {heading}." + Style.RESET_ALL)
    ControlTimeout()
    SendEmail(f'Stat OK: elapsed time is {int(time.time() - START)}')
    print(Fore.GREEN + datetime.now().strftime('[%m-%d|%H:%M:%S]') + f'All data was uploaded successfully!' + Style.RESET_ALL)


def Stamp():
    return datetime.now().strftime('[%m-%d|%H:%M:%S] ')


def ProcessProductsWarehouse(token: str, client_id: str, sheet:str, service):
    list_of_products = GetData(SHEETS[sheet]['GetAll'], token, client_id)
    product_ids = [item['product_id'] for item in list_of_products['result']['items']]
    body_id = {'product_id': product_ids}
    list_of_info = GetData(SHEETS[sheet]['InfoAboutAll'], token, client_id, body_id)
    products_sku = []
    for item in list_of_info['result']['items']:
        if int(item['sku']) != 0:
            products_sku.append(str(item['sku']))
        else:
            products_sku.append(str(item['fbo_sku']))
    body_sku = {'skus': products_sku}
    list_of_ratings = GetData(SHEETS[sheet]['GetRating'], token, client_id, body_sku)
    prepared = PrepareData(list_of_info, list_of_ratings, sheet)
    ExecuteRetry(UploadData, prepared, sheet, len(SHEETS[sheet]['Columns']), SPREADSHEET_ID, service)


def GetIntermediateDates():
    current_date = datetime.strptime(TODAY, '%Y-%m-%dT%H:%M:%S.%fZ')
    intermediate_dates = [TODAY]
    for i in range(1, MONTHS_HISTORY):
        intermediate_dates.append((current_date - timedelta(days=DAYS_IN_MONTH * i)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    intermediate_dates.sort()
    date_pairs = list(zip(intermediate_dates, intermediate_dates[1:]))
    return date_pairs


def ProcessTransactions(token: str, client_id: str, service):
    row = 2
    intermediate_pairs = GetIntermediateDates()
    for gap in intermediate_pairs:
        list_of_rows = []
        body = SAMPLE.copy()
        body['filter']['date']['from'] = gap[0]
        body['filter']['date']['to'] = gap[1]
        body['page'] = 1
        raw = GetData(SHEETS['Transactions']['GetData'], token, client_id, body)
        for j in range(1, int(raw['result']['page_count']) + 1):
            body['page'] = j
            raw = GetData(SHEETS['Transactions']['GetData'], token, client_id, body)
            for k in range(len(raw['result']['operations'])):
                items_count = len(raw['result']['operations'][k]['items'])
                if items_count == 0:
                    empty_items = True
                    items_count = 1
                else:
                    empty_items = False
                services_sum = 0.0
                if len(raw['result']['operations'][k]['services']) != 0:
                    for z in range(len(raw['result']['operations'][k]['services'])):
                        services_sum += float(raw['result']['operations'][k]['services'][z]['price'])
                for n in range(items_count):
                    one_row = []
                    for column in SHEETS['Transactions']['Columns']:
                        match column:
                            case 'delivery_schema' | 'order_date' | 'posting_number' | 'warehouse_id':
                                one_row.append(str(raw['result']['operations'][k]['posting'][column]))
                            case 'operation_id':
                                if empty_items:
                                    one_row.append(str(raw['result']['operations'][k][column]) + '-0')
                                else:
                                    one_row.append(str(raw['result']['operations'][k][column]) + f'-{n + 1}')
                            case 'name' | 'sku':
                                if empty_items:
                                    one_row.append('')
                                else:
                                    one_row.append(str(raw['result']['operations'][k]['items'][n][column]))
                            case 'services_sum':
                                one_row.append(str(services_sum).replace('.', ','))
                            case _:
                                one_row.append(str(raw['result']['operations'][k][column]).replace('.', ','))
                    list_of_rows.append(one_row)
        ExecuteRetry(UploadData, list_of_rows, 'Transactions', len(SHEETS['Transactions']['Columns']), SPREADSHEET_ID, service, row)
        row += len(list_of_rows)


def PrepareData(main_data: dict, ratings: dict, sheet_name: str):
    try:
        height = len(main_data['result']['items'])
    except TypeError:
        height = 0
        print(Fore.LIGHTMAGENTA_EX + datetime.now().strftime(
            '[%m-%d|%H:%M:%S] ') + f'For sheet {sheet_name} found NO rows!' + Style.RESET_ALL)
    else:
        print(Fore.GREEN + datetime.now().strftime(
            '[%m-%d|%H:%M:%S] ') + f'For sheet {sheet_name} found {height} rows.' + Style.RESET_ALL)

    list_of_rows = []
    for i in range(height):
        one_row = []
        for column in SHEETS[sheet_name]['Columns']:
            match column:
                case 'sku':
                    if int(main_data['result']['items'][i][column]) == 0:
                        main_data['result']['items'][i][column] = main_data['result']['items'][i]['fbo_sku']
                    one_row.append(str(main_data['result']['items'][i][column]))
                case 'rating':
                    for product in ratings['products']:
                        if int(product['sku']) == int(main_data['result']['items'][i]['sku']):
                            one_row.append(str(product['sku']))
                case 'brand':
                    one_row.append('Foodteria')
                case 'state':
                    one_row.append(str(main_data['result']['items'][i]['status']['state_name']))
                case 'present' | 'reserved':
                    one_row.append(str(main_data['result']['items'][i]['stocks'][column]))
                case _:
                    one_row.append(str(main_data['result']['items'][i][column]))
        list_of_rows.append(one_row)
    return list_of_rows


def GetData(url: str, token: str, client_id: str, body=None):
    headers = {'Api-Key': token, 'Client-Id': client_id}
    print(Fore.LIGHTBLUE_EX + Stamp() + f'Trying to connect OZON URL: {url}...' + Style.RESET_ALL)
    try:
        if body is None:
            response = requests.post(url, headers=headers)
        else:
            body = json.dumps(body)
            response = requests.post(url, headers=headers, data=body)
    except requests.ConnectionError:
        print(Fore.RED + Stamp() + f'Connection error on OZON URL: {url}!' + Style.RESET_ALL)
        Sleep(LONG_SLEEP)
        ControlTimeout()
        raw = GetData(url, token, client_id, body)
    else:
        ControlTimeout()
        if response.status_code == 200:
            print(Fore.GREEN + Stamp() + f'Success status = {response.status_code} on OZON URL: {url}.' + Style.RESET_ALL)
            raw = response.json()
        else:
            print(Fore.RED + Stamp() + f'Error status = {response.status_code} on OZON URL: {url}!' + Style.RESET_ALL)
            Sleep(LONG_SLEEP)
            raw = GetData(url, token, client_id, body)
    return raw


def UploadData(list_of_rows: list, sheet_name: str, width: int, spreadsheet_id: str, service, row=2):
    body = {'values': list_of_rows}
    try:
        res = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                                     range=f'{sheet_name}!A{row}:{column_indexes[width]}{row + len(list_of_rows)}',
                                                     valueInputOption='USER_ENTERED', body=body).execute()
    except HttpError as err:
        print(Fore.RED + Stamp() + f'Error status = {err} on uploading data to sheet {sheet_name}!' + Style.RESET_ALL)
        return False
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror):
        print(Fore.RED + Stamp() + f'Connection error on uploading data to sheet {sheet_name}!' + Style.RESET_ALL)
        return False
    else:
        print(Fore.GREEN + Stamp() + f"Uploading success: {res.get('updatedRows')} rows in range {res.get('updatedRange')}." + Style.RESET_ALL)
        return True


def PrepareEmpty(width: int):
    list_of_empty = []
    one_row = [''] * width
    for k in range(BLANK_ROWS):
        list_of_empty.append(one_row)
    return list_of_empty


def ExecuteRetry(func, *args):
    while not func(*args):
        ControlTimeout()
        Sleep(LONG_SLEEP)


def SwitchIndicator(color: dict, sheet_name: str, width: int, sheet_id: str, service):
    color['requests'][0]['repeatCell']['range']['endColumnIndex'] = width
    try:
        response = service.spreadsheets().get(spreadsheetId=sheet_id, ranges=[sheet_name],
                                              includeGridData=False).execute()
        color['requests'][0]['repeatCell']['range']['sheetId'] = response.get('sheets')[0].get('properties').get(
            'sheetId')
        service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=color).execute()
    except HttpError as err:
        print(Fore.RED + Stamp() + f'Error status = {err} on switching indicator for sheet {sheet_name}!' + Style.RESET_ALL)
        return False
    except (TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror):
        print(Fore.RED + Stamp() + f'Connection error on switching indicator for sheet {sheet_name}!' + Style.RESET_ALL)
        return False
    else:
        print(Fore.GREEN + Stamp() + f"Switching success." + Style.RESET_ALL)
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


def SendEmail(theme: str):
    user = 'kyliancromwell@gmail.com'
    password = 'cgyv tsjl fvgv exne'
    receiver = 'mishenin_r@mail.ru'
    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(user, password)
        print(Fore.GREEN + Stamp() + 'Gmail authorization success.' + Style.RESET_ALL)
        msg = MIMEMultipart()
        msg['Subject'] = theme
        smtp_server.sendmail(user, receiver, msg.as_string())
        print(Fore.GREEN + Stamp() + 'Gmail letter sending success.' + Style.RESET_ALL)
    except Exception:
        print(Fore.RED + Stamp() + "Error during sending email!" + Style.RESET_ALL)


def ControlTimeout():
    current = time.time()
    if (current - START) > TIMEOUT:
        print(Fore.RED + Stamp() + f'Timeout error: elapsed time is {int(current - START)}, while allowed is {TIMEOUT}!' + Style.RESET_ALL)
        SendEmail(f'Stat FAIL: elapsed time is {int(current - START)}, while allowed is {TIMEOUT}!')
        sys.exit()
    else:
        print(Fore.GREEN + Stamp() + f'Timeout OK: elapsed time is {int(current - START)}, while allowed is {TIMEOUT}.' + Style.RESET_ALL)


def BuildService():
    print(Fore.LIGHTBLUE_EX + Stamp() + f'Trying to build service...' + Style.RESET_ALL)
    try:
        service = build('sheets', 'v4', credentials=CREDS)
    except (HttpError, TimeoutError, httplib2.error.ServerNotFoundError, socket.gaierror):
        print(Fore.RED + Stamp() + f'Connection error on building service!' + Style.RESET_ALL)
        Sleep(LONG_SLEEP)
        ControlTimeout()
        BuildService()
    else:
        ControlTimeout()
        print(Fore.GREEN + Stamp() + f'Built service successfully.' + Style.RESET_ALL)
        return service


def Sleep(timer: int):
    print(Fore.LIGHTBLUE_EX + Stamp() + f'Sleeping for {timer} seconds...')
    if timer == SHORT_SLEEP:
        time.sleep(SHORT_SLEEP)
    else:
        for _ in range(timer):
            time.sleep(1)


def ParseConfig():
    config = configparser.ConfigParser()
    config.read(Path(Path.cwd(), 'config.ini'), encoding='utf-8')
    sections = config.sections()
    return config, sections


def ParseCurrentHeading(config, heading: str):
    token = config[heading]['Token']
    client_id = config[heading]['ClientID']
    return token, client_id


if __name__ == '__main__':
    column_indexes = MakeColumnIndexes()
    main()

from discharge.source import *


def main():
    config, sections = ParseConfig('discharge')
    service = BuildService()
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        token, client_id, sheet_id = ParseCurrentHeading(config, heading)
        for sheet in SHEETS.keys():
            ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', sheet, len(SHEETS[sheet]['Columns']), sheet_id, service)
            empty = PrepareEmpty(len(SHEETS[sheet]['Columns']), BLANK_ROWS)
            ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, sheet, sheet_id, service)
            if sheet == 'Transactions':
                ProcessTransactions(token, client_id, sheet_id, service)
            else:
                ProcessProductsWarehouse(token, client_id, sheet, sheet_id, service)
            ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', sheet, len(SHEETS[sheet]['Columns']), sheet_id, service)
        Stamp(f'End of processing {heading}', 'b')
    Finish(TIMEOUT, NAME)


def ParseCurrentHeading(config, heading: str):
    token = config[heading]['Token']
    client_id = config[heading]['ClientID']
    sheet_id = config[heading]['SheetID']
    return token, client_id, sheet_id


def ProcessProductsWarehouse(token: str, client_id: str, sheet:str, sheet_id: str, service):
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
    list_of_ratings = GetAllSkus(products_sku, GetData, SHEETS[sheet]['GetRating'], token, client_id)
    prepared = PrepareData(list_of_info, list_of_ratings, sheet)
    ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, prepared, sheet, sheet_id, service)


def GetAllSkus(big_list, func, *args):
    all_data = []
    for i in range(0, len(big_list), CHUNK_SIZE):
        chunk = big_list[i:i+CHUNK_SIZE]
        body_sku = {'skus': chunk}
        data = func(*args, body_sku)
        all_data += data['products']
    return all_data


def GetIntermediateDates():
    current_date = datetime.strptime(TODAY, '%Y-%m-%dT%H:%M:%S.%fZ')
    intermediate_dates = [TODAY]
    for i in range(1, MONTHS_HISTORY):
        intermediate_dates.append((current_date - timedelta(days=DAYS_IN_MONTH * i)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    intermediate_dates.sort()
    date_pairs = list(zip(intermediate_dates, intermediate_dates[1:]))
    return date_pairs


def ProcessTransactions(token: str, client_id: str, sheet_id: str, service):
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
        ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, list_of_rows, 'Transactions', sheet_id, service, row)
        row += len(list_of_rows)


def PrepareData(main_data: dict, ratings: list, sheet_name: str):
    list_of_rows = []
    for i in range(SmartLen(main_data['result']['items'])):
        one_row = []
        for column in SHEETS[sheet_name]['Columns']:
            match column:
                case 'sku':
                    if int(main_data['result']['items'][i][column]) == 0:
                        main_data['result']['items'][i][column] = main_data['result']['items'][i]['fbo_sku']
                    one_row.append(str(main_data['result']['items'][i][column]))
                case 'rating':
                    for product in ratings:
                        if int(product['sku']) == int(main_data['result']['items'][i]['sku']):
                            one_row.append(str(product['rating']).replace('.', ','))
                case 'brand':
                    one_row.append('')
                case 'state':
                    one_row.append(str(main_data['result']['items'][i]['status']['state_name']))
                case 'present' | 'reserved':
                    one_row.append(str(main_data['result']['items'][i]['stocks'][column]))
                case _:
                    one_row.append(str(main_data['result']['items'][i][column]))
        list_of_rows.append(one_row)
    return list_of_rows


def GetData(url: str, token: str, client_id: str, body=None):
    Stamp(f'Trying to connect {url}', 'i')
    headers = {'Api-Key': token, 'Client-Id': client_id}
    ControlTimeout(TIMEOUT, NAME)
    try:
        if body is None:
            response = requests.post(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, data=json.dumps(body))
    except requests.ConnectionError:
        Stamp(f'On connection {url}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(url, token, client_id, body)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {url}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response in empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {url}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetData(url, token, client_id, body)
    return raw


if __name__ == '__main__':
    main()

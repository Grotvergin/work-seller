from statist.source import *


def Main() -> None:
    config, sections = ParseConfig(NAME.lower())
    service = BuildService()
    for heading in sections:
        Stamp(f'Start of processing {heading}', 'b')
        token, date_from, date_to, sheet_id = ParseCurrentHeading(config, heading)
        for sheet, url in SHEETS_AND_URL.items():
            ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'r', sheet, len(SHEETS_AND_COLS[sheet]), sheet_id, service)
            empty = PrepareEmpty(len(SHEETS_AND_COLS[sheet]), BLANK_ROWS)
            ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, empty, sheet, sheet_id, service)
            data = GetData(url[0], token, date_from, date_to)
            if sheet == 'Realisations':
                # data += GetData(url[1], token, date_from, date_to)
                data = SortByRRD_ID(data)
            data = ProcessData(Normalize(data), sheet)
            ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, UploadData, data, sheet, sheet_id, service)
            ExecuteRetry(TIMEOUT, NAME, LONG_SLEEP, SwitchIndicator, 'g', sheet, len(SHEETS_AND_COLS[sheet]), sheet_id, service)
            Sleep(SHORT_SLEEP)
    Finish(TIMEOUT, NAME)


def GetData(url: str, token: str, date_from: str, date_to: str) -> list:
    Stamp(f'Trying to connect {url}', 'i')
    ControlTimeout(TIMEOUT, NAME)
    try:
        response = requests.get(url, headers={'Authorization': token}, params={'dateFrom': date_from, 'dateTo': date_to})
    except requests.ConnectionError:
        Stamp(f'On connection {url}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(url, token, date_from, date_to)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {url}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response in empty', 'w')
                raw = []
        else:
            Stamp(f'Status = {response.status_code} on {url}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetData(url, token, date_from, date_to)
    return raw


def ParseCurrentHeading(config: ConfigParser, heading: str) -> (str, str, str, str):
    token = config[heading]['Token']
    sheet_id = config[heading]['SheetID']
    date_to = datetime.now().strftime("%Y-%m-%d")
    if heading[0:5] == PREFIX:
        date_from = datetime.now().strftime("%Y-%m") + '-01'
    else:
        date_from = DATE_FROM
    return token, date_from, date_to, sheet_id


def Normalize(raw: list) -> list:
    if SmartLen(raw) > 0:
        Stamp('Data normalising', 'i')
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
    return raw


def ProcessData(raw: list, sheet_name: str) -> list:
    num = 2
    list_of_rows = []
    for i in range(SmartLen(raw)):
        one_row = []
        for key, value in SHEETS_AND_COLS[sheet_name].items():
            if value is None:
                one_row.append(str(raw[i][key]).replace('.', ','))
            elif key == 'quantity' and raw[i]['totalPrice'] < 0:
                raw[i]['quantity'] = '-' + value
                one_row.append(raw[i]['quantity'])
            elif key == 'retail_commission':
                if float(raw[i]['ppvz_sales_commission']) != 0:
                    raw[i]['retail_commission'] = (float(raw[i]['ppvz_vw_nds'])
                                                   + float(raw[i]['ppvz_sales_commission']))
                elif float(raw[i]['commission_percent']) != 0:
                    raw[i]['retail_commission'] = (float(raw[i]['commission_percent'])
                                                   * float(raw[i]['retail_price_withdisc_rub'])
                                                   - float(raw[i]['retail_price_withdisc_rub'])
                                                   + float(raw[i]['retail_amount']))
                else:
                    raw[i]['retail_commission'] = float(raw[i]['retail_amount']) * float(raw[i]['ppvz_spp_prc'])
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


def SortByRRD_ID(raw: list) -> list:
    if SmartLen(raw) > 1:
        Stamp('Sorting by rrd_id', 'i')
        swap = True
        while swap:
            swap = False
            for i in range(len(raw) - 1):
                if raw[i]['rrd_id'] > raw[i + 1]['rrd_id']:
                    raw[i], raw[i + 1] = raw[i + 1], raw[i]
                    swap = True
    return raw


if __name__ == '__main__':
    Main()

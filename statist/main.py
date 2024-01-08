from statist.source import *


@Inspector(NAMES[NAME])
def Main() -> None:
    config, sections = ParseConfig(NAME)
    service = BuildService()
    for sheet_name in SHEETS.keys():
        Body(config, service, sections[:4], sheet_name)
        Body(config, service, sections[4:], sheet_name, PREFIX_MONTH)


def Body(config: ConfigParser, service: googleapiclient.discovery.Resource, sections: list, sheet_name: str, period: str = None):
    Stamp(f'Processing sheet {sheet_name} for period {period}', 'b')
    start = time.time()
    for heading in sections:
        token, date_from, date_to, sheet_id = ParseCurrentHeading(config, heading, period)
        CleanSheet(len(SHEETS[sheet_name]['Columns']), sheet_name, sheet_id, service, 'C')
        data = GetData(SHEETS[sheet_name]['URL'][0], token, date_from, date_to)
        data = SortByRRD_ID(data) if sheet_name == 'Realisations' else data
        data = ProcessData(Normalize(data), sheet_name)
        UploadData(data, sheet_name, sheet_id, service)
    elapsed = time.time() - start
    if elapsed < SLEEP:
        Sleep(SLEEP - elapsed)
    else:
        Stamp(f'No extra sleep needed, elapsed = {int(elapsed)}', 'l')


@ControlRecursion
def GetData(url: str, token: str, date_from: str, date_to: str) -> list:
    Stamp(f'Trying to connect {url}', 'i')
    try:
        response = requests.get(url, headers={'Authorization': token}, params={'dateFrom': date_from, 'dateTo': date_to})
    except requests.ConnectionError:
        Stamp(f'On connection {url}', 'e')
        Sleep(SLEEP)
        raw = GetData(url, token, date_from, date_to)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {url}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response is empty', 'w')
                raw = []
        else:
            Stamp(f'Status = {response.status_code} on {url}', 'e')
            Sleep(SLEEP)
            raw = GetData(url, token, date_from, date_to)
    return raw


def ParseCurrentHeading(config: ConfigParser, heading: str, period: str = None) -> (str, str, str, str):
    date_to = TODAY
    token_key = 'Token' + heading[5:] if period else 'Token' + heading
    token = config['DEFAULT'][token_key]
    sheet_id = config[heading]['SheetID']
    date_from = START_OF_MONTH if period else DATE_FROM
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
        for key, value in SHEETS[sheet_name]['Columns'].items():
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
        Stamp('Sorting by RRD_ID', 'i')
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
